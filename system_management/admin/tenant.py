from django.contrib import admin
from system_management.models import Tenant
from django import forms
from django.utils.html import format_html
from system_management.custom_admin import tenant_admin_site

class TenantAdminForm(forms.ModelForm):
    required_css_class = 'required'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Tenant
        fields = "__all__"


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    form = TenantAdminForm

    def edit(self, obj):
        return format_html(
            '<a class="btn btn-success" href="/tenant-admin/system_management/tenant/{}/change/">Edit</a>',
            obj.pk,
        )


    list_display = ('subdomain', 'name', 'created', 'edit', )
    search_fields = ('subdomain', 'name')
    fieldsets = (
        (
            "Tenant Information - Send an email to support@example.com to update your tenant information.",
                {
                    'fields': (
                       'subdomain',
                       'name',
                       'address',
                       'telephone',
                       'email',
                       'image',
                       )
                }

        ),
    )

    filter_horizontal = ()
    readonly_fields = (
                        'subdomain',
                        'name',
                        'address',
                        'telephone',
                        'email',
                       )

    def has_add_permission(self, request):
            return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request, 'tenant'):
            return qs.filter(subdomain=request.tenant)
        return qs


    def save_model(self, request, obj, form, change):
        if hasattr(request, 'tenant'):
            obj.tenant = request.tenant
        super().save_model(request, obj, form, change)


    def get_form(self, request, obj=None, **kwargs):
        # Set the tenant attribute when the form is requested
        self.tenant = request.tenant
        return super().get_form(request, obj, **kwargs)


tenant_admin_site.register(Tenant, TenantAdmin)