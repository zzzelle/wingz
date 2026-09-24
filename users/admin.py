from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from users.models import User


class UserAdmin(BaseUserAdmin, admin.ModelAdmin):
    list_display = [
        "email"
    ]
    list_filter = [
        "is_staff",
        "is_superuser",
        "is_active",
    ]
    search_fields = [
        "email"
    ]
    readonly_fields = [
        "date_joined",
        "last_login",
    ]
    ordering = [
        "email",
    ]

    fieldsets = (
        (None, {"fields": ("email", "password", "role"), }),
        (
            _("Personal info"),
            {
                "fields": (
                    ("first_name", "last_name"),
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', "first_name", "last_name", "role"),
        }),
    )


admin.site.register(User, UserAdmin)
