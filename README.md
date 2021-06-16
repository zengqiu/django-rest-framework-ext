Django REST framework Ext
=========================

Some extensions of Django REST framework.


DynamicSizePageNumberPagination
-------------------------------

Support using ``limit`` parameter to specify the page size for querying.

Return all data when the ``page`` parameter is not specified.

### Usage:

```
REST_FRAMEWORK = {
    ...
    'DEFAULT_PAGINATION_CLASS': 'djangorestframework_ext.pagination.DynamicSizePageNumberPagination',
    ...
}
```

### Request:

```
GET https://api.example.org/accounts/?page=4&limit=100
```

DjangoModelPermissions
----------------------

Add ``view`` permission control.

### Usage:

```
from djangorestframework_ext.permissions import DjangoModelPermissions
```

IsCurrentUser
-------------

Determine whether it is the current login user.

### Usage:

```
from djangorestframework_ext.permissions import IsCurrentUser
```

RecursiveSerializer
-------------------

### Usage:

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

### Response:

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

ExportModelSerializer
---------------------

Use verbose name or label replace field name.

### Usage:

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

### Response:

```
[{
    "Name": "aaa",
    "Creator": "John"
}]
```

DynamicFieldsModelSerializer
----------------------------

It's copied from [official document](https://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields).

DEFAULT_QUERY_PARAMS
--------------------

Default query params: ``page_query_param``, ``page_size_query_param`` and ``ORDERING_PARAM``.

exception_handler
-----------------

Some exception handlers.

### Usage: 

```
REST_FRAMEWORK = {
    ...
    'EXCEPTION_HANDLER': 'djangorestframework_ext.views.exception_handler',
    ...
}
```
