from tempfile import template
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("password-set/", views.SetPasswordView.as_view(), name="password-set"),
    path("forgot-password/", 
         auth_views.PasswordResetView.as_view(template_name = "forgot-password.html"),
         name="forgot-password"),
    path("reset-password-done/", 
         auth_views.PasswordResetDoneView.as_view(template_name = "reset-password-done.html"), 
         name="password_reset_done"),  
    path("reset-password/<uidb64>/<token>/",
         views.ResetPasswordConfirmView.as_view(),
         name="password_reset_confirm"),  
]
