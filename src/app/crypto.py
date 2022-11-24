from __future__ import annotations

from dataclasses import dataclass
from hashlib import scrypt

from flask_migrate import os
from pyflocker.ciphers import AES, base
from pyflocker.ciphers.backends import exc


@dataclass
class SecretData:
    secret_data: bytes
    nonce: bytes
    salt: bytes
    token: bytes


ITERATION_COUNT = 260000


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


def encrypt_data(data: str, password: str) -> SecretData:
    """
    Encrypts the given ``data`` with the given ``password`` and returns a
    packed version of ``data``.

    Args:
        data: A string value to be encrypted.
        password: A string representing the password.

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
    secret_data = cipher.update(data.encode())
    cipher.finalize()
    # the tag that will be used to authenticate decryption
    tag = cipher.calculate_tag()
    assert tag is not None

    return SecretData(secret_data, nonce, salt, tag)


def decrypt_data(payload: SecretData, password: str) -> str:
    # unpack the cipher parameters
    encrypted_data = payload.secret_data
    nonce = payload.nonce
    salt = payload.salt
    tag = payload.token
    # generate the key from the password
    key = scrypt_derive_key(password, salt)
    # decrypt the data
    cipher = AES.new(False, key, AES.MODE_GCM, nonce)
    assert isinstance(cipher, base.BaseAEADCipher)
    decrypted_data = cipher.update(encrypted_data)
    # fail if incorrect password
    try:
        cipher.finalize(tag)
    except exc.DecryptionError:
        raise ValueError("Failed to decrypt data")
    return decrypted_data.decode()
