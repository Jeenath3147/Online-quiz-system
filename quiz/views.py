from django import forms
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404

from .bulk_parser import parse_questions, save_questions
from .models import Question, Choice, Quiz


class RegisterForm(UserCreationForm):
    """
    Same as Django's built-in sign-up form, plus an email address. The email
    is required so "Forgot password?" has somewhere to send the reset link.
    """
    email = forms.EmailField(required=True, help_text="Needed if you ever use \"Forgot password?\".")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')


def home(request):
    """
    Public landing page — anyone can see it, no login required. Lists every
    quiz that exists, each as its own card, six per page. Only clicking
    "Start Quiz" (which points at the login-protected `quiz` view) requires
    logging in.
    """
    quizzes_qs = Quiz.objects.annotate(question_count=Count('questions')).order_by('title')
    paginator = Paginator(quizzes_qs, 6)
    quizzes = paginator.get_page(request.GET.get('page'))
    return render(request, 'quiz/home.html', {'quizzes': quizzes})


def register(request):
    if request.user.is_authenticated:
        return redirect('quiz-home')

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log the new user straight in
            return redirect('quiz-home')
    else:
        form = RegisterForm()

    return render(request, 'quiz/register.html', {'form': form})


@login_required(login_url='login')
def quiz(request, quiz_id):
    quiz_obj = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz_obj.questions.all()

    if request.method == "POST":
        score = 0
        review = []
        for q in questions:
            selected_id = request.POST.get(f"q{q.id}")
            selected_choice = q.choice_set.filter(id=selected_id).first() if selected_id else None
            correct_choice = q.choice_set.filter(is_correct=True).first()
            is_correct = bool(selected_choice and selected_choice.is_correct)
            if is_correct:
                score += 1
            review.append({
                'question': q,
                'selected_choice': selected_choice,
                'correct_choice': correct_choice,
                'is_correct': is_correct,
            })
        return render(request, 'quiz/results.html', {
            'score': score,
            'questions_count': questions.count(),
            'quiz_obj': quiz_obj,
            'review': review,
        })

    return render(request, 'quiz/quiz.html', {'questions': questions, 'quiz_obj': quiz_obj})


@staff_member_required(login_url='login')
def bulk_add(request):
    """
    Lets a staff/admin user paste several questions at once instead of
    adding them one-by-one through the Django admin. Every batch must be
    given a quiz heading — typing the title of an existing quiz adds more
    questions to it, and any new title starts a brand new, separate quiz.
    Uses the same parser as the `load_questions` management command, so
    pasted text and an uploaded file follow identical rules.
    """
    added_count = None
    errors = []
    pasted_text = ""
    quiz_title = ""
    saved_quiz_title = None

    if request.method == "POST":
        quiz_title = request.POST.get("quiz_title", "").strip()
        pasted_text = request.POST.get("questions_text", "")

        if not quiz_title:
            errors.append("Please give this batch of questions a quiz heading (e.g. \"Java Basics\").")
            questions = []
        else:
            questions, errors = parse_questions(pasted_text)

        if not errors:
            quiz_obj = Quiz.objects.filter(title__iexact=quiz_title).first()
            if not quiz_obj:
                quiz_obj = Quiz.objects.create(title=quiz_title)

            added_count = save_questions(questions, quiz_obj)
            saved_quiz_title = quiz_obj.title
            pasted_text = ""  # clear the box after a successful save
            quiz_title = ""

    return render(request, 'quiz/bulk_add.html', {
        'added_count': added_count,
        'saved_quiz_title': saved_quiz_title,
        'errors': errors,
        'pasted_text': pasted_text,
        'quiz_title': quiz_title,
    })


@staff_member_required(login_url='login')
def manage_quizzes(request):
    """
    A staff-only page, styled like the rest of the site, for renaming a
    quiz, changing its time limit, or deleting it — without having to use
    the plain Django admin panel.
    """
    quizzes = Quiz.objects.annotate(question_count=Count('questions')).order_by('title')
    return render(request, 'quiz/manage_quizzes.html', {'quizzes': quizzes})


@staff_member_required(login_url='login')
def edit_quiz(request, quiz_id):
    quiz_obj = get_object_or_404(Quiz, pk=quiz_id)
    error = None

    if request.method == "POST":
        new_title = request.POST.get("title", "").strip()
        time_limit_raw = request.POST.get("time_limit_minutes", "").strip()

        if not new_title:
            error = "Quiz heading can't be empty."
        elif not time_limit_raw.isdigit() or int(time_limit_raw) < 1:
            error = "Time limit must be a whole number of minutes, at least 1."
        else:
            quiz_obj.title = new_title
            quiz_obj.time_limit_minutes = int(time_limit_raw)
            quiz_obj.save()
            return redirect('manage-quizzes')

    return render(request, 'quiz/edit_quiz.html', {'quiz_obj': quiz_obj, 'error': error})


@staff_member_required(login_url='login')
def delete_quiz(request, quiz_id):
    quiz_obj = get_object_or_404(Quiz, pk=quiz_id)

    if request.method == "POST":
        quiz_obj.delete()
        return redirect('manage-quizzes')

    return render(request, 'quiz/delete_quiz.html', {'quiz_obj': quiz_obj})
