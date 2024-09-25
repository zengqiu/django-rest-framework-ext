from rest_framework import permissions


class DjangoModelPermissions(permissions.DjangoModelPermissions):
    perms_map = {
        **permissions.DjangoModelPermissions.perms_map,
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s']
    }


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class HasPermission(permissions.BasePermission):
    permission_codename = ''

    def __init__(self, permission_codename):
        super().__init__()
        self.permission_codename = permission_codename

    def __call__(self):
        return self

    def has_permission(self, request, view):
        return request.user.has_perm(self.permission_codename)
