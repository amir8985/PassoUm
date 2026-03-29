"""
add_audio_questions.py — ONE-TIME local migration
===================================================
Adds the fourth vocabulary question type (Audio → English) to the
existing content.db, using the audio_path already stored on every word.

Run ONCE locally:
    python add_audio_questions.py

It is safe to re-run — it detects existing audio questions and exits early.
Do NOT run on the server; content.db is read-only there.
"""
import random
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "content.db"


def main() -> None:
    if not DB_PATH.exists():
        print(f"ERROR: {DB_PATH} not found. Run seed/build_content_db.py first.")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # ── Guard: skip if audio questions already exist ──────────────────────
    existing = conn.execute(
        "SELECT COUNT(1) FROM questions "
        "WHERE category='vocabulary' AND audio_path != '' AND audio_path IS NOT NULL"
    ).fetchone()[0]
    if existing > 0:
        print(f"Audio vocabulary questions already present ({existing:,}). Nothing to do.")
        conn.close()
        return

    # ── Load all vocabulary words ─────────────────────────────────────────
    words = conn.execute(
        "SELECT id, word, translation, category, audio_path FROM vocabulary"
    ).fetchall()
    print(f"Loaded {len(words):,} words from vocabulary table.")

    # Verify audio coverage
    with_audio    = [w for w in words if w["audio_path"]]
    without_audio = [w for w in words if not w["audio_path"]]
    print(f"  {len(with_audio):,} words have audio_path  |  "
          f"{len(without_audio):,} words missing audio (will be skipped)")

    # ── Build category index for same-category distractors ────────────────
    by_cat: dict[str, list] = {}
    for w in words:
        by_cat.setdefault(w["category"], []).append(w)

    random.seed(42)
    inserts = []

    for w in with_audio:
        wid         = int(w["id"])
        translation = w["translation"]
        category    = w["category"]
        audio_path  = w["audio_path"]

        # 3 English-translation distractors from the same category
        pool = [x for x in by_cat.get(category, []) if int(x["id"]) != wid]
        if len(pool) < 3:
            pool = [x for x in words if int(x["id"]) != wid]
        sample = random.sample(pool, min(3, len(pool)))
        while len(sample) < 3:
            sample.append(random.choice(pool))
        distractors = [x["translation"] for x in sample[:3]]

        opts = [translation] + distractors
        random.shuffle(opts)

        inserts.append({
            "category":      "vocabulary",
            "word_id":       wid,
            "question_text": "What is the meaning of the word you just heard?",
            "option_a":      opts[0],
            "option_b":      opts[1],
            "option_c":      opts[2],
            "option_d":      opts[3],
            "correct_answer": translation,
            "topic":         category,
            "audio_path":    audio_path,
        })

    # ── Insert all questions ──────────────────────────────────────────────
    conn.executemany(
        """
        INSERT INTO questions
            (category, word_id, question_text,
             option_a, option_b, option_c, option_d,
             correct_answer, topic, audio_path)
        VALUES
            (:category, :word_id, :question_text,
             :option_a, :option_b, :option_c, :option_d,
             :correct_answer, :topic, :audio_path)
        """,
        inserts,
    )
    conn.commit()

    # ── Final report ──────────────────────────────────────────────────────
    total_vocab_qs = conn.execute(
        "SELECT COUNT(1) FROM questions WHERE category='vocabulary'"
    ).fetchone()[0]
    audio_qs = conn.execute(
        "SELECT COUNT(1) FROM questions WHERE category='vocabulary' AND audio_path != ''"
    ).fetchone()[0]
    conn.close()

    print(f"\nDONE: Inserted {len(inserts):,} audio vocabulary questions.")
    print(f"  Total vocab questions in DB : {total_vocab_qs:,}  "
          f"(was {total_vocab_qs - len(inserts):,}, now +{len(inserts):,})")
    print(f"  Audio-type questions        : {audio_qs:,}")
    print("\nAll audio_path links intact. No new audio files generated.")
    print("Commit content.db to git when ready to deploy.")


if __name__ == "__main__":
    main()
