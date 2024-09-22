from system_management.models import TenantAwareModel

class GhostModel(TenantAwareModel):

    class Meta:
        verbose_name_plural = 'Ghost Example'
        app_label = 'ghost'