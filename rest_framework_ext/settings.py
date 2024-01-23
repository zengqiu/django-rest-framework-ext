from django.conf import settings

USER_SETTINGS = getattr(settings, 'REST_FRAMEWORK_EXT', {})

DEFAULTS = {
    'PAGE_QUERY_PARAM': 'page',
    'PAGE_SIZE_QUERY_PARAM': 'limit',
}

globals().update({**DEFAULTS, **USER_SETTINGS})
