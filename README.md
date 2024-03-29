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
    'DEFAULT_PAGINATION_CLASS': 'djangorestframework_ext.pagination.DynamicSizePageNumberPagination',
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

# Permissions

## IsCurrentUser

Determine whether the object is the current login user.

Usage:

```
from djangorestframework_ext.permissions import IsCurrentUser
```

## IsSuperuser

Determine whether the request user is superuser.

Usage:

```
from djangorestframework_ext.permissions import IsSuperuser
```

## HasPermission

Mainly used for providing permission validation to `@api_view`.

```
@api_view(['GET'])
@permission_classes([HasPermission('user.change_user')])
def change_user(request):
    ...
```

# Serializers

## RecursiveSerializer

Usage:

```
from rest_framework import serializers
from djangorestframework_ext.serializers import RecursiveSerializer
from django.db import models


class Department(models.Model):
    name = models.CharField('Name', max_length=100)
    parent = models.ForeignKey('self', related_name='children', verbose_name='Parent')


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

## ExportModelSerializer

Use verbose name or label replace field name.

Usage:

```
from djangorestframework_ext.serializers import ExportModelSerializer
from django.db import models


class Department(models.Model):
    name = models.CharField('Name', max_length=100)
    creator = models.ForeignKey(User, null=False, verbose_name='Creator')


class DepartmentExportSerializer(ExportModelSerializer):
    creator = serializers.StringRelatedField(label='Creator', read_only=True)
    
    class Meta:
        model = Department
        fields = ['name', 'creator']
```

Response:

```
[{
    "Name": "aaa",
    "Creator": "John"
}]
```

## DynamicFieldsModelSerializer

It's copied from [official document](https://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields).

When using `DynamicFieldsModelSerializer`, the settings in `Meta` such as `exclude` and `fields` are ignored. Instead, the `fields` specified in the parameter that is passed in will take precedence.

# Mixins

## MultiFieldLookupMixin

From [Multiple lookup_fields for django rest framework](https://stackoverflow.com/questions/38461366/multiple-lookup-fields-for-django-rest-framework).

Used for multi field lookup.

Usage:

views.py:

```
class ExampleViewSet(MultipleFieldLookupMixin, viewsets.ModelViewSet):
    lookup_fields = ['pk', 'field_one', 'field_two']
```

urls.py:

```
urlpatterns = [
    path(r'examples/<str:field_one>/<str:field_two>/', views.ExampleViewSet.as_view({'get': 'retrieve'}))
]
```

# ViewSets

## ExportModelViewSet

Use `epxort` action and `ExportPermission` to exporting data.

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
    'EXCEPTION_HANDLER': 'djangorestframework_ext.views.exception_handler',
    ...
}
```

# Validators

## ActiveValidator

Validate whether the corresponding object is active using the specified key (default is `is_active`) and value (default is `True`).

Usage:

```
from rest_framework import serializers

class MySerializer(serializers.ModelSerializer):
    relation = serializers.PrimaryKeyRelatedField(queryset=Relation.objects.all(), validators=[ActiveValidator()])
```
