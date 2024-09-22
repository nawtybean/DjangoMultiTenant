from django.db import models
from system_management.models import TenantAwareModel
import uuid

class GhostModel(TenantAwareModel):

    class Meta:
        verbose_name_plural = 'Ghost Example'
        app_label = 'ghost'