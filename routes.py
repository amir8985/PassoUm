"""
Flask route definitions for PassoUm.
Version sourced from version.py — do not hard-code elsewhere.
Routes:
  /                         — Home dashboard (4 buttons)
  /vocabulary               — Full word list
  /learn/words              — Show 10 new words before quiz
  /learn/start              — POST: kick off step-by-step learn quiz
  /practice/start           — POST: kick off practice quiz (mastered words)
  /exam                     — Mock-exam hub (history + start button)
  /exam/start               — POST: build a 20-question mock exam session
  /exam/session             — GET: single-page scrollable mock exam
  /exam/session/submit      — POST: record all answers, redirect to results
  /quiz/question            — Step-by-step question view (learn / practice)
  /quiz/answer              — POST: record one answer, advance index
  /quiz/results             — Final score + per-question breakdown
  /quiz/restart             — POST: clear session, return home
  /db-status                — JSON debug endpoint
"""
from version import __version__  # noqa: F401 — version stamped in logs via config

import json
import uuid
from datetime import datetime, timezone

from flask import (
    Flask, abort, jsonify, redirect, render_template,
    request, session, url_for,
)

from config import APP_VERSION, CONTENT_DB_PATH, get_logger
from models import (
    get_db_stats, get_mastered_count, get_passage_text,
    get_questions_by_ids, get_recent_exam_scores,
    get_unseen_words, get_vocab_list,
    get_vocab_questions_for_words, get_mastered_vocab_questions,
    get_last_practice_info, get_practice_words,
    init_user_db, mark_word_learn_result,
    save_score, save_session, score_already_saved,
    select_exam_questions, get_session,
)

log = get_logger(__name__)


def register_routes(app: Flask) -> None:
    log.info("[1.0.0.6] Build 1.0.0.6 - Disabled instant feedback in Exam mode; "
             "Enabled full review post-submission.")
    log.info("[1.0.0.7] Mobile-first dashboard, vocabulary progress bar, "
             "spaced-repetition practice logic.")
    log.info("[1.0.0.9] Continuous session counting for practice; "
             "content statistics row on home screen.")
    log.info("[1.0.0.8] Practice: 1 question/word (10 total), Scenario A/B end-of-session.")

    # ── helpers ────────────────────────────────────────────────────────────

    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

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

    # ── static pages ───────────────────────────────────────────────────────

    @app.route("/")
    def index():
        log.info("GET /")
        mastered      = get_mastered_count()          if _db_ok() else 0
        exam_history  = get_recent_exam_scores(limit=3) if _db_ok() else []
        content_stats = get_db_stats()                if _db_ok() else {}
        return render_template(
            "index.html",
            mastered_count = mastered,
            exam_history   = exam_history,
            content_stats  = content_stats,
        )

    @app.route("/vocabulary")
    def vocabulary():
        log.info("GET /vocabulary")
        err = _db_required()
        if err:
            return err
        words = get_vocab_list()
        return render_template("vocabulary.html", words=words)

    @app.route("/db-status")
    def db_status():
        log.info("GET /db-status")
        if not _db_ok():
            return jsonify({"error": "content.db not found"}), 503
        return jsonify(get_db_stats())

    # ── Learn New Words ─────────────────────────────────────────────────────

    @app.route("/learn/words")
    def learn_words():
        """Show 10 unseen words; user reviews them, then starts the quiz."""
        log.info("GET /learn/words")
        err = _db_required()
        if err:
            return err
        words = get_unseen_words(limit=10)
        if not words:
            return render_template(
                "error.html",
                message="You have already seen all 600 words! "
                        "Use 'Practice Known Words' to keep revising."
            )
        session["pending_learn_word_ids"] = [int(w["id"]) for w in words]
        return render_template("learn.html", words=words)

    @app.route("/learn/start", methods=["POST"])
    def learn_start():
        """Build a 20-question step-by-step quiz (2 per word) for the 10 pending words."""
        log.info("POST /learn/start")
        err = _db_required()
        if err:
            return err
        word_ids = session.get("pending_learn_word_ids", [])
        if not word_ids:
            return redirect(url_for("learn_words"))

        questions = get_vocab_questions_for_words(word_ids, n_per_word=2)
        if not questions:
            return render_template(
                "error.html",
                message="No vocabulary questions found for these words."
            )

        key = str(uuid.uuid4())
        session["quiz_key"]      = key
        session["quiz_type"]     = "learn"
        session["learner_name"]  = "Learner"

        save_session(
            key           = key,
            quiz_type     = "learn",
            question_ids  = [int(q["id"]) for q in questions],
            word_ids      = word_ids,
            answers       = {},
            current_index = 0,
            started_at    = _now(),
        )
        log.info("Learn quiz created key=%s words=%d questions=%d",
                 key, len(word_ids), len(questions))
        return redirect(url_for("quiz_question"))

    # ── Practice Known Words ────────────────────────────────────────────────

    @app.route("/practice")
    def practice():
        """Practice entry screen — shows last session info and resets session state."""
        log.info("GET /practice")
        err = _db_required()
        if err:
            return err
        mastered = get_mastered_count()
        if mastered == 0:
            return render_template(
                "error.html",
                message="No mastered words yet. Complete a 'Learn New Words' session first."
            )
        last_info = get_last_practice_info()
        # Fresh practice session — clear carry-over state and cumulative tracking
        session.pop("practice_seen_ids",   None)
        session.pop("practice_failed_ids", None)
        session["practice_session_word_ids"]    = []
        session["practice_session_correct_ids"] = []
        return render_template(
            "practice.html",
            mastered_count = mastered,
            last_info      = last_info,
        )

    @app.route("/practice/start", methods=["POST"])
    def practice_start():
        """Spaced-repetition practice: prioritise failed words, exclude already-seen."""
        log.info("POST /practice/start")
        err = _db_required()
        if err:
            return err

        # Spaced-repetition state (persists across "Continue Practice" rounds)
        seen_ids     = session.get("practice_seen_ids",   [])
        priority_ids = session.get("practice_failed_ids", [])

        # Failed words may re-appear — only exclude seen words that aren't failed
        filtered_exclude = [i for i in seen_ids if i not in priority_ids]
        word_ids = get_practice_words(limit=10,
                                       exclude_ids=filtered_exclude,
                                       prioritize_ids=priority_ids)

        if not word_ids:
            # All mastered words reviewed this session — start fresh
            log.info("[1.0.0.7] Practice: all mastered words seen, resetting session")
            session.pop("practice_seen_ids",   None)
            session.pop("practice_failed_ids", None)
            word_ids = get_practice_words(limit=10)

        if not word_ids:
            return render_template(
                "error.html",
                message="No mastered words to practice. Complete a 'Learn' session first."
            )

        # Exactly 1 question per word → 10 questions for 10 unique words
        questions = get_vocab_questions_for_words(word_ids, n_per_word=1)
        if not questions:
            return render_template(
                "error.html",
                message="No vocabulary questions found for these words."
            )

        key = str(uuid.uuid4())
        session["quiz_key"]     = key
        session["quiz_type"]    = "practice"
        session["learner_name"] = "Learner"

        # Accumulate seen words for deduplication in future Continue rounds
        session["practice_seen_ids"] = list(set(seen_ids + word_ids))

        save_session(
            key           = key,
            quiz_type     = "practice",
            question_ids  = [int(q["id"]) for q in questions],
            word_ids      = word_ids,
            answers       = {},
            current_index = 0,
            started_at    = _now(),
        )
        log.info("[1.0.0.8] Practice quiz: key=%s words=%d (1 q/word) priority=%d",
                 key, len(word_ids), len(priority_ids))
        return redirect(url_for("quiz_question"))

    @app.route("/practice/review-again", methods=["POST"])
    def practice_review_again():
        """Reset practice session state and restart from the full mastered pool."""
        log.info("POST /practice/review-again")
        err = _db_required()
        if err:
            return err
        # Full reset — every mastered word becomes eligible again
        session.pop("practice_seen_ids",   None)
        session.pop("practice_failed_ids", None)

        word_ids = get_practice_words(limit=10)
        if not word_ids:
            return render_template(
                "error.html",
                message="No mastered words to practice."
            )

        questions = get_vocab_questions_for_words(word_ids, n_per_word=1)
        if not questions:
            return render_template(
                "error.html",
                message="No vocabulary questions found."
            )

        key = str(uuid.uuid4())
        session["quiz_key"]          = key
        session["quiz_type"]         = "practice"
        session["learner_name"]      = "Learner"
        session["practice_seen_ids"] = list(word_ids)

        save_session(
            key           = key,
            quiz_type     = "practice",
            question_ids  = [int(q["id"]) for q in questions],
            word_ids      = word_ids,
            answers       = {},
            current_index = 0,
            started_at    = _now(),
        )
        log.info("[1.0.0.8] Practice review-again: key=%s words=%d", key, len(word_ids))
        return redirect(url_for("quiz_question"))

    # ── Mock Exam ───────────────────────────────────────────────────────────

    @app.route("/exam")
    def exam():
        """Exam hub: shows last 10 results + start button."""
        log.info("GET /exam")
        history = get_recent_exam_scores(limit=10) if _db_ok() else []
        return render_template("exam.html", history=history)

    @app.route("/exam/start", methods=["POST"])
    def exam_start():
        """Build a 20-question A1 mock exam and redirect to the single-page view."""
        log.info("POST /exam/start")
        err = _db_required()
        if err:
            return err
        questions = select_exam_questions(reading_quota=5,
                                          listening_quota=5,
                                          grammar_quota=10)
        if not questions:
            return render_template(
                "error.html",
                message="No exam questions available in the database."
            )

        key = str(uuid.uuid4())
        session["quiz_key"]     = key
        session["quiz_type"]    = "exam"
        session["learner_name"] = "Learner"

        save_session(
            key           = key,
            quiz_type     = "exam",
            question_ids  = [int(q["id"]) for q in questions],
            word_ids      = [],
            answers       = {},
            current_index = 0,
            started_at    = _now(),
        )
        log.info("Exam created key=%s questions=%d — routing to single-page view",
                 key, len(questions))
        # Exam uses the dedicated single-page view, NOT the step-by-step quiz
        return redirect(url_for("exam_session"))

    @app.route("/exam/session")
    def exam_session():
        """Single-page scrollable mock exam (all 20 questions at once)."""
        log.info("GET /exam/session")
        key = session.get("quiz_key")
        if not key:
            return redirect(url_for("index"))

        quiz = get_session(key)
        if not quiz or quiz.get("quiz_type") != "exam":
            return redirect(url_for("index"))

        if quiz["submitted_at"]:
            return redirect(url_for("quiz_results"))

        q_ids     = quiz["question_ids"]
        questions = get_questions_by_ids(q_ids)

        # Build a map of passage_id → passage text (avoid repeated DB hits)
        passage_texts: dict[int, str] = {}
        for q in questions:
            if q.get("passage_id"):
                pid = int(q["passage_id"])
                if pid not in passage_texts:
                    passage_texts[pid] = get_passage_text(pid) or ""

        log.info("[1.0.0.5] Single-Page Exam Mode: key=%s questions=%d",
                 key, len(questions))
        return render_template(
            "exam_page.html",
            questions     = questions,
            passage_texts = passage_texts,
            total         = len(questions),
        )

    @app.route("/exam/session/submit", methods=["POST"])
    def exam_session_submit():
        """Collect all answers from the single-page exam form and persist."""
        log.info("POST /exam/session/submit")
        key = session.get("quiz_key")
        if not key:
            return redirect(url_for("index"))

        quiz = get_session(key)
        if not quiz:
            return redirect(url_for("index"))

        # Harvest answer_<qid> fields; skip questions left blank
        answers: dict[str, str] = {}
        for qid in quiz["question_ids"]:
            val = request.form.get(f"answer_{qid}", "").strip()
            if val:
                answers[str(qid)] = val

        now = _now()
        save_session(
            key           = key,
            quiz_type     = "exam",
            question_ids  = quiz["question_ids"],
            word_ids      = [],
            answers       = answers,
            current_index = len(answers),
            started_at    = quiz["started_at"],
            submitted_at  = now,
        )
        skipped = len(quiz["question_ids"]) - len(answers)
        log.info("[1.0.1.0] Exam submitted key=%s answered=%d/%d skipped=%d",
                 key, len(answers), len(quiz["question_ids"]), skipped)
        return redirect(url_for("quiz_results"))

    # ── Step-by-step quiz engine (learn / practice) ─────────────────────────

    @app.route("/quiz/question")
    def quiz_question():
        key = session.get("quiz_key")
        if not key:
            return redirect(url_for("index"))

        quiz = get_session(key)
        if not quiz:
            return redirect(url_for("index"))

        if quiz["submitted_at"]:
            return redirect(url_for("quiz_results"))

        quiz_type = quiz.get("quiz_type", "exam")

        # Exam uses its own single-page view — redirect if somehow landed here
        if quiz_type == "exam":
            return redirect(url_for("exam_session"))

        idx   = quiz["current_index"]
        q_ids = quiz["question_ids"]
        total = len(q_ids)

        if idx >= total:
            return redirect(url_for("quiz_results"))

        qs = get_questions_by_ids([q_ids[idx]])
        if not qs:
            log.error("Question id=%d not found", q_ids[idx])
            abort(500)
        question = qs[0]

        passage_text = None
        if question.get("passage_id"):
            passage_text = get_passage_text(int(question["passage_id"]))

        progress_pct = int(idx / total * 100)

        # Compute running score so the counter can be displayed
        correct_so_far = 0
        if quiz["answers"]:
            answered_ids = [int(k) for k in quiz["answers"].keys()]
            answered_qs  = get_questions_by_ids(answered_ids)
            for q in answered_qs:
                user_ans = quiz["answers"].get(str(q["id"]), "")
                if user_ans.strip().lower() == q["correct_answer"].strip().lower():
                    correct_so_far += 1

        log.info("[1.0.0.5] Step-by-Step Mode: q %d/%d id=%d cat=%s type=%s",
                 idx + 1, total, q_ids[idx], question["category"], quiz_type)

        return render_template(
            "quiz_learn.html",
            question        = question,
            passage_text    = passage_text,
            current         = idx + 1,
            total           = total,
            progress_pct    = progress_pct,
            quiz_type       = quiz_type,
            correct_so_far  = correct_so_far,
            answered_so_far = idx,      # questions answered before this one
        )

    @app.route("/quiz/answer", methods=["POST"])
    def quiz_answer():
        key = session.get("quiz_key")
        if not key:
            return redirect(url_for("index"))

        quiz = get_session(key)
        if not quiz or quiz["submitted_at"]:
            return redirect(url_for("index"))

        qid    = int(request.form.get("question_id", 0))
        answer = request.form.get("answer", "").strip()
        if not answer:
            return redirect(url_for("quiz_question"))

        answers   = quiz["answers"]
        answers[str(qid)] = answer
        new_index = quiz["current_index"] + 1
        total     = len(quiz["question_ids"])
        submitted_at = _now() if new_index >= total else None

        save_session(
            key           = key,
            quiz_type     = quiz.get("quiz_type", "exam"),
            question_ids  = quiz["question_ids"],
            word_ids      = quiz["word_ids"],
            answers       = answers,
            current_index = new_index,
            started_at    = quiz["started_at"],
            submitted_at  = submitted_at,
        )
        log.info("Answered qid=%d (%d/%d)", qid, new_index, total)

        if submitted_at:
            return redirect(url_for("quiz_results"))
        return redirect(url_for("quiz_question"))

    @app.route("/quiz/results")
    def quiz_results():
        key = session.get("quiz_key")
        if not key:
            return redirect(url_for("index"))

        quiz = get_session(key)
        if not quiz:
            return redirect(url_for("index"))

        q_ids      = quiz["question_ids"]
        answers    = quiz["answers"]
        word_ids   = quiz["word_ids"]
        quiz_type  = quiz.get("quiz_type", "exam")
        questions  = get_questions_by_ids(q_ids)

        # ── Grade ────────────────────────────────────────────────────────────
        results       = []
        correct_count = 0
        for q in questions:
            qid         = str(q["id"])
            user_ans    = answers.get(qid, "")
            is_correct  = user_ans.strip().lower() == q["correct_answer"].strip().lower()
            if is_correct:
                correct_count += 1

            passage_text = None
            if q.get("passage_id"):
                passage_text = get_passage_text(int(q["passage_id"]))

            results.append({
                "question":     q,
                "user_answer":  user_ans,
                "is_correct":   is_correct,
                "passage_text": passage_text,
            })

        total     = len(questions)
        score_pct = round(correct_count / total * 100) if total else 0

        # ── Practice: word-level scoring + spaced-repetition state update ──────
        word_score              = 0
        word_count              = 0
        has_more_practice_words = False

        if quiz_type == "practice" and word_ids:
            word_count = len(word_ids)
            failed_ids: list[int] = []
            for wid in word_ids:
                items_for_word = [r for r in results
                                  if r["question"].get("word_id")
                                  and int(r["question"]["word_id"]) == wid]
                if items_for_word and all(r["is_correct"] for r in items_for_word):
                    word_score += 1
                else:
                    failed_ids.append(wid)
            session["practice_failed_ids"] = failed_ids

            # ── Accumulate unique word IDs for the whole continuous session ───────
            # A "session" begins at /practice and ends only at quiz_restart (Back to Home).
            # Each round adds its unique words; the final cumulative save happens in
            # quiz_restart so that 10 words + 2 re-tried words = 10, not 12.
            sess_seen    = set(session.get("practice_session_word_ids", []))
            sess_correct = set(session.get("practice_session_correct_ids", []))
            failed_set   = set(failed_ids)
            for wid in word_ids:
                sess_seen.add(wid)
                if wid not in failed_set:
                    sess_correct.add(wid)
                else:
                    sess_correct.discard(wid)   # overwrite: wrong this time beats earlier correct
            session["practice_session_word_ids"]    = list(sess_seen)
            session["practice_session_correct_ids"] = list(sess_correct)

            # Scenario A vs B: are there more mastered words unseen this session?
            seen_this_session       = session.get("practice_seen_ids", [])
            mastered_total          = get_mastered_count()
            has_more_practice_words = mastered_total > len(seen_this_session)

            log.info("[1.0.0.9] Practice round: %d/%d words | session unique: %d correct/%d seen | "
                     "more_words: %s",
                     word_score, word_count,
                     len(sess_correct), len(sess_seen), has_more_practice_words)

        # ── Mastery (learn mode only) ────────────────────────────────────────
        mastery_report: list[dict] = []
        if quiz_type == "learn" and word_ids:
            word_correct: dict[int, int] = {wid: 0 for wid in word_ids}
            word_total:   dict[int, int] = {wid: 0 for wid in word_ids}
            for item in results:
                wid = item["question"].get("word_id")
                if wid and int(wid) in word_correct:
                    wid = int(wid)
                    word_total[wid]   += 1
                    if item["is_correct"]:
                        word_correct[wid] += 1

            for wid in word_ids:
                c = word_correct.get(wid, 0)
                t = word_total.get(wid, 0)
                mark_word_learn_result(wid, c, t)
                mastery_report.append({
                    "word_id": wid,
                    "correct": c,
                    "total":   t,
                    "mastered": c == t and t > 0,
                })

        # ── Persist score (once) ─────────────────────────────────────────────
        # Practice scores are saved cumulatively in quiz_restart (Back to Home),
        # so each 10-word round does NOT write its own DB row.
        if quiz["submitted_at"] and quiz_type != "practice" and not score_already_saved(key):
            save_score(
                session_key  = key,
                quiz_type    = quiz_type,
                learner_name = quiz.get("learner_name") or "Learner",
                correct      = correct_count,
                total        = total,
                taken_at     = quiz["submitted_at"],
            )

        log.info("Results key=%s type=%s score=%d/%d", key, quiz_type, correct_count, total)

        # ── Exam: full-page review with colour-coded answers ─────────────────
        if quiz_type == "exam":
            skipped_count = sum(
                1 for item in results
                if not item["user_answer"]
            )
            log.info("[1.0.1.0] Exam results: key=%s score=%d/%d (%d%%) skipped=%d",
                     key, correct_count, total, score_pct, skipped_count)

            # Build passage_texts dict for the review template
            passage_texts: dict[int, str] = {}
            for item in results:
                q = item["question"]
                if q.get("passage_id"):
                    pid = int(q["passage_id"])
                    if pid not in passage_texts:
                        passage_texts[pid] = item["passage_text"] or ""

            return render_template(
                "exam_review.html",
                results       = results,
                correct       = correct_count,
                total         = total,
                score_pct     = score_pct,
                skipped_count = skipped_count,
                passage_texts = passage_texts,
            )

        # ── Learn / Practice: compact summary with mastery report ────────────
        new_mastered = sum(1 for m in mastery_report if m["mastered"])

        return render_template(
            "results.html",
            results                 = results,
            correct                 = correct_count,
            total                   = total,
            score_pct               = score_pct,
            quiz_type               = quiz_type,
            mastery_report          = mastery_report,
            new_mastered            = new_mastered,
            word_score              = word_score,
            word_count              = word_count,
            has_more_practice_words = has_more_practice_words,
        )

    @app.route("/quiz/restart", methods=["POST"])
    def quiz_restart():
        # Save the cumulative practice session before wiping state.
        # This ensures 10 words + Continue 2 words = 10 unique total, not two separate rows.
        if session.get("quiz_type") == "practice":
            total_w = len(session.pop("practice_session_word_ids",    []))
            total_c = len(session.pop("practice_session_correct_ids", []))
            if total_w > 0:
                save_score(
                    session_key  = f"practice-{uuid.uuid4()}",
                    quiz_type    = "practice",
                    learner_name = "Learner",
                    correct      = total_c,
                    total        = total_w,
                    taken_at     = _now(),
                )
                log.info("[1.0.0.9] Practice session saved: %d/%d unique words correct",
                         total_c, total_w)
        else:
            session.pop("practice_session_word_ids",    None)
            session.pop("practice_session_correct_ids", None)

        session.pop("quiz_key",                None)
        session.pop("quiz_type",               None)
        session.pop("pending_learn_word_ids",  None)
        session.pop("practice_seen_ids",       None)
        session.pop("practice_failed_ids",     None)
        log.info("[1.0.0.9] Session cleared, returning home")
        return redirect(url_for("index"))
