from django.contrib import admin
from system_management.custom_admin import tenant_admin_site

from django.urls import path

from .models import GhostModel
from .views import *


class GhostModelAdmin(admin.ModelAdmin):
    """
    Custom ModelAdmin for GhostModel with a custom URL routing.

    Attributes:
        model (Model): The GhostModel that this admin interface manages.

    Methods:
        get_urls():
            Overrides the default URL configuration to add a custom path for the GhostModel changelist view.
            Returns a URL pattern for the 'ghost/' path, which maps to a GhostView.

    Admin Registration:
        tenant_admin_site.register(GhostModel, GhostModelAdmin):
            Registers the GhostModel with the tenant_admin_site using the custom GhostModelAdmin configuration.
    """

    model = GhostModel

    def get_urls(self):
        view_name = '{}_{}_changelist'.format(
            self.model._meta.app_label, self.model._meta.model_name)
        return [
            path('ghost/', GhostView.as_view(), name=view_name),
        ]

tenant_admin_site.register(GhostModel, GhostModelAdmin)