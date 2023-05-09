from django.contrib.auth.password_validation import validate_password


class ValidatePasswordHandler:

    def __init__(self, password: str):
        self.password = password

    def validate(self):
        validate_password(self.password)
