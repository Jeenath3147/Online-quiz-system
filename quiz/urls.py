from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

urlpatterns = [
    path('', views.home, name='quiz-home'),
    path('take/<int:quiz_id>/', views.quiz, name='take-quiz'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='quiz/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('bulk-add/', views.bulk_add, name='bulk-add'),

    path('manage-quizzes/', views.manage_quizzes, name='manage-quizzes'),
    path('manage-quizzes/<int:quiz_id>/edit/', views.edit_quiz, name='edit-quiz'),
    path('manage-quizzes/<int:quiz_id>/delete/', views.delete_quiz, name='delete-quiz'),

    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='quiz/password_reset_form.html',
            email_template_name='quiz/password_reset_email.html',
            subject_template_name='quiz/password_reset_subject.txt',
            success_url=reverse_lazy('password_reset_done'),
        ),
        name='password_reset',
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='quiz/password_reset_done.html'),
        name='password_reset_done',
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='quiz/password_reset_confirm.html',
            success_url=reverse_lazy('password_reset_complete'),
        ),
        name='password_reset_confirm',
    ),
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='quiz/password_reset_complete.html'),
        name='password_reset_complete',
    ),
]
