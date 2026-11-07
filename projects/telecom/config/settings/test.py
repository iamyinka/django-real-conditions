"""Settings for the automated test suite."""

import os

# Tests need a SECRET_KEY, but they shouldn't need a real secret. setdefault keeps
# any value that's already set, and it has to run before base.py is imported,
# because base.py reads the variable at import time.
os.environ.setdefault("DJANGO_SECRET_KEY", "test-only-not-a-secret")

from .base import *  # noqa: E402, F403

# The default hasher is deliberately slow to resist password cracking.
# In tests that slowness is only cost, so use a fast one.
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
