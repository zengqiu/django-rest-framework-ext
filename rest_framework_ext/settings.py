from django.conf import settings
from rest_framework.settings import api_settings


USER_SETTINGS = getattr(settings, 'REST_FRAMEWORK_EXT', {})

DEFAULTS = {
    'PAGE_QUERY_PARAM': api_settings.DEFAULT_PAGINATION_CLASS.page_query_param,
    'PAGE_SIZE_QUERY_PARAM': 'limit',
}

globals().update({**DEFAULTS, **USER_SETTINGS})
