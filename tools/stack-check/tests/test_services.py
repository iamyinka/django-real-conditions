"""Needs the Compose services: Celery worker, Redis/Valkey, SeaweedFS S3, ASGI/WSGI servers."""

import io
import json
import urllib.request

import pytest
from asgiref.sync import async_to_sync
from channels.testing import WebsocketCommunicator
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image

from probe.models import Item
from probe.tasks import add
from stackcheck.asgi import application

pytestmark = pytest.mark.services


def test_celery_roundtrip_through_real_worker():
    assert add.delay(2, 3).get(timeout=20) == 5


# Consumers call close_old_connections() on connect, so pytest-django must allow DB access.
@pytest.mark.django_db(transaction=True)
def test_channels_redis_group_broadcast():
    async def scenario():
        a = WebsocketCommunicator(application, "/ws/echo/")
        b = WebsocketCommunicator(application, "/ws/echo/")
        assert (await a.connect())[0] and (await b.connect())[0]
        await a.send_json_to({"hello": "field"})
        got = await b.receive_json_from(timeout=5)
        await a.disconnect()
        await b.disconnect()
        return got

    assert async_to_sync(scenario)() == {"hello": "field"}


@pytest.mark.django_db
def test_pillow_thumbnail_to_s3_and_presigned_get():
    buf = io.BytesIO()
    Image.new("RGB", (800, 600), "orange").save(buf, "JPEG")
    img = Image.open(io.BytesIO(buf.getvalue()))
    img.thumbnail((200, 200))
    out = io.BytesIO()
    img.save(out, "JPEG")
    item = Item.objects.create(name="photo", kind="site")
    item.image.save("site.jpg", ContentFile(out.getvalue()))
    assert default_storage.exists(item.image.name)
    url = item.image.url  # presigned (querystring_auth defaults on)
    assert "X-Amz-Signature" in url
    data = urllib.request.urlopen(url, timeout=5).read()
    assert Image.open(io.BytesIO(data)).size == (200, 150)


@pytest.mark.parametrize("server", ["gunicorn:8000", "uvicorn:8000", "daphne:8000"])
def test_app_servers_serve_requests(server):
    body = json.load(urllib.request.urlopen(f"http://{server}/healthz", timeout=5))
    assert body == {"status": "ok"}
