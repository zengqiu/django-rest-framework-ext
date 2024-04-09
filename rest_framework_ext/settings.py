from django.conf import settings
from rest_framework.pagination import PageNumberPagination


USER_SETTINGS = getattr(settings, 'REST_FRAMEWORK_EXT', {})

DEFAULTS = {
    'PAGE_QUERY_PARAM': PageNumberPagination.page_query_param,
    'PAGE_SIZE_QUERY_PARAM': 'limit',
}

globals().update({**DEFAULTS, **USER_SETTINGS})
