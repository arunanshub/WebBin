from __future__ import annotations

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app import crypto


@given(raw_paste=st.builds(crypto.RawPaste), password=st.text(min_size=1))
def test_encrypt_and_decrypt_paste(
    raw_paste: crypto.RawPaste,
    password: str,
) -> None:
    encrypted_paste = raw_paste.encrypt(password)

    decrypted_paste = encrypted_paste.decrypt(password)
    assert raw_paste.data == decrypted_paste.data
    assert raw_paste.title == decrypted_paste.title


@given(
    raw_paste=st.builds(crypto.RawPaste, data=st.text(min_size=100)),
    password=st.text(min_size=1),
    compression_threshold_size=st.integers(min_value=100),
)
def test_encrypt_and_decrypt_with_compression_size(
    raw_paste: crypto.RawPaste,
    password: str,
    compression_threshold_size: int,
):
    encrypted_paste = raw_paste.encrypt(password, compression_threshold_size)

    if len(raw_paste.data.encode()) >= compression_threshold_size:
        assert encrypted_paste.is_compressed

    decrypted_paste = encrypted_paste.decrypt(password)
    assert raw_paste.data == decrypted_paste.data
    assert raw_paste.title == decrypted_paste.title


@given(
    raw_paste=st.builds(crypto.RawPaste),
    passwords=st.tuples(st.text(), st.text()).filter(lambda x: x[0] != x[1]),
)
def test_encrypt_and_decrypt_failure(
    raw_paste: crypto.RawPaste,
    passwords: tuple[str, str],
):
    password, not_password = passwords
    with pytest.raises(ValueError):
        raw_paste.encrypt(password).decrypt(not_password)
