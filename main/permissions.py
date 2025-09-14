from rest_framework import permissions


class CustomAdminPermission(permissions.BasePermission):
    """
    - Normal user with `can_create_project`: can create + view.
    - Normal user without permission: read-only.
    - Admin (staff/superuser): full access.
    """

    def has_permission(self, request, view):
        user = request.user

        # Everyone can list/retrieve (view)
        if view.action in ["list", "retrieve"]:
            return True

        # Admins can do everything
        if user.is_staff or user.is_superuser:
            return True

        # Check if user has the custom permission
        if view.action == "create" and user.has_perm("main.can_create_project"):
            return True

        # All other actions (update, delete, approve) → admin only
        return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
