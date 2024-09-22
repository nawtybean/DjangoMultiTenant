from system_management.models import Tenant
from urllib.parse import urlparse, urlunparse

# get the host name
def get_hostname(request):
    """
    Extracts and returns the hostname from the request object.

    Args:
    - request: Request object

    Returns:
    - str: Hostname in lowercase
    """
    return request.get_host().split(':')[0].lower()


# check and get the signed in tenant
def get_tenant(request):
    """
    Retrieves the tenant based on the request's subdomain.

    Args:
    - request: Request object

    Returns:
    - Tenant object: Retrieved tenant object based on subdomain
    """
    hostname = get_hostname(request)
    subdomain = hostname.split('.')[0]
    return Tenant.objects.filter(subdomain=subdomain).first()