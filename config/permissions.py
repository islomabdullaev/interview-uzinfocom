from rest_framework import permissions

from users.choices import UserRoleType


class IsAdminOrOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        if (request.user.role == UserRoleType.admin.value or
            request.user.role == UserRoleType.owner.value):
            return True

        return False


class IsAdminOrClient(permissions.BasePermission):

    def has_permission(self, request, view):
        if (request.user.role == UserRoleType.client.value or
            request.user.role == UserRoleType.admin.value):

            return True

        return False