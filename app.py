import json
import os
import secrets
import datetime
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, send_file
from functools import wraps
import firestore_db
from questions import get_exam, get_question, list_exams, EXAMS, ALL_DOMAINS, ALL_OBJECTIVES

app = Flask(__name__, template_folder="templates", static_folder="static")

# A4 — secret_key persistant (ne change pas au redémarrage)
_key_file = os.path.join(os.path.dirname(__file__), ".secret_key")
if os.path.exists(_key_file):
    with open(_key_file) as _f:
        app.secret_key = _f.read().strip()
else:
    _k = secrets.token_hex(32)
    with open(_key_file, "w") as _f:
        _f.write(_k)
    app.secret_key = _k

# A8 — cookies sécurisés
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# ─────────────────────────────────────────────────────────────────────────────
# Auth helpers
# ─────────────────────────────────────────────────────────────────────────────

def get_user_by_token(token):
    return firestore_db.get_user_by_token(token)


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
    sessions = firestore_db.get_sessions_by_user(user["id"])
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

    # Access control: regular users can only access
    # (1) exams marked visible_to_users, OR
    # (2) exams they already have an in-progress session for (started via token)
    if user["role"] != "admin":
        allowed = False
        # Check if exam is visible
        all_exams = list_exams()
        for e in all_exams:
            if e["id"] == exam_id and e.get("visible_to_users"):
                allowed = True
                break
        # Check if they have an existing in-progress session (started via exam token)
        if not allowed:
            if firestore_db.get_inprogress_session(user["id"], exam_id):
                allowed = True
        if not allowed:
            return redirect(url_for("dashboard"))

    mode = request.args.get("mode", "practice")  # 'practice' or 'exam'
    if mode not in ("practice", "exam"):
        mode = "practice"
    try:
        duration = min(max(5, int(request.args.get("duration", 60))), 300)
    except ValueError:
        duration = 60

    existing = firestore_db.get_inprogress_session(user["id"], exam_id)
    if existing:
        session_id = existing["id"]
        mode = existing["mode"]
        duration = existing["duration_minutes"]
        started_at = existing["started_at"]
    else:
        session_id, started_at = firestore_db.create_exam_session(
            user["id"], exam_id, len(exam["questions"]), mode, duration
        )

    # Compute seconds remaining
    try:
        start_dt = datetime.datetime.strptime(started_at, "%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc)
    except Exception:
        start_dt = datetime.datetime.now(datetime.timezone.utc)
    elapsed = int((datetime.datetime.now(datetime.timezone.utc) - start_dt).total_seconds())
    time_remaining = max(0, duration * 60 - elapsed)

    return render_template("exam.html", exam=exam, session_id=session_id, user=user,
                           exam_mode=mode, time_remaining=time_remaining)


@app.route("/results/<session_id>")
@require_token
def results_page(session_id):
    user = request.current_user
    if user["role"] == "admin":
        sess = firestore_db.get_session_by_id(session_id)
    else:
        sess = firestore_db.get_session_by_id(session_id, user["id"])
    if not sess:
        if user["role"] != "admin":
            return redirect(url_for("dashboard"))
        return "Session not found", 404

    answers = firestore_db.get_answers_by_session(session_id)
    owner = firestore_db.get_user_by_id(sess["user_id"])
    sess["owner_username"] = owner["username"] if owner else "Unknown"

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
    users = firestore_db.get_all_users()
    return render_template("admin.html", users=users, user=request.current_user, exams=list_exams())


@app.route("/admin/download_db")
@require_admin
def download_db():
    # M3 — Log d'audit
    print(f"[AUDIT] DB download attempted by '{request.current_user['username']}' "
          f"from IP {request.remote_addr} at {datetime.datetime.now(datetime.timezone.utc).isoformat()}Z", flush=True)
    return jsonify({"error": "DB is now Firestore — use the Firebase console to export data"}), 410


# ─────────────────────────────────────────────────────────────────────────────
# API
# ─────────────────────────────────────────────────────────────────────────────

# C2 — Rate limiting login : max 10 tentatives / IP / 5 min
_login_attempts: dict = {}  # {ip: [timestamp, ...]}
_RATE_LIMIT_MAX = 10
_RATE_LIMIT_WINDOW = 300  # secondes


def _check_rate_limit(ip: str) -> bool:
    """Retourne True si l'IP est autorisée, False si bloquée."""
    now = datetime.datetime.now(datetime.timezone.utc).timestamp()
    attempts = [t for t in _login_attempts.get(ip, []) if now - t < _RATE_LIMIT_WINDOW]
    _login_attempts[ip] = attempts
    if len(attempts) >= _RATE_LIMIT_MAX:
        return False
    _login_attempts[ip].append(now)
    return True


@app.route("/api/login", methods=["POST"])
def api_login():
    ip = request.remote_addr or "unknown"
    if not _check_rate_limit(ip):
        return jsonify({"error": "Too many attempts, retry in 5 minutes"}), 429
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
    user = request.current_user
    # Regular users must have an active session for this exam
    if user["role"] != "admin":
        if not firestore_db.get_inprogress_session(user["id"], exam_id):
            return jsonify({"error": "Access denied"}), 403
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
    sess = firestore_db.get_session_by_id(session_id, user["id"])
    if not sess or sess.get("status") != "in_progress":
        return jsonify({"error": "Session not found or already finished"}), 404

    # M1 — Vérifier que le temps imparti n'est pas dépassé côté serveur
    try:
        start_dt = datetime.datetime.strptime(sess["started_at"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc)
        elapsed_s = (datetime.datetime.now(datetime.timezone.utc) - start_dt).total_seconds()
        if elapsed_s > sess["duration_minutes"] * 60:
            firestore_db.expire_exam_session(session_id)
            return jsonify({"error": "Time expired", "expired": True}), 403
    except Exception:
        pass

    q = get_question(sess["exam_id"], q_num)
    if not q:
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

    firestore_db.upsert_answer(
        session_id, q_num, user_answer_str, is_correct, result,
        q.get("objective", ""), q.get("domain", "")
    )

    # C3 — Ne révéler correct_answer et explanation qu'en mode practice
    resp = {"result": result, "is_correct": bool(is_correct)}
    if sess["mode"] == "practice":
        resp["correct_answer"] = q["correct_answer"]
        resp["explanation"] = q.get("explanation", "")
        resp["key_takeaway"] = q.get("key_takeaway", "")
    return jsonify(resp)


@app.route("/api/finish", methods=["POST"])
@require_token
def api_finish():
    data = request.json or {}
    session_id = data.get("session_id")
    user = request.current_user
    sess = firestore_db.get_session_by_id(session_id, user["id"])
    if not sess:
        return jsonify({"error": "Not found"}), 404

    score = firestore_db.count_correct_answers(session_id)
    firestore_db.finish_exam_session(session_id, score)
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
    try:
        firestore_db.create_user(username, token)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"ok": True, "username": username, "token": token})


@app.route("/api/admin/delete_user/<int:user_id>", methods=["DELETE"])
@require_admin
def api_delete_user(user_id):
    firestore_db.delete_user(user_id)
    return jsonify({"ok": True})


@app.route("/api/admin/reset_token/<int:user_id>", methods=["POST"])
@require_admin
def api_reset_token(user_id):
    new_token = "usr-" + secrets.token_hex(16)
    firestore_db.update_user_token(user_id, new_token)
    return jsonify({"ok": True, "token": new_token})


@app.route("/api/admin/stats")
@require_admin
def api_admin_stats():
    from questions import STATIC_QUESTION_COUNT, ALL_OBJECTIVES
    stats = firestore_db.get_admin_stats()
    return jsonify({
        "users": stats["users"],
        "completed_exams": stats["completed_exams"],
        "in_progress_exams": stats["in_progress_exams"],
        "exam_tokens": stats["exam_tokens"],
        "custom_exams": stats["custom_exams_total"],
        "regular_exams": stats["regular_exams"] + 2,
        "objective_quizzes": stats["objective_quizzes"],
        "total_questions": STATIC_QUESTION_COUNT + stats["custom_questions"],
        "objectives_count": len(ALL_OBJECTIVES),
    })


@app.route("/api/admin/all_exams")
@require_admin
def api_admin_all_exams():
    all_exams = list_exams()
    # Enrich each exam with source label for the frontend
    result = []
    for e in all_exams:
        result.append({
            "id": e["id"],
            "title": e["title"],
            "total": e["total"],
            "exam_type": e.get("exam_type", "regular"),
            "source": e.get("source", "file"),
            "visible_to_users": e.get("visible_to_users", True if e.get("source") == "file" else False),
        })
    return jsonify(result)


@app.route("/api/admin/leaderboard")
@require_admin
def api_admin_leaderboard():
    exam_id = request.args.get("exam_id", type=int)
    mode = request.args.get("mode", "").strip()

    rows = firestore_db.get_leaderboard(exam_id=exam_id, mode=mode or None)
    return jsonify(rows)


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
    try:
        firestore_db.create_exam_token(token, exam_id, assigned_to, mode, duration, label)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"ok": True, "token": token, "exam_id": exam_id, "mode": mode, "duration": duration})


@app.route("/api/admin/exam_tokens")
@require_admin
def api_list_exam_tokens():
    rows = firestore_db.get_all_exam_tokens()
    return jsonify(rows)


@app.route("/api/admin/delete_exam_token/<int:token_id>", methods=["DELETE"])
@require_admin
def api_delete_exam_token(token_id):
    firestore_db.delete_exam_token_by_id(token_id)
    return jsonify({"ok": True})


@app.route("/api/admin/all_results")
@require_admin
def api_all_results():
    rows = firestore_db.get_all_sessions_with_users()
    return jsonify(rows)


@app.route("/api/redeem_exam_token", methods=["POST"])
@require_token
def api_redeem_exam_token():
    data = request.json or {}
    et_token = data.get("exam_token", "").strip()
    user = request.current_user

    et = firestore_db.get_exam_token(et_token)
    if not et:
        return jsonify({"error": "Invalid exam token"}), 404

    if et["assigned_to"] and et["assigned_to"] != user["id"]:
        return jsonify({"error": "This token is assigned to a different user"}), 403

    # C4 — Token à usage unique : bloqué dès qu'il a été utilisé (même user)
    if et["used_by"]:
        return jsonify({"error": "This token has already been used"}), 403

    firestore_db.mark_exam_token_used(et["id"], user["id"])

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

    new_id = firestore_db.get_next_custom_exam_id()
    try:
        firestore_db.create_custom_exam(new_id, title, description, exam_type,
                                        filter_objectives, request.current_user["id"])
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    if exam_type == "objective" and objectives:
        from questions import _questions_for_objectives
        matched = _questions_for_objectives(objectives)
        for pos, q in enumerate(matched, 1):
            firestore_db.create_quiz_link(new_id, q["exam_id"], q["num"], pos)

    return jsonify({"ok": True, "id": new_id, "title": title, "exam_type": exam_type})


@app.route("/api/admin/delete_custom_exam/<int:exam_id>", methods=["DELETE"])
@require_admin
def api_delete_custom_exam(exam_id):
    firestore_db.delete_custom_questions_by_exam(exam_id)
    firestore_db.delete_quiz_links_by_quiz(exam_id)
    firestore_db.delete_custom_exam(exam_id)
    return jsonify({"ok": True})


@app.route("/api/admin/custom_exams")
@require_admin
def api_list_custom_exams():
    rows = firestore_db.get_active_custom_exams()
    result = []
    for row in rows:
        if row["exam_type"] == "objective":
            from questions import _build_objective_exam
            exam = _build_objective_exam(row)
            row["question_count"] = len(exam["questions"])
        else:
            row["question_count"] = len(firestore_db.get_custom_questions_by_exam(row["id"]))
        raw = row.get("filter_objectives") or ""
        row["objectives_list"] = [o for o in raw.split("|||") if o]
        result.append(row)
    return jsonify(result)


@app.route("/api/admin/quiz_links/<int:quiz_id>")
@require_admin
def api_quiz_links(quiz_id):
    links = firestore_db.get_quiz_links(quiz_id)
    return jsonify(links)


@app.route("/api/admin/add_quiz_link", methods=["POST"])
@require_admin
def api_add_quiz_link():
    data = request.json or {}
    quiz_id = data.get("quiz_id")
    source_exam_id = data.get("source_exam_id")
    source_question_num = data.get("source_question_num")
    if not all([quiz_id, source_exam_id, source_question_num]):
        return jsonify({"error": "quiz_id, source_exam_id, source_question_num required"}), 400
    if firestore_db.get_existing_link(quiz_id, source_exam_id, source_question_num):
        return jsonify({"error": "Question already linked"}), 409
    max_pos = firestore_db.get_max_link_position(quiz_id)
    firestore_db.create_quiz_link(quiz_id, source_exam_id, source_question_num, max_pos + 1)
    return jsonify({"ok": True})


@app.route("/api/admin/remove_quiz_link/<int:link_id>", methods=["DELETE"])
@require_admin
def api_remove_quiz_link(link_id):
    firestore_db.delete_quiz_link(link_id)
    return jsonify({"ok": True})


@app.route("/api/admin/toggle_quiz_visibility/<int:exam_id>", methods=["POST"])
@require_admin
def api_toggle_quiz_visibility(exam_id):
    try:
        new_val = firestore_db.toggle_custom_exam_visibility(exam_id)
    except ValueError:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"ok": True, "visible_to_users": new_val})


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

    exam_row = firestore_db.get_custom_exam_by_id(exam_id)
    if not exam_row or exam_row.get("exam_type") != "regular":
        return jsonify({"error": "Exam not found or is not a regular exam"}), 404

    q_num = firestore_db.get_max_question_num(exam_id) + 1
    correct_json = json.dumps(correct_answer) if isinstance(correct_answer, list) else correct_answer
    options_json = json.dumps(all_options)

    new_id = firestore_db.create_custom_question(
        exam_id, q_num, question_text, q_type, correct_json, options_json,
        domain, objective, explanation, key_takeaway
    )
    return jsonify({"ok": True, "id": new_id, "question_num": q_num})


@app.route("/api/admin/delete_question/<int:q_id>", methods=["DELETE"])
@require_admin
def api_delete_question(q_id):
    firestore_db.delete_custom_question(q_id)
    return jsonify({"ok": True})


@app.route("/api/admin/exam_questions/<int:exam_id>")
@require_admin
def api_exam_questions(exam_id):
    rows = firestore_db.get_custom_questions_by_exam(exam_id)
    return jsonify(rows)


@app.route("/api/admin/exam_skeleton")
@require_admin
def api_exam_skeleton():
    """Génère et retourne un fichier JSON squelette prêt à remplir."""
    try:
        n = min(max(1, int(request.args.get("n", 10))), 200)
    except (ValueError, TypeError):
        n = 10
    title = request.args.get("title", "Mon Quiz").strip() or "Mon Quiz"

    skeleton = {
        "title": title,
        "description": "",
        "questions": [
            {
                "question": "",
                "type": "multiple_choice",
                "correct_answer": ["A"],
                "all_options": {"A": "", "B": "", "C": "", "D": ""},
                "domain": "",
                "explanation": "",
                "key_takeaway": ""
            }
            for _ in range(n)
        ]
    }
    from io import BytesIO
    buf = BytesIO(json.dumps(skeleton, indent=2, ensure_ascii=False).encode("utf-8"))
    buf.seek(0)
    filename = title.lower().replace(" ", "_")[:40] + "_skeleton.json"
    return send_file(buf, mimetype="application/json",
                     as_attachment=True, download_name=filename)


@app.route("/api/admin/import_exam", methods=["POST"])
@require_admin
def api_import_exam():
    """Importe un quiz depuis un fichier JSON uploadé ou un body JSON."""
    # Support multipart file upload ou JSON direct
    if request.files.get("file"):
        try:
            data = json.load(request.files["file"])
        except Exception:
            return jsonify({"error": "Invalid JSON file"}), 400
    else:
        data = request.json or {}

    title = (data.get("title") or "").strip()
    description = (data.get("description") or "").strip()
    questions = data.get("questions", [])

    if not title:
        return jsonify({"error": "title is required"}), 400
    if not questions or not isinstance(questions, list):
        return jsonify({"error": "questions list is required"}), 400

    new_id = firestore_db.get_next_custom_exam_id()
    firestore_db.create_custom_exam(new_id, title, description, "regular",
                                    "", request.current_user["id"])

    imported = 0
    for i, q in enumerate(questions, 1):
        question_text = (q.get("question") or "").strip()
        if not question_text:
            continue  # sauter les questions vides
        q_type = q.get("type", "multiple_choice")
        correct = q.get("correct_answer", [])
        if isinstance(correct, str):
            correct = [correct]
        all_options = q.get("all_options") or {}
        correct_json = json.dumps(correct)
        options_json = json.dumps(all_options)
        firestore_db.create_custom_question(
            new_id, i,
            question_text, q_type, correct_json, options_json,
            (q.get("domain") or "").strip(),
            (q.get("objective") or "").strip(),
            (q.get("explanation") or "").strip(),
            (q.get("key_takeaway") or "").strip(),
        )
        imported += 1

    return jsonify({"ok": True, "id": new_id, "title": title, "imported_count": imported})


if __name__ == "__main__":
    from firestore_db import init_firestore
    init_firestore()
    debug_mode = os.environ.get("DEBUG", "0") == "1"
    app.run(host="0.0.0.0", debug=debug_mode, port=8080)
