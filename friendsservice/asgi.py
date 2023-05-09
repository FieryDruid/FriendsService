"""
ASGI config for friendsservice project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from typing import Callable

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "friendsservice.settings")

django_app = get_asgi_application()


async def application(scope: dict, receive: Callable, send: Callable):
    if scope['type'] == 'http':
        await django_app(scope, receive, send)
    else:
        msg = f'Unknown scope type: "{scope["type"]}"'
        raise NotImplementedError(msg)
