from rest_framework.permissions import BasePermission, SAFE_METHODS


class AdminOrRead(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            and (user.is_admin or user.is_superuser)
            or request.method in SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            user.is_authenticated
            and (user.is_admin or user.is_superuser)
            or request.method in SAFE_METHODS
        )


class ModerOrRead(AdminOrRead):

    def has_permission(self, request, view):
        user = request.user
        return (
            super().has_permission(request, view)
            or user.is_authenticated and user.is_moderator
            or request.method in SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            super().has_object_permission(request, view, obj)
            or user.is_authenticated and user.is_moderator
        )


class OwnerOrRead(ModerOrRead):
    def has_permission(self, request, view):
        user = request.user
        return (
            super().has_permission(request, view)
            or user.is_authenticated and user.is_user
            or request.method in SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            super().has_object_permission(request, view, obj)
            or obj.author == user or request.method in SAFE_METHODS
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
