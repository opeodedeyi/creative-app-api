from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.IsAdminUser):
    '''
    Permission to allow only Admin to edit 
    and create while other users read only
    '''
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in permissions.SAFE_METHODS or is_admin


class IsAuthorOrReadOnly(permissions.BasePermission):
    '''
    Permission to allow object owners to edit 
    while other users read only
    '''
    def has_object_permission(self, request, view, obj):
        if request.methods in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user