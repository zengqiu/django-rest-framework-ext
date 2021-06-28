from rest_framework import serializers
from django.utils import dateformat
from django.utils.dateparse import parse_datetime


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        kwargs = {
            'context': self.context
        }
        if issubclass(self.parent.parent.__class__, DynamicFieldsModelSerializer):
            kwargs['fields'] = self.parent.parent.fields

        serializer = self.parent.parent.__class__(value, **kwargs)
        return serializer.data


class ExportModelSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        data = super().to_representation(obj)
        result = dict()
        for k, v in data.items():
            field = self.get_fields()[k]
            if isinstance(field, serializers.DateTimeField) and v:
                value = dateformat.format(parse_datetime(v), 'Y-m-d H:i:s')
            else:
                value = v
            result[getattr(field, 'label') or k] = value
        return result


# https://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
