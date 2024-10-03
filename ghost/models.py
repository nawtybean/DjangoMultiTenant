from system_management.models import TenantAwareModel

class GhostModel(TenantAwareModel):
    """
    Model representing a tenant-aware "Ghost" entity, inheriting from TenantAwareModel.

    Meta:
        verbose_name_plural (str): The plural name for this model in the admin interface is 'Ghost Example'.
        app_label (str): Specifies the application label as 'ghost'.
    """

    class Meta:
        verbose_name_plural = 'Ghost Example'
        app_label = 'ghost'