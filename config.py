"""
Central configuration and logging for PassoUm.
Version is sourced exclusively from version.py — single source of truth.
"""
from version import __version__

import logging
import os
from pathlib import Path

BASE_DIR    = Path(__file__).resolve().parent
APP_VERSION = __version__       # alias used throughout the codebase
MAJOR, MINOR, PATCH, BUILD = (int(x) for x in APP_VERSION.split("."))

# ── Paths ─────────────────────────────────────────────────────────────────────
CONTENT_DB_PATH = BASE_DIR / "content.db"   # pre-built, READ-ONLY on server
AUDIO_DIR       = BASE_DIR / "static" / "audio"

# USER_DB_PATH honours the DISK_PATH env var so Render's Persistent Disk
# survives redeployments.  Locally, DISK_PATH is unset → falls back to BASE_DIR.
#
# Render setup (one-time, in the Render Dashboard):
#   1. Service → Settings → Disks → Add Disk
#      Name: userdata  |  Mount Path: /data  |  Size: 1 GB
#   2. Service → Environment → Add Variable
#      Key: DISK_PATH   Value: /data
#
# That's it.  user.db will live at /data/user.db and survive every deploy.
_disk_root  = os.getenv("DISK_PATH", str(BASE_DIR))
USER_DB_PATH = Path(_disk_root) / "user.db"

# ── Logging (version stamped in every line) ───────────────────────────────────
LOG_FORMAT = (
    f"%(asctime)s  [v{APP_VERSION}]  [%(levelname)-8s]  "
    "%(name)s  %(funcName)s  —  %(message)s"
)
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt="%Y-%m-%d %H:%M:%S",
)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


# ── Flask config dict ─────────────────────────────────────────────────────────
class FlaskConfig:
    SECRET_KEY  = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-change-me")
    DEBUG       = os.getenv("FLASK_DEBUG", "0") == "1"
    APP_VERSION = APP_VERSION
