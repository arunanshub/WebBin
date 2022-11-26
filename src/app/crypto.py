from __future__ import annotations

from dataclasses import dataclass
from hashlib import scrypt

from flask_migrate import os
from pyflocker.ciphers import AES, base
from pyflocker.ciphers.backends import exc


@dataclass
class EncryptedPaste:
    title: bytes
    secret_data: bytes
    nonce: bytes
    salt: bytes
    token: bytes


@dataclass
class RawPaste:
    title: str
    paste: str


def scrypt_derive_key(password: str, salt: bytes) -> bytes:
    return scrypt(
        password.encode(),
        salt=salt,
        n=2**16,
        r=8,
        p=1,
        dklen=32,
        maxmem=67111936,
    )


def encrypt_paste(raw_paste: RawPaste, password: str) -> EncryptedPaste:
    """
    Encrypts the given paste with the given ``password`` and returns a
    packed version of ``data``.

    Args:
        raw_paste: The raw paste data.

    Returns:
        The encrypted data with its cipher parameters in a packed form.
    """
    # generate params for cipher
    nonce = os.urandom(16)
    salt = os.urandom(32)
    key = scrypt_derive_key(password, salt)
    # use AES cipher to encrypt data
    cipher = AES.new(True, key, AES.MODE_GCM, nonce)
    assert isinstance(cipher, base.BaseAEADCipher)
    # encrypt the title and data
    encrypted_title = cipher.update(raw_paste.title.encode())
    secret_data = cipher.update(raw_paste.paste.encode())
    cipher.finalize()
    # the tag that will be used to authenticate decryption
    tag = cipher.calculate_tag()
    assert tag is not None

    return EncryptedPaste(encrypted_title, secret_data, nonce, salt, tag)


def decrypt_paste(encrypted_paste: EncryptedPaste, password: str) -> RawPaste:
    # unpack the cipher parameters
    encrypted_data = encrypted_paste.secret_data
    nonce = encrypted_paste.nonce
    salt = encrypted_paste.salt
    tag = encrypted_paste.token
    # generate the key from the password
    key = scrypt_derive_key(password, salt)
    # decrypt the data
    cipher = AES.new(False, key, AES.MODE_GCM, nonce)
    assert isinstance(cipher, base.BaseAEADCipher)
    paste_title = cipher.update(encrypted_paste.title)
    paste = cipher.update(encrypted_data)
    # fail if incorrect password
    try:
        cipher.finalize(tag)
    except exc.DecryptionError:
        raise ValueError("Failed to decrypt data")
    return RawPaste(paste_title.decode(), paste.decode())
