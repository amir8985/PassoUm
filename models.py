"""
DB connection helpers for content.db (read-only) and user.db (writable).
All schema definitions live here.
"""
from version import __version__  # noqa: F401 — version stamped in logs via config

import json
import random
import sqlite3
from pathlib import Path

from config import CONTENT_DB_PATH, USER_DB_PATH, get_logger

log = get_logger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Connection helpers
# ─────────────────────────────────────────────────────────────────────────────

def content_db() -> sqlite3.Connection:
    """Open content.db in read-only mode (immutable static asset)."""
    log.debug("Opening content.db (read-only)")
    conn = sqlite3.connect(f"file:{CONTENT_DB_PATH}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def user_db() -> sqlite3.Connection:
    """Open user.db with full read/write access."""
    log.debug("Opening user.db")
    USER_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(USER_DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


# ─────────────────────────────────────────────────────────────────────────────
# user.db schema
# ─────────────────────────────────────────────────────────────────────────────

_USER_SCHEMA = """
CREATE TABLE IF NOT EXISTS quiz_sessions (
    session_key   TEXT PRIMARY KEY,
    quiz_type     TEXT NOT NULL DEFAULT 'exam',   -- 'learn' | 'exam'
    question_ids  TEXT NOT NULL,
    word_ids      TEXT NOT NULL DEFAULT '[]',     -- word IDs being learned
    answers       TEXT NOT NULL DEFAULT '{}',
    current_index INTEGER NOT NULL DEFAULT 0,
    started_at    TEXT NOT NULL,
    submitted_at  TEXT,
    learner_name  TEXT
);

CREATE TABLE IF NOT EXISTS quiz_scores (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    session_key  TEXT NOT NULL,
    quiz_type    TEXT NOT NULL DEFAULT 'exam',
    learner_name TEXT,
    score_pct    REAL NOT NULL,
    correct      INTEGER NOT NULL,
    total        INTEGER NOT NULL,
    taken_at     TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS word_progress (
    word_id        INTEGER PRIMARY KEY,
    times_seen     INTEGER NOT NULL DEFAULT 0,
    times_correct  INTEGER NOT NULL DEFAULT 0,
    mastered       INTEGER NOT NULL DEFAULT 0,
    last_seen      TEXT
);
"""


def init_user_db() -> None:
    log.info("Initialising user.db schema")
    conn = user_db()
    try:
        conn.executescript(_USER_SCHEMA)
        # ── migrate existing tables that lack new columns ──────────────────
        existing_qs_cols = {
            row[1] for row in
            conn.execute("PRAGMA table_info(quiz_sessions)").fetchall()
        }
        if "quiz_type" not in existing_qs_cols:
            log.info("Migrating quiz_sessions: adding quiz_type column")
            conn.execute(
                "ALTER TABLE quiz_sessions ADD COLUMN quiz_type TEXT NOT NULL DEFAULT 'exam'"
            )
        if "word_ids" not in existing_qs_cols:
            log.info("Migrating quiz_sessions: adding word_ids column")
            conn.execute(
                "ALTER TABLE quiz_sessions ADD COLUMN word_ids TEXT NOT NULL DEFAULT '[]'"
            )

        existing_score_cols = {
            row[1] for row in
            conn.execute("PRAGMA table_info(quiz_scores)").fetchall()
        }
        if "quiz_type" not in existing_score_cols:
            log.info("Migrating quiz_scores: adding quiz_type column")
            conn.execute(
                "ALTER TABLE quiz_scores ADD COLUMN quiz_type TEXT NOT NULL DEFAULT 'exam'"
            )

        conn.commit()
        log.info("user.db ready")
    finally:
        conn.close()


def reset_user_data() -> None:
    """
    Wipe every table in user.db — quiz sessions, scores, and word progress.
    Used by the 'Reset Progress' feature.  The schema is preserved; only rows
    are deleted so the app continues working immediately after the reset.
    """
    conn = user_db()
    try:
        conn.execute("DELETE FROM quiz_sessions")
        conn.execute("DELETE FROM quiz_scores")
        conn.execute("DELETE FROM word_progress")
        conn.commit()
        log.info("[1.0.2.2] User data reset — all tables cleared")
    finally:
        conn.close()


# ─────────────────────────────────────────────────────────────────────────────
# Quiz-session helpers
# ─────────────────────────────────────────────────────────────────────────────

def get_session(key: str) -> dict | None:
    log.info("Fetching session key=%s", key)
    conn = user_db()
    try:
        row = conn.execute(
            "SELECT * FROM quiz_sessions WHERE session_key=?", (key,)
        ).fetchone()
        if not row:
            return None
        d = dict(row)
        d["question_ids"] = json.loads(d["question_ids"])
        d["word_ids"]     = json.loads(d.get("word_ids") or "[]")
        d["answers"]      = json.loads(d["answers"])
        return d
    finally:
        conn.close()


def save_session(key: str, quiz_type: str, question_ids: list[int],
                 word_ids: list[int], answers: dict, current_index: int,
                 started_at: str, submitted_at: str | None = None,
                 learner_name: str | None = None) -> None:
    log.info("Saving session key=%s type=%s idx=%d answered=%d",
             key, quiz_type, current_index, len(answers))
    conn = user_db()
    try:
        conn.execute(
            """
            INSERT INTO quiz_sessions
              (session_key, quiz_type, question_ids, word_ids, answers,
               current_index, started_at, submitted_at, learner_name)
            VALUES (?,?,?,?,?,?,?,?,?)
            ON CONFLICT(session_key) DO UPDATE SET
              answers       = excluded.answers,
              current_index = excluded.current_index,
              submitted_at  = excluded.submitted_at,
              learner_name  = excluded.learner_name
            """,
            (key, quiz_type,
             json.dumps(question_ids), json.dumps(word_ids),
             json.dumps(answers), current_index,
             started_at, submitted_at, learner_name),
        )
        conn.commit()
    finally:
        conn.close()


def save_score(session_key: str, quiz_type: str, learner_name: str,
               correct: int, total: int, taken_at: str) -> None:
    score_pct = round(correct / total * 100, 2) if total else 0.0
    log.info("Saving score session=%s type=%s pct=%.1f%%",
             session_key, quiz_type, score_pct)
    conn = user_db()
    try:
        conn.execute(
            """INSERT INTO quiz_scores
               (session_key, quiz_type, learner_name,
                score_pct, correct, total, taken_at)
               VALUES (?,?,?,?,?,?,?)""",
            (session_key, quiz_type, learner_name,
             score_pct, correct, total, taken_at),
        )
        conn.commit()
    finally:
        conn.close()


def score_already_saved(session_key: str) -> bool:
    conn = user_db()
    try:
        return bool(conn.execute(
            "SELECT 1 FROM quiz_scores WHERE session_key=?", (session_key,)
        ).fetchone())
    finally:
        conn.close()


# ─────────────────────────────────────────────────────────────────────────────
# Word-progress helpers
# ─────────────────────────────────────────────────────────────────────────────

def mark_word_learn_result(word_id: int,
                           questions_correct: int,
                           questions_total: int) -> None:
    """
    Update a word's progress after a learn-quiz.
    A word is marked 'mastered' only if ALL its questions were correct (100%).
    """
    mastered_flag = 1 if questions_correct == questions_total else 0
    log.debug("mark_word word_id=%d correct=%d/%d mastered=%d",
              word_id, questions_correct, questions_total, mastered_flag)
    conn = user_db()
    try:
        conn.execute(
            """
            INSERT INTO word_progress
              (word_id, times_seen, times_correct, mastered, last_seen)
            VALUES (?, ?, ?, ?, datetime('now'))
            ON CONFLICT(word_id) DO UPDATE SET
              times_seen    = times_seen    + ?,
              times_correct = times_correct + ?,
              mastered      = CASE WHEN ? = 1 THEN 1 ELSE mastered END,
              last_seen     = datetime('now')
            """,
            (word_id, questions_total, questions_correct, mastered_flag,
             questions_total, questions_correct, mastered_flag),
        )
        conn.commit()
    finally:
        conn.close()


def get_mastered_count() -> int:
    conn = user_db()
    try:
        return conn.execute(
            "SELECT COUNT(1) FROM word_progress WHERE mastered=1"
        ).fetchone()[0]
    finally:
        conn.close()


def get_seen_word_ids() -> set[int]:
    conn = user_db()
    try:
        rows = conn.execute(
            "SELECT word_id FROM word_progress WHERE times_seen > 0"
        ).fetchall()
        return {int(r[0]) for r in rows}
    finally:
        conn.close()


def get_mastered_word_ids() -> set[int]:
    conn = user_db()
    try:
        rows = conn.execute(
            "SELECT word_id FROM word_progress WHERE mastered=1"
        ).fetchall()
        return {int(r[0]) for r in rows}
    finally:
        conn.close()


def get_recent_exam_scores(limit: int = 10) -> list[dict]:
    conn = user_db()
    try:
        rows = conn.execute(
            "SELECT * FROM quiz_scores WHERE quiz_type='exam' "
            "ORDER BY taken_at DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


# ─────────────────────────────────────────────────────────────────────────────
# Content query helpers
# ─────────────────────────────────────────────────────────────────────────────

def get_unseen_words(limit: int = 10) -> list[dict]:
    """Return up to `limit` vocabulary words not yet seen by the user."""
    seen_ids = get_seen_word_ids()
    log.info("Fetching %d unseen words (already seen: %d)", limit, len(seen_ids))
    conn = content_db()
    try:
        rows = conn.execute(
            "SELECT id, word, translation, category, audio_path "
            "FROM vocabulary ORDER BY id"
        ).fetchall()
        unseen = [dict(r) for r in rows if int(r["id"]) not in seen_ids]
        return unseen[:limit]
    finally:
        conn.close()


def get_vocab_questions_for_words(word_ids: list[int],
                                  n_per_word: int = 2) -> list[dict]:
    """
    Return exactly n_per_word questions for each word_id.
    Questions are shuffled but grouped by word so every word is represented.
    """
    if not word_ids:
        return []
    log.info("Fetching %d vocab questions for %d words",
             n_per_word * len(word_ids), len(word_ids))
    conn = content_db()
    try:
        buckets: list[list[dict]] = []
        for wid in word_ids:
            rows = conn.execute(
                "SELECT * FROM questions "
                "WHERE category='vocabulary' AND word_id=? "
                "ORDER BY RANDOM() LIMIT ?",
                (wid, n_per_word),
            ).fetchall()
            buckets.append([dict(r) for r in rows])

        # interleave so questions don't all cluster by word
        merged: list[dict] = []
        while any(buckets):
            for bucket in buckets:
                if bucket:
                    merged.append(bucket.pop(0))
        return merged
    finally:
        conn.close()


def get_mastered_vocab_questions(limit: int = 20) -> list[dict]:
    """Pick random questions from mastered words for Practice mode."""
    mastered = list(get_mastered_word_ids())
    if not mastered:
        return []
    random.shuffle(mastered)
    sample = mastered[:limit]
    return get_vocab_questions_for_words(sample, n_per_word=2)[:limit]


def get_last_practice_info() -> dict | None:
    """Return the date, word count, and word score of the most recent practice session."""
    conn = user_db()
    try:
        row = conn.execute(
            "SELECT taken_at, total, correct FROM quiz_scores "
            "WHERE quiz_type='practice' ORDER BY taken_at DESC LIMIT 1"
        ).fetchone()
        if row:
            return {
                "date":    row["taken_at"][:10],
                "count":   row["total"],     # words reviewed (1 question per word)
                "correct": row["correct"],   # successful words
            }
        return None
    finally:
        conn.close()


def get_practice_words(limit: int = 10,
                       exclude_ids: list[int] | None = None,
                       prioritize_ids: list[int] | None = None) -> list[int]:
    """
    Pick up to `limit` mastered word IDs for a spaced-repetition practice round.

    prioritize_ids: appear first (words the learner got wrong last round).
    exclude_ids:    skip these entirely (words already reviewed this session,
                    UNLESS they also appear in prioritize_ids).
    """
    exclude_set = set(exclude_ids or [])
    priority    = [i for i in (prioritize_ids or [])][:limit]
    result      = list(priority)

    remaining = limit - len(result)
    if remaining > 0:
        all_mastered = list(get_mastered_word_ids())
        available = [i for i in all_mastered
                     if i not in exclude_set and i not in result]
        random.shuffle(available)
        result += available[:remaining]

    log.info("get_practice_words: selected=%d (priority=%d)", len(result), len(priority))
    return result


def select_exam_questions(reading_quota: int = 5,
                          listening_quota: int = 5,
                          grammar_quota:   int = 10) -> list[dict]:
    """
    Assemble a 20-question A1 mock exam:
      • 2 random passages → sample down to reading_quota questions
      • listening_quota random listening questions
      • fill remaining with grammar/vocabulary
    Reading questions come first (grouped by passage), then the rest shuffled.
    """
    log.info("Building exam: reading=%d listening=%d grammar=%d",
             reading_quota, listening_quota, grammar_quota)
    conn = content_db()
    try:
        # ── Reading ──────────────────────────────────────────────────────────
        passage_ids = [
            int(r["id"]) for r in
            conn.execute(
                "SELECT id FROM passages ORDER BY RANDOM() LIMIT 2"
            ).fetchall()
        ]
        reading_rows: list[dict] = []
        if passage_ids:
            ph   = ",".join("?" * len(passage_ids))
            pool = [dict(r) for r in conn.execute(
                f"SELECT * FROM questions WHERE category='reading' "
                f"AND passage_id IN ({ph}) ORDER BY passage_id, id",
                tuple(passage_ids),
            ).fetchall()]
            if len(pool) > reading_quota:
                random.shuffle(pool)
                pool = sorted(pool[:reading_quota],
                              key=lambda r: (r["passage_id"], r["id"]))
            reading_rows = pool

        # ── Listening ─────────────────────────────────────────────────────
        listening_rows = [dict(r) for r in conn.execute(
            "SELECT * FROM questions WHERE category='listening' "
            "ORDER BY RANDOM() LIMIT ?", (listening_quota,)
        ).fetchall()]

        # ── Grammar / Vocab fill — at least 3 pure grammar guaranteed ────────
        need = max(
            0, reading_quota + listening_quota + grammar_quota
               - len(reading_rows) - len(listening_rows)
        )
        # Step 1: pull at least 3 (or up to 'need') pure grammar questions
        grammar_min = min(3, need)
        grammar_guaranteed = [dict(r) for r in conn.execute(
            "SELECT * FROM questions WHERE category='grammar' "
            "ORDER BY RANDOM() LIMIT ?", (grammar_min,)
        ).fetchall()]

        # Step 2: fill remaining slots with mixed grammar+vocabulary
        remaining = need - len(grammar_guaranteed)
        if remaining > 0:
            skip_ids = tuple(r["id"] for r in grammar_guaranteed)
            if skip_ids:
                ph = ",".join("?" * len(skip_ids))
                filler = [dict(r) for r in conn.execute(
                    f"SELECT * FROM questions "
                    f"WHERE category IN ('grammar','vocabulary') AND id NOT IN ({ph}) "
                    "ORDER BY RANDOM() LIMIT ?",
                    skip_ids + (remaining,),
                ).fetchall()]
            else:
                filler = [dict(r) for r in conn.execute(
                    "SELECT * FROM questions WHERE category IN ('grammar','vocabulary') "
                    "ORDER BY RANDOM() LIMIT ?", (remaining,)
                ).fetchall()]
            grammar_rows = grammar_guaranteed + filler
        else:
            grammar_rows = grammar_guaranteed

        others = listening_rows + grammar_rows
        random.shuffle(others)
        result = reading_rows + others
        pure_gram = sum(1 for r in grammar_rows if r["category"] == "grammar")
        log.info("[1.0.1.0] Exam assembled: total=%d (grammar=%d guaranteed≥3)",
                 len(result), pure_gram)
        return result
    finally:
        conn.close()


def get_passage_text(passage_id: int) -> str | None:
    conn = content_db()
    try:
        row = conn.execute(
            "SELECT text FROM passages WHERE id=?", (passage_id,)
        ).fetchone()
        return row["text"] if row else None
    finally:
        conn.close()


def get_questions_by_ids(ids: list[int]) -> list[dict]:
    if not ids:
        return []
    log.info("Fetching %d questions by id", len(ids))
    conn = content_db()
    try:
        ph    = ",".join("?" * len(ids))
        rows  = conn.execute(
            f"SELECT * FROM questions WHERE id IN ({ph})", tuple(ids)
        ).fetchall()
        by_id = {int(r["id"]): dict(r) for r in rows}
        return [by_id[i] for i in ids if i in by_id]
    finally:
        conn.close()


def get_vocab_list(limit: int = 600) -> list[dict]:
    conn = content_db()
    try:
        return [dict(r) for r in conn.execute(
            "SELECT id, word, translation, category, audio_path "
            "FROM vocabulary ORDER BY id LIMIT ?", (limit,)
        ).fetchall()]
    finally:
        conn.close()


def get_db_stats() -> dict:
    conn = content_db()
    try:
        cats = {
            r["category"]: r["n"]
            for r in conn.execute(
                "SELECT category, COUNT(1) AS n FROM questions GROUP BY category"
            ).fetchall()
        }
        return {
            "vocabulary_words":     conn.execute("SELECT COUNT(1) FROM vocabulary").fetchone()[0],
            "passages":             conn.execute("SELECT COUNT(1) FROM passages").fetchone()[0],
            "listening_clips":      conn.execute("SELECT COUNT(1) FROM listening_clips").fetchone()[0],
            "questions_reading":    cats.get("reading", 0),
            "questions_listening":  cats.get("listening", 0),
            "questions_grammar":    cats.get("grammar", 0),
            "questions_vocabulary": cats.get("vocabulary", 0),
            "questions_total":      sum(cats.values()),
        }
    finally:
        conn.close()
