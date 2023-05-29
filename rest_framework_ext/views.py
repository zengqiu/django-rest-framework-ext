from rest_framework.views import exception_handler as exc_handler
from rest_framework.response import Response
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from rest_framework import status


def exception_handler(exc, context):
    response = exc_handler(exc, context)

    if isinstance(exc, (IntegrityError, ValidationError)) and not response:
        response = Response(str(exc), status=status.HTTP_400_BAD_REQUEST)

    return response
