# 🎓 Online Quiz System

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-Framework-092E20?logo=django&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

A web-based quiz application built with **Django**. Users can register, log in, take timed quizzes, and instantly see their score with a full answer review. Staff members get a dedicated page to manage quizzes and can bulk-upload questions.

**🔗 Live demo:** [jeenath3147.pythonanywhere.com](https://jeenath3147.pythonanywhere.com)

> 💡 *Add a screenshot or GIF of the app below — this is the single biggest thing left that would make this README stand out even more.*

<!-- ![App Screenshot](docs/screenshot.png) -->

---

## 📑 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Setup](#-setup)
- [Email / Password Reset](#-email--password-reset)
- [Bulk-Adding Questions](#-bulk-adding-questions)
- [Project Structure](#-project-structure)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

- **User accounts** — sign up, log in, log out, and "Forgot password" recovery via email
- **Multiple named quizzes** to choose from
- **Timed quizzes** with a live countdown and automatic submission when time runs out
- **Instant scoring** after submission, with a full review of correct vs. selected answers
- **Bulk-adding questions** from a simple text format (staff only)
- **"Manage Quizzes" page** for staff to create/edit/delete quizzes
- **Paginated home page** for browsing quizzes

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python / Django |
| Database | SQLite (default) |
| Frontend scripting | Vanilla JavaScript (quiz timer / auto-submit) |
| Styling | Plain CSS |

## 🚀 Setup

1. **Create and activate a virtual environment:**
   ```bash
   python -m venv myenv1
   myenv1\Scripts\activate      # Windows
   source myenv1/bin/activate   # macOS/Linux
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Copy `.env.example` to `.env`** and fill in the values (a random `SECRET_KEY`, and optionally Gmail credentials for real password-reset emails — see below):
   ```bash
   copy .env.example .env   # Windows
   cp .env.example .env     # macOS/Linux
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create an admin (staff) account:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

## 📧 Email / Password Reset

If `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` are left blank in `.env`, password-reset emails are simply printed to the terminal instead of being sent — useful for local development. To send real emails, fill in a Gmail address and a Gmail **"App Password"** (not your normal Gmail password) in `.env`.

## 📥 Bulk-Adding Questions

Staff can add many questions to a quiz at once, either through the **"Bulk Add"** page in the nav bar or with the `load_questions` management command:

```bash
python manage.py load_questions your_file.txt --quiz "Quiz Name"
```

(`--quiz` must exactly match the name of an existing quiz — create the quiz first through "Manage Quizzes", then load its questions in.)

Both use the same plain-text format:

```
What does CSS stand for?
*Cascading Style Sheets
Creative Style System
Computer Styled Sections
```

One blank line between questions. The first line is the question text, every line after it is an answer choice, and a `*` at the start of a line marks that choice as correct.

## 📂 Project Structure

```
onlinequiz/
├── manage.py
├── requirements.txt
├── .env.example
├── onlinequiz/   # project settings, URLs
└── quiz/         # the quiz app (models, views, templates)
```

## 🗺 Roadmap

- [x] Deploy a live demo
- [ ] Add automated tests
- [ ] Add per-category quiz filtering
- [ ] Add a leaderboard

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to check the [issues page](../../issues) or open a pull request.

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
