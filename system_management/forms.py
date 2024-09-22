from django.contrib.auth.forms import AuthenticationForm
from django import forms

class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if hasattr(self.request, 'tenant') and user.tenant != self.request.tenant:
            raise forms.ValidationError("Invalid login for this tenant.", code='invalid_login')
        super().confirm_login_allowed(user)