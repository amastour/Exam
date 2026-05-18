# 🏗️ Terraform Exam – TA-004 Practice Platform

A self-hosted web application to practise for the **HashiCorp Certified Terraform Associate (TA-004)** exam.  
Users log in with a token, take timed exams in **Practice** or **Exam** mode, and see detailed results broken down by objective domain.  
Admins manage users, generate exam tokens, and monitor every candidate's progress.

---

## Table of Contents

1. [Features](#features)
2. [Project Structure](#project-structure)
3. [Quick Start](#quick-start)
4. [Configuration](#configuration)
5. [Database Schema](#database-schema)
6. [API Reference](#api-reference)
7. [Exam Modes](#exam-modes)
8. [Timer](#timer)
9. [Exam Tokens](#exam-tokens)
10. [Admin Panel](#admin-panel)
11. [Adding More Exams](#adding-more-exams)

---

## Features

| Feature | Details |
|---|---|
| Token-based auth | Each user gets a unique hex token — no passwords |
| Two exams | Exam #2 and Exam #3 (57 questions each) |
| Practice mode | Immediate feedback after each answer (correct/incorrect + explanation) |
| Exam mode | No feedback until the exam is finished |
| Countdown timer | Configurable per session (default 60 min) — auto-submits on expiry |
| Exam tokens | Admin generates a `et-…` token that encodes exam, mode and duration |
| Per-user history | Every session (in-progress and finished) is saved per user |
| Results & metrics | Score card, pass/fail (≥70%), performance breakdown by objective domain |
| Question review | Filterable review of all questions with correct answers and explanations |
| Admin panel | Create/delete users, generate exam tokens, view all results |

---

## Project Structure

```
terraform_exam/
├── exam2_questions.py          # 57 questions – Exam #2
├── exam3_questions.py          # 57 questions – Exam #3
├── README.md                   # This file
└── app/
    ├── app.py                  # Flask application & all routes
    ├── models.py               # SQLite schema + DB helpers
    ├── questions.py            # Question loader & normaliser
    ├── requirements.txt        # Python dependencies
    ├── exam.db                 # SQLite database (auto-created)
    ├── static/
    │   └── style.css           # Dark theme CSS
    └── templates/
        ├── login.html          # Token login page
        ├── dashboard.html      # Exam list, history, token redemption
        ├── exam.html           # Exam UI (timer, navigator, questions)
        ├── results.html        # Score card, objectives, question review
        └── admin.html          # Admin panel
```

---

## Quick Start

### 1 — Install dependencies

```bash
cd terraform_exam/app
pip install flask
```

### 2 — Run the server

```bash
python app.py
```

On the **first run** the database is created and a default admin account is generated:

```
[INIT] Admin created. Token: admin-<hex>
```

Copy that token — you will need it to log in as admin.

### 3 — Open the app

```
http://localhost:5000
```

Paste the admin token on the login page.

---

## Configuration

| Setting | Where | Default |
|---|---|---|
| Flask secret key | `app.py` (generated at startup) | Random hex — changes on each restart |
| Database path | `models.py` → `DB_PATH` | `app/exam.db` |
| Server port | `app.py` → `app.run(port=5000)` | `5000` |
| Default exam duration | Dashboard UI & exam token form | `60` minutes |
| Pass threshold | Hard-coded in templates | `70 %` |

---

## Database Schema

### `users`
| Column | Type | Description |
|---|---|---|
| `id` | INTEGER PK | Auto-increment |
| `username` | TEXT UNIQUE | Display name |
| `token` | TEXT UNIQUE | Login token (`admin-…` or `usr-…`) |
| `role` | TEXT | `admin` or `user` |
| `created_at` | DATETIME | Creation timestamp |

### `exam_sessions`
| Column | Type | Description |
|---|---|---|
| `id` | INTEGER PK | Auto-increment |
| `user_id` | INTEGER FK | Owner |
| `exam_id` | INTEGER | `2` or `3` |
| `started_at` | DATETIME | Session start (used to compute remaining time) |
| `finished_at` | DATETIME | Null until finished |
| `score` | INTEGER | Number of correct answers |
| `total` | INTEGER | Total questions |
| `status` | TEXT | `in_progress` or `finished` |
| `mode` | TEXT | `practice` or `exam` |
| `duration_minutes` | INTEGER | Allowed time in minutes |

### `answers`
| Column | Type | Description |
|---|---|---|
| `id` | INTEGER PK | Auto-increment |
| `session_id` | INTEGER FK | Parent session |
| `question_num` | INTEGER | Question number (1-based) |
| `user_answer` | TEXT | JSON array for multi-select, plain string otherwise |
| `is_correct` | INTEGER | `1` / `0` |
| `result` | TEXT | `correct`, `incorrect`, or `skipped` |
| `objective` | TEXT | Objective domain label |

### `exam_tokens`
| Column | Type | Description |
|---|---|---|
| `id` | INTEGER PK | Auto-increment |
| `token` | TEXT UNIQUE | `et-<hex>` token shared with candidate |
| `exam_id` | INTEGER | Target exam |
| `assigned_to` | INTEGER FK | Specific user, or NULL (any user) |
| `mode` | TEXT | `exam` or `practice` |
| `duration_minutes` | INTEGER | Timer duration |
| `used_by` | INTEGER FK | User who redeemed it |
| `used_at` | DATETIME | Redemption timestamp |
| `label` | TEXT | Optional descriptive label |
| `created_at` | DATETIME | Creation timestamp |

---

## API Reference

All endpoints require a valid session cookie (set by `POST /api/login`) unless noted.  
Admin endpoints additionally require `role = admin`.

### Auth

| Method | Path | Body | Description |
|---|---|---|---|
| `POST` | `/api/login` | `{ token }` | Validates token, sets session cookie |
| `POST` | `/api/logout` | — | Clears session |

### Exam

| Method | Path | Body / Params | Description |
|---|---|---|---|
| `GET` | `/exam/<exam_id>` | `?mode=exam&duration=60` | Loads or resumes a session |
| `GET` | `/api/question/<exam_id>/<q_num>` | — | Returns question **without** correct answer |
| `POST` | `/api/answer` | `{ session_id, question_num, answer \| skipped }` | Submits answer, returns result + correct answer |
| `POST` | `/api/finish` | `{ session_id }` | Finalises session, calculates score |

### Results

| Method | Path | Description |
|---|---|---|
| `GET` | `/results/<session_id>` | Full results page for a session |

### Exam Tokens

| Method | Path | Body | Description |
|---|---|---|---|
| `POST` | `/api/redeem_exam_token` | `{ exam_token }` | Validates and redeems an exam token, returns exam/mode/duration |

### Admin

| Method | Path | Body | Description |
|---|---|---|---|
| `POST` | `/api/admin/create_user` | `{ username }` | Creates user, returns `usr-…` token |
| `DELETE` | `/api/admin/delete_user/<id>` | — | Deletes non-admin user |
| `POST` | `/api/admin/reset_token/<id>` | — | Generates new login token |
| `GET` | `/api/admin/stats` | — | User count, completed exams, exam token count |
| `POST` | `/api/admin/create_exam_token` | `{ exam_id, assigned_to?, mode, duration, label? }` | Creates exam token |
| `GET` | `/api/admin/exam_tokens` | — | Lists all exam tokens |
| `DELETE` | `/api/admin/delete_exam_token/<id>` | — | Deletes exam token |
| `GET` | `/api/admin/all_results` | — | All sessions for all users |

---

## Exam Modes

### 🧪 Practice Mode
- Feedback is shown **immediately** after each answer: correct/incorrect highlight, explanation, key takeaway.
- Navigator buttons turn **green** (correct) or **red** (incorrect).
- Progress bar shows `✅ X ❌ Y ⏭ Z`.
- Ideal for self-study and learning the material.

### 📝 Exam Mode
- **No feedback** is given until the exam is finished.
- Submitted options are dimmed (purple highlight = "answered") but not marked right/wrong.
- Navigator buttons show only "answered" vs "skipped" vs "unanswered".
- Progress bar shows only `📝 X answered`.
- All correct answers and explanations appear on the **Results** page after finishing.
- Simulates real exam conditions.

---

## Timer

- Displayed in the navbar as `⏱ MM:SS` (or `H:MM:SS` for durations ≥ 1 hour).
- **Last 5 minutes**: turns orange and pulses.
- **Expired**: turns red, auto-skips all unanswered questions and redirects to the Results page.
- The remaining time is computed server-side on page load (`started_at` vs `utcnow()`), so **refreshing the page does not reset the clock**.
- Default duration: **60 minutes** (configurable via the dashboard selector or exam token).

---

## Exam Tokens

Exam tokens (`et-…`) let an admin pre-configure an exam attempt and share a single token with a candidate.

### Admin workflow
1. Open **Admin Panel → 🎟️ Create Exam Token**.
2. Select the exam, optionally assign to a specific user, choose mode and duration.
3. Copy the generated `et-…` token and share it with the candidate (e.g. by email).

### Candidate workflow
1. Log in with the personal `usr-…` login token.
2. On the Dashboard, paste the `et-…` token in **"Enter Exam Token"** and click **▶ Start Exam**.
3. The exam launches immediately with the admin-configured mode and timer.

### Rules
- If the token is assigned to a specific user, only that user can redeem it.
- An unassigned token can be redeemed by any authenticated user.
- Once redeemed, the token is locked to that user — it cannot be used by someone else.
- The candidate can resume an in-progress session normally (the token is not consumed again).

---

## Adding More Exams

1. Create a new file, e.g. `exam4_questions.py`, with a dict named `exam4` following the same structure as `exam2_questions.py`.
2. In `questions.py`, import it and add it to the `EXAMS` dict:

```python
from exam4_questions import exam4

EXAMS = {
    2: _build(exam2, 2),
    3: _build(exam3, 3),
    4: _build(exam4, 4),   # ← add this
}
```

3. Restart the server — the new exam appears automatically on the dashboard.

---

## Question Format

Each question dict supports the following keys:

| Key | Required | Description |
|---|---|---|
| `question` | ✅ | Full question text |
| `type` | ✅ | `multiple_choice`, `multi_select`, `true_false`, `open` |
| `correct_answer` | ✅ | String or list of strings |
| `all_options` | — | Dict of `{ "A": "option text", … }` for MC questions |
| `domain` | — | Domain name (e.g. `"Infrastructure as Code Concepts"`) |
| `objective` | — | Specific objective within the domain |
| `explanation` | — | Why the answer is correct |
| `key_takeaway` | — | One-line summary for revision |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, Flask 3.x |
| Database | SQLite (stdlib `sqlite3`) |
| Frontend | Vanilla JS, Jinja2 templates |
| Styling | Custom CSS (dark theme, CSS variables) |
| Auth | Hex token in server-side session cookie |
