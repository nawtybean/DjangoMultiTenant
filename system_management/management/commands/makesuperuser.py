import os
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from system_management.models import Tenant

# from dotenv import load_dotenv
# load_dotenv('./.env')

# email = os.environ['DEFAULT_EMAIL']

email = "tenant2@exampleza.com"

class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Handles the logic for creating a new user with specific attributes.

        Args:
            *args: Variable positional arguments.
            **options: Variable keyword arguments.

        Comments:
            to use run 'python manage.py makesuperuser'
        """
        password = make_password("root", salt=None, hasher='default')
        User = get_user_model()
        qs = User.objects.filter(email=email)

        # If the user does not exist, create a new user with the following attributes
        if not qs.exists():
            print("creating Tenant and User...")
            new_tenant = Tenant.objects.create(name='Tenant2',
                                address='Tenant2 Address',
                                telephone='9999',
                                email=email,
                                subdomain='tenant2',)

            new_tenant.save()
            tenant_id = new_tenant.id

            User.objects.create(first_name='Shaun',
                                last_name='De Ponte',
                                email=email,
                                phone='12345678',
                                tenant_id=tenant_id,
                                password=password,
                                is_confirmed=True,
                                is_staff=True,
                                is_active=True,)
            print("User and Tenant created successfully")