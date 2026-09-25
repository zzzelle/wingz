from rest_framework import permissions


class AdminRoleOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and hasattr(request.user, "role")
            and request.user.role == "admin"
        )
