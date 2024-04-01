from rest_framework import permissions


class DjangoModelPermissions(permissions.DjangoModelPermissions):
    perms_map = {
        **permissions.DjangoModelPermissions.perms_map,
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s']
    }


class IsCurrentUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


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


class ExportPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'export':
            model = view.get_queryset().model
            kwargs = {
                'app_label': model._meta.app_label,
                'model_name': model._meta.model_name
            }

            return request.user.has_perm('%(app_label)s.export_%(model_name)s' % kwargs)
        else:
            return False
