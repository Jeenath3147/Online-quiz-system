from django.contrib import admin
from .models import Question, Choice, Quiz


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2   # show 2 empty choice fields by default


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('question_text', 'quiz')
    list_filter = ('quiz',)


class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_limit_minutes', 'created_at')


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
