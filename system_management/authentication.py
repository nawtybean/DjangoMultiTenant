from django.contrib.auth.backends import ModelBackend, BaseBackend
from django.contrib.auth import get_user_model

from django.contrib.auth.hashers import check_password

class TenantBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        tenant = getattr(request, 'tenant', None)
        if tenant is None:
            return None
        try:
            user = UserModel.objects.get(email=username, tenant=tenant)
        except UserModel.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None