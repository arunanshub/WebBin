from __future__ import annotations

import os
import typing

if typing.TYPE_CHECKING:
    from flask import Flask

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(16).hex())
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEFAULT_PASTE_ID_NUM_BYTES = 6
    SSL_REDIRECT = bool(os.environ.get("SSL_REDIRECT"))

    @staticmethod
    def init_app(_: Flask) -> None:
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL", "sqlite:///" + os.path.join(basedir, "data-dev.db")
    )


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "data.db")

    @classmethod
    def init_app(cls, app: Flask) -> None:
        # handle reverse proxy server headers
        from werkzeug.middleware.proxy_fix import ProxyFix

        app.wsgi_app = ProxyFix(app.wsgi_app)


CONFIG = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
