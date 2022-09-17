from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path("signup/", views.CustomSignupView.as_view(), name="register"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.logout, name="logout"),
    path("user-panel/edit", views.edit_user_panel, name="edit-user-panel"),
    path("teacher/info/<int:user_id>/", views.teacher_info, name="teacher-info"),
    path("teacher/panel/", views.teacher_panel, name="teacher-panel"),
    path("teacher/panel/edit/", views.edit_teacher_panel, name="edit-teacher-panel"),
    path("confirm-email/<key>/", views.EmailConfirmationView.as_view(), name="account_confirm_email",),
    path("user-panel/", views.user_panel, name="user-panel"),
    path("forgot-password/", 
         auth_views.PasswordResetView.as_view(template_name="forgot-password.html"),
         name="forgot-password"),
    path("reset-password-done/", 
         auth_views.PasswordResetDoneView.as_view(template_name = "reset-password-done.html"), 
         name="password_reset_done"),  
    path("reset-password/<uidb64>/<token>/",
         views.ResetPasswordConfirmView.as_view(),
         name="password_reset_confirm"),  
]
