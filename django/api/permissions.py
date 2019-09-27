from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, User):
            return bool(request.user == obj)

        return bool(request.user == obj.user)


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user == obj.user)


class IsRelatedUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        try:
            return bool(obj.users.get(pk=request.user.pk))
        except User.DoesNotExist:
            return False
