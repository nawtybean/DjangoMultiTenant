from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group

class TenantAdminSite(AdminSite):
    """
    Custom admin site for tenant-based administration.

    Methods:
        has_permission(request):
            Determines whether the current user has access to the admin site.

        get_queryset(request):
            Returns the queryset filtered by the tenant associated with the request,
            if a tenant is present. Otherwise, returns the default queryset.

    Attributes:
        tenant_admin_site (TenantAdminSite): Instance of the custom tenant admin site with
        the name 'tenant_admin'.
    """

    def has_permission(self, request):
        return request.user.is_active

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if hasattr(request, 'tenant'):
            return queryset.filter(tenant=request.tenant)
        return queryset

tenant_admin_site = TenantAdminSite(name='tenant_admin')