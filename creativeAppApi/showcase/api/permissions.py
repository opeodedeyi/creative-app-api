from rest_framework import permissions


class IsUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return False
        return obj.user == request.user


class IsAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return False
        return request.user.administrators.filter(pk=obj.pk).exists()


class IsAdminOrOwner(permissions.BasePermission):
    '''
    permission for collaborators to delete collaborations
    '''
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return False
        return obj.user == request.user or obj.post.administrator.filter(pk=request.user.pk).exists()