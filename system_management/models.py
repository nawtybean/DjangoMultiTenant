from django.db import models
from datetime import datetime
from django.utils.translation import gettext_lazy as _
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager, LowercaseEmailField


class Tenant(models.Model):
    """
    Model representing a tenant with unique identification and associated details.

    Fields:
        id (UUIDField): Unique identifier for each tenant, generated automatically.
        name (CharField): Name of the tenant (e.g., company name), default is 'Acme'.
        address (CharField): Address of the tenant, default is 'Acme Address'.
        telephone (CharField): Contact telephone number of the tenant, default is '9999'.
        email (CharField): Contact email of the tenant, default is 'acme@explosive.com'.
        image (ImageField): Optional field for storing an image associated with the tenant.
        subdomain (CharField): Subdomain assigned to the tenant, used for identifying tenant-specific
            resources, default is 'acme'.

        created (DateTimeField): Timestamp when the tenant was created, automatically set.
        date_modified (DateTimeField): Timestamp for the last modification of the tenant's details,
            automatically updated.

    Methods:
        __str__():
            Returns the tenant's subdomain as its string representation.

    Meta:
        verbose_name_plural (str): The plural form of the model's name is 'Instance'.
    """


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, default='Acme')
    address = models.CharField(max_length=255, default='Acme Address')
    telephone = models.CharField(max_length=255, default='9999')
    email = models.CharField(max_length=255, default='acme@explosive.com')
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    subdomain = models.CharField(max_length=255, default='acme')

    created = models.DateTimeField(editable=False, auto_now_add=True)
    date_modified = models.DateTimeField(null=True, editable=False, auto_now=True)

    def __str__(self):
        return self.subdomain

    class Meta:
        verbose_name_plural = 'Instance'


class TenantAwareModel(models.Model):
    """
    Abstract model for tenant-aware objects that associate records with a specific tenant.

    Fields:
        tenant_aware_id (UUIDField): Unique identifier for the tenant-aware object, automatically generated.
        tenant (ForeignKey): Foreign key linking the object to a specific Tenant instance. When the linked
            Tenant is deleted, the related records will also be deleted (on_delete=models.CASCADE).

    Meta:
        verbose_name_plural (str): The plural form of the model's name is 'TenantAwareModel'.
    """

    tenant_aware_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'TenantAwareModel'


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model extending AbstractBaseUser and PermissionsMixin, with tenant awareness and additional fields.

    Fields:
        id (UUIDField): Unique identifier for the user, automatically generated.
        email (LowercaseEmailField): Unique email address used as the username for authentication.
        first_name (CharField): Optional first name of the user.
        last_name (CharField): Optional last name of the user.
        phone (CharField): Optional phone number for the user, default is 0.
        is_confirmed (BooleanField): Indicates whether the user's email is confirmed, default is False.
        is_staff (BooleanField): Indicates if the user has staff access to the site, default is True.
        is_active (BooleanField): Indicates if the user is active and allowed to log in, default is True.
        tenant (ForeignKey): Foreign key linking the user to a Tenant, optional field.

        created (DateTimeField): Timestamp when the user was created, default is the current time.

    Methods:
        __str__():
            Returns the user's email as the string representation.

        get_full_name():
            Returns the user's full name (in this case, their email).

        get_short_name():
            Returns the user's short name (in this case, their email).

        has_perm(perm, obj=None):
            Always returns True, indicating the user has the specified permission.

        has_module_perms(app_label):
            Always returns True, indicating the user has permissions to view the specified app.

        save(*args, **kwargs):
            Overrides the save method to set the tenant automatically when creating a new user if
            no tenant is provided.

    Meta:
        verbose_name (str): The singular name for the model in the admin interface is 'Users'.
        verbose_name_plural (str): The plural name for the model in the admin interface is 'Users'.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = LowercaseEmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=500, blank=True, default=0)
    is_confirmed = models.BooleanField(default=False)
    is_staff = models.BooleanField(_('staff status'), default=True,
                                   help_text=_('Designates whether the user can log into this site.'), )
    is_active = models.BooleanField(_('active'), default=True, help_text=_(
        'Designates whether this user should be treated as active. ''Unselect this instead of deleting accounts.'), )
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True)

    created = models.DateTimeField(editable=False, default=datetime.now)
    # history = HistoricalRecords()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def save(self, *args, **kwargs):
        if not self.pk and not self.tenant_id:
            self.tenant = self._state.adding and self.tenant or None
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = _('Users')
        verbose_name_plural = _('Users')
