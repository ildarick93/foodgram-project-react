from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return (request.user
                and request.user.is_authenticated
                and request.user.is_superuser)


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user
                and request.user.is_authenticated
                and request.user.is_active
                and request.user.is_admin)

    def has_object_permission(self, request, view, obj):
        return (request.user
                and request.user.is_authenticated
                and request.user.is_active
                and request.user.is_admin)


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.user
                and request.user.is_authenticated
                and obj.author == request.user)
