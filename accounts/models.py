from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(UserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


def profile_picture_path(instance, filename):
    return f"user_{instance.id}/{filename}"


class CustomUser(AbstractUser):
    username = models.CharField(_("username"), max_length=150,)
    email = models.EmailField(verbose_name=_("Email Address"), unique=True)
    phone_number = PhoneNumberField(verbose_name=_("Phone Number"),  blank=True)
    profile_picture = models.ImageField(verbose_name=_('Profile Picture'), upload_to=profile_picture_path,
                                        default="sutdent-prof.png")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    @property
    def is_teacher(self):
        return hasattr(self, "teacher")


class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name=_("User"))
    bio = models.TextField(verbose_name=_("Bio"))
    instagram = models.URLField(null=True, blank=True, verbose_name=_("Instagram"))
    telegram = models.URLField(null=True, blank=True, verbose_name=_("telegram"))
    linkedin = models.URLField(null=True, blank=True, verbose_name=_("linkedin"))
    github = models.URLField(null=True, blank=True, verbose_name=_("github"))

    class Meta:
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")