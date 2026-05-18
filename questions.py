"""
Loads questions from exam2_questions.py and exam3_questions.py
and also from custom_exams / custom_questions in the database.
"""
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from exam2_questions import exam2
from exam3_questions import exam3


def _normalize(q_num, q_data, exam_id):
    correct = q_data.get("correct_answer", "")
    if isinstance(correct, list):
        correct_list = correct
    else:
        correct_list = [correct]
    q_type = q_data.get("type", "multiple_choice")
    all_options = q_data.get("all_options") or {}
    return {
        "num": q_num,
        "exam_id": exam_id,
        "question": q_data.get("question", ""),
        "type": q_type,
        "correct_answer": correct_list,
        "domain": q_data.get("domain", ""),
        "objective": q_data.get("objective", ""),
        "explanation": q_data.get("explanation", ""),
        "key_takeaway": q_data.get("key_takeaway", ""),
        "all_options": all_options,
    }


# ── Static file-based exams ─────────────────────────────────────────────────
EXAMS = {
    2: {
        "id": 2,
        "title": exam2["exam_title"],
        "exam_type": "regular",
        "source": "file",
        "questions": {num: _normalize(num, q, 2) for num, q in exam2["questions"].items()},
    },
    3: {
        "id": 3,
        "title": exam3["exam_title"],
        "exam_type": "regular",
        "source": "file",
        "questions": {num: _normalize(num, q, 3) for num, q in exam3["questions"].items()},
    },
}

ALL_DOMAINS = sorted({
    q["domain"] for e in EXAMS.values() for q in e["questions"].values() if q.get("domain")
})

ALL_OBJECTIVES = sorted({
    q["objective"] for e in EXAMS.values() for q in e["questions"].values() if q.get("objective")
})

# Total question count across all static exams
STATIC_QUESTION_COUNT = sum(len(e["questions"]) for e in EXAMS.values())


def _questions_for_objectives(objectives):
    """Return all static questions matching any of the given objectives/domains (list of strings)."""
    obj_set = set(o.strip() for o in objectives if o.strip())
    result = []
    for exam in EXAMS.values():
        for q in exam["questions"].values():
            if q.get("objective") in obj_set or q.get("domain") in obj_set:
                result.append(q)
    return result


def _build_objective_exam(db_row, db=None):
    """Build an objective-quiz by filtering all static questions by one or more objectives."""
    raw = db_row.get("filter_objectives") or db_row.get("filter_domain") or ""
    objectives = [o.strip() for o in raw.split("|||") if o.strip()]

    # Check if there are linked questions (quiz_question_links)
    linked_questions = []
    if db:
        links = db.execute(
            "SELECT * FROM quiz_question_links WHERE quiz_id=? ORDER BY position",
            (db_row["id"],)
        ).fetchall()
        for lnk in links:
            src = EXAMS.get(lnk["source_exam_id"])
            if src:
                q = src["questions"].get(lnk["source_question_num"])
                if q:
                    linked_questions.append(dict(q, num=lnk["position"], exam_id=db_row["id"]))

    if linked_questions:
        questions = {q["num"]: q for q in linked_questions}
    elif objectives:
        raw_qs = _questions_for_objectives(objectives)
        questions = {i+1: dict(q, num=i+1, exam_id=db_row["id"]) for i, q in enumerate(raw_qs)}
    else:
        questions = {}

    return {
        "id": db_row["id"],
        "title": db_row["title"],
        "description": db_row.get("description") or "",
        "exam_type": "objective",
        "filter_objectives": objectives,
        "source": "db",
        "questions": questions,
    }


def _build_regular_db_exam(db_row, db):
    rows = db.execute(
        "SELECT * FROM custom_questions WHERE exam_id=? ORDER BY question_num",
        (db_row["id"],)
    ).fetchall()
    questions = {}
    for r in rows:
        try:
            opts = json.loads(r["all_options"] or "{}")
        except Exception:
            opts = {}
        try:
            correct = json.loads(r["correct_answer"])
        except Exception:
            correct = [r["correct_answer"]]
        if isinstance(correct, str):
            correct = [correct]
        questions[r["question_num"]] = {
            "num": r["question_num"],
            "exam_id": db_row["id"],
            "question": r["question"],
            "type": r["type"],
            "correct_answer": correct,
            "all_options": opts,
            "domain": r["domain"] or "",
            "objective": r["objective"] or "",
            "explanation": r["explanation"] or "",
            "key_takeaway": r["key_takeaway"] or "",
        }
    return {
        "id": db_row["id"],
        "title": db_row["title"],
        "description": db_row.get("description") or "",
        "exam_type": "regular",
        "source": "db",
        "questions": questions,
    }


def get_db_exam(exam_id):
    from models import get_db
    db = get_db()
    row = db.execute("SELECT * FROM custom_exams WHERE id=? AND is_active=1", (exam_id,)).fetchone()
    if not row:
        db.close()
        return None
    row = dict(row)
    if row["exam_type"] == "objective":
        exam = _build_objective_exam(row, db)
    else:
        exam = _build_regular_db_exam(row, db)
    db.close()
    return exam


def get_exam(exam_id):
    if exam_id in EXAMS:
        return EXAMS[exam_id]
    return get_db_exam(exam_id)


def get_question(exam_id, q_num):
    exam = get_exam(exam_id)
    if exam:
        return exam["questions"].get(q_num)
    return None


def list_exams():
    result = [
        {"id": e["id"], "title": e["title"], "total": len(e["questions"]),
         "exam_type": e.get("exam_type", "regular"), "source": "file"}
        for e in EXAMS.values()
    ]
    try:
        from models import get_db
        db = get_db()
        rows = db.execute("SELECT * FROM custom_exams WHERE is_active=1 ORDER BY created_at").fetchall()
        for row in rows:
            row = dict(row)
            if row["exam_type"] == "objective":
                exam = _build_objective_exam(row, db)
                total = len(exam["questions"])
            else:
                total = db.execute(
                    "SELECT COUNT(*) as cnt FROM custom_questions WHERE exam_id=?", (row["id"],)
                ).fetchone()["cnt"]
            raw = row.get("filter_objectives") or ""
            objectives = [o.strip() for o in raw.split("|||") if o.strip()]
            result.append({
                "id": row["id"],
                "title": row["title"],
                "total": total,
                "exam_type": row["exam_type"],
                "source": "db",
                "filter_objectives": objectives,
                "visible_to_users": bool(row.get("visible_to_users", 0)),
            })
        db.close()
    except Exception:
        pass
    return result
