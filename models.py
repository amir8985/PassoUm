"""
DB connection helpers for content.db (read-only static asset).

v1.0.3.1 — user.db removed entirely.  All user progress is stored in the
browser via localStorage.  This module only serves content: vocabulary,
questions, passages, and stats.
"""
from version import __version__  # noqa: F401 — version stamped in logs via config

import random
import sqlite3

from config import CONTENT_DB_PATH, get_logger

log = get_logger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Connection helper
# ─────────────────────────────────────────────────────────────────────────────

def content_db() -> sqlite3.Connection:
    """Open content.db in read-only mode (immutable static asset)."""
    log.debug("Opening content.db (read-only)")
    conn = sqlite3.connect(f"file:{CONTENT_DB_PATH}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


# ─────────────────────────────────────────────────────────────────────────────
# Static content helpers
# ─────────────────────────────────────────────────────────────────────────────

def get_db_stats() -> dict:
    """Return content counts for the home-screen statistics row."""
    conn = content_db()
    try:
        vocab     = conn.execute("SELECT COUNT(1) FROM vocabulary").fetchone()[0]
        vocab_q   = conn.execute(
            "SELECT COUNT(1) FROM questions WHERE category='vocabulary'"
        ).fetchone()[0]
        grammar   = conn.execute(
            "SELECT COUNT(1) FROM questions WHERE category='grammar'"
        ).fetchone()[0]
        reading   = conn.execute(
            "SELECT COUNT(1) FROM questions WHERE category='reading'"
        ).fetchone()[0]
        listening = conn.execute(
            "SELECT COUNT(1) FROM questions WHERE category='listening'"
        ).fetchone()[0]
        return {
            "vocabulary_words":     vocab,
            "questions_vocabulary": vocab_q,
            "questions_grammar":    grammar,
            "questions_reading":    reading,
            "questions_listening":  listening,
        }
    finally:
        conn.close()


def get_vocab_list() -> list[dict]:
    """Return all vocabulary words for the Vocabulary page."""
    log.info("Fetching full vocab list")
    conn = content_db()
    try:
        rows = conn.execute(
            "SELECT id, word, translation, category, audio_path "
            "FROM vocabulary ORDER BY id"
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


# ─────────────────────────────────────────────────────────────────────────────
# Question helpers
# ─────────────────────────────────────────────────────────────────────────────

def _enrich_with_passages(questions: list[dict]) -> list[dict]:
    """Add passage_text field to reading questions that have a passage_id."""
    if not questions:
        return questions
    pid_set = {q.get("passage_id") for q in questions if q.get("passage_id")}
    if not pid_set:
        for q in questions:
            q["passage_text"] = None
        return questions
    conn = content_db()
    try:
        ph = ",".join("?" * len(pid_set))
        rows = conn.execute(
            f"SELECT id, text FROM passages WHERE id IN ({ph})", tuple(pid_set)
        ).fetchall()
        passage_map = {int(r["id"]): r["text"] for r in rows}
    finally:
        conn.close()
    for q in questions:
        q["passage_text"] = passage_map.get(int(q.get("passage_id") or 0))
    return questions


def get_vocab_questions_for_words(word_ids: list[int],
                                  n_per_word: int = 2) -> list[dict]:
    """
    Return n_per_word random questions per word, interleaved so questions
    don't cluster by word.
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
        merged: list[dict] = []
        while any(buckets):
            for bucket in buckets:
                if bucket:
                    merged.append(bucket.pop(0))
        return merged
    finally:
        conn.close()


def _select_exam_questions(reading_quota: int = 5,
                           listening_quota: int = 5,
                           grammar_quota: int = 10) -> list[dict]:
    """Assemble a 20-question exam set (passage-enriched by caller)."""
    conn = content_db()
    try:
        # Reading — 2 random passages
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

        # Listening
        listening_rows = [dict(r) for r in conn.execute(
            "SELECT * FROM questions WHERE category='listening' "
            "ORDER BY RANDOM() LIMIT ?", (listening_quota,)
        ).fetchall()]

        # Grammar / Vocab fill (min 3 pure grammar)
        need = max(
            0, reading_quota + listening_quota + grammar_quota
            - len(reading_rows) - len(listening_rows)
        )
        grammar_min = min(3, need)
        grammar_guaranteed = [dict(r) for r in conn.execute(
            "SELECT * FROM questions WHERE category='grammar' "
            "ORDER BY RANDOM() LIMIT ?", (grammar_min,)
        ).fetchall()]
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
                    "SELECT * FROM questions "
                    "WHERE category IN ('grammar','vocabulary') "
                    "ORDER BY RANDOM() LIMIT ?", (remaining,)
                ).fetchall()]
            grammar_rows = grammar_guaranteed + filler
        else:
            grammar_rows = grammar_guaranteed

        others = listening_rows + grammar_rows
        random.shuffle(others)
        return reading_rows + others
    finally:
        conn.close()


# ─────────────────────────────────────────────────────────────────────────────
# JSON API bundle helpers  (called by /api/* routes in routes.py)
# ─────────────────────────────────────────────────────────────────────────────

def get_learn_bundle(seen_ids: list[int], limit: int = 10) -> dict:
    """
    Pick `limit` unseen vocabulary words and return their data plus
    2 questions each (interleaved, random type per question).

    Returns {"no_more": True} when all 600 words have been seen.
    """
    seen_set = set(seen_ids)
    conn = content_db()
    try:
        rows = conn.execute(
            "SELECT id, word, translation, category, audio_path "
            "FROM vocabulary ORDER BY id"
        ).fetchall()
        unseen = [dict(r) for r in rows if int(r["id"]) not in seen_set]
    finally:
        conn.close()

    if not unseen:
        return {"no_more": True, "words": [], "questions": []}

    words     = unseen[:limit]
    word_ids  = [int(w["id"]) for w in words]
    questions = get_vocab_questions_for_words(word_ids, n_per_word=2)
    return {
        "no_more":   False,
        "words":     words,
        "questions": [dict(q) for q in questions],
    }


def get_practice_bundle(mastered_ids: list[int],
                        exclude_ids: list[int],
                        limit: int = 10) -> dict:
    """
    Pick `limit` mastered words that aren't in exclude_ids.

    mastered_ids should be pre-ordered by the client (failed words first,
    rest shuffled) — this function preserves that order, no server-side shuffle.

    Returns {"questions": [], "word_ids": [], "has_more": False} when empty.
    """
    exclude_set = set(exclude_ids)
    available   = [mid for mid in mastered_ids if mid not in exclude_set]
    selected    = available[:limit]

    if not selected:
        return {"questions": [], "word_ids": [], "has_more": False}

    questions = get_vocab_questions_for_words(selected, n_per_word=1)
    return {
        "questions": [dict(q) for q in questions],
        "word_ids":  selected,
        "has_more":  len(available) > limit,
    }


def get_exam_bundle() -> dict:
    """Return a fresh 20-question exam with passage texts embedded."""
    questions = _select_exam_questions()
    questions = _enrich_with_passages(questions)
    return {"questions": [dict(q) for q in questions]}
