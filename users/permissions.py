from rest_framework.permissions import BasePermission
from .models import User


class IsUserOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj