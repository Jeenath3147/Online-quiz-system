from django.core.management.base import BaseCommand, CommandError

from quiz.bulk_parser import parse_questions, save_questions
from quiz.models import Quiz


class Command(BaseCommand):
    help = (
        "Bulk-load quiz questions from a text file into a named quiz. Same "
        "format as the Bulk Add web page: one blank line between questions, "
        "first line is the question text, remaining lines are choices, and a "
        "'*' at the start of a choice marks it as correct.\n\n"
        "Example usage:\n"
        "  python manage.py load_questions questions.txt --quiz \"Java Basics\"\n\n"
        "If a quiz with that title already exists, the questions are added to "
        "it. Otherwise a brand new quiz is created with that title."
    )

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help="Path to a .txt file of questions.")
        parser.add_argument(
            '--quiz', type=str, required=True,
            help="Title of the quiz these questions belong to (created if it doesn't exist)."
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        quiz_title = options['quiz'].strip()

        if not quiz_title:
            raise CommandError("--quiz cannot be empty.")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except FileNotFoundError:
            raise CommandError(f"File not found: {file_path}")
        except OSError as e:
            raise CommandError(f"Could not read {file_path}: {e}")

        questions, errors = parse_questions(text)

        if errors:
            self.stderr.write(self.style.ERROR("Nothing was saved. Fix these problems and try again:"))
            for error in errors:
                self.stderr.write(self.style.ERROR(f"  - {error}"))
            raise CommandError(f"{len(errors)} problem(s) found in {file_path}")

        quiz_obj = Quiz.objects.filter(title__iexact=quiz_title).first()
        if not quiz_obj:
            quiz_obj = Quiz.objects.create(title=quiz_title)

        added = save_questions(questions, quiz_obj)
        self.stdout.write(self.style.SUCCESS(
            f"Added {added} question(s) to \"{quiz_obj.title}\" from {file_path}."
        ))
