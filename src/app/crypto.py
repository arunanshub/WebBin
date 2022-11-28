from __future__ import annotations

import zlib
from dataclasses import dataclass
from hashlib import scrypt

from flask_migrate import os
from pyflocker.ciphers import AES, base
from pyflocker.ciphers.backends import exc


@dataclass(frozen=True)
class EncryptedPaste:
    title: bytes
    data: bytes
    nonce: bytes
    salt: bytes
    token: bytes
    is_compressed: bool


@dataclass(frozen=True)
class RawPaste:
    title: str
    data: str


#: Size of data after which it should be compressed.
COMPRESSION_THRESHOLD_SIZE = 1 << 10


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


def encrypt_paste(
    raw_paste: RawPaste,
    password: str,
    compression_threshold_size: int | None = None,
) -> EncryptedPaste:
    """
    Encrypts the given paste with the given ``password`` and returns a
    packed version of ``data``.

    Args:
        raw_paste: The raw paste data.
        password: A string that encrypts paste data and title.
        compression_threshold_size:
            If the paste data size is greater than the threshold, it will be
            compressed with ``zlib`` algorithm.

    Returns:
        The encrypted data with its cipher parameters in a packed form.
    """
    compression_threshold_size = (
        COMPRESSION_THRESHOLD_SIZE
        if compression_threshold_size is None
        else compression_threshold_size
    )
    # generate params for cipher
    nonce = os.urandom(12)
    salt = os.urandom(32)
    key = scrypt_derive_key(password, salt)
    # use AES cipher to encrypt data
    cipher = AES.new(True, key, AES.MODE_GCM, nonce)
    assert isinstance(cipher, base.BaseAEADCipher)
    # encrypt the title and data
    encrypted_title = cipher.update(raw_paste.title.encode())
    # compress data if it is >= 1KiB
    is_compressed = False
    encoded_raw_paste = raw_paste.data.encode()
    if len(encoded_raw_paste) >= compression_threshold_size:
        encoded_raw_paste = zlib.compress(encoded_raw_paste)
        is_compressed = not is_compressed

    secret_data = cipher.update(encoded_raw_paste)
    cipher.finalize()
    # the tag that will be used to authenticate decryption
    tag = cipher.calculate_tag()
    assert tag is not None

    return EncryptedPaste(
        encrypted_title,
        secret_data,
        nonce,
        salt,
        tag,
        is_compressed,
    )


def decrypt_paste(encrypted_paste: EncryptedPaste, password: str) -> RawPaste:
    # unpack the cipher parameters
    encrypted_data = encrypted_paste.data
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
    # decompress data if it has been compressed
    if encrypted_paste.is_compressed:
        paste = zlib.decompress(paste)
    return RawPaste(paste_title.decode(), paste.decode())
