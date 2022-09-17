from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetConfirmView
from allauth.account.views import LoginView, SignupView
from django.urls import reverse_lazy
from allauth.account.views import ConfirmEmailView
from allauth.account.models import EmailAddress
from allauth.account import app_settings
from .forms import CustomUserUpdateForm, TeacherUpdateFrom
from .decorators import teacher_login_required
from .models import Teacher
from blog.models import Post
User = get_user_model()


class ResetPasswordConfirmView(PasswordResetConfirmView):
    template_name = "account/reset-password.html"
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
def edit_user_panel(request):
    if request.method == "POST":
        form = CustomUserUpdateForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return render(request, "account/edit-teacher-info.html", context={"form": form})
        else:
            return render(request, "account/edit-teacher-info.html", context={"form": form})
    else:
        form = CustomUserUpdateForm(instance=request.user)
        return render(request, "account/edit-teacher-info.html", context={"form": form})


@login_required(login_url=reverse_lazy("login"))   
def user_panel(request):
    return render(request, "account/user-panel.html") 


@teacher_login_required
def teacher_panel(request):
    posts = Post.objects.filter(author=request.user).order_by("publish")
    return render(request, "account/teacher-panel.html", context={"posts": posts})


def teacher_info(request, user_id):
    author = get_object_or_404(klass=User, id=user_id)
    posts = Post.published.filter(author=author)
    return render(request, "account/teacher-info.html", context={"posts": posts, "user": author})


@teacher_login_required
def edit_teacher_panel(request):
    user_form = CustomUserUpdateForm(instance=request.user)
    teacher_form = TeacherUpdateFrom(instance=request.user.teacher)
    context = {
        "user_form": user_form,
        "teacher_form": teacher_form
    }
    if request.method == "POST":
        user_form = CustomUserUpdateForm(data=request.POST, files=request.FILES, instance=request.user)
        teacher_form = TeacherUpdateFrom(data=request.POST, instance=request.user.teacher)
        if all([user_form.is_valid(), teacher_form.is_valid()]):
            user_form.save()
            teacher_form.save()
            return render(request, "account\edit-teacher-info.html", context=context)
        else:
            return render(request, "account\edit-teacher-info.html", context={"user_form": user_form,
                                                                            "teacher_form": teacher_form})
    else:
        return render(request, "account\edit-teacher-info.html", context=context)


class EmailConfirmationView(ConfirmEmailView):
    def post(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        email_adress = confirmation.email_address
        print(email_adress)
        print(len(EmailAddress.objects.filter(user=email_adress.user)), EmailAddress.objects.filter(user=email_adress.user))
        if len(EmailAddress.objects.filter(user=email_adress.user)) >= 2:
            EmailAddress.objects.filter(user=email_adress.user)[0].delete()
        confirmation.confirm(self.request)

        # In the event someone clicks on an email confirmation link
        # for one account while logged into another account,
        # logout of the currently logged in account.
        if (
            self.request.user.is_authenticated
            and self.request.user.pk != confirmation.email_address.user_id
        ):
            self.logout()

        if app_settings.LOGIN_ON_EMAIL_CONFIRMATION:
            resp = self.login_on_confirm(confirmation)
            if resp is not None:
                return resp
        # Don't -- allauth doesn't touch is_active so that sys admin can
        # use it to block users et al
        #
        # user = confirmation.email_address.user
        # user.is_active = True
        # user.save()
        redirect_url = self.get_redirect_url()
        if not redirect_url:
            ctx = self.get_context_data()
            return self.render_to_response(ctx)
        return redirect(redirect_url)