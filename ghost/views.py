from django.shortcuts import HttpResponse
from system_management.custom_admin import tenant_admin_site
from django.contrib.auth.mixins import LoginRequiredMixin
from system_management.utilities import get_tenant
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
        """
        Generates and returns the context data for a view, extending the base context with additional information.

        Args:
            **kwargs: Additional keyword arguments passed to the context.

        Returns:
            dict: The updated context dictionary with the following entries:
                - Admin site context from `tenant_admin_site.each_context(self.request)`.
                - "opts": Model metadata from `self.model._meta`.
                - "custom_data": A custom string value, "This is some custom context data".
        """
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
        """
        Handles POST requests and returns a JSON response with tenant-specific data.

        Args:
            request (HttpRequest): The incoming HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: A JSON-formatted response containing the "data" object, if the request method is POST.

        Notes:
            - The tenant is retrieved from the request using `get_tenant(request)`.
            - The response content is formatted as JSON with an indentation of 4 spaces.
        """

        tenant = get_tenant(request)
        if request.method == 'POST':
            data = {
                "data": data
            }
            data = json.dumps(data, indent=4, default=str)
            return HttpResponse(data, content_type='application/json')


    # An example GET Request. Do some cool stuff here.
    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and returns a JSON response containing tenant-specific customer data.

        Args:
            request (HttpRequest): The incoming HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: A JSON-formatted response with customer data specific to the tenant.

        Notes:
            - The tenant is retrieved from the request using `get_tenant(request)`.
            - Retrieves the list of customers associated with the tenant from the Customer model.
            - The response content is formatted as JSON with an indentation of 4 spaces.
        """
        tenant = get_tenant(request)

        if request.method == 'GET':

            customers = list(Customer.objects.filter(tenant=tenant).values())

            data = {
                "data": customers
            }
            data = json.dumps(data, indent=4, default=str)
            return HttpResponse(data, content_type='application/json')

