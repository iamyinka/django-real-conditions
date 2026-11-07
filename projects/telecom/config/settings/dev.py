"""Local development settings. Never use these on a server reachable by others."""

from config.env import env_bool, env_list

from .base import *  # noqa: F403  (deliberate: this module extends base settings)

DEBUG = env_bool("DJANGO_DEBUG", True)

ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", ["localhost", "127.0.0.1"])
