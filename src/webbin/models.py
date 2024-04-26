from __future__ import annotations

import sys

from . import db

Model = db.Model


if sys.version_info >= (3, 11):
    from datetime import UTC, datetime

    def get_utc_now() -> datetime:
        return datetime.now(UTC)
else:
    from datetime import datetime

    def get_utc_now() -> datetime:
        return datetime.utcnow()


class Paste(Model):  # type: ignore[valid-type,misc]
    __tablename__ = "pastes"
    id = db.Column(db.String(32), unique=True, index=True, primary_key=True)
    title = db.Column(db.LargeBinary(100))
    data = db.Column(db.LargeBinary(), nullable=False)
    is_compressed = db.Column(db.Boolean())
    nonce = db.Column(db.LargeBinary(16), nullable=False)
    salt = db.Column(db.LargeBinary(32), nullable=False)
    token = db.Column(db.LargeBinary(32), nullable=False)
    created_at: datetime = db.Column(
        db.DateTime(),
        nullable=False,
        default=get_utc_now,
    )
    expires_after = db.Column(db.Interval(), nullable=False)
    views = db.Column(db.Integer(), nullable=False, default=0)
