from rest_framework.exceptions import ValidationError


class ActiveValidator:
    message = 'This field is not active.'
    key = 'is_active'
    value = True

    def __init__(self, message=None, key=None, value=None):
        self.message = message or self.message
        self.key = key or self.key
        self.value = value or self.value

    def __call__(self, value):
        if getattr(value, self.key, None) != self.value:
            raise ValidationError(self.message)
