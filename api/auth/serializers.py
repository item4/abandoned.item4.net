from rest_auth.registration.serializers import (
    RegisterSerializer as RARegisterSerializer
)
from rest_auth.serializers import (
    LoginSerializer as RALoginSerializer,
    PasswordResetSerializer as RAPasswordResetSerializer
)

from .fields import TimezoneField


class LoginSerializer(RALoginSerializer):
    """Own serializer for login."""

    username = None  # DO NOT REMOVE THIS LINE.


class RegisterSerializer(RARegisterSerializer):
    """Own serializer for register."""

    # DO NOT REMOVE BELOW LINE (username)
    # It cause strange username requirement.
    # We do not use username field but default of rest_auth serializer need
    # username param. It must not be blank and not be longer than 0.
    # WTF?!
    username = None
    # END

    tz = TimezoneField(required=True)

    def get_cleaned_data(self):
        return {
            'email': self.validated_data.get('email', ''),
            'password': self.validated_data.get('password1', ''),
            'tz': self.validated_data.get('tz', ''),
        }


class PasswordResetSerializer(RAPasswordResetSerializer):
    """Own serializer for reset password."""

    def get_email_options(self):
        """Override this method to change default e-mail options"""
        return {
            'subject_template_name': 'auth/password_reset_subject.txt',
            'email_template_name': 'auth/password_reset_email.html',
        }
