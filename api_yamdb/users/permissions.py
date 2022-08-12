from rest_framework.permissions import BasePermission


class AdminOnly(BasePermission):
    def has_permission(self, request, view):
        
        return (
            request.user.is_authenticated and request.user.role == 'admin'
        )
