"""Block until the database accepts connections, or give up after a deadline.

Compose's `depends_on: condition: service_healthy` covers `docker compose up`. It does
nothing for `docker compose run --no-deps`, a database that restarts, or a platform
without Compose (Module 7). This command is the app's own guard, and it's bounded:
retrying forever turns an outage into a container that hangs silently.
"""

import time

from django.core.management.base import BaseCommand, CommandError
from django.db import OperationalError, connection


class Command(BaseCommand):
    help = "Wait until the default database accepts connections (bounded retry)."

    def add_arguments(self, parser):
        parser.add_argument("--timeout", type=float, default=30.0, help="Give up after N seconds.")
        parser.add_argument("--interval", type=float, default=1.0, help="Seconds between tries.")

    def handle(self, *args, timeout, interval, **options):
        deadline = time.monotonic() + timeout  # monotonic: immune to wall-clock changes
        attempt = 0
        while True:
            attempt += 1
            try:
                connection.ensure_connection()
            except OperationalError as exc:
                if time.monotonic() + interval > deadline:
                    raise CommandError(
                        f"Database still unavailable after {attempt} attempts ({timeout:g}s): {exc}"
                    ) from exc
                self.stderr.write(
                    f"Database unavailable (attempt {attempt}), retrying in {interval:g}s"
                )
                time.sleep(interval)
            else:
                self.stdout.write(self.style.SUCCESS(f"Database available (attempt {attempt})."))
                return
