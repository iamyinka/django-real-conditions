"""Health probes, for machines rather than people.

/healthz (liveness): "Is the Python process up and serving requests?" It deliberately
    touches nothing else, so a database outage doesn't make the app look dead. Restarting
    a web container never fixes a database.
/readyz (readiness): "Can this instance do useful work right now?" It checks the database,
    and it returns 503 so a load balancer stops sending traffic here until things recover.
"""

import logging

from django.db import DatabaseError, connection
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET

logger = logging.getLogger(__name__)


@never_cache  # a cached "ok" from five minutes ago is worse than no answer
@require_GET
def healthz(request):
    return JsonResponse({"status": "ok"})


@never_cache
@require_GET
def readyz(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except DatabaseError:
        # Full details go to the logs. The response says only *which* check failed:
        # probe URLs are often reachable by people who shouldn't see connection errors.
        logger.exception("Readiness check failed: database unavailable")
        return JsonResponse({"status": "unavailable", "checks": {"database": "error"}}, status=503)
    return JsonResponse({"status": "ok", "checks": {"database": "ok"}})
