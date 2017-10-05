from allauth.account.adapter import DefaultAccountAdapter
from allauth.utils import build_absolute_uri


class AccountAdapter(DefaultAccountAdapter):
    """Own account Adapter."""

    def get_email_confirmation_url(self, request, emailconfirmation):
        """Override default action."""

        return build_absolute_uri(
            request,
            f'/auth/confirm/{emailconfirmation.key}/'
        )
