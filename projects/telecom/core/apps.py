from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Project-wide plumbing that isn't a business feature: health probes, ops commands."""

    name = "core"
