from __future__ import annotations

from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy

from config import CONFIG

db = SQLAlchemy()
bootstrap = Bootstrap5()


def config_app(config_name: str) -> Flask:
    app = Flask(__name__)

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    # apply config
    app.config.from_object(CONFIG[config_name])
    CONFIG[config_name].init_app(app)

    # register extensions
    db.init_app(app)
    bootstrap.init_app(app)
    return app
