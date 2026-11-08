"""Playwright drives real Chromium against Django's live_server."""

import os

import pytest

# Playwright's sync API runs an event loop in this thread, so Django's async-safety guard
# refuses the test database setup/teardown. Safe here: this process only runs browser tests,
# and nothing else shares the thread. Don't set this in application settings.
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = pytest.mark.django_db(transaction=True)


def test_django_csp_blocks_inline_script_in_real_chromium(live_server, page):
    # SECURE_CSP = default-src 'self' (settings.py). The page has an inline <script>,
    # so a real browser must refuse to run it and report a CSP violation.
    messages = []
    page.on("console", lambda m: messages.append(m.text))
    page.goto(f"{live_server.url}/page/")
    assert page.title() == "stack-check"
    assert page.locator("#h").get_attribute("data-js") is None  # script did not run
    assert any("Content Security Policy" in m for m in messages)
