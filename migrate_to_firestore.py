"""
migrate_to_firestore.py — Migration one-shot SQLite → Firestore.

Usage :
    export GOOGLE_APPLICATION_CREDENTIALS=/path/to/serviceAccountKey.json
    python migrate_to_firestore.py [--dry-run] [--skip-existing]

Options :
    --dry-run        Affiche ce qui serait migré sans rien écrire dans Firestore
    --skip-existing  Ne réécrit pas les documents déjà présents dans Firestore

Ordre de migration (respecte les dépendances FK) :
    1. users
    2. exam_sessions
    3. answers
    4. exam_tokens
    5. custom_exams
    6. custom_questions
    7. quiz_question_links
"""

import sys
import os
import sqlite3
import json

# ── Config ──────────────────────────────────────────────────────────────────
SQLITE_PATH = os.path.join(os.path.dirname(__file__), "exam.db")
DRY_RUN = "--dry-run" in sys.argv
SKIP_EXISTING = "--skip-existing" in sys.argv

# ── Helpers ──────────────────────────────────────────────────────────────────

def get_sqlite():
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_fs():
    from firestore_client import get_firestore_client
    return get_firestore_client()


def col(name):
    return get_fs().collection(name)


def existing_ids(collection_name: str) -> set:
    """Retourne l'ensemble des doc IDs déjà présents dans la collection Firestore."""
    return {doc.id for doc in col(collection_name).stream()}


def batch_write(collection_name: str, docs: list[dict], id_field: str = "id"):
    """
    Écrit les docs par batch de 499 (limite Firestore).
    id_field : champ du dict utilisé comme document ID Firestore.
    """
    fs = get_fs()
    BATCH_SIZE = 499
    total = len(docs)
    written = 0

    already_there = existing_ids(collection_name) if SKIP_EXISTING else set()

    for i in range(0, total, BATCH_SIZE):
        chunk = docs[i : i + BATCH_SIZE]
        batch = fs.batch()
        count_chunk = 0
        for doc in chunk:
            doc_id = str(doc[id_field])
            if SKIP_EXISTING and doc_id in already_there:
                continue
            ref = col(collection_name).document(doc_id)
            if DRY_RUN:
                print(f"    [DRY] {collection_name}/{doc_id} ← {list(doc.keys())}")
            else:
                batch.set(ref, doc)
            count_chunk += 1
        if not DRY_RUN and count_chunk:
            batch.commit()
        written += count_chunk

    return written


# ── Migration par table ──────────────────────────────────────────────────────

def migrate_users(conn) -> dict:
    """
    Retourne un mapping {sqlite_id: firestore_doc_id}.
    Pour les users on utilise l'id SQLite directement comme doc ID.
    """
    rows = conn.execute("SELECT * FROM users").fetchall()
    docs = []
    id_map = {}
    for r in rows:
        d = dict(r)
        doc_id = str(d["id"])
        id_map[d["id"]] = doc_id
        docs.append(d)
    n = batch_write("users", docs, id_field="id")
    print(f"  ✓ users : {n}/{len(rows)} migrés")
    return id_map


def migrate_exam_sessions(conn) -> dict:
    rows = conn.execute("SELECT * FROM exam_sessions").fetchall()
    docs = [dict(r) for r in rows]
    n = batch_write("exam_sessions", docs, id_field="id")
    print(f"  ✓ exam_sessions : {n}/{len(rows)} migrés")
    return {d["id"]: str(d["id"]) for d in docs}


def migrate_answers(conn):
    rows = conn.execute("SELECT * FROM answers").fetchall()
    docs = [dict(r) for r in rows]
    # answers : session_id stocké comme string dans Firestore (cohérence firestore_db.py)
    for d in docs:
        d["session_id"] = str(d["session_id"])
    n = batch_write("answers", docs, id_field="id")
    print(f"  ✓ answers : {n}/{len(rows)} migrés")


def migrate_exam_tokens(conn):
    rows = conn.execute("SELECT * FROM exam_tokens").fetchall()
    docs = [dict(r) for r in rows]
    n = batch_write("exam_tokens", docs, id_field="id")
    print(f"  ✓ exam_tokens : {n}/{len(rows)} migrés")


def migrate_custom_exams(conn):
    rows = conn.execute("SELECT * FROM custom_exams").fetchall()
    docs = [dict(r) for r in rows]
    n = batch_write("custom_exams", docs, id_field="id")
    print(f"  ✓ custom_exams : {n}/{len(rows)} migrés")


def migrate_custom_questions(conn):
    rows = conn.execute(
        "SELECT * FROM custom_questions ORDER BY exam_id, question_num"
    ).fetchall()
    docs = [dict(r) for r in rows]
    n = batch_write("custom_questions", docs, id_field="id")
    print(f"  ✓ custom_questions : {n}/{len(rows)} migrés")


def migrate_quiz_question_links(conn):
    rows = conn.execute(
        "SELECT * FROM quiz_question_links ORDER BY quiz_id, position"
    ).fetchall()
    docs = [dict(r) for r in rows]
    n = batch_write("quiz_question_links", docs, id_field="id")
    print(f"  ✓ quiz_question_links : {n}/{len(rows)} migrés")


# ── Vérification post-migration ──────────────────────────────────────────────

def verify(conn):
    print("\n📊 Vérification post-migration :")
    tables = [
        "users", "exam_sessions", "answers",
        "exam_tokens", "custom_exams", "custom_questions", "quiz_question_links"
    ]
    all_ok = True
    for t in tables:
        sqlite_cnt = conn.execute(f"SELECT COUNT(*) as c FROM {t}").fetchone()["c"]
        fs_cnt = sum(1 for _ in col(t).stream())
        status = "✅" if fs_cnt >= sqlite_cnt else "⚠️ "
        if fs_cnt < sqlite_cnt:
            all_ok = False
        print(f"  {status} {t:25s}  SQLite={sqlite_cnt:4d}  Firestore={fs_cnt:4d}")
    if all_ok:
        print("\n✅ Migration complète — tous les comptes correspondent.")
    else:
        print("\n⚠️  Certaines collections ont moins de documents qu'attendu.")
        print("   Relancer avec --skip-existing pour compléter sans doublons.")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    if not os.path.exists(SQLITE_PATH):
        print(f"❌ SQLite introuvable : {SQLITE_PATH}")
        sys.exit(1)

    print(f"🚀 Migration SQLite → Firestore")
    print(f"   Source  : {SQLITE_PATH}")
    print(f"   Projet  : {get_fs().project}")
    print(f"   Mode    : {'DRY RUN (rien écrit)' if DRY_RUN else 'RÉEL'}")
    print(f"   Doublons: {'ignorés (--skip-existing)' if SKIP_EXISTING else 'écrasés'}")
    print()

    conn = get_sqlite()
    try:
        migrate_users(conn)
        migrate_exam_sessions(conn)
        migrate_answers(conn)
        migrate_exam_tokens(conn)
        migrate_custom_exams(conn)
        migrate_custom_questions(conn)
        migrate_quiz_question_links(conn)

        if not DRY_RUN:
            verify(conn)
        else:
            print("\n[DRY RUN] Rien n'a été écrit. Relancer sans --dry-run pour migrer.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
