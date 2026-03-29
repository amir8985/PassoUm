"""
PassoUm — European Portuguese Learning App
Version: sourced from version.py (single source of truth)
"""
# load_dotenv() MUST be the very first executable line so that
# FLASK_DEBUG (and any other env vars) are in os.environ before
# config.py evaluates FlaskConfig.DEBUG at class-definition time.
from dotenv import load_dotenv
load_dotenv()

from version import __version__
import os
from flask import Flask

from config import FlaskConfig, APP_VERSION, get_logger
from routes import register_routes

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
# user.db removed in v1.0.3.1 — progress lives in browser localStorage
log.info("Starting PassoUm %s", __version__)
app = create_app()


if __name__ == "__main__":
    port      = int(os.getenv("PORT", 5000))
    debug_on  = FlaskConfig.DEBUG
    app.run(host="0.0.0.0", port=port, debug=debug_on, use_reloader=debug_on)
    # When FLASK_DEBUG=1 in .env, Flask watches every .py and .html for changes
    # and reloads automatically — no need to stop/start the server manually.
