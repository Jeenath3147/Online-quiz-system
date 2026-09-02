# Online Quiz System

A web-based quiz application built with Django. Users can register, log in, take timed quizzes, and instantly see their score with a full answer review. Staff members get a dedicated page to manage quizzes and can bulk-upload questions.

## Features

- User accounts: sign up, log in, log out, and "Forgot password" recovery via email
- Multiple named quizzes to choose from
- Timed quizzes with a live countdown and automatic submission when time runs out
- Instant scoring after submission, with a full review of correct vs. selected answers
- Bulk-adding questions from a simple text format (staff only)
- "Manage Quizzes" page for staff to create/edit/delete quizzes
- Paginated home page for browsing quizzes

## Tech stack

- Python / Django
- SQLite (default database)
- Vanilla JavaScript (quiz timer/auto-submit)
- Plain CSS

## Setup

1. Create and activate a virtual environment:
   ```
   python -m venv myenv1
   myenv1\Scripts\activate   (Windows)
   source myenv1/bin/activate   (macOS/Linux)
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in the values (a random `SECRET_KEY`, and optionally Gmail credentials for real password-reset emails — see below):
   ```
   copy .env.example .env   (Windows)
   cp .env.example .env     (macOS/Linux)
   ```
4. Apply database migrations:
   ```
   python manage.py migrate
   ```
5. Create an admin (staff) account:
   ```
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```
   python manage.py runserver
   ```

### Email / password reset

If `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` are left blank in `.env`, password-reset emails are simply printed to the terminal instead of being sent — useful for local development. To send real emails, fill in a Gmail address and a Gmail "App Password" (not your normal Gmail password) in `.env`.

## Bulk-adding questions

Staff can add many questions to a quiz at once, either through the "Bulk Add" page in the nav bar or with the `load_questions` management command:

```
python manage.py load_questions your_file.txt
```

Both use the same plain-text format:

```
What does CSS stand for?
*Cascading Style Sheets
Creative Style System
Computer Styled Sections
```

One blank line between questions. The first line is the question text, every line after it is an answer choice, and a `*` at the start of a line marks that choice as correct.

## Project structure

```
onlinequiz/
├── manage.py
├── requirements.txt
├── .env.example
├── onlinequiz/        # project settings, URLs
└── quiz/               # the quiz app (models, views, templates)
```
