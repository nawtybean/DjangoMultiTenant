from django.db import models
from datetime import datetime
from django.utils.translation import gettext_lazy as _
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager, LowercaseEmailField


class Tenant(models.Model):
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
    tenant_aware_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'TenantAwareModel'


class CustomUser(AbstractBaseUser, PermissionsMixin):
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
