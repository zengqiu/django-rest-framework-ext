from rest_framework import serializers
from django.utils import dateformat
from django.utils.dateparse import parse_datetime


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
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
            result[str(getattr(field, 'label')) or k] = value
        return result
