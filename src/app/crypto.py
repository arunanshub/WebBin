from __future__ import annotations

from dataclasses import dataclass
from hashlib import pbkdf2_hmac

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


def encrypt_data(data: str, password: str) -> SecretData:
    # generate params for cipher
    nonce = os.urandom(16)
    salt = os.urandom(32)
    key = pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        ITERATION_COUNT,
        dklen=32,
    )
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
    key = pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        ITERATION_COUNT,
        dklen=32,
    )
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
