from django.db import models
import uuid
from system_management.models import TenantAwareModel

class Customer(TenantAwareModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    created = models.DateTimeField(editable=False, auto_now_add=True)
    date_modified = models.DateTimeField(null=True, editable=False, auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'
