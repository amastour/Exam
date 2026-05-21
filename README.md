# 🏗️ Terraform Exam – TA-004 Practice Platform

A self-hosted web application to practise for the **HashiCorp Certified Terraform Associate (TA-004)** exam.  
Users log in with a token, take timed exams in **Practice** or **Exam** mode, and see detailed results broken down by objective domain.  
Admins manage users, generate exam tokens, build custom quizzes, and monitor every candidate's progress across a three-page admin panel.

---

## Table of Contents

1. [Features](#features)
2. [Project Structure](#project-structure)
3. [Quick Start](#quick-start)
4. [Configuration](#configuration)
5. [Database (Firestore)](#database-firestore)
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
| Built-in exams | Exam #2 and Exam #3 (57 questions each, loaded from Python modules) |
| Custom exams | Admin builds custom exams question-by-question or via JSON import |
| Edit questions | Admin can edit any custom question inline in the quiz builder |
| Practice mode | Immediate feedback after each answer (correct/incorrect + explanation) |
| Exam mode | No feedback until the exam is finished |
| Countdown timer | Configurable per session (default 60 min) — auto-submits on expiry |
| Exam tokens | Admin generates a `et-…` token that encodes exam, mode and duration |
| Per-user history | Every session (in-progress and finished) is saved per user |
| Results & metrics | Score card, pass/fail (≥70%), performance breakdown by objective domain |
| Question review | Filterable review of all questions with correct answers and explanations |
| Leaderboard | Top performers ranked by average score across all sessions |
| Three-page admin | Separate pages for analytics, user management and quiz management |
| Dark / Light theme | Bootstrap 5.3.3 + CSS variable theming, persisted in `localStorage` |
| Cloud backend | Google Firestore — no local database file required |

---

## Project Structure

```
terraform_exam/
├── credentials.json                # Google service-account key (do NOT commit)
├── exam2_questions.py              # 57 questions – Exam #2
├── exam3_questions.py              # 57 questions – Exam #3
└── app/
    ├── app.py                      # Flask application & all routes (~770 lines)
    ├── firestore_db.py             # Firestore CRUD helpers
    ├── firestore_client.py         # Firestore connection initialisation
    ├── questions.py                # Question loader & normaliser
    ├── requirements.txt            # Python dependencies
    ├── README.md                   # This file
    ├── static/
    │   └── style.css               # CSS variables, dark/light theme, Bootstrap overrides
    └── templates/
        ├── login.html              # Token login page
        ├── dashboard.html          # Exam list, history, exam-token redemption
        ├── exam.html               # Exam UI (timer, navigator, questions)
        ├── results.html            # Score card, objectives breakdown, question review
        ├── admin.html              # Admin – 📊 Analytics (stats, leaderboard, all results)
        ├── admin_users.html        # Admin – 👥 Users (create/delete users, exam tokens)
        └── admin_quizzes.html      # Admin – 📚 Quizzes (exam builder, import, edit questions)
```

---

## Quick Start

### 1 — Clone & install dependencies

```bash
cd terraform_exam/app
pip install -r requirements.txt
```

> **Recommended:** use a dedicated virtual environment.  
> The project was developed with **pyenv** env `exam` (Python 3.13).

### 2 — Configure Google credentials

Choose **one** of the three methods (evaluated in order at startup):

| Priority | Method | How |
|---|---|---|
| 1 | `GOOGLE_CREDENTIALS_JSON` env var | Set to the full JSON content of the service-account key |
| 2 | `GOOGLE_APPLICATION_CREDENTIALS` env var | Set to the absolute path of `credentials.json` |
| 3 | Application Default Credentials (ADC) | Run `gcloud auth application-default login` |

```bash
# Example — path-based method
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/terraform_exam/credentials.json
```

### 3 — Run the server

```bash
python app.py
```

On the **first run** the Firestore collections are empty.  
An admin user is created automatically:

```
[INIT] Admin created. Token: admin-<hex>
```

Copy that token — you will need it to log in as admin.

### 4 — Open the app

```
http://localhost:8080
```

Paste the admin token on the login page.

---

## Configuration

| Setting | Where | Default |
|---|---|---|
| Flask secret key | `app.py` (generated at startup) | Random hex — changes on each restart |
| Firestore project ID | `firestore_client.py` | `quizz-terraform` |
| Server port | `app.py` → `app.run(port=8080)` | `8080` |
| Default exam duration | Dashboard UI & exam token form | `60` minutes |
| Pass threshold | Hard-coded in templates | `70 %` |

---

## Database (Firestore)

The application uses **Google Firestore** (project `quizz-terraform`) instead of a local SQLite file.  
All helpers live in `firestore_db.py`; the client is initialised once in `firestore_client.py`.

### Collections

| Collection | Description |
|---|---|
| `users` | One document per user: `username`, `token`, `role`, `created_at` |
| `exam_sessions` | One document per attempt: `user_id`, `exam_id`, `started_at`, `finished_at`, `score`, `total`, `status`, `mode`, `duration_minutes` |
| `answers` | Sub-collection under each session: `question_num`, `user_answer`, `is_correct`, `result`, `objective` |
| `exam_tokens` | Pre-configured attempt tokens: `token`, `exam_id`, `assigned_to`, `mode`, `duration_minutes`, `used_by`, `used_at`, `label`, `created_at` |
| `custom_exams` | Admin-created exam metadata: `name`, `description`, `created_at` |
| `custom_questions` | Questions linked to a custom exam: full question fields + `exam_id` reference |

### Key `firestore_db.py` functions

| Function | Purpose |
|---|---|
| `get_user_by_token(token)` | Authenticate a user by token |
| `create_user(username)` | Create user, return `usr-…` token |
| `get_all_sessions()` | Fetch all sessions (admin leaderboard / all-results) |
| `create_custom_exam(name, description)` | Create a custom exam document |
| `add_custom_question(exam_id, …)` | Append a question to a custom exam |
| `get_custom_question_by_id(q_id)` | Fetch a single question for editing |
| `update_custom_question(q_id, …)` | Update an existing question in-place |
| `delete_custom_question(q_id)` | Remove a question document |

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

### Admin – Pages

| Method | Path | Description |
|---|---|---|
| `GET` | `/admin` | Analytics: stats cards, leaderboard, all results |
| `GET` | `/admin/users` | User management: create/delete users, exam tokens |
| `GET` | `/admin/quizzes` | Quiz management: exam builder, JSON import, edit questions |

### Admin – API

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
| `POST` | `/api/admin/create_custom_exam` | `{ name, description }` | Creates a new custom exam |
| `GET` | `/api/admin/custom_exams` | — | Lists all custom exams |
| `DELETE` | `/api/admin/delete_custom_exam/<id>` | — | Deletes a custom exam and its questions |
| `POST` | `/api/admin/add_question` | `{ exam_id, question, type, correct_answer, … }` | Adds a question to a custom exam |
| `GET` | `/api/admin/question/<q_id>` | — | Fetches a single question (for edit pre-fill) |
| `PUT` | `/api/admin/update_question/<q_id>` | `{ question, type, correct_answer, … }` | Updates an existing question |
| `DELETE` | `/api/admin/delete_question/<q_id>` | — | Deletes a question |
| `POST` | `/api/admin/import_questions` | `{ exam_id, questions[] }` | Bulk-imports questions from JSON |

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
1. Open **Admin → 👥 Users → 🎟️ Create Exam Token**.
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

## Admin Panel

The admin panel is split into three focused pages, accessible from the navbar on any admin page:

### 📊 `/admin` — Analytics
- **Stats cards**: total users, completed exams, active exam tokens
- **Leaderboard**: top performers ranked by average score
- **All Results**: every session from every user with score, mode and date

### 👥 `/admin/users` — User Management
- **Create User**: enter a username → receive a `usr-…` token to share
- **Users Table**: list all users, copy token, reset token, delete user
- **Create Exam Token**: configure exam, mode, duration and optional assignment → receive `et-…` token
- **Exam Tokens Table**: list all tokens with status (unused / redeemed by whom)

### 📚 `/admin/quizzes` — Quiz Management
- **Exam Builder**: create a custom exam (name + description)
- **Question Editor**: add questions one-by-one with type, options, correct answer, domain, explanation and key takeaway
- **Edit Questions**: click ✏️ on any question row — form pre-fills via `GET /api/admin/question/<id>`, saves via `PUT /api/admin/update_question/<id>`
- **Import JSON**: paste a JSON array of questions to bulk-import into any custom exam
- **Custom Exams Table**: manage custom exams and their question lists

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
