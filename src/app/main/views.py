from __future__ import annotations

from . import main


@main.route("/")
def index() -> str:
    return "hello world"
