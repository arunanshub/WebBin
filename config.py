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

    @staticmethod
    def init_app(_: Flask) -> None:
        pass


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URI", "sqlite:///" + os.path.join(basedir, "data-dev.db")
    )


class ProductionConfig(Config):
    ENV = "production"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "data.db")


CONFIG = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
