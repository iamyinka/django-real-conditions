"""Django 6.1 + Postgres 18 + DRF/django-filter/cors/whitenoise/factory_boy/time-machine."""

import datetime as dt

import factory
import pytest
import time_machine
from django.core.management import call_command
from django.db import IntegrityError, connection, transaction
from django.utils import timezone
from psycopg.types.range import Range

from probe.models import Booking, Item
from probe.tasks import multiply

pytestmark = pytest.mark.django_db


class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Item

    name = factory.Sequence(lambda n: f"item-{n}")
    kind = "router"


def test_versions():
    import django

    assert django.VERSION[:3] == (6, 1, 3)
    with connection.cursor() as c:
        c.execute("SHOW server_version")
        assert c.fetchone()[0].startswith("18.")


def test_drf_filter_and_pagination(client):
    ItemFactory.create_batch(3)
    ItemFactory(kind="modem")
    body = client.get("/api/items/?kind=router").json()
    assert body["count"] == 3 and len(body["results"]) == 2 and body["next"]


def test_cors_preflight(client):
    r = client.options(
        "/api/items/",
        headers={"Origin": "https://app.example.com", "Access-Control-Request-Method": "GET"},
    )
    assert r["access-control-allow-origin"] == "https://app.example.com"


def test_csp_header_from_django_core(client):
    assert client.get("/healthz")["Content-Security-Policy"] == "default-src 'self'"


def test_whitenoise_serves_hashed_static(client, settings, tmp_path):
    settings.STATIC_ROOT = tmp_path
    call_command("collectstatic", "--noinput", verbosity=0)
    from django.templatetags.static import static
    from whitenoise.middleware import WhiteNoiseMiddleware  # re-scan new STATIC_ROOT

    url = static("probe/site.css")
    assert url != "/static/probe/site.css"  # manifest storage hashed the name
    mw = WhiteNoiseMiddleware(lambda r: None)
    assert mw.files.get(url) is not None


def test_exclusion_constraint_rejects_overlap():
    t0 = timezone.now()
    h = dt.timedelta(hours=1)
    Booking.objects.create(technician=1, slot=Range(t0, t0 + 2 * h))
    with pytest.raises(IntegrityError), transaction.atomic():
        Booking.objects.create(technician=1, slot=Range(t0 + h, t0 + 3 * h))  # overlaps
    Booking.objects.create(technician=2, slot=Range(t0, t0 + 2 * h))  # other tech: fine


def test_select_for_update_skip_locked():
    ItemFactory()
    with transaction.atomic():
        assert list(Item.objects.select_for_update(skip_locked=True))


def test_time_machine_freezes_auto_now():
    with time_machine.travel(dt.datetime(2030, 1, 2, 3, 4, tzinfo=dt.UTC), tick=False):
        assert ItemFactory().created == dt.datetime(2030, 1, 2, 3, 4, tzinfo=dt.UTC)


def test_django_tasks_framework():
    result = multiply.enqueue(6, 7)
    assert result.return_value == 42


def test_livekit_token():
    import jwt  # installed by livekit-api
    from livekit import api

    token = (
        api.AccessToken("devkey", "devsecret-devsecret-devsecret-32b")
        .with_identity("tech-1")
        .with_grants(api.VideoGrants(room_join=True, room="consult-1"))
        .to_jwt()
    )
    claims = jwt.decode(token, "devsecret-devsecret-devsecret-32b", algorithms=["HS256"])
    assert claims["sub"] == "tech-1" and claims["video"]["room"] == "consult-1"
