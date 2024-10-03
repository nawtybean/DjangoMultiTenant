from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import get_object_or_404
from django.http import Http404
from .models import Tenant

import threading

local_data = threading.local()


class TenantMiddleware(MiddlewareMixin):
    """
    Middleware to process and assign the tenant based on the subdomain in the request's host.

    Methods:
        process_request(request):
            Extracts the subdomain from the request's HTTP host and attempts to find the corresponding tenant.
            If a subdomain is present and valid, the tenant is assigned to the request. If no valid subdomain
            is found or the tenant is not found, assigns None to the request's tenant.

    Args:
        request (HttpRequest): The incoming request object.

    Attributes:
        request.tenant (Tenant or None): The tenant object corresponding to the subdomain, or None if no
        subdomain is found or the tenant does not exist.
    """

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
    """
    Middleware and utility functions for tenant-based file path management and client IP extraction.

    Classes:
        TenantFilePathMiddleware:
            Middleware to attach tenant information to a local thread during a request's lifecycle.

        Methods:
            __init__(get_response):
                Initializes the middleware with the provided response handler.

            __call__(request):
                Extracts tenant information from the request, assigns it to thread-local data, and proceeds
                with the request handling.

    Functions:
        get_tenant_from_request(request):
            Extracts the tenant from the request object. Returns the tenant associated with the user,
            if available. Otherwise, returns None.

        get_current_tenant():
            Returns the tenant stored in thread-local data. If no tenant is found, returns None.

        get_client_ip(request):
            Extracts and returns the client IP address from the request.
            Checks the 'HTTP_X_FORWARDED_FOR' header if available, otherwise returns 'REMOTE_ADDR'.
    """


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