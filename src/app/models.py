from __future__ import annotations

from datetime import datetime
from typing import Any

from . import db

Model: Any = db.Model


class Paste(Model):
    __tablename__ = "pastes"
    id: str = db.Column(
        db.String(32),
        unique=True,
        index=True,
        primary_key=True,
    )
    title: bytes = db.Column(db.LargeBinary(100))
    data: bytes = db.Column(db.LargeBinary(), nullable=False)
    is_compressed: bool = db.Column(db.Boolean())
    nonce: bytes = db.Column(db.LargeBinary(16), nullable=False)
    salt: bytes = db.Column(db.LargeBinary(32), nullable=False)
    token: bytes = db.Column(db.LargeBinary(32), nullable=False)
    expires_at: datetime = db.Column(
        db.DateTime(),
        default=datetime.utcnow(),
        nullable=False,
    )
    is_temporary: bool = db.Column(db.Boolean(), default=True)
