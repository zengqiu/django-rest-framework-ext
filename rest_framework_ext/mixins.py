from django.shortcuts import get_object_or_404


class MultiFieldLookupMixin:
    """From: https://stackoverflow.com/questions/38461366/multiple-lookup-fields-for-django-rest-framework"""
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field, None):
                filter_kwargs[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj
