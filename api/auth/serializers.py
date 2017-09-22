from rest_auth.serializers import LoginSerializer as RALoginSerializer
from rest_auth.registration.serializers import (
    RegisterSerializer as RARegisterSerializer
)


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
