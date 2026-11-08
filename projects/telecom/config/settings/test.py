"""Settings for the automated test suite."""

import os

# Tests need a SECRET_KEY, but they shouldn't need a real secret. setdefault keeps
# any value that's already set, and it has to run before base.py is imported,
# because base.py reads the variable at import time.
os.environ.setdefault("DJANGO_SECRET_KEY", "test-only-not-a-secret")
# Database defaults so tests that don't touch the database can run anywhere. Tests that
# do touch it run inside the web container, where the real values come from .env.
for name, value in {
    "POSTGRES_DB": "telecom",
    "POSTGRES_USER": "telecom",
    "POSTGRES_PASSWORD": "telecom",
    "DB_HOST": "localhost",
}.items():
    os.environ.setdefault(name, value)

from .base import *  # noqa: E402, F403

# The default hasher is deliberately slow to resist password cracking.
# In tests that slowness is only cost, so use a fast one.
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
