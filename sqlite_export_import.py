"""
SQLite Export / Import utility for the Terraform Exam app.

Usage:
  Export:  python sqlite_export_import.py export [--db PATH] [--out FILE]
  Import:  python sqlite_export_import.py import <file.json> [--db PATH] [--merge]

Options:
  --db    PATH   Path to exam.db  (default: ./exam.db)
  --out   FILE   Output JSON file (default: export_<timestamp>.json)
  --merge        On import, skip rows whose primary key already exists
                 (default: wipe each table and re-insert everything)
"""

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime


# ── helpers ──────────────────────────────────────────────────────────────────

TABLES_ORDER = [
    "users",
    "exam_tokens",
    "exam_sessions",
    "answers",
    "custom_exams",
    "custom_questions",
    "quiz_question_links",
]


def connect(db_path: str) -> sqlite3.Connection:
    if not os.path.exists(db_path):
        print(f"[ERROR] Database not found: {db_path}", file=sys.stderr)
        sys.exit(1)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = OFF")
    return conn


def table_exists(conn: sqlite3.Connection, name: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)
    ).fetchone()
    return row is not None


# ── export ───────────────────────────────────────────────────────────────────

def export_db(db_path: str, out_path: str) -> None:
    conn = connect(db_path)
    data = {
        "_meta": {
            "exported_at": datetime.utcnow().isoformat() + "Z",
            "source_db": os.path.abspath(db_path),
        },
        "tables": {},
    }

    for table in TABLES_ORDER:
        if not table_exists(conn, table):
            print(f"  [SKIP] table '{table}' does not exist — skipping")
            continue
        rows = conn.execute(f"SELECT * FROM {table}").fetchall()
        data["tables"][table] = [dict(r) for r in rows]
        print(f"  [OK]   exported {len(rows):>5} rows from '{table}'")

    conn.close()

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)

    size_kb = os.path.getsize(out_path) / 1024
    print(f"\n✅ Export complete → {out_path}  ({size_kb:.1f} KB)")


# ── import ───────────────────────────────────────────────────────────────────

def import_db(db_path: str, in_path: str, merge: bool) -> None:
    if not os.path.exists(in_path):
        print(f"[ERROR] Import file not found: {in_path}", file=sys.stderr)
        sys.exit(1)

    with open(in_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    meta = data.get("_meta", {})
    print(f"  Importing from: {in_path}")
    print(f"  Exported at:    {meta.get('exported_at', 'unknown')}")
    print(f"  Source DB:      {meta.get('source_db', 'unknown')}")
    print(f"  Mode:           {'merge (skip duplicates)' if merge else 'replace (wipe + re-insert)'}")
    print()

    conn = connect(db_path)
    tables = data.get("tables", {})

    for table in TABLES_ORDER:
        if table not in tables:
            continue
        rows = tables[table]
        if not rows:
            print(f"  [SKIP] '{table}' — no rows in export")
            continue
        if not table_exists(conn, table):
            print(f"  [SKIP] '{table}' — table doesn't exist in target DB")
            continue

        if not merge:
            conn.execute(f"DELETE FROM {table}")

        cols = list(rows[0].keys())
        placeholders = ", ".join("?" * len(cols))
        col_names = ", ".join(cols)
        conflict_clause = "OR IGNORE" if merge else "OR REPLACE"
        sql = f"INSERT {conflict_clause} INTO {table} ({col_names}) VALUES ({placeholders})"

        inserted = 0
        skipped = 0
        for row in rows:
            values = [row.get(c) for c in cols]
            try:
                conn.execute(sql, values)
                inserted += 1
            except sqlite3.IntegrityError:
                skipped += 1

        conn.commit()
        print(f"  [OK]   '{table}': {inserted} inserted, {skipped} skipped")

    conn.execute("PRAGMA foreign_keys = ON")
    conn.close()
    print(f"\n✅ Import complete → {db_path}")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Export or import the Terraform Exam SQLite database to/from JSON."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # export
    exp = sub.add_parser("export", help="Export DB to a JSON file")
    exp.add_argument("--db", default="exam.db", help="Path to exam.db (default: exam.db)")
    exp.add_argument(
        "--out",
        default=None,
        help="Output JSON file (default: export_<timestamp>.json)",
    )

    # import
    imp = sub.add_parser("import", help="Import a JSON file into the DB")
    imp.add_argument("file", help="JSON file to import")
    imp.add_argument("--db", default="exam.db", help="Path to exam.db (default: exam.db)")
    imp.add_argument(
        "--merge",
        action="store_true",
        help="Skip rows whose primary key already exists (default: wipe + re-insert)",
    )

    args = parser.parse_args()

    if args.command == "export":
        out = args.out or f"export_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        print(f"Exporting '{args.db}' …")
        export_db(args.db, out)

    elif args.command == "import":
        if not args.merge:
            confirm = input(
                f"⚠️  This will WIPE and replace data in '{args.db}'. Continue? [y/N] "
            ).strip().lower()
            if confirm != "y":
                print("Aborted.")
                sys.exit(0)
        print(f"Importing into '{args.db}' …")
        import_db(args.db, args.file, args.merge)


if __name__ == "__main__":
    main()
