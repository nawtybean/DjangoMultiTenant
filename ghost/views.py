from django.shortcuts import HttpResponse
from system_management.custom_admin import tenant_admin_site
from django.contrib.auth.mixins import LoginRequiredMixin
from system_management.utilities import get_tenant
from system_management.utilities import table_data
from django.views import View
from customers.models import Customer
import json


from django.views.generic import ListView
from .models import (
    GhostModel
)

# Cache Control
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

decorators= (never_cache)
@method_decorator(decorators, name='dispatch')
class GhostView(LoginRequiredMixin, ListView):
    template_name = "ghost/overview.html"
    model = GhostModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            **tenant_admin_site.each_context(self.request),  # Admin site context
            "opts": self.model._meta,  # Model metadata
            "custom_data": "This is some custom context data"  # Custom context data
        })
        return context


decorators= (never_cache)
@method_decorator(decorators, name='dispatch')
class GhostData(LoginRequiredMixin, View):

    # An example POST Request. Do some cool stuff here.
    def post(self, request, *args, **kwargs):
        tenant = get_tenant(request)
        if request.method == 'POST':
            data = {
                "data": data
            }
            data = json.dumps(data, indent=4, default=str)
            return HttpResponse(data, content_type='application/json')

    # An example GET Request. Do some cool stuff here.
    def get(self, request, *args, **kwargs):

        tenant = get_tenant(request)

        if request.method == 'GET':

            customers = list(Customer.objects.filter(tenant=tenant).values())

            data = {
                "data": customers
            }
            data = json.dumps(data, indent=4, default=str)
            return HttpResponse(data, content_type='application/json')

