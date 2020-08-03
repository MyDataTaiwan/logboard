from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from apps.users.models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ("id", "username", "email", "created_at")
    readonly_fields = ("id",)


admin.site.register(CustomUser, CustomUserAdmin)
