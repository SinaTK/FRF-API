from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerorReadonly(BasePermission):
    message = 'Permission denied'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.user
    

class AdminOrOwnerOrReadOnly(BasePermission):
    message = 'Permission denied'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            if request.user == obj or request.user.is_superuser:
                return True
            return False
