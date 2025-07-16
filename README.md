Django REST framework Ext
=========================

Some extensions of Django REST framework.

# Pagination

## DynamicSizePageNumberPagination

Support setting `PAGE_QUERY_PARAM` (default is `page`) parameter to specify the page size for querying.

Return all data when the `PAGE_QUERY_PARAM` (default is `limit`) parameter is not specified.

Usage:

```
REST_FRAMEWORK = {
    ...
    'DEFAULT_PAGINATION_CLASS': 'rest_framework_ext.pagination.DynamicSizePageNumberPagination',
    ...
}

REST_FRAMEWORK_EXT = {
    'PAGE_QUERY_PARAM': 'page',  # Default is page (If not set)
    'PAGE_SIZE_QUERY_PARAM': 'limit',
}
```

Request:

```
GET https://api.example.org/accounts/?page=4&limit=100
```

If no limit is specified, all data will be returned regardless of the page number.

```
GET https://api.example.org/accounts/
GET https://api.example.org/accounts/?page=4
```

# Permissions

## DjangoModelPermissions

Add `view` permission control.

Usage:

```
from rest_framework_ext.permissions import DjangoModelPermissions

class MyModelViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissions]
```

Or use globally in `settings.py`:

```
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'djangorestframework_ext.permissions.DjangoModelPermissions',
    ),
}
```

## ReadOnly

Requests will only be permitted if the request method is one of the "safe" methods (`GET`, `HEAD` or `OPTIONS`).

Usage:

```
from rest_framework_ext.permissions import ReadOnly
```

## IsSuperuser

Determine whether the request user is superuser.

Usage:

```
from rest_framework_ext.permissions import IsSuperuser
```

## HasPermission

Mainly used for providing permission validation to `@api_view`.

```
from rest_framework_ext.permissions import HasPermission


@api_view(['GET'])
@permission_classes([HasPermission('user.change_user')])
def change_user(request):
    ...
```

# Serializers

## RecursiveSerializer

Usage:

models.py:

```
from django.db import models


class Department(models.Model):
    name = models.CharField('Name', max_length=100)
    parent = models.ForeignKey('self', related_name='children', verbose_name='Parent')
```

serializers.py:

```
from rest_framework import serializers
from rest_framework_ext.serializers import RecursiveSerializer


class DepartmentTreeListSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)

    class Meta:
        model = Department
        fields = '__all__'
```

Response:

```
[{
    "id": 1,
    "children": [{
        "id": 2,
        "children": [{
            "id": 3,
            "children": [{
                "id": 4,
                "children": [],
                "name": "aaa",
                "parent": 3
            }],
            "name": "ddd",
            "parent": 2
        }, {
            "id": 5,
            "children": [{
                "id": 6,
                "children": [],
                "name": "eee",
                "parent": 7
            }],
            "name": "xxx",
            "parent": 2
        }],
        "name": "yyy",
        "parent": 1
    }],
    "name": "zzz",
    "parent": null
}]
```

## DynamicFieldsModelSerializer

It's copied from [official document](https://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields).

Use `fields` to specify the fields to be used by a serializer at the point of initializing it.

Or use `exclude` to specify the fields to be excluded by a serializer at the point of initializing it.

Usage:

models.py:

```
from django.db import models


class Parent(models.Model):
    name = models.CharField('name', max_length=100)


class Child(models.Model):
    name = models.CharField('name', max_length=100)
    parent = models.ForeignKey(Parent, verbose_name='parent')
```

serializer.py:

```
from rest_framework import serializers
from rest_framework_ext.serializers import DynamicFieldsModelSerializer


class ChildSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'


class ParentSerializer(serializers.ModelSerializer):
    children = ChildSerializer(many=True, read_only=True, exclude=['parent'])
```

# Mixins

## MultipleFieldLookupMixin

From [Creating custom mixins](https://www.django-rest-framework.org/api-guide/generic-views/#creating-custom-mixins) and [Multiple lookup_fields for django rest framework](https://stackoverflow.com/questions/38461366/multiple-lookup-fields-for-django-rest-framework).

Used for Multiple field lookup.

Usage:

views.py:

```
from rest_framework import viewsets
from rest_framework_ext.mixins import MultipleFieldLookupMixin


class ExampleViewSet(MultipleFieldLookupMixin, viewsets.ModelViewSet):
    lookup_fields = ['pk', 'field_one', 'field_two']
```

urls.py:

```
from django.urls import path
from . import views


urlpatterns = [
    path(r'examples/<str:field_one>/<str:field_two>/', views.ExampleViewSet.as_view({'get': 'retrieve'}))
]
```

## DisableActionsMixin

Batch disable actions for viewset.

Usage:

```
from rest_framework import viewsets
from rest_framework_ext.mixins import DisableActionsMixin


class ExampleViewSet(DisableActionsMixin, viewsets.ModelViewSet):
    disabled_actions = ['retrieve', 'update', 'custom_action']
```

# Utils

## get_default_query_params

Get default query params.

# Views

## exception_handler

Some exception handlers.

Usage: 

```
REST_FRAMEWORK = {
    ...
    'EXCEPTION_HANDLER': 'rest_framework_ext.views.exception_handler',
    ...
}
```

# Validators

## ActiveValidator

Validate whether the corresponding object is active using the specified key (default is `is_active`) and value (default is `True`).

Usage:

```
from rest_framework import serializers
from rest_framework_ext.validators import ActiveValidator


class MySerializer(serializers.ModelSerializer):
    relation = serializers.PrimaryKeyRelatedField(queryset=Relation.objects.all(), validators=[ActiveValidator()])
```
