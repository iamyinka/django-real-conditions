import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stackcheck.settings")
django_asgi = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter  # noqa: E402
from django.urls import path  # noqa: E402

from probe.consumers import EchoConsumer  # noqa: E402

application = ProtocolTypeRouter(
    {"http": django_asgi, "websocket": URLRouter([path("ws/echo/", EchoConsumer.as_asgi())])}
)
