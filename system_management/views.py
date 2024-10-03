from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import CustomAuthenticationForm
from django.views import View
from django.shortcuts import render

class TenantLoginView(LoginView):

    """
    Custom login view for tenant-specific authentication.

    Attributes:
        form_class (CustomAuthenticationForm): The custom authentication form used for login.

    Methods:
        form_valid(form):
            Validates the user and ensures the tenant from the login form matches the tenant in the request.
            If the tenant does not match, an error is added, and the form is marked as invalid.
            On success, logs the user in and redirects to the success URL.

        form_invalid(form):
            Renders the login form again with validation errors if the form is invalid.

    Views:
        access_denied(request):
            Renders the 'access_denied.html' template when access is denied.

        index(request):
            Renders the landing page (home.html) for the site.
    """
    form_class = CustomAuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        if user.tenant != self.request.tenant:
            form.add_error(None, "Invalid login for this tenant.")
            return self.form_invalid(form)
        login(self.request, user)
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return render(self.request, 'registration/login.html', {'form': form})


def access_denied(request):
    return render(request, 'access_denied.html')

def index(request):
    return render(request, 'landing/home.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

