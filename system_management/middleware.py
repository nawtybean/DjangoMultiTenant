from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import get_object_or_404
from django.http import Http404
from .models import Tenant

import threading

local_data = threading.local()


class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Extract the host parts
        host_parts = request.META['HTTP_HOST'].split('.')

        # Determine the subdomain
        if len(host_parts) > 2 and host_parts[0] != 'www':
            subdomain = host_parts[0]
        else:
            subdomain = None

        # Logic to handle subdomain or default to example.com
        if subdomain is None:
            request.tenant = None
        else:
            try:
                request.tenant = get_object_or_404(Tenant, subdomain=subdomain)
            except Http404:
                request.tenant = None  # Handle case where no tenant is found


class TenantFilePathMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract tenant information from the request
        # This could be from the user, session, or another source
        tenant = get_tenant_from_request(request)
        local_data.tenant = tenant
        response = self.get_response(request)
        return response


def get_tenant_from_request(request):
    # Implement your logic to get the tenant from the request
    return request.user.tenant if hasattr(request.user, 'tenant') else None


def get_current_tenant():
    return getattr(local_data, 'tenant', None)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip