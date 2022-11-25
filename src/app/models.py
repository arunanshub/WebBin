from __future__ import annotations

from datetime import datetime
from typing import Any

from . import db

Model: Any = db.Model


class Secret(Model):
    __tablename__ = "secrets"
    id = db.Column(db.Integer, primary_key=True)
    paste_id = db.Column(db.String(32), unique=True, index=True)
    secret_data = db.Column(db.LargeBinary(), nullable=False)
    nonce = db.Column(db.LargeBinary(16), nullable=False)
    salt = db.Column(db.LargeBinary(32), nullable=False)
    token = db.Column(db.LargeBinary(32), nullable=False)
    created_at = db.Column(
        db.DateTime(),
        nullable=False,
        default=datetime.utcnow,
    )
    expires_after = db.Column(db.Interval(), nullable=False)
