from allauth.account.adapter import DefaultAccountAdapter

from rest_auth.views import LoginView, LogoutView
from rest_auth.registration.views import RegisterView, VerifyEmailView

from django.http.response import JsonResponse

from .serializers import LoginSerializer, RegisterSerializer


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
