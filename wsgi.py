from __future__ import annotations

import os

from dotenv import load_dotenv
from flask_migrate import Migrate, upgrade

from app import config_app, db

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = config_app(os.environ.get("FLASK_CONFIG", "development"))
Migrate(app, db)


@app.cli.command()
def deploy() -> None:
    """
    Prepare the application for deployment.
    """
    upgrade()
