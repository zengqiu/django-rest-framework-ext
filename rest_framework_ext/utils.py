from rest_framework.settings import api_settings


def get_default_query_params():
    return {
        api_settings.DEFAULT_PAGINATION_CLASS.page_query_param,
        api_settings.DEFAULT_PAGINATION_CLASS.page_size_query_param,
        api_settings.ORDERING_PARAM
    }
