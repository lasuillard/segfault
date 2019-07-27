from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS)


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user == obj.user)
