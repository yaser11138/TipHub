from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout as django_logout, login as django_login
from django.contrib.auth.views import PasswordResetView
from .forms import CustomUserCreationForm


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
    
    
def logout(request):
    django_logout(request)
    return redirect("homepage")
    