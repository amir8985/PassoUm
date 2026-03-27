"""
build_content_db.py  —  Run ONCE locally to produce:
  • content.db   (pre-built, read-only static asset)
  • static/audio/*.mp3  (gTTS European Portuguese, lang='pt', tld='pt')

Usage:
    cd <project_root>
    python seed/build_content_db.py

Set SKIP_AUDIO=1 to rebuild DB only, skipping audio (fast re-seed).
"""

import logging
import os
import random
import sqlite3
import sys
from pathlib import Path

# ── paths ──────────────────────────────────────────────────────────────────
ROOT      = Path(__file__).resolve().parent.parent
DB_PATH   = ROOT / "content.db"
AUDIO_DIR = ROOT / "static" / "audio"

sys.path.insert(0, str(ROOT))           # so we can import config
sys.path.insert(0, str(ROOT / "seed"))  # so we can import seed modules

# ── logging ────────────────────────────────────────────────────────────────
LOG_FORMAT = "%(asctime)s  [%(levelname)-8s]  %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt="%H:%M:%S")
log = logging.getLogger("build_content_db")

SKIP_AUDIO = os.getenv("SKIP_AUDIO", "0") == "1"

# ──────────────────────────────────────────────────────────────────────────
# Schema
# ──────────────────────────────────────────────────────────────────────────

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS vocabulary (
    id          INTEGER PRIMARY KEY,
    word        TEXT    NOT NULL,
    translation TEXT    NOT NULL,
    category    TEXT    NOT NULL,
    audio_path  TEXT    NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS passages (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT    NOT NULL,
    text  TEXT    NOT NULL,
    topic TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS listening_clips (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    transcript TEXT    NOT NULL,
    topic      TEXT    NOT NULL,
    audio_path TEXT    NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS questions (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    category       TEXT    NOT NULL
                   CHECK (category IN ('vocabulary','grammar','listening','reading')),
    passage_id     INTEGER REFERENCES passages(id),
    clip_id        INTEGER REFERENCES listening_clips(id),
    word_id        INTEGER REFERENCES vocabulary(id),
    question_text  TEXT    NOT NULL,
    option_a       TEXT    NOT NULL,
    option_b       TEXT    NOT NULL,
    option_c       TEXT    NOT NULL,
    option_d       TEXT    NOT NULL,
    correct_answer TEXT    NOT NULL,
    topic          TEXT,
    audio_path     TEXT    NOT NULL DEFAULT ''
);
"""


# ──────────────────────────────────────────────────────────────────────────
# Audio helpers
# ──────────────────────────────────────────────────────────────────────────

def _audio_path(filename: str) -> str:
    return f"static/audio/{filename}"


def _generate_audio(text: str, filename: str) -> str:
    """Generate MP3 via gTTS (European PT). Returns relative path."""
    dest = AUDIO_DIR / filename
    if dest.exists():
        return _audio_path(filename)
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang="pt", tld="pt", slow=False)
        tts.save(str(dest))
        log.info("  🔊 %s", filename)
    except Exception as exc:
        log.warning("  Audio FAILED for %s: %s", filename, exc)
    return _audio_path(filename)


# ──────────────────────────────────────────────────────────────────────────
# Grammar question instruction prefixer
# ──────────────────────────────────────────────────────────────────────────

_PT_TO_EN_PHRASES: dict[str, str] = {
    "Como se diz 'thank you' em português?":       "How do you say 'thank you' in Portuguese?",
    "Como se diz 'you're welcome' em português?":  "How do you say 'you're welcome' in Portuguese?",
    "O que significa 'com licença'?":              "What does 'com licença' mean?",
    "Qual é a tradução de 'Bom dia'?":             "What is the translation of 'Bom dia'?",
    "O que quer dizer 'até logo'?":                "What does 'até logo' mean?",
    "Qual é a tradução de 'Boa noite'?":           "What is the translation of 'Boa noite'?",
    "Um livro → ___":                              "What is the plural of: um livro",
    "Uma cidade → ___":                            "What is the plural of: uma cidade",
    "Um pão → ___":                                "What is the plural of: um pão",
    "Um animal → ___":                             "What is the plural of: um animal",
    "Um português → ___":                          "What is the plural of: um português",
    "Uma flor → ___":                              "What is the plural of: uma flor",
    "Um irmão → ___":                              "What is the plural of: um irmão",
}


def _apply_grammar_instruction(q_text: str) -> str:
    """
    Return an English-instructed version of a grammar question_text.
    • Exact-match lookup for known phrase/translation questions.
    • Any question containing ___ → 'Fill in the blank:' prefix.
    • Everything else is returned as-is.
    """
    # direct English translation for known Portuguese instructions
    if q_text in _PT_TO_EN_PHRASES:
        return _PT_TO_EN_PHRASES[q_text]

    # all fill-in-blank patterns (whether at start or mid-sentence)
    if "___" in q_text:
        return f"Fill in the blank: {q_text}"

    return q_text


# ──────────────────────────────────────────────────────────────────────────
# Vocabulary MCQ generation
# ──────────────────────────────────────────────────────────────────────────

def _make_vocab_questions(words: list[tuple]) -> list[dict]:
    """
    Generate 3 MCQ types per word using other words as distractors.
    words: list of (id, word, translation, category)
    Returns list of question dicts ready for DB insert.
    """
    log.info("Generating vocabulary MCQs for %d words …", len(words))
    random.seed(42)

    # index by category for smarter distractors
    by_cat: dict[str, list] = {}
    for w in words:
        by_cat.setdefault(w[3], []).append(w)

    questions = []

    for wid, word, translation, category in words:
        pool = by_cat.get(category, [])
        others = [w for w in pool if w[0] != wid]
        if len(others) < 3:
            others = [w for w in words if w[0] != wid]

        def _distractors_trans(n=3):
            sample = random.sample(others, min(n, len(others)))
            while len(sample) < n:
                sample.append(random.choice(others))
            return [s[2] for s in sample]

        def _distractors_word(n=3):
            sample = random.sample(others, min(n, len(others)))
            while len(sample) < n:
                sample.append(random.choice(others))
            return [s[1] for s in sample]

        dt = _distractors_trans()
        dw = _distractors_word()

        # Q1 — meaning: Portuguese → English
        opts_t = [translation] + dt[:3]
        random.shuffle(opts_t)
        questions.append({
            "category": "vocabulary",
            "word_id": wid,
            "question_text": f"What does «{word}» mean?",
            "option_a": opts_t[0], "option_b": opts_t[1],
            "option_c": opts_t[2], "option_d": opts_t[3],
            "correct_answer": translation,
            "topic": category,
        })

        # Q2 — translation: English → Portuguese
        opts_w = [word] + dw[:3]
        random.shuffle(opts_w)
        questions.append({
            "category": "vocabulary",
            "word_id": wid,
            "question_text": f"How do you say «{translation}» in Portuguese?",
            "option_a": opts_w[0], "option_b": opts_w[1],
            "option_c": opts_w[2], "option_d": opts_w[3],
            "correct_answer": word,
            "topic": category,
        })

        # Q3 — context fill-in (English instruction frame + Portuguese sentence)
        sentence, blank_answer, wrong1, wrong2, wrong3 = _context_question(
            word, translation, category, dw
        )
        opts_c = [blank_answer, wrong1, wrong2, wrong3]
        random.shuffle(opts_c)
        questions.append({
            "category": "vocabulary",
            "word_id": wid,
            "question_text": sentence,
            "option_a": opts_c[0], "option_b": opts_c[1],
            "option_c": opts_c[2], "option_d": opts_c[3],
            "correct_answer": blank_answer,
            "topic": category,
        })

    log.info("Generated %d vocabulary questions", len(questions))
    return questions


def _context_question(word, translation, category, distractors):
    """Return (sentence, correct, wrong1, wrong2, wrong3).
    English instruction frame wraps the Portuguese sentence being practised.
    """
    templates = {
        "verb":        f"Fill in the blank: Eu ___ todos os dias. ({translation})",
        "noun":        f"Fill in the blank: Isto é ___. ({translation})",
        "adjective":   f"Fill in the blank: Esta coisa é muito ___. ({translation})",
        "adverb":      f"Fill in the blank: Falo português ___. ({translation})",
        "number":      f"Fill in the blank: Tenho ___ maçãs. ({translation})",
        "phrase":      f"Choose the correct Portuguese phrase for: '{translation}'",
        "pronoun":     f"Fill in the blank: ___ sou português. ({translation})",
        "preposition": f"Fill in the blank: Estou ___ casa. ({translation})",
    }
    template = templates.get(category, f"Choose the correct Portuguese word for: '{translation}'")
    w1, w2, w3 = (distractors + distractors)[:3]
    return template, word, w1, w2, w3


# ──────────────────────────────────────────────────────────────────────────
# Main build
# ──────────────────────────────────────────────────────────────────────────

def main():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    # ── fresh DB ────────────────────────────────────────────────────────
    if DB_PATH.exists():
        log.info("Removing existing content.db")
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    conn.commit()
    log.info("Schema created in %s", DB_PATH)

    # ── 1. Vocabulary ───────────────────────────────────────────────────
    from words_600 import WORDS
    log.info("Inserting %d words …", len(WORDS))
    for wid, word, translation, category in WORDS:
        audio_file = f"word_{wid}.mp3"
        audio_rel  = _audio_path(audio_file)
        if not SKIP_AUDIO:
            _generate_audio(word, audio_file)
        conn.execute(
            "INSERT OR REPLACE INTO vocabulary (id, word, translation, category, audio_path) "
            "VALUES (?,?,?,?,?)",
            (wid, word, translation, category, audio_rel),
        )
    conn.commit()
    log.info("Vocabulary inserted.")

    # ── 2. Vocab MCQs ──────────────────────────────────────────────────
    vocab_qs = _make_vocab_questions(WORDS)
    for q in vocab_qs:
        conn.execute(
            """INSERT INTO questions
               (category, word_id, question_text,
                option_a, option_b, option_c, option_d, correct_answer, topic)
               VALUES (:category, :word_id, :question_text,
                       :option_a, :option_b, :option_c, :option_d,
                       :correct_answer, :topic)""",
            q,
        )
    conn.commit()
    log.info("Vocab MCQs inserted: %d", len(vocab_qs))

    # ── 3. Listening clips + questions ──────────────────────────────────
    from listening_40 import LISTENING
    log.info("Inserting %d listening clips …", len(LISTENING))
    for i, clip in enumerate(LISTENING, start=1):
        audio_file = f"clip_{i}.mp3"
        audio_rel  = _audio_path(audio_file)
        if not SKIP_AUDIO:
            _generate_audio(clip["transcript"], audio_file)
        cur = conn.execute(
            "INSERT INTO listening_clips (transcript, topic, audio_path) VALUES (?,?,?)",
            (clip["transcript"], clip["topic"], audio_rel),
        )
        clip_id = cur.lastrowid
        for q in clip["questions"]:
            conn.execute(
                """INSERT INTO questions
                   (category, clip_id, question_text,
                    option_a, option_b, option_c, option_d, correct_answer,
                    topic, audio_path)
                   VALUES ('listening', ?, ?,?,?,?,?,?,?,?)""",
                (clip_id, q["question_text"],
                 q["option_a"], q["option_b"], q["option_c"], q["option_d"],
                 q["correct_answer"], clip["topic"], audio_rel),
            )
    conn.commit()
    log.info("Listening inserted.")

    # ── 4. Passages + reading questions ─────────────────────────────────
    from passages_30 import PASSAGES
    log.info("Inserting %d passages …", len(PASSAGES))
    for passage in PASSAGES:
        cur = conn.execute(
            "INSERT INTO passages (title, text, topic) VALUES (?,?,?)",
            (passage["title"], passage["text"], passage["topic"]),
        )
        pid = cur.lastrowid
        for q in passage["questions"]:
            conn.execute(
                """INSERT INTO questions
                   (category, passage_id, question_text,
                    option_a, option_b, option_c, option_d, correct_answer, topic)
                   VALUES ('reading', ?, ?,?,?,?,?,?,?)""",
                (pid, q["question_text"],
                 q["option_a"], q["option_b"], q["option_c"], q["option_d"],
                 q["correct_answer"], passage["topic"]),
            )
    conn.commit()
    log.info("Passages inserted.")

    # ── 5. Grammar questions ────────────────────────────────────────────
    from grammar_400 import GRAMMAR
    log.info("Inserting %d grammar questions …", len(GRAMMAR))
    for q in GRAMMAR:
        conn.execute(
            """INSERT INTO questions
               (category, question_text,
                option_a, option_b, option_c, option_d, correct_answer, topic)
               VALUES ('grammar', ?,?,?,?,?,?,?)""",
            (_apply_grammar_instruction(q["question_text"]),
             q["option_a"], q["option_b"], q["option_c"], q["option_d"],
             q["correct_answer"], q["topic"]),
        )
    conn.commit()
    log.info("Grammar questions inserted.")

    conn.close()

    # ── Summary ─────────────────────────────────────────────────────────
    conn2 = sqlite3.connect(DB_PATH)
    stats = {
        "vocabulary":       conn2.execute("SELECT COUNT(1) FROM vocabulary").fetchone()[0],
        "passages":         conn2.execute("SELECT COUNT(1) FROM passages").fetchone()[0],
        "listening_clips":  conn2.execute("SELECT COUNT(1) FROM listening_clips").fetchone()[0],
        "q_vocabulary":     conn2.execute("SELECT COUNT(1) FROM questions WHERE category='vocabulary'").fetchone()[0],
        "q_grammar":        conn2.execute("SELECT COUNT(1) FROM questions WHERE category='grammar'").fetchone()[0],
        "q_listening":      conn2.execute("SELECT COUNT(1) FROM questions WHERE category='listening'").fetchone()[0],
        "q_reading":        conn2.execute("SELECT COUNT(1) FROM questions WHERE category='reading'").fetchone()[0],
        "q_total":          conn2.execute("SELECT COUNT(1) FROM questions").fetchone()[0],
    }
    conn2.close()

    log.info("=" * 60)
    log.info("BUILD COMPLETE — content.db summary:")
    for k, v in stats.items():
        log.info("  %-25s %d", k, v)
    log.info("=" * 60)


if __name__ == "__main__":
    main()
