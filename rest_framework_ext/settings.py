from django.conf import settings
from django.core.signals import setting_changed
from rest_framework.settings import APISettings

USER_SETTINGS = getattr(settings, 'REST_FRAMEWORK_EXT', {})

DEFAULTS = {
    'PAGE_QUERY_PARAM': 'page',
    'PAGE_SIZE_QUERY_PARAM': 'limit',
}

api_settings = APISettings(USER_SETTINGS, DEFAULTS)


def reload_api_settings(*args, **kwargs):
    global api_settings

    setting, value = kwargs['setting'], kwargs['value']

    if setting == 'REST_FRAMEWORK_EXT':
        api_settings = APISettings(value, DEFAULTS)


setting_changed.connect(reload_api_settings)
