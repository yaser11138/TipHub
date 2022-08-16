import urllib
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import pre_social_login
from django.core.files import File
from allauth.account.utils import perform_login
from django.contrib.auth import get_user_model
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import redirect
from django.conf import settings

User = get_user_model()

@receiver(user_signed_up)
def populate_profile(sender,request,user,sociallogin,**kwargs):
    if sociallogin.account.provider == 'google':
        user_picture_url = user.socialaccount_set.filter(provider='google')[0].extra_data["picture"]
        result = urllib.request.urlretrieve(user_picture_url)
        user.profile_picture.save(f"profile_user_{user.id}.png", File(open(result[0], 'rb')))
        user.save()
    elif sociallogin.account.provider == 'github':
        user_picture_url = user.socialaccount_set.filter(provider='github')[0].extra_data["avatar_url"]
        result = urllib.request.urlretrieve(user_picture_url)
        user.profile_picture.save(f"profile_user_{user.id}.png", File(open(result[0], 'rb')))
        user.save()    
        
@receiver(pre_social_login)
def link_to_local_user(sender, request, sociallogin, **kwargs):
    email_address = sociallogin.account.extra_data['email']
    users = User.objects.filter(email=email_address)
    if users:
        perform_login(request, users[0], email_verification="optinal")
        raise ImmediateHttpResponse(redirect(settings.LOGIN_REDIRECT_URL))    