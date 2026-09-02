"""
Shared parsing logic for adding many quiz questions at once — used by both
the "Bulk Add" web page and the `load_questions` management command, so
pasted text and an uploaded file behave exactly the same way.

Expected format: one blank line between questions. The first line of a
block is the question text; every line after it is an answer choice.
Put a '*' at the start of the one correct choice.

Example:

    What does CSS stand for?
    *Cascading Style Sheets
    Creative Style System
    Computer Styled Sections

    Which HTTP method is used to submit a form that changes server data?
    GET
    *POST
    LINK
"""

import re


def parse_questions(text):
    """
    Returns (questions, errors).

    `questions` is a list of dicts:
        {"question_text": str, "choices": [{"text": str, "is_correct": bool}, ...]}

    `errors` is a list of human-readable strings. If errors is non-empty,
    `questions` should NOT be saved — the caller should show the errors and
    let the user fix their input instead of saving a partial batch.
    """
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    blocks = [b for b in re.split(r'\n\s*\n', text.strip()) if b.strip()]

    questions = []
    errors = []

    if not blocks:
        errors.append("No questions found. Paste at least one question block.")
        return questions, errors

    for i, block in enumerate(blocks, start=1):
        lines = [line.strip() for line in block.splitlines() if line.strip()]

        if len(lines) < 3:
            errors.append(
                f"Question {i}: needs a question line plus at least 2 choices "
                f"(found {max(len(lines) - 1, 0)} choice line(s))."
            )
            continue

        question_text = lines[0]
        choice_lines = lines[1:]

        correct_indexes = [idx for idx, line in enumerate(choice_lines) if line.startswith('*')]

        if len(correct_indexes) == 0:
            errors.append(
                f"Question {i} (\"{question_text}\"): no choice is marked correct. "
                f"Put a '*' at the start of the correct answer's line."
            )
            continue
        if len(correct_indexes) > 1:
            errors.append(
                f"Question {i} (\"{question_text}\"): more than one choice is marked "
                f"correct. Only one line should start with '*'."
            )
            continue

        choices = []
        for idx, line in enumerate(choice_lines):
            is_correct = idx == correct_indexes[0]
            choice_text = line[1:].strip() if is_correct else line
            if not choice_text:
                errors.append(f"Question {i} (\"{question_text}\"): one of the choices is empty.")
                break
            choices.append({"text": choice_text, "is_correct": is_correct})
        else:
            questions.append({"question_text": question_text, "choices": choices})

    return questions, errors


def save_questions(questions, quiz):
    """Saves parsed questions under the given Quiz. Call only after confirming no errors."""
    from .models import Question, Choice

    created = 0
    for q in questions:
        question = Question.objects.create(quiz=quiz, question_text=q["question_text"])
        for choice in q["choices"]:
            Choice.objects.create(
                question=question,
                option_text=choice["text"],
                is_correct=choice["is_correct"],
            )
        created += 1
    return created
