from __future__ import annotations

from typing import Any

from flask import render_template

from . import main


@main.app_errorhandler(404)
def page_not_found(_: Any) -> tuple[str, int]:
    return render_template("404.html"), 404


@main.app_errorhandler(500)
def internal_server_error(_: Any) -> tuple[str, int]:
    return render_template("500.html"), 500
