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

    def save_user(self, request, user, form, commit=True):
        """
        Override default user save action.

        This method will run at new user is created by rest_auth.

        """

        data = form.cleaned_data
        user.email = data['email']
        user.tz = data['tz']

        user.set_password(data['password'])

        if commit:
            user.save()

        return user
