from django.contrib import admin
from django.urls import include, path
from system_management import views
from system_management.custom_admin import tenant_admin_site
from system_management.views import index
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('tenant-admin/', tenant_admin_site.urls),
     path('', index, name='home'),

     path('system-management/', include('system_management.urls')),
     path('ghost/', include('ghost.urls')),

     path('logout', views.LogoutView.as_view(), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
