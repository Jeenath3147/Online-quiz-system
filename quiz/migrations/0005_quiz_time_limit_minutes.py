from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_alter_quiz_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='time_limit_minutes',
            field=models.PositiveIntegerField(
                default=10,
                help_text='How many minutes a user gets to finish this quiz.',
            ),
        ),
    ]
