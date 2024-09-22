from django.contrib import admin
from django.http import HttpRequest
from customers.models import Customer
from django import forms
from django.utils.html import format_html
from system_management.custom_admin import tenant_admin_site
from django.contrib.auth import get_user_model


User = get_user_model()

class CustomerAdmin(forms.ModelForm):
    required_css_class = 'required'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Customer
        fields = "__all__"



@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    form = CustomerAdmin

    def edit(self, obj):
        return format_html(
            '<a class="btn btn-success" href="/tenant-admin/customer/customer/{}/change/">Edit</a>',
            obj.pk,
        )

    def get_name(self, obj):
        return obj.podcast_fk.title
    get_name.admin_order_field  = 'title'  #Allows column order sorting
    get_name.short_description = 'Podcast Name'  #Renames column head

    list_per_page = 25

    list_display = ['first_name',
                    'last_name',
                    'email',
                    'phone_number',
                    'address',
                    'city',
                    'country',
                    'created',
                    'edit']
    fieldsets = (
        (
            "Customer Information",
            {
                "fields": (
                    'first_name',
                    'last_name',
                    'email',
                    'phone_number',
                    'address',
                    'city',
                    'country',
                )
            },
        ),
        (
            "Date Information",
            {
                "fields": (
                    'created',
                    'date_modified',
                )
            },
        ),

    )

    filter_horizontal = ()
    readonly_fields = (
                        'created',
                        'date_modified',
                       )





    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request, 'tenant'):
            return qs.filter(tenant=request.tenant)
        return qs


    def save_model(self, request, obj, form, change):
        if hasattr(request, 'tenant'):
            obj.tenant = request.tenant
        super().save_model(request, obj, form, change)


    def get_form(self, request, obj=None, **kwargs):
        # Set the tenant attribute when the form is requested
        self.tenant = request.tenant
        return super().get_form(request, obj, **kwargs)


    # This method is called by the formfield_for_foreignkey method
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "foreign_key_field_name_fk":
    #         kwargs["queryset"] = db_field.related_model.objects.filter(tenant=request.tenant)
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)

tenant_admin_site.register(Customer, CustomerAdmin)