from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    id = models.CharField(
        max_length=150, primary_key=True, default=uuid4, editable=False
    )
    email = models.EmailField(_("email address"))
    username = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "id"
    REQUIRED_FIELDS = ["email", "username", "password"]

    objects = CustomUserManager()

    def __str__(self):
        return self.username
