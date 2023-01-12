from rest_framework.permissions import BasePermission, SAFE_METHODS

class AdminOrRead(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return (user.is_authenticated
                and (user.is_admin or user.is_superuser))

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (user.is_authenticated
                and (user.is_admin or user.is_superuser))


class ModerOrRead(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.is_moderator

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_authenticated and user.is_moderator


class OwnerOrRead(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (user.is_authenticated and user.is_user
                or request.method in SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.author == user or request.method in SAFE_METHODS