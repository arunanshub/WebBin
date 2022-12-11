from __future__ import annotations

from datetime import datetime
from typing import Any

from . import db

Model: Any = db.Model


class Paste(Model):
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
        default=datetime.utcnow,
    )
    expires_after = db.Column(db.Interval(), nullable=False)
    views = db.Column(db.Integer(), nullable=False, default=0)
