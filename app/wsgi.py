import os

from django.core.wsgi import get_wsgi_application

settings_module = 'app.settings.development' if 'DEVELOPMENT' in os.environ else 'app.settings.production'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
