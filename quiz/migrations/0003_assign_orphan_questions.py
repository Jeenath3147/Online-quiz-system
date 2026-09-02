from django.db import migrations


def assign_orphan_questions(apps, schema_editor):
    """
    Any question that existed before quizzes were introduced has no quiz yet.
    Group all of those together into one quiz called "General Knowledge Quiz"
    so nothing already added disappears from the site.
    """
    Quiz = apps.get_model('quiz', 'Quiz')
    Question = apps.get_model('quiz', 'Question')

    orphans = Question.objects.filter(quiz__isnull=True)
    if orphans.exists():
        default_quiz, _ = Quiz.objects.get_or_create(title='General Knowledge Quiz')
        orphans.update(quiz=default_quiz)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_quiz_question_quiz'),
    ]

    operations = [
        migrations.RunPython(assign_orphan_questions, noop_reverse),
    ]
