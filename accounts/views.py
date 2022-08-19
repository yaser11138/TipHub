import imp
from operator import ge
from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as django_logout, login as django_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordResetConfirmView
from allauth.account.views import PasswordSetView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomUserUpdate
User = get_user_model()
from allauth.account.views import LoginView

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
    
        
class CustomLoginView(LoginView):
    success_url = reverse_lazy("homepage")
    
@login_required(login_url=reverse_lazy("login"))    
def logout(request):
    django_logout(request)
    return redirect("homepage")


@login_required(login_url=reverse_lazy("login"))      
def edit_user_panel(request, user_id):
    user = get_object_or_404(klass=User, id=user_id) 
    if request.method == "POST":
        form = CustomUserUpdate(data=request.POST, instance=user)
        if form.is_valid():
            x=form.save()
            print(x.username)
            return render(request, "edit-user-panel.html", context={"form": form})
        else:
            return render(request, "edit-user-panel.html", context={"form": form})  
    else:
        form = CustomUserUpdate(instance = user)        
        return render(request, "edit-user-panel.html", context={"form": form})    


@login_required(login_url=reverse_lazy("login"))   
def user_panel(request):
    return render(request, "user-panel.html") 
    