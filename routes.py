"""
Flask route definitions for PassoUm v1.0.3.1.

All user progress is stored in the browser (localStorage) — no user.db.

Routes
──────
  GET  /                                  Home dashboard (localStorage-driven)
  GET  /vocabulary                        Full 600-word list
  GET  /learn                             JS-driven learn + quiz + results page
  GET  /practice                          JS-driven practice + quiz + results page
  GET  /exam                              JS-driven exam hub + exam + review page

JSON API
────────
  GET  /api/learn?seen_ids=1,2,3          words + questions bundle for Learn
  GET  /api/practice?mastered_ids=...     questions bundle for Practice
               &exclude_ids=...
  GET  /api/exam                          20-question exam bundle
  GET  /db-status                         Debug: content.db stats
"""
from version import __version__  # noqa

from flask import Flask, jsonify, render_template, request

from config import CONTENT_DB_PATH, get_logger
from models import (
    get_db_stats,
    get_exam_bundle,
    get_learn_bundle,
    get_practice_bundle,
    get_vocab_list,
)

log = get_logger(__name__)


def register_routes(app: Flask) -> None:
    log.info("[1.0.3.1] localStorage progress tracking — user.db removed.")

    # ── helpers ────────────────────────────────────────────────────────────

    def _db_ok() -> bool:
        return CONTENT_DB_PATH.exists()

    def _db_required():
        if not _db_ok():
            return render_template(
                "error.html",
                message="Content database not found. "
                        "Run seed/build_content_db.py first."
            ), 503
        return None

    def _parse_ids(raw: str) -> list[int]:
        """Parse a comma-separated string of integers, ignoring blanks."""
        return [int(x) for x in raw.split(",") if x.strip().isdigit()]

    # ── HTML pages ─────────────────────────────────────────────────────────

    @app.route("/")
    def index():
        log.info("GET /")
        content_stats = get_db_stats() if _db_ok() else {}
        return render_template("index.html", content_stats=content_stats)

    @app.route("/vocabulary")
    def vocabulary():
        log.info("GET /vocabulary")
        err = _db_required()
        if err:
            return err
        return render_template("vocabulary.html", words=get_vocab_list())

    @app.route("/learn")
    def learn():
        log.info("GET /learn")
        err = _db_required()
        if err:
            return err
        return render_template("learn.html")

    @app.route("/practice")
    def practice():
        log.info("GET /practice")
        err = _db_required()
        if err:
            return err
        return render_template("practice.html")

    @app.route("/exam")
    def exam():
        log.info("GET /exam")
        err = _db_required()
        if err:
            return err
        return render_template("exam.html")

    # ── JSON API ────────────────────────────────────────────────────────────

    @app.route("/api/learn")
    def api_learn():
        """Return unseen words + their questions for the Learn module."""
        err = _db_required()
        if err:
            return err
        seen_ids = _parse_ids(request.args.get("seen_ids", ""))
        log.info("GET /api/learn  seen=%d", len(seen_ids))
        return jsonify(get_learn_bundle(seen_ids))

    @app.route("/api/practice")
    def api_practice():
        """Return a practice round of questions for mastered words."""
        err = _db_required()
        if err:
            return err
        mastered_ids = _parse_ids(request.args.get("mastered_ids", ""))
        exclude_ids  = _parse_ids(request.args.get("exclude_ids",  ""))
        log.info("GET /api/practice  mastered=%d  exclude=%d",
                 len(mastered_ids), len(exclude_ids))
        return jsonify(get_practice_bundle(mastered_ids, exclude_ids))

    @app.route("/api/exam")
    def api_exam():
        """Return a fresh 20-question exam bundle."""
        err = _db_required()
        if err:
            return err
        log.info("GET /api/exam")
        return jsonify(get_exam_bundle())

    @app.route("/db-status")
    def db_status():
        log.info("GET /db-status")
        if not _db_ok():
            return jsonify({"error": "content.db not found"}), 503
        return jsonify(get_db_stats())
