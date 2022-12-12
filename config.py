from __future__ import annotations

import os
import typing

if typing.TYPE_CHECKING:
    from flask import Flask

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(16).hex())
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #: No. of bytes to use to create a paste ID
    DEFAULT_PASTE_ID_NUM_BYTES = 6
    SSL_REDIRECT = bool(os.environ.get("SSL_REDIRECT"))
    COMPRESSION_THRESHOLD_SIZE = int(
        os.getenv("COMPRESSION_THRESHOLD_SIZE", 1 << 10)
    )

    @staticmethod
    def init_app(_: Flask) -> None:
        pass


class DevelopmentConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DEV_DATABASE_URL", "sqlite:///" + os.path.join(basedir, "data-dev.db")
    )


class ProductionConfig(Config):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(basedir, "data.db"),
    )

    @classmethod
    def init_app(cls, app: Flask) -> None:
        # handle reverse proxy server headers
        from werkzeug.middleware.proxy_fix import ProxyFix

        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)


CONFIG = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
