from django.contrib import admin
from system_management.custom_admin import tenant_admin_site

from django.urls import path

from .models import GhostModel
from .views import *


class GhostModelAdmin(admin.ModelAdmin):
    model = GhostModel

    def get_urls(self):
        view_name = '{}_{}_changelist'.format(
            self.model._meta.app_label, self.model._meta.model_name)
        return [
            path('ghost/', GhostView.as_view(), name=view_name),
        ]

tenant_admin_site.register(GhostModel, GhostModelAdmin)