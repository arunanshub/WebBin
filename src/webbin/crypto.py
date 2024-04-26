from __future__ import annotations

import os
import zlib
from dataclasses import dataclass
from hashlib import scrypt

from pyflocker.ciphers import AES, base
from pyflocker.ciphers.backends import exc

#: Size of data after which it should be compressed.
COMPRESSION_THRESHOLD_SIZE = 1 << 10


def scrypt_derive_key(password: str, salt: bytes) -> bytes:
    if not password:
        msg = "password must be greater than 0 bytes"
        raise ValueError(msg)
    return scrypt(
        password.encode(),
        salt=salt,
        n=2**16,
        r=8,
        p=1,
        dklen=32,
        maxmem=67111936,
    )


@dataclass(frozen=True)
class EncryptedPaste:
    title: bytes
    data: bytes
    nonce: bytes
    salt: bytes
    token: bytes
    is_compressed: bool

    def decrypt(
        self,
        password: str,
    ) -> RawPaste:
        # unpack the cipher parameters
        encrypted_data = self.data
        nonce = self.nonce
        salt = self.salt
        tag = self.token
        # generate the key from the password
        key = scrypt_derive_key(password, salt)
        # decrypt the data
        cipher = AES.new(False, key, AES.MODE_GCM, nonce)
        assert isinstance(cipher, base.BaseAEADCipher)
        paste_title = cipher.update(self.title)
        paste = cipher.update(encrypted_data)
        # fail if incorrect password
        try:
            cipher.finalize(tag)
        except exc.DecryptionError as e:
            msg = "Failed to decrypt data"
            raise ValueError(msg) from e
        # decompress data if it has been compressed
        if self.is_compressed:
            paste = zlib.decompress(paste)
        return RawPaste(paste_title.decode(), paste.decode())


@dataclass(frozen=True)
class RawPaste:
    title: str
    data: str

    def encrypt(
        self,
        password: str,
        compression_threshold_size: int | None = None,
    ) -> EncryptedPaste:
        """
        Encrypts the given paste with the given ``password`` and returns a
        packed version of ``data``.

        Args:
            password:
                A string that encrypts paste data and title. Must be greater
                than 0 bytes.
            compression_threshold_size:
                If the paste data size is greater than the threshold, it will
                be compressed with ``zlib`` algorithm.

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
        encrypted_title = cipher.update(self.title.encode())
        # compress data if it is >= 1KiB
        is_compressed = False
        encoded_raw_paste = self.data.encode()
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
