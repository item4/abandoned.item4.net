from allauth.account.adapter import DefaultAccountAdapter

from django.http.response import JsonResponse

from rest_auth.registration.views import RegisterView, VerifyEmailView
from rest_auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView,
)

from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    PasswordResetSerializer
)


class Login(LoginView):
    """View for Login"""

    serializer_class = LoginSerializer
    adapter_class = DefaultAccountAdapter


class Logout(LogoutView):
    """View for Logout"""

    adapter_class = DefaultAccountAdapter


class Register(RegisterView):
    """View for register"""

    serializer_class = RegisterSerializer
    adapter_class = DefaultAccountAdapter


class Confirm(VerifyEmailView):
    """View for confirmation."""

    adapter_class = DefaultAccountAdapter

    def get(self, *args, **kwargs):
        """Overwrite default get view. Default was HTML page"""

        obj = self.get_object()
        return JsonResponse({'key': obj.key})  # FIXME: Redirect to frontend


class PasswordChange(PasswordChangeView):
    """View for change password."""

    adapter_class = DefaultAccountAdapter


class PasswordReset(PasswordResetView):
    """View for reset password."""

    serializer_class = PasswordResetSerializer
    adapter_class = DefaultAccountAdapter


class PasswordResetConfirm(PasswordResetConfirmView):
    """View for Confirm resetting password."""

    adapter_class = DefaultAccountAdapter
