from rest_framework.pagination import PageNumberPagination
from .settings import rest_framework_ext_settings


class DynamicSizePageNumberPagination(PageNumberPagination):
    page_query_param = rest_framework_ext_settings.PAGE_QUERY_PARAM
    page_size_query_param = rest_framework_ext_settings.PAGE_SIZE_QUERY_PARAM

    def paginate_queryset(self, queryset, request, view=None):
        if self.page_query_param not in request.query_params:
            return None

        return super().paginate_queryset(queryset, request, view)
