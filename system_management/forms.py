from django.contrib.auth.forms import AuthenticationForm
from django import forms

class CustomAuthenticationForm(AuthenticationForm):
    """
    Custom authentication form that validates user login against a tenant.

    Methods:
        confirm_login_allowed(user):
            Checks if the user's tenant matches the tenant in the request.
            Raises a ValidationError if the user is attempting to log in to an invalid tenant.
            Calls the parent method to proceed with standard login validation.
    """

    def confirm_login_allowed(self, user):
        if hasattr(self.request, 'tenant') and user.tenant != self.request.tenant:
            raise forms.ValidationError("Invalid login for this tenant.", code='invalid_login')
        super().confirm_login_allowed(user)