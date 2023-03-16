from rest_framework import serializers
from django.utils import dateformat
from django.utils.dateparse import parse_datetime
from django.db.models import ManyToManyRel


class ModelSerializer(serializers.ModelSerializer):
    @property
    def errors(self):
        errors = {}

        for field_name, error in super().errors.items():
            errors[self.get_field_label(field_name)] = error
        return errors

    def get_field_label(self, name):
        label = str(getattr(self.get_fields()[name], 'label'))
        if not label:
            field = self.Meta.model._meta.get_field(name)
            if hasattr(field, 'verbose_name'):
                label = field.verbose_name
            elif isinstance(field, ManyToManyRel):
                label = field.related_model._meta.verbose_name
            else:
                label = name
        return label


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        kwargs = {
            'context': self.context
        }
        if issubclass(self.parent.parent.__class__, DynamicFieldsModelSerializer):
            kwargs['fields'] = self.parent.parent.fields

        serializer = self.parent.parent.__class__(value, **kwargs)
        return serializer.data


class ExportModelSerializer(ModelSerializer):
    def to_representation(self, obj):
        data = super().to_representation(obj)
        result = dict()
        for k, v in data.items():
            field = self.get_fields()[k]
            if isinstance(field, serializers.DateTimeField) and v:
                value = dateformat.format(parse_datetime(v), 'Y-m-d H:i:s')
            else:
                value = v
            result[self.get_field_label(k)] = value
        return result


# https://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
class DynamicFieldsModelSerializer(ModelSerializer):
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
