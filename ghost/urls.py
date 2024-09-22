from django.urls import path
from ghost.views import GhostData

urlpatterns = [
    # API
    path('get-customers/', GhostData.as_view(), name='get-customers'),

]