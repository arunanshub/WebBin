from __future__ import annotations

from hypothesis import given
from hypothesis import strategies as st

from app import crypto


@given(
    paste=st.text(),
    title=st.text(),
    password=st.text(),
    compression_threshold_size=st.integers(min_value=1),
)
def test_encrypt_and_decrypt_paste(
    paste: str,
    title: str,
    password: str,
    compression_threshold_size: int,
) -> None:
    raw_paste = crypto.RawPaste(title, paste)
    encrypted_paste = crypto.encrypt_paste(
        raw_paste,
        password,
        compression_threshold_size,
    )

    if len(paste.encode()) >= compression_threshold_size:
        assert encrypted_paste.is_compressed

    decrypted_paste = crypto.decrypt_paste(encrypted_paste, password)
    assert raw_paste.data == decrypted_paste.data
    assert raw_paste.title == decrypted_paste.title
