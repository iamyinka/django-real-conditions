"""Root URL configuration: maps URL prefixes to each app's routes."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),  # /healthz and /readyz
]
