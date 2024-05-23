from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    bsn = models.CharField(_("Citizen service number"), unique=True, max_length=9, validators=(MinLengthValidator(9),))
