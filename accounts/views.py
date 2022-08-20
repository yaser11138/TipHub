from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetConfirmView
from allauth.account.views import PasswordSetView,sensitive_post_parameters_m
from allauth.account.views import LoginView, SignupView
from django.urls import reverse_lazy, reverse
from .forms import CustomUserUpdate
User = get_user_model()


class SetPasswordView(PasswordSetView):
    template_name = "set-password.html"
    success_url = reverse_lazy("homepage")
    
    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.has_usable_password():
            return HttpResponseRedirect(reverse("homepage"))
        return super(PasswordSetView, self).dispatch(request, *args, **kwargs)

class ResetPasswordConfirmView(PasswordResetConfirmView):
    template_name = "reset-password.html"
    success_url = reverse_lazy("login")


class CustomSignupView(SignupView):
    success_url = reverse_lazy("login")
    template_name = "account/signup.html"
    
        
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
        form = CustomUserUpdate(data=request.POST,files=request.FILES, instance=user)
        print(request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return render(request, "edit-user-panel.html", context={"form": form})
        else:
            return render(request, "edit-user-panel.html", context={"form": form})  
    else:
        form = CustomUserUpdate(instance = user)        
        return render(request, "edit-user-panel.html", context={"form": form})    


@login_required(login_url=reverse_lazy("login"))   
def user_panel(request):
    return render(request, "user-panel.html") 
    