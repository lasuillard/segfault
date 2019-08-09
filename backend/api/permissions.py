from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(obj.user == request.user)


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user == obj.user)
