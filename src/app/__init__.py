from __future__ import annotations

from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_minify import Minify
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from werkzeug.middleware.proxy_fix import ProxyFix

from config import CONFIG

db = SQLAlchemy()
bootstrap = Bootstrap5()
minify = Minify()

CSP = {
    "script-src": ["'self'"],
    "style-src": ["'self'", "cdn.jsdelivr.net"],
}


def config_app(config_name: str) -> Flask:
    app = Flask(__name__)

    # apply config
    app.config.from_object(CONFIG[config_name])
    CONFIG[config_name].init_app(app)

    # register extensions
    db.init_app(app)
    bootstrap.init_app(app)
    if not app.testing:
        minify.init_app(app)

    # register CSP enforcer
    Talisman(
        app,
        content_security_policy=CSP,
        content_security_policy_nonce_in=["script-src"],
    )

    # if behind a proxy, tell Flask to use a proxy fixer
    if app.config.get("SSL_REDIRECT") is not None:
        app.wsgi_app = ProxyFix(app.wsgi_app)

    # register blueprints
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)
    return app
