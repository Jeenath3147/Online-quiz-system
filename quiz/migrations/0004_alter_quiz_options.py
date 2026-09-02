from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_assign_orphan_questions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quiz',
            options={'ordering': ['title'], 'verbose_name_plural': 'Quizzes'},
        ),
    ]
