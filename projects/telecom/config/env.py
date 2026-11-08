"""Read configuration from environment variables.

Settings modules call these helpers at import time, so a missing or malformed
value stops the process at startup with a clear message, before any request
is served. We use a few small functions instead of a library so you can see
exactly what happens.
"""

import os

from django.core.exceptions import ImproperlyConfigured

_REQUIRED = object()  # sentinel: "no default given", which is different from default=None

_TRUE = {"1", "true", "yes", "on"}
_FALSE = {"0", "false", "no", "off"}


def env(name, default=_REQUIRED):
    """Return the variable as a string, or the default.

    An empty value counts as unset, because `FOO=` in an env file is usually
    a mistake rather than a deliberate empty string.
    """
    value = os.environ.get(name, "")
    if value == "":
        if default is _REQUIRED:
            raise ImproperlyConfigured(f"Set the {name} environment variable.")
        return default
    return value


def env_bool(name, default=_REQUIRED):
    """Parse true/false-style values. Anything unrecognized is an error, not False."""
    value = env(name, default)
    if isinstance(value, bool):
        return value
    lowered = value.strip().lower()
    if lowered in _TRUE:
        return True
    if lowered in _FALSE:
        return False
    raise ImproperlyConfigured(f"{name} must be true or false, got {value!r}.")


def env_list(name, default=_REQUIRED):
    """Split a comma-separated value into a list, ignoring blanks and spaces."""
    value = env(name, default)
    if isinstance(value, list):
        return value
    return [item.strip() for item in value.split(",") if item.strip()]
