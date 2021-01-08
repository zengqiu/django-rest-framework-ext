from rest_framework.pagination import PageNumberPagination


class DynamicSizePageNumberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'limit'

    def paginate_queryset(self, queryset, request, view=None):
        if 'page' not in request.query_params:
            return None

        return super().paginate_queryset(queryset, request, view)
