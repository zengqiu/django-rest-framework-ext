from rest_framework import permissions


class DjangoModelPermissions(permissions.DjangoModelPermissions):
    def __init__(self):
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
        self.perms_map['OPTIONS'] = ['%(app_label)s.view_%(model_name)s']
        self.perms_map['HEAD'] = ['%(app_label)s.view_%(model_name)s']


class IsCurrentUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user
