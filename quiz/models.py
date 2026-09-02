from django.db import models


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    time_limit_minutes = models.PositiveIntegerField(
        default=10,
        help_text="How many minutes a user gets to finish this quiz."
    )

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE, null=True, blank=True)
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    option_text = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text
