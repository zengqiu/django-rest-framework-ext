from rest_framework.permissions import BasePermission


class IsCurrentUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class ExportPermission(BasePermission):
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
