from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    list_display = ["email", "role", "first_name", "last_name"]
    list_filter = [
        "is_staff",
        "is_superuser",
        "is_active",
    ]
    search_fields = ["email"]
    readonly_fields = [
        "date_joined",
        "last_login",
    ]
    ordering = [
        "email",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": ("email", "password", "role", ("first_name", "last_name")),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "role",
                ),
            },
        ),
    )


# Groups aren't used, access is controlled by User.role.
admin.site.unregister(Group)
