import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "munera.settings")
os.environ.setdefault("MUNERA_DEBUG", "0")

application = get_wsgi_application()
