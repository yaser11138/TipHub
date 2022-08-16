from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout as django_logout, login as django_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetConfirmView
from .forms import CustomUserCreationForm
from allauth.account.views import PasswordSetView


class SetPasswordView(PasswordSetView):
    template_name = "set-password.html"
    success_url = reverse_lazy("homepage")

class ResetPasswordConfirmView(PasswordResetConfirmView):
    template_name = "reset-password.html"
    success_url = reverse_lazy("login")


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("homepage")
        else:
            return render(request, "register.html", context={"form":form})
    else:
        form = CustomUserCreationForm()
        return render(request, "register.html", context={"form": form})
    
        
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            django_login(request, form.get_user())
            return redirect("homepage")
        else:
            return render(request, "login.html", context={"form": form})
    else:
        form = AuthenticationForm()
        return render(request, "login.html", context={"form": form})

    
@login_required(redirect_field_name=reverse_lazy("login"))    
def logout(request):
    django_logout(request)
    return redirect("homepage")
    