from rest_framework.permissions import BasePermission


class IsAdminRole(BasePermission):
    """Only users with role='admin' are allowed."""
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_admin_role
        )


class IsStaffOrAdmin(BasePermission):
    """Both staff and admin users are allowed."""
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
        )