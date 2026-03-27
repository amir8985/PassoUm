"""
PassoUm — European Portuguese Learning App
Version: sourced from version.py (single source of truth)
"""
from version import __version__

import os

from dotenv import load_dotenv
from flask import Flask

from config import FlaskConfig, APP_VERSION, get_logger
from models import init_user_db
from routes import register_routes

load_dotenv()
log = get_logger(__name__)


def create_app() -> Flask:
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(FlaskConfig)

    # Make version available to every template as both {{ APP_VERSION }} and {{ version }}
    @app.context_processor
    def inject_globals():
        return {
            "APP_VERSION": __version__,
            "version":     __version__,
        }

    # Disable HTML caching in dev
    @app.after_request
    def no_cache(response):
        if response.content_type.startswith("text/html"):
            response.headers["Cache-Control"] = "no-store"
        return response

    register_routes(app)
    return app


# Module-level instance so Gunicorn can find it with:  gunicorn app:app
log.info("Initialising user.db …")
init_user_db()
log.info("Starting PassoUm %s", __version__)
app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=FlaskConfig.DEBUG)
