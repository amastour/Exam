import json
import secrets
import datetime
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from functools import wraps
from models import get_db, init_db
from questions import get_exam, get_question, list_exams, EXAMS, ALL_DOMAINS, ALL_OBJECTIVES

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = secrets.token_hex(32)

# ─────────────────────────────────────────────────────────────────────────────
# Auth helpers
# ─────────────────────────────────────────────────────────────────────────────

def get_user_by_token(token):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE token = ?", (token,)).fetchone()
    db.close()
    return user


def require_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = session.get("token") or request.headers.get("X-Token")
        if not token:
            return redirect(url_for("login_page"))
        user = get_user_by_token(token)
        if not user:
            session.clear()
            return redirect(url_for("login_page"))
        request.current_user = dict(user)
        return f(*args, **kwargs)
    return decorated


def require_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = session.get("token") or request.headers.get("X-Token")
        if not token:
            return redirect(url_for("login_page"))
        user = get_user_by_token(token)
        if not user or user["role"] != "admin":
            return jsonify({"error": "Admin access required"}), 403
        request.current_user = dict(user)
        return f(*args, **kwargs)
    return decorated


# ─────────────────────────────────────────────────────────────────────────────
# Pages
# ─────────────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    if session.get("token"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login_page"))


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/dashboard")
@require_token
def dashboard():
    user = request.current_user
    db = get_db()
    sessions = db.execute(
        "SELECT * FROM exam_sessions WHERE user_id = ? ORDER BY started_at DESC",
        (user["id"],)
    ).fetchall()
    db.close()
    all_exams = list_exams()
    # Regular users only see quizzes explicitly made visible
    if user["role"] != "admin":
        visible_exams = [e for e in all_exams if e.get("visible_to_users")]
    else:
        visible_exams = all_exams
    return render_template("dashboard.html", user=user, sessions=[dict(s) for s in sessions], exams=visible_exams)


@app.route("/exam/<int:exam_id>")
@require_token
def exam_page(exam_id):
    exam = get_exam(exam_id)
    if not exam:
        return "Exam not found", 404
    user = request.current_user
    mode = request.args.get("mode", "practice")  # 'practice' or 'exam'
    try:
        duration = max(1, int(request.args.get("duration", 60)))
    except ValueError:
        duration = 60

    db = get_db()
    # Check for existing in-progress session
    existing = db.execute(
        "SELECT * FROM exam_sessions WHERE user_id=? AND exam_id=? AND status='in_progress'",
        (user["id"], exam_id)
    ).fetchone()
    if existing:
        session_id = existing["id"]
        mode = existing["mode"]
        duration = existing["duration_minutes"]
        started_at = existing["started_at"]
    else:
        cur = db.execute(
            "INSERT INTO exam_sessions (user_id, exam_id, total, mode, duration_minutes) VALUES (?, ?, ?, ?, ?)",
            (user["id"], exam_id, len(exam["questions"]), mode, duration)
        )
        session_id = cur.lastrowid
        db.commit()
        started_at = db.execute("SELECT started_at FROM exam_sessions WHERE id=?", (session_id,)).fetchone()["started_at"]
    db.close()

    # Compute seconds remaining
    try:
        start_dt = datetime.datetime.strptime(started_at, "%Y-%m-%d %H:%M:%S")
    except Exception:
        start_dt = datetime.datetime.utcnow()
    elapsed = int((datetime.datetime.utcnow() - start_dt).total_seconds())
    time_remaining = max(0, duration * 60 - elapsed)

    return render_template("exam.html", exam=exam, session_id=session_id, user=user,
                           exam_mode=mode, time_remaining=time_remaining)


@app.route("/results/<int:session_id>")
@require_token
def results_page(session_id):
    user = request.current_user
    db = get_db()
    # Admins can view any session; regular users only their own
    if user["role"] == "admin":
        sess = db.execute(
            "SELECT * FROM exam_sessions WHERE id=?",
            (session_id,)
        ).fetchone()
    else:
        sess = db.execute(
            "SELECT * FROM exam_sessions WHERE id=? AND user_id=?",
            (session_id, user["id"])
        ).fetchone()
    if not sess:
        return "Session not found", 404

    answers = db.execute(
        "SELECT * FROM answers WHERE session_id=? ORDER BY question_num",
        (session_id,)
    ).fetchall()

    answers = [dict(a) for a in answers]
    sess = dict(sess)

    # Fetch the session owner's username (useful when admin views another user's session)
    owner = db.execute("SELECT username FROM users WHERE id=?", (sess["user_id"],)).fetchone()
    sess["owner_username"] = owner["username"] if owner else "Unknown"
    db.close()

    exam = get_exam(sess["exam_id"])
    questions = exam["questions"] if exam else {}

    # Build metrics by domain (backfill domain from questions if not stored)
    by_domain = {}
    for a in answers:
        q_data = questions.get(a["question_num"]) or {}
        domain = a.get("domain") or q_data.get("domain") or "Unknown"
        # Clean domain: strip leading "Objective N - " prefix if present for short label
        if domain not in by_domain:
            by_domain[domain] = {"correct": 0, "incorrect": 0, "skipped": 0, "total": 0}
        by_domain[domain]["total"] += 1
        by_domain[domain][a.get("result", "skipped")] += 1

    return render_template(
        "results.html",
        session=sess,
        answers=answers,
        by_objective=by_domain,
        questions=questions,
        user=user
    )


@app.route("/admin")
@require_admin
def admin_page():
    db = get_db()
    users = db.execute("SELECT * FROM users ORDER BY created_at DESC").fetchall()
    db.close()
    return render_template("admin.html", users=[dict(u) for u in users], user=request.current_user, exams=list_exams())


# ─────────────────────────────────────────────────────────────────────────────
# API
# ─────────────────────────────────────────────────────────────────────────────

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.json or {}
    token = data.get("token", "").strip()
    user = get_user_by_token(token)
    if not user:
        return jsonify({"error": "Invalid token"}), 401
    session["token"] = token
    return jsonify({"ok": True, "role": user["role"], "username": user["username"]})


@app.route("/api/logout", methods=["POST"])
def api_logout():
    session.clear()
    return jsonify({"ok": True})


@app.route("/api/question/<int:exam_id>/<int:q_num>")
@require_token
def api_question(exam_id, q_num):
    q = get_question(exam_id, q_num)
    if not q:
        return jsonify({"error": "Not found"}), 404
    # Return question without correct_answer
    safe = {k: v for k, v in q.items() if k != "correct_answer"}
    return jsonify(safe)


@app.route("/api/answer", methods=["POST"])
@require_token
def api_answer():
    data = request.json or {}
    session_id = data.get("session_id")
    q_num = data.get("question_num")
    user_answer = data.get("answer")  # string or list
    skipped = data.get("skipped", False)

    user = request.current_user
    db = get_db()

    sess = db.execute(
        "SELECT * FROM exam_sessions WHERE id=? AND user_id=? AND status='in_progress'",
        (session_id, user["id"])
    ).fetchone()

    if not sess:
        db.close()
        return jsonify({"error": "Session not found or already finished"}), 404

    q = get_question(sess["exam_id"], q_num)
    if not q:
        db.close()
        return jsonify({"error": "Question not found"}), 404

    if skipped:
        result = "skipped"
        is_correct = 0
        user_answer_str = ""
    else:
        correct = q["correct_answer"]
        if isinstance(user_answer, list):
            ua_set = set(str(x).strip().lower() for x in user_answer)
            ca_set = set(str(x).strip().lower() for x in correct)
            is_correct = 1 if ua_set == ca_set else 0
        else:
            is_correct = 1 if str(user_answer).strip().lower() == str(correct[0]).strip().lower() else 0
        result = "correct" if is_correct else "incorrect"
        user_answer_str = json.dumps(user_answer) if isinstance(user_answer, list) else str(user_answer)

    # Upsert answer
    existing_ans = db.execute(
        "SELECT id FROM answers WHERE session_id=? AND question_num=?",
        (session_id, q_num)
    ).fetchone()

    if existing_ans:
        db.execute(
            "UPDATE answers SET user_answer=?, is_correct=?, result=?, objective=?, domain=? WHERE id=?",
            (user_answer_str, is_correct, result, q.get("objective", ""), q.get("domain", ""), existing_ans["id"])
        )
    else:
        db.execute(
            "INSERT INTO answers (session_id, question_num, user_answer, is_correct, result, objective, domain) VALUES (?,?,?,?,?,?,?)",
            (session_id, q_num, user_answer_str, is_correct, result, q.get("objective", ""), q.get("domain", ""))
        )
    db.commit()
    db.close()

    return jsonify({"result": result, "is_correct": bool(is_correct), "correct_answer": q["correct_answer"], "explanation": q.get("explanation", ""), "key_takeaway": q.get("key_takeaway", "")})


@app.route("/api/finish", methods=["POST"])
@require_token
def api_finish():
    data = request.json or {}
    session_id = data.get("session_id")
    user = request.current_user
    db = get_db()

    sess = db.execute(
        "SELECT * FROM exam_sessions WHERE id=? AND user_id=?",
        (session_id, user["id"])
    ).fetchone()
    if not sess:
        db.close()
        return jsonify({"error": "Not found"}), 404

    score = db.execute(
        "SELECT COUNT(*) as cnt FROM answers WHERE session_id=? AND is_correct=1",
        (session_id,)
    ).fetchone()["cnt"]

    db.execute(
        "UPDATE exam_sessions SET status='finished', finished_at=CURRENT_TIMESTAMP, score=? WHERE id=?",
        (score, session_id)
    )
    db.commit()
    db.close()
    return jsonify({"ok": True, "score": score, "session_id": session_id})


# ─────────────────────────────────────────────────────────────────────────────
# Admin API
# ─────────────────────────────────────────────────────────────────────────────

@app.route("/api/admin/create_user", methods=["POST"])
@require_admin
def api_create_user():
    data = request.json or {}
    username = data.get("username", "").strip()
    if not username:
        return jsonify({"error": "Username required"}), 400
    token = "usr-" + secrets.token_hex(16)
    db = get_db()
    try:
        db.execute("INSERT INTO users (username, token, role) VALUES (?, ?, 'user')", (username, token))
        db.commit()
    except Exception as e:
        db.close()
        return jsonify({"error": str(e)}), 400
    db.close()
    return jsonify({"ok": True, "username": username, "token": token})


@app.route("/api/admin/delete_user/<int:user_id>", methods=["DELETE"])
@require_admin
def api_delete_user(user_id):
    db = get_db()
    db.execute("DELETE FROM users WHERE id=? AND role != 'admin'", (user_id,))
    db.commit()
    db.close()
    return jsonify({"ok": True})


@app.route("/api/admin/reset_token/<int:user_id>", methods=["POST"])
@require_admin
def api_reset_token(user_id):
    new_token = "usr-" + secrets.token_hex(16)
    db = get_db()
    db.execute("UPDATE users SET token=? WHERE id=?", (new_token, user_id))
    db.commit()
    db.close()
    return jsonify({"ok": True, "token": new_token})


@app.route("/api/admin/stats")
@require_admin
def api_admin_stats():
    from questions import STATIC_QUESTION_COUNT, ALL_OBJECTIVES
    db = get_db()
    users = db.execute("SELECT COUNT(*) as cnt FROM users WHERE role='user'").fetchone()["cnt"]
    sessions = db.execute("SELECT COUNT(*) as cnt FROM exam_sessions WHERE status='finished'").fetchone()["cnt"]
    exam_tokens = db.execute("SELECT COUNT(*) as cnt FROM exam_tokens").fetchone()["cnt"]
    custom_exams_total = db.execute("SELECT COUNT(*) as cnt FROM custom_exams WHERE is_active=1").fetchone()["cnt"]
    regular_exams = db.execute("SELECT COUNT(*) as cnt FROM custom_exams WHERE is_active=1 AND exam_type='regular'").fetchone()["cnt"]
    objective_quizzes = db.execute("SELECT COUNT(*) as cnt FROM custom_exams WHERE is_active=1 AND exam_type='objective'").fetchone()["cnt"]
    custom_q_count = db.execute("SELECT COUNT(*) as cnt FROM custom_questions").fetchone()["cnt"]
    in_progress = db.execute("SELECT COUNT(*) as cnt FROM exam_sessions WHERE status='in_progress'").fetchone()["cnt"]
    db.close()
    return jsonify({
        "users": users,
        "completed_exams": sessions,
        "in_progress_exams": in_progress,
        "exam_tokens": exam_tokens,
        "custom_exams": custom_exams_total,
        "regular_exams": regular_exams + 2,  # +2 for file-based exams
        "objective_quizzes": objective_quizzes,
        "total_questions": STATIC_QUESTION_COUNT + custom_q_count,
        "objectives_count": len(ALL_OBJECTIVES),
    })


@app.route("/api/admin/create_exam_token", methods=["POST"])
@require_admin
def api_create_exam_token():
    data = request.json or {}
    exam_id = data.get("exam_id")
    assigned_to = data.get("assigned_to") or None  # user id, optional
    mode = data.get("mode", "exam")
    try:
        duration = max(1, int(data.get("duration", 60)))
    except (ValueError, TypeError):
        duration = 60
    label = data.get("label", "").strip()

    if not exam_id:
        return jsonify({"error": "exam_id required"}), 400

    token = "et-" + secrets.token_hex(20)
    db = get_db()
    try:
        db.execute(
            "INSERT INTO exam_tokens (token, exam_id, assigned_to, mode, duration_minutes, label) VALUES (?,?,?,?,?,?)",
            (token, exam_id, assigned_to, mode, duration, label)
        )
        db.commit()
    except Exception as e:
        db.close()
        return jsonify({"error": str(e)}), 400
    db.close()
    return jsonify({"ok": True, "token": token, "exam_id": exam_id, "mode": mode, "duration": duration})


@app.route("/api/admin/exam_tokens")
@require_admin
def api_list_exam_tokens():
    db = get_db()
    rows = db.execute("""
        SELECT et.*, u.username as assigned_username, ub.username as used_username
        FROM exam_tokens et
        LEFT JOIN users u ON et.assigned_to = u.id
        LEFT JOIN users ub ON et.used_by = ub.id
        ORDER BY et.created_at DESC
    """).fetchall()
    db.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/admin/delete_exam_token/<int:token_id>", methods=["DELETE"])
@require_admin
def api_delete_exam_token(token_id):
    db = get_db()
    db.execute("DELETE FROM exam_tokens WHERE id=?", (token_id,))
    db.commit()
    db.close()
    return jsonify({"ok": True})


@app.route("/api/admin/all_results")
@require_admin
def api_all_results():
    db = get_db()
    rows = db.execute("""
        SELECT es.*, u.username
        FROM exam_sessions es
        JOIN users u ON es.user_id = u.id
        ORDER BY es.started_at DESC
    """).fetchall()
    db.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/redeem_exam_token", methods=["POST"])
@require_token
def api_redeem_exam_token():
    data = request.json or {}
    et_token = data.get("exam_token", "").strip()
    user = request.current_user

    db = get_db()
    et = db.execute("SELECT * FROM exam_tokens WHERE token=?", (et_token,)).fetchone()
    if not et:
        db.close()
        return jsonify({"error": "Invalid exam token"}), 404

    et = dict(et)
    # Check if assigned to someone else
    if et["assigned_to"] and et["assigned_to"] != user["id"]:
        db.close()
        return jsonify({"error": "This token is assigned to a different user"}), 403

    # Check already used by someone else
    if et["used_by"] and et["used_by"] != user["id"]:
        db.close()
        return jsonify({"error": "This token has already been used"}), 403

    # Mark used
    db.execute(
        "UPDATE exam_tokens SET used_by=?, used_at=CURRENT_TIMESTAMP WHERE id=?",
        (user["id"], et["id"])
    )
    db.commit()
    db.close()

    return jsonify({
        "ok": True,
        "exam_id": et["exam_id"],
        "mode": et["mode"],
        "duration": et["duration_minutes"]
    })


# ─────────────────────────────────────────────────────────────────────────────
# Admin – Custom Exam Builder
# ─────────────────────────────────────────────────────────────────────────────

@app.route("/api/admin/domains")
@require_admin
def api_domains():
    return jsonify({"domains": ALL_DOMAINS, "objectives": ALL_OBJECTIVES})


@app.route("/api/admin/create_custom_exam", methods=["POST"])
@require_admin
def api_create_custom_exam():
    data = request.json or {}
    title = data.get("title", "").strip()
    description = data.get("description", "").strip()
    exam_type = data.get("exam_type", "regular")
    # objectives is a list of strings (objectives or domains)
    objectives = data.get("objectives", [])
    if isinstance(objectives, str):
        objectives = [objectives]
    filter_objectives = "|||".join(o.strip() for o in objectives if o.strip())

    if not title:
        return jsonify({"error": "Title is required"}), 400

    db = get_db()
    row = db.execute("SELECT COALESCE(MAX(id), 999) + 1 as next_id FROM custom_exams").fetchone()
    new_id = max(row["next_id"], 1000)

    try:
        db.execute(
            "INSERT INTO custom_exams (id, title, description, exam_type, filter_objectives, created_by) VALUES (?,?,?,?,?,?)",
            (new_id, title, description, exam_type, filter_objectives, request.current_user["id"])
        )
        db.commit()
    except Exception as e:
        db.close()
        return jsonify({"error": str(e)}), 400

    # For objective quizzes: auto-create quiz_question_links from matching questions
    if exam_type == "objective" and objectives:
        from questions import _questions_for_objectives
        matched = _questions_for_objectives(objectives)
        for pos, q in enumerate(matched, 1):
            db.execute(
                "INSERT INTO quiz_question_links (quiz_id, source_exam_id, source_question_num, position) VALUES (?,?,?,?)",
                (new_id, q["exam_id"], q["num"], pos)
            )
        db.commit()

    db.close()
    return jsonify({"ok": True, "id": new_id, "title": title, "exam_type": exam_type})


@app.route("/api/admin/delete_custom_exam/<int:exam_id>", methods=["DELETE"])
@require_admin
def api_delete_custom_exam(exam_id):
    db = get_db()
    db.execute("DELETE FROM custom_questions WHERE exam_id=?", (exam_id,))
    db.execute("DELETE FROM custom_exams WHERE id=?", (exam_id,))
    db.commit()
    db.close()
    return jsonify({"ok": True})


@app.route("/api/admin/custom_exams")
@require_admin
def api_list_custom_exams():
    db = get_db()
    rows = db.execute("SELECT * FROM custom_exams WHERE is_active=1 ORDER BY created_at DESC").fetchall()
    result = []
    for row in rows:
        row = dict(row)
        if row["exam_type"] == "objective":
            from questions import _build_objective_exam
            exam = _build_objective_exam(row, db)
            row["question_count"] = len(exam["questions"])
        else:
            cnt = db.execute("SELECT COUNT(*) as c FROM custom_questions WHERE exam_id=?", (row["id"],)).fetchone()["c"]
            row["question_count"] = cnt
        raw = row.get("filter_objectives") or ""
        row["objectives_list"] = [o for o in raw.split("|||") if o]
        result.append(row)
    db.close()
    return jsonify(result)


@app.route("/api/admin/quiz_links/<int:quiz_id>")
@require_admin
def api_quiz_links(quiz_id):
    db = get_db()
    links = db.execute(
        "SELECT * FROM quiz_question_links WHERE quiz_id=? ORDER BY position", (quiz_id,)
    ).fetchall()
    db.close()
    return jsonify([dict(l) for l in links])


@app.route("/api/admin/add_quiz_link", methods=["POST"])
@require_admin
def api_add_quiz_link():
    data = request.json or {}
    quiz_id = data.get("quiz_id")
    source_exam_id = data.get("source_exam_id")
    source_question_num = data.get("source_question_num")
    if not all([quiz_id, source_exam_id, source_question_num]):
        return jsonify({"error": "quiz_id, source_exam_id, source_question_num required"}), 400
    db = get_db()
    # Check not already linked
    existing = db.execute(
        "SELECT id FROM quiz_question_links WHERE quiz_id=? AND source_exam_id=? AND source_question_num=?",
        (quiz_id, source_exam_id, source_question_num)
    ).fetchone()
    if existing:
        db.close()
        return jsonify({"error": "Question already linked"}), 409
    max_pos = db.execute("SELECT COALESCE(MAX(position),0) as m FROM quiz_question_links WHERE quiz_id=?", (quiz_id,)).fetchone()["m"]
    db.execute(
        "INSERT INTO quiz_question_links (quiz_id, source_exam_id, source_question_num, position) VALUES (?,?,?,?)",
        (quiz_id, source_exam_id, source_question_num, max_pos + 1)
    )
    db.commit()
    db.close()
    return jsonify({"ok": True})


@app.route("/api/admin/remove_quiz_link/<int:link_id>", methods=["DELETE"])
@require_admin
def api_remove_quiz_link(link_id):
    db = get_db()
    db.execute("DELETE FROM quiz_question_links WHERE id=?", (link_id,))
    db.commit()
    db.close()
    return jsonify({"ok": True})


@app.route("/api/admin/toggle_quiz_visibility/<int:exam_id>", methods=["POST"])
@require_admin
def api_toggle_quiz_visibility(exam_id):
    db = get_db()
    row = db.execute("SELECT visible_to_users FROM custom_exams WHERE id=?", (exam_id,)).fetchone()
    if not row:
        db.close()
        return jsonify({"error": "Not found"}), 404
    new_val = 0 if row["visible_to_users"] else 1
    db.execute("UPDATE custom_exams SET visible_to_users=? WHERE id=?", (new_val, exam_id))
    db.commit()
    db.close()
    return jsonify({"ok": True, "visible_to_users": bool(new_val)})


@app.route("/api/admin/add_question", methods=["POST"])
@require_admin
def api_add_question():
    data = request.json or {}
    exam_id = data.get("exam_id")
    question_text = data.get("question", "").strip()
    q_type = data.get("type", "multiple_choice")
    correct_answer = data.get("correct_answer")  # string or list
    all_options = data.get("all_options", {})
    domain = data.get("domain", "").strip()
    objective = data.get("objective", "").strip()
    explanation = data.get("explanation", "").strip()
    key_takeaway = data.get("key_takeaway", "").strip()

    if not exam_id or not question_text or not correct_answer:
        return jsonify({"error": "exam_id, question and correct_answer are required"}), 400

    db = get_db()
    # Check exam exists and is regular type
    exam_row = db.execute("SELECT * FROM custom_exams WHERE id=? AND is_active=1", (exam_id,)).fetchone()
    if not exam_row or dict(exam_row)["exam_type"] != "regular":
        db.close()
        return jsonify({"error": "Exam not found or is not a regular exam"}), 404

    # Next question number
    max_num = db.execute("SELECT COALESCE(MAX(question_num), 0) as m FROM custom_questions WHERE exam_id=?", (exam_id,)).fetchone()["m"]
    q_num = max_num + 1

    correct_json = json.dumps(correct_answer) if isinstance(correct_answer, list) else correct_answer
    options_json = json.dumps(all_options)

    db.execute(
        """INSERT INTO custom_questions
           (exam_id, question_num, question, type, correct_answer, all_options, domain, objective, explanation, key_takeaway)
           VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (exam_id, q_num, question_text, q_type, correct_json, options_json, domain, objective, explanation, key_takeaway)
    )
    db.commit()
    new_id = db.execute("SELECT last_insert_rowid() as id").fetchone()["id"]
    db.close()
    return jsonify({"ok": True, "id": new_id, "question_num": q_num})


@app.route("/api/admin/delete_question/<int:q_id>", methods=["DELETE"])
@require_admin
def api_delete_question(q_id):
    db = get_db()
    db.execute("DELETE FROM custom_questions WHERE id=?", (q_id,))
    db.commit()
    db.close()
    return jsonify({"ok": True})


@app.route("/api/admin/exam_questions/<int:exam_id>")
@require_admin
def api_exam_questions(exam_id):
    db = get_db()
    rows = db.execute("SELECT * FROM custom_questions WHERE exam_id=? ORDER BY question_num", (exam_id,)).fetchall()
    db.close()
    return jsonify([dict(r) for r in rows])


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=8080)
