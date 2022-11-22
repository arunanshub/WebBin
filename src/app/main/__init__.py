from __future__ import annotations

from flask import Blueprint

main = Blueprint("main", __name__)

from . import errors, views  # noqa: E402

__all__ = [
    "errors",
    "views",
]
