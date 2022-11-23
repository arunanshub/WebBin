from __future__ import annotations

from typing import Any

from . import db

Model: Any = db.Model


class Secret(Model):
    __tablename__ = "secrets"
    id = db.Column(db.Integer, primary_key=True)
    paste_id = db.Column(db.String(32), unique=True, index=True)
    secret_data = db.Column(db.Text, nullable=False)
    nonce = db.Column(db.BINARY(16), nullable=False)
    salt = db.Column(db.BINARY(32), nullable=False)
    token = db.Column(db.BINARY(32), nullable=False)
