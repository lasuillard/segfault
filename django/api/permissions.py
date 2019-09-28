from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsAdminUser(permissions.IsAdminUser):

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_staff)


class IsOwner(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, User):
            return bool(request.user and request.user == obj)

        return bool(request.user and request.user == obj.user)


class IsOwnerOrReadOnly(permissions.IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user and request.user == obj.user)


class IsRelatedUser(permissions.IsAuthenticated):
    """
    Check is user in object.users ManyToMany field.
    """
    def has_object_permission(self, request, view, obj):
        try:
            return bool(request.user == obj.users.get(pk=request.user.pk))
        except User.DoesNotExist:
            return False
