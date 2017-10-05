from django.http.response import JsonResponse

from rest_auth.registration.views import RegisterView, VerifyEmailView
from rest_auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
)

from .adapter import AccountAdapter
from .serializers import (
    LoginSerializer,
    PasswordResetSerializer,
    RegisterSerializer,
)


class Login(LoginView):
    """View for Login"""

    serializer_class = LoginSerializer
    adapter_class = AccountAdapter


class Logout(LogoutView):
    """View for Logout"""

    adapter_class = AccountAdapter


class Register(RegisterView):
    """View for register"""

    serializer_class = RegisterSerializer
    adapter_class = AccountAdapter


class Confirm(VerifyEmailView):
    """View for confirmation."""

    adapter_class = AccountAdapter

    def get(self, *args, **kwargs):
        """Overwrite default get view. Default was HTML page"""

        obj = self.get_object()
        return JsonResponse({'key': obj.key})


class PasswordChange(PasswordChangeView):
    """View for change password."""

    adapter_class = AccountAdapter


class PasswordReset(PasswordResetView):
    """View for reset password."""

    serializer_class = PasswordResetSerializer
    adapter_class = AccountAdapter


class PasswordResetConfirm(PasswordResetConfirmView):
    """View for Confirm resetting password."""

    adapter_class = AccountAdapter
