from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import CustomAuthenticationForm
from django.views import View
from django.shortcuts import render

class TenantLoginView(LoginView):
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

