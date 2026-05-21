"""
firestore_db.py — Couche d'accès Firestore.

Remplace models.py (SQLite) sans toucher app.py.
Chaque fonction expose la même interface que ce qu'app.py attendait de SQLite :
  - retourne des dict (ou list[dict]) — compatible sqlite3.Row
  - retourne None si non trouvé
  - lève des exceptions Python standards en cas d'erreur

Collections Firestore utilisées :
  users / exam_sessions / answers / exam_tokens /
  custom_exams / custom_questions / quiz_question_links

IDs :
  - users, exam_sessions, answers, exam_tokens, custom_questions, quiz_question_links
    → Firestore auto-ID (string) stocké aussi dans le champ "id" du document
  - custom_exams → ID numérique explicite (≥ 1000) conservé tel quel (string dans Firestore)

Conventions :
  - Les timestamps sont stockés comme strings ISO8601 (même format que SQLite CURRENT_TIMESTAMP)
  - Les fonctions qui "créent" retournent l'id (int ou str selon le cas)
"""

import secrets
import datetime
from firestore_client import get_firestore_client
from google.cloud.firestore_v1.base_query import FieldFilter

# ─────────────────────────────────────────────────────────────────────────────
# Helpers internes
# ─────────────────────────────────────────────────────────────────────────────

def _now() -> str:
    """Timestamp UTC au format SQLite : 'YYYY-MM-DD HH:MM:SS'"""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def _doc_to_dict(doc) -> dict | None:
    """Convertit un DocumentSnapshot en dict avec le champ 'id' inclus."""
    if doc is None or not doc.exists:
        return None
    d = doc.to_dict()
    d["id"] = _parse_id(doc.id)
    return d


def _parse_id(raw_id: str):
    """Essaie de convertir l'id Firestore en int si possible (rétro-compat SQLite)."""
    try:
        return int(raw_id)
    except (ValueError, TypeError):
        return raw_id


def _col(name: str):
    """Raccourci collection."""
    return get_firestore_client().collection(name)


# ─────────────────────────────────────────────────────────────────────────────
# USERS
# ─────────────────────────────────────────────────────────────────────────────

def get_user_by_token(token: str) -> dict | None:
    docs = _col("users").where(filter=FieldFilter("token", "==", token)).limit(1).stream()
    for doc in docs:
        return _doc_to_dict(doc)
    return None


def get_user_by_id(user_id: int | str) -> dict | None:
    doc = _col("users").document(str(user_id)).get()
    return _doc_to_dict(doc)


def get_all_users() -> list[dict]:
    docs = _col("users").stream()
    result = [_doc_to_dict(d) for d in docs]
    result.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return result


def create_user(username: str, token: str, role: str = "user") -> dict:
    """Crée un utilisateur, retourne le dict complet avec son id."""
    fs = get_firestore_client()
    # Vérifier unicité username
    existing = _col("users").where(filter=FieldFilter("username", "==", username)).limit(1).stream()
    for _ in existing:
        raise ValueError(f"Username '{username}' already exists")
    ref = _col("users").document()
    data = {
        "username": username,
        "token": token,
        "role": role,
        "created_at": _now(),
    }
    ref.set(data)
    data["id"] = _parse_id(ref.id)
    return data


def delete_user(user_id: int | str) -> None:
    """Supprime un user non-admin."""
    ref = _col("users").document(str(user_id))
    doc = ref.get()
    if doc.exists and doc.to_dict().get("role") != "admin":
        ref.delete()


def update_user_token(user_id: int | str, new_token: str) -> None:
    _col("users").document(str(user_id)).update({"token": new_token})


def count_users(role: str = "user") -> int:
    docs = _col("users").where(filter=FieldFilter("role", "==", role)).stream()
    return sum(1 for _ in docs)


def get_or_create_admin() -> dict | None:
    """Crée l'admin par défaut si aucun n'existe. Retourne l'admin existant ou créé."""
    docs = list(_col("users").where(filter=FieldFilter("role", "==", "admin")).limit(1).stream())
    if docs:
        return None  # déjà existant, rien à faire
    admin_token = "admin-" + secrets.token_hex(16)
    data = create_user("admin", admin_token, role="admin")
    print(f"[INIT] Admin created. Token: {admin_token}")
    return data


# ─────────────────────────────────────────────────────────────────────────────
# EXAM SESSIONS
# ─────────────────────────────────────────────────────────────────────────────

def get_session_by_id(session_id: int | str, user_id: int | str | None = None) -> dict | None:
    doc = _col("exam_sessions").document(str(session_id)).get()
    result = _doc_to_dict(doc)
    if result and user_id is not None and str(result.get("user_id")) != str(user_id):
        return None
    return result


def get_sessions_by_user(user_id: int | str) -> list[dict]:
    docs = (_col("exam_sessions")
            .where(filter=FieldFilter("user_id", "==", int(user_id)))
            .stream())
    result = [_doc_to_dict(d) for d in docs]
    result.sort(key=lambda x: x.get("started_at", ""), reverse=True)
    return result


def get_inprogress_session(user_id: int | str, exam_id: int) -> dict | None:
    docs = (_col("exam_sessions")
            .where(filter=FieldFilter("user_id", "==", int(user_id)))
            .where(filter=FieldFilter("exam_id", "==", exam_id))
            .where(filter=FieldFilter("status", "==", "in_progress"))
            .limit(1)
            .stream())
    for doc in docs:
        return _doc_to_dict(doc)
    return None


def create_exam_session(user_id: int | str, exam_id: int, total: int,
                        mode: str, duration_minutes: int) -> tuple[int | str, str]:
    """Crée une session, retourne (session_id, started_at)."""
    ref = _col("exam_sessions").document()
    started_at = _now()
    data = {
        "user_id": int(user_id),
        "exam_id": exam_id,
        "total": total,
        "mode": mode,
        "duration_minutes": duration_minutes,
        "status": "in_progress",
        "started_at": started_at,
        "finished_at": None,
        "score": None,
    }
    ref.set(data)
    return _parse_id(ref.id), started_at


def finish_exam_session(session_id: int | str, score: int) -> None:
    _col("exam_sessions").document(str(session_id)).update({
        "status": "finished",
        "finished_at": _now(),
        "score": score,
    })


def expire_exam_session(session_id: int | str) -> None:
    _col("exam_sessions").document(str(session_id)).update({
        "status": "finished",
        "finished_at": _now(),
    })


def get_all_sessions_with_users() -> list[dict]:
    """Pour /api/admin/all_results — jointure manuelle sessions + users."""
    sessions = list(_col("exam_sessions").stream())
    sessions_dicts = [_doc_to_dict(d) for d in sessions]
    sessions_dicts.sort(key=lambda x: x.get("started_at", ""), reverse=True)
    result = []
    for s in sessions_dicts:
        user = get_user_by_id(s["user_id"])
        s["username"] = user["username"] if user else "Unknown"
        result.append(s)
    return result


def count_sessions(status: str | None = None) -> int:
    q = _col("exam_sessions")
    if status:
        q = q.where(filter=FieldFilter("status", "==", status))
    return sum(1 for _ in q.stream())


# ─────────────────────────────────────────────────────────────────────────────
# ANSWERS
# ─────────────────────────────────────────────────────────────────────────────

def get_answers_by_session(session_id: int | str) -> list[dict]:
    docs = (_col("answers")
            .where(filter=FieldFilter("session_id", "==", str(session_id)))
            .stream())
    result = [_doc_to_dict(d) for d in docs]
    result.sort(key=lambda x: x.get("question_num", 0))
    return result


def get_answer(session_id: int | str, question_num: int) -> dict | None:
    docs = (_col("answers")
            .where(filter=FieldFilter("session_id", "==", str(session_id)))
            .where(filter=FieldFilter("question_num", "==", question_num))
            .limit(1)
            .stream())
    for doc in docs:
        return _doc_to_dict(doc)
    return None


def upsert_answer(session_id: int | str, question_num: int, user_answer: str,
                  is_correct: int, result: str, objective: str, domain: str) -> None:
    """Crée ou met à jour une réponse (upsert)."""
    existing = get_answer(session_id, question_num)
    data = {
        "session_id": str(session_id),
        "question_num": question_num,
        "user_answer": user_answer,
        "is_correct": is_correct,
        "result": result,
        "objective": objective,
        "domain": domain,
    }
    if existing:
        _col("answers").document(str(existing["id"])).update(data)
    else:
        _col("answers").document().set(data)


def count_correct_answers(session_id: int | str) -> int:
    docs = (_col("answers")
            .where(filter=FieldFilter("session_id", "==", str(session_id)))
            .where(filter=FieldFilter("is_correct", "==", 1))
            .stream())
    return sum(1 for _ in docs)


# ─────────────────────────────────────────────────────────────────────────────
# EXAM TOKENS
# ─────────────────────────────────────────────────────────────────────────────

def get_exam_token(token_str: str) -> dict | None:
    docs = _col("exam_tokens").where(filter=FieldFilter("token", "==", token_str)).limit(1).stream()
    for doc in docs:
        return _doc_to_dict(doc)
    return None


def get_all_exam_tokens() -> list[dict]:
    """Pour /api/admin/exam_tokens — avec usernames résolus."""
    docs_raw = list(_col("exam_tokens").stream())
    docs = sorted(docs_raw, key=lambda d: d.to_dict().get("created_at", ""), reverse=True)
    result = []
    for doc in docs:
        t = _doc_to_dict(doc)
        # Résoudre assigned_to
        if t.get("assigned_to"):
            u = get_user_by_id(t["assigned_to"])
            t["assigned_username"] = u["username"] if u else None
        else:
            t["assigned_username"] = None
        # Résoudre used_by
        if t.get("used_by"):
            u = get_user_by_id(t["used_by"])
            t["used_username"] = u["username"] if u else None
        else:
            t["used_username"] = None
        result.append(t)
    return result


def create_exam_token(token_str: str, exam_id: int, assigned_to: int | None,
                      mode: str, duration_minutes: int, label: str) -> None:
    ref = _col("exam_tokens").document()
    ref.set({
        "token": token_str,
        "exam_id": exam_id,
        "assigned_to": assigned_to,
        "mode": mode,
        "duration_minutes": duration_minutes,
        "label": label,
        "used_by": None,
        "used_at": None,
        "created_at": _now(),
    })


def mark_exam_token_used(token_doc_id: int | str, user_id: int | str) -> None:
    _col("exam_tokens").document(str(token_doc_id)).update({
        "used_by": int(user_id),
        "used_at": _now(),
    })


def delete_exam_token_by_id(token_doc_id: int | str) -> None:
    _col("exam_tokens").document(str(token_doc_id)).delete()


def get_used_token_for_user_and_exam(user_id: int | str, exam_id: int) -> dict | None:
    """Vérifie si l'user a utilisé un token pour cet exam (accès autorisé)."""
    docs = (_col("exam_tokens")
            .where(filter=FieldFilter("used_by", "==", int(user_id)))
            .where(filter=FieldFilter("exam_id", "==", exam_id))
            .limit(1)
            .stream())
    for doc in docs:
        return _doc_to_dict(doc)
    return None


def count_exam_tokens() -> int:
    return sum(1 for _ in _col("exam_tokens").stream())


# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM EXAMS
# ─────────────────────────────────────────────────────────────────────────────

def get_next_custom_exam_id() -> int:
    """Reproduit COALESCE(MAX(id), 999) + 1, min 1000."""
    docs = list(_col("custom_exams").stream())
    if not docs:
        return 1000
    ids = []
    for doc in docs:
        try:
            ids.append(int(doc.id))
        except ValueError:
            pass
    return max(max(ids) + 1, 1000) if ids else 1000


def get_custom_exam_by_id(exam_id: int | str) -> dict | None:
    doc = _col("custom_exams").document(str(exam_id)).get()
    return _doc_to_dict(doc)


def get_active_custom_exams() -> list[dict]:
    docs = (_col("custom_exams")
            .where(filter=FieldFilter("is_active", "==", 1))
            .stream())
    result = [_doc_to_dict(d) for d in docs]
    result.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return result


def create_custom_exam(new_id: int, title: str, description: str, exam_type: str,
                       filter_objectives: str, created_by: int | str) -> None:
    _col("custom_exams").document(str(new_id)).set({
        "title": title,
        "description": description,
        "exam_type": exam_type,
        "filter_objectives": filter_objectives,
        "created_by": int(created_by),
        "created_at": _now(),
        "is_active": 1,
        "visible_to_users": 0,
    })


def delete_custom_exam(exam_id: int | str) -> None:
    _col("custom_exams").document(str(exam_id)).delete()


def toggle_custom_exam_visibility(exam_id: int | str) -> bool:
    """Inverse visible_to_users. Retourne la nouvelle valeur (bool)."""
    ref = _col("custom_exams").document(str(exam_id))
    doc = ref.get()
    if not doc.exists:
        raise ValueError(f"Custom exam {exam_id} not found")
    current = doc.to_dict().get("visible_to_users", 0)
    new_val = 0 if current else 1
    ref.update({"visible_to_users": new_val})
    return bool(new_val)


def count_custom_exams(exam_type: str | None = None) -> int:
    q = _col("custom_exams").where(filter=FieldFilter("is_active", "==", 1))
    if exam_type:
        q = q.where(filter=FieldFilter("exam_type", "==", exam_type))
    return sum(1 for _ in q.stream())


# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM QUESTIONS
# ─────────────────────────────────────────────────────────────────────────────

def get_custom_questions_by_exam(exam_id: int | str) -> list[dict]:
    docs = (_col("custom_questions")
            .where(filter=FieldFilter("exam_id", "==", int(exam_id)))
            .stream())
    result = [_doc_to_dict(d) for d in docs]
    result.sort(key=lambda x: x.get("question_num", 0))
    return result


def get_max_question_num(exam_id: int | str) -> int:
    docs = list(_col("custom_questions").where(filter=FieldFilter("exam_id", "==", int(exam_id))).stream())
    if not docs:
        return 0
    nums = [d.to_dict().get("question_num", 0) for d in docs]
    return max(nums)


def create_custom_question(exam_id: int | str, question_num: int, question: str,
                           q_type: str, correct_answer: str, all_options: str,
                           domain: str, objective: str, explanation: str,
                           key_takeaway: str) -> str:
    """Crée une question custom, retourne son Firestore doc id."""
    ref = _col("custom_questions").document()
    ref.set({
        "exam_id": int(exam_id),
        "question_num": question_num,
        "question": question,
        "type": q_type,
        "correct_answer": correct_answer,
        "all_options": all_options,
        "domain": domain,
        "objective": objective,
        "explanation": explanation,
        "key_takeaway": key_takeaway,
    })
    return ref.id


def get_custom_question_by_id(q_id: int | str) -> dict | None:
    return _doc_to_dict(_col("custom_questions").document(str(q_id)).get())


def update_custom_question(q_id: int | str, question: str, q_type: str,
                           correct_answer: str, all_options: str,
                           domain: str, objective: str, explanation: str,
                           key_takeaway: str) -> None:
    _col("custom_questions").document(str(q_id)).update({
        "question": question,
        "type": q_type,
        "correct_answer": correct_answer,
        "all_options": all_options,
        "domain": domain,
        "objective": objective,
        "explanation": explanation,
        "key_takeaway": key_takeaway,
    })


def delete_custom_question(q_id: int | str) -> None:
    _col("custom_questions").document(str(q_id)).delete()


def delete_custom_questions_by_exam(exam_id: int | str) -> None:
    docs = _col("custom_questions").where(filter=FieldFilter("exam_id", "==", int(exam_id))).stream()
    for doc in docs:
        doc.reference.delete()


def count_custom_questions() -> int:
    return sum(1 for _ in _col("custom_questions").stream())


# ─────────────────────────────────────────────────────────────────────────────
# QUIZ QUESTION LINKS
# ─────────────────────────────────────────────────────────────────────────────

def get_quiz_links(quiz_id: int | str) -> list[dict]:
    docs = (_col("quiz_question_links")
            .where(filter=FieldFilter("quiz_id", "==", int(quiz_id)))
            .stream())
    result = [_doc_to_dict(d) for d in docs]
    result.sort(key=lambda x: x.get("position", 0))
    return result


def get_max_link_position(quiz_id: int | str) -> int:
    docs = list(_col("quiz_question_links").where(filter=FieldFilter("quiz_id", "==", int(quiz_id))).stream())
    if not docs:
        return 0
    return max(d.to_dict().get("position", 0) for d in docs)


def get_existing_link(quiz_id: int | str, source_exam_id: int, source_question_num: int) -> dict | None:
    docs = (_col("quiz_question_links")
            .where(filter=FieldFilter("quiz_id", "==", int(quiz_id)))
            .where(filter=FieldFilter("source_exam_id", "==", source_exam_id))
            .where(filter=FieldFilter("source_question_num", "==", source_question_num))
            .limit(1)
            .stream())
    for doc in docs:
        return _doc_to_dict(doc)
    return None


def create_quiz_link(quiz_id: int | str, source_exam_id: int,
                     source_question_num: int, position: int) -> None:
    _col("quiz_question_links").document().set({
        "quiz_id": int(quiz_id),
        "source_exam_id": source_exam_id,
        "source_question_num": source_question_num,
        "position": position,
    })


def delete_quiz_link(link_id: int | str) -> None:
    _col("quiz_question_links").document(str(link_id)).delete()


def delete_quiz_links_by_quiz(quiz_id: int | str) -> None:
    docs = _col("quiz_question_links").where(filter=FieldFilter("quiz_id", "==", int(quiz_id))).stream()
    for doc in docs:
        doc.reference.delete()


# ─────────────────────────────────────────────────────────────────────────────
# LEADERBOARD (remplace la requête SQL avec JOIN + GROUP BY)
# ─────────────────────────────────────────────────────────────────────────────

def get_leaderboard(exam_id: int | None = None, mode: str | None = None) -> list[dict]:
    """
    Reproduit la requête leaderboard SQL (GROUP BY user, MAX/AVG score, COUNT passed).
    Assemblage Python car Firestore n'a pas de GROUP BY.
    """
    q = _col("exam_sessions").where(filter=FieldFilter("status", "==", "finished"))
    if exam_id:
        q = q.where(filter=FieldFilter("exam_id", "==", exam_id))
    if mode:
        q = q.where(filter=FieldFilter("mode", "==", mode))

    sessions = list(q.stream())

    # Agréger par user_id
    by_user: dict[int, dict] = {}
    for doc in sessions:
        s = doc.to_dict()
        uid = s.get("user_id")
        total = s.get("total") or 1
        score = s.get("score") or 0
        pct = score / total * 100

        if uid not in by_user:
            by_user[uid] = {
                "user_id": uid,
                "total_finished": 0,
                "best_pct": 0.0,
                "sum_pct": 0.0,
                "best_score": 0,
                "best_total": 0,
                "passed": 0,
                "last_exam": s.get("finished_at", ""),
            }
        agg = by_user[uid]
        agg["total_finished"] += 1
        agg["sum_pct"] += pct
        agg["best_pct"] = max(agg["best_pct"], pct)
        agg["best_score"] = max(agg["best_score"], score)
        agg["best_total"] = max(agg["best_total"], total)
        if pct >= 70:
            agg["passed"] += 1
        if s.get("finished_at", "") > agg["last_exam"]:
            agg["last_exam"] = s.get("finished_at", "")

    # Résoudre les usernames + calculer avg_pct
    result = []
    for uid, agg in by_user.items():
        user = get_user_by_id(uid)
        if not user or user.get("role") != "user":
            continue
        agg["username"] = user["username"]
        agg["avg_pct"] = agg["sum_pct"] / agg["total_finished"]
        del agg["sum_pct"]
        result.append(agg)

    result.sort(key=lambda x: (-x["best_pct"], -x["avg_pct"], -x["total_finished"]))
    return result


# ─────────────────────────────────────────────────────────────────────────────
# ADMIN STATS
# ─────────────────────────────────────────────────────────────────────────────

def get_admin_stats() -> dict:
    return {
        "users": count_users("user"),
        "completed_exams": count_sessions("finished"),
        "in_progress_exams": count_sessions("in_progress"),
        "exam_tokens": count_exam_tokens(),
        "custom_exams_total": count_custom_exams(),
        "regular_exams": count_custom_exams("regular"),
        "objective_quizzes": count_custom_exams("objective"),
        "custom_questions": count_custom_questions(),
    }


# ─────────────────────────────────────────────────────────────────────────────
# INIT (remplace init_db de models.py)
# ─────────────────────────────────────────────────────────────────────────────

def init_firestore():
    """
    Vérifie la connexion Firestore et crée l'admin par défaut si nécessaire.
    Appelé au démarrage de l'app à la place de init_db().
    """
    try:
        # Test de connexion : lecture légère
        get_firestore_client().collection("users").limit(1).stream()
        print("[INIT] Firestore connection OK")
    except Exception as e:
        raise RuntimeError(f"[INIT] Firestore connection failed: {e}")

    get_or_create_admin()
