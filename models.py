import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "exam.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            token TEXT UNIQUE NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS exam_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            exam_id INTEGER NOT NULL,
            started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            finished_at DATETIME,
            score INTEGER,
            total INTEGER,
            status TEXT DEFAULT 'in_progress',
            mode TEXT DEFAULT 'practice',
            duration_minutes INTEGER DEFAULT 60,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            question_num INTEGER NOT NULL,
            user_answer TEXT,
            is_correct INTEGER,
            result TEXT DEFAULT 'skipped',
            objective TEXT,
            domain TEXT,
            FOREIGN KEY(session_id) REFERENCES exam_sessions(id)
        );

        CREATE TABLE IF NOT EXISTS exam_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT UNIQUE NOT NULL,
            exam_id INTEGER NOT NULL,
            assigned_to INTEGER,
            mode TEXT DEFAULT 'exam',
            duration_minutes INTEGER DEFAULT 60,
            used_by INTEGER,
            used_at DATETIME,
            label TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(assigned_to) REFERENCES users(id),
            FOREIGN KEY(used_by) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS custom_exams (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            exam_type TEXT DEFAULT 'regular',
            filter_objectives TEXT,
            created_by INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1,
            visible_to_users INTEGER DEFAULT 0,
            FOREIGN KEY(created_by) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS custom_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exam_id INTEGER NOT NULL,
            question_num INTEGER NOT NULL,
            question TEXT NOT NULL,
            type TEXT DEFAULT 'multiple_choice',
            correct_answer TEXT NOT NULL,
            all_options TEXT DEFAULT '{}',
            domain TEXT DEFAULT '',
            objective TEXT DEFAULT '',
            explanation TEXT DEFAULT '',
            key_takeaway TEXT DEFAULT '',
            FOREIGN KEY(exam_id) REFERENCES custom_exams(id)
        );

        CREATE TABLE IF NOT EXISTS quiz_question_links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_id INTEGER NOT NULL,
            source_exam_id INTEGER NOT NULL,
            source_question_num INTEGER NOT NULL,
            position INTEGER NOT NULL,
            FOREIGN KEY(quiz_id) REFERENCES custom_exams(id)
        );
    """)
    conn.commit()

    # Migrate: add new columns if they don't exist yet
    for col, definition in [("mode", "TEXT DEFAULT 'practice'"), ("duration_minutes", "INTEGER DEFAULT 60")]:
        try:
            c.execute(f"ALTER TABLE exam_sessions ADD COLUMN {col} {definition}")
            conn.commit()
        except Exception:
            pass  # column already exists

    # Migrate answers table
    try:
        c.execute("ALTER TABLE answers ADD COLUMN domain TEXT")
        conn.commit()
    except Exception:
        pass  # already exists

    # Migrate custom_exams: rename filter_domain -> filter_objectives if needed
    try:
        c.execute("ALTER TABLE custom_exams ADD COLUMN filter_objectives TEXT")
        conn.commit()
    except Exception:
        pass

    # Create quiz_question_links if missing (safe, uses CREATE IF NOT EXISTS above)
    try:
        c.execute("ALTER TABLE custom_exams ADD COLUMN visible_to_users INTEGER DEFAULT 0")
        conn.commit()
    except Exception:
        pass  # already exists

    # Create default admin if not exists
    import secrets
    existing = c.execute("SELECT id FROM users WHERE role='admin'").fetchone()
    if not existing:
        admin_token = "admin-" + secrets.token_hex(16)
        c.execute(
            "INSERT INTO users (username, token, role) VALUES (?, ?, ?)",
            ("admin", admin_token, "admin"),
        )
        conn.commit()
        print(f"[INIT] Admin created. Token: {admin_token}")

    conn.close()
