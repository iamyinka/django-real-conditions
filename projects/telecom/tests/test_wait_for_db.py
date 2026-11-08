from unittest import mock

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import OperationalError

ENSURE = "core.management.commands.wait_for_db.connection.ensure_connection"
SLEEP = "core.management.commands.wait_for_db.time.sleep"


def test_returns_once_database_comes_up():
    failures_then_ok = [OperationalError("refused"), OperationalError("refused"), None]
    with mock.patch(ENSURE, side_effect=failures_then_ok) as ensure, mock.patch(SLEEP) as sleep:
        call_command("wait_for_db", timeout=10, interval=1)
    assert ensure.call_count == 3
    assert sleep.call_count == 2


def test_gives_up_after_the_deadline():
    # Fake clock: each sleep advances time, so the test runs instantly.
    # Tries at t=0, 1, 2, 3; the next would land past the 3s deadline.
    clock = {"now": 0.0}
    with (
        mock.patch(ENSURE, side_effect=OperationalError("refused")),
        mock.patch(SLEEP, side_effect=lambda s: clock.__setitem__("now", clock["now"] + s)),
        mock.patch(
            "core.management.commands.wait_for_db.time.monotonic", side_effect=lambda: clock["now"]
        ),
        pytest.raises(CommandError, match="still unavailable after 4 attempts"),
    ):
        call_command("wait_for_db", timeout=3, interval=1)
