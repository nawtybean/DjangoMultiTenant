from django.contrib.auth.backends import ModelBackend, BaseBackend
from django.contrib.auth import get_user_model

from django.contrib.auth.hashers import check_password

class TenantBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate a user based on email and password within the context of a tenant.

        Args:
            request (HttpRequest): The current request object, which contains the tenant.
            username (str, optional): The email address of the user attempting to authenticate.
            password (str, optional): The password of the user attempting to authenticate.
            **kwargs: Additional keyword arguments.

        Returns:
            User or None: The authenticated user object if authentication is successful;
            otherwise, None.
        """

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