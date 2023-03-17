from rest_framework import permissions


class DjangoModelPermissions(permissions.DjangoModelPermissions):
    def __init__(self):
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
        self.perms_map['OPTIONS'] = ['%(app_label)s.view_%(model_name)s']
        self.perms_map['HEAD'] = ['%(app_label)s.view_%(model_name)s']


class IsCurrentUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


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
