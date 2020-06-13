"""
ASGI config for Dalmo project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
import django

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Dalmo.settings')
django.setup()
application = get_asgi_application()

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)]
            # "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')]
        },
    },
}

# worker: python manage.py runworker -v1