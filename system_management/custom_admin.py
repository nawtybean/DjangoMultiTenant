from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group

class TenantAdminSite(AdminSite):
    def has_permission(self, request):
        return request.user.is_active

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if hasattr(request, 'tenant'):
            return queryset.filter(tenant=request.tenant)
        return queryset

tenant_admin_site = TenantAdminSite(name='tenant_admin')