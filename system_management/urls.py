from django.urls import path
from .views import access_denied

urlpatterns = [
    path('access_denied/', access_denied, name='access_denied'),
]