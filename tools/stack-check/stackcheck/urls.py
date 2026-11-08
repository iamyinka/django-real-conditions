from django.urls import include, path
from rest_framework.routers import DefaultRouter

from probe import views

router = DefaultRouter()
router.register("items", views.ItemViewSet)
urlpatterns = [
    path("api/", include(router.urls)),
    path("page/", views.page),
    path("healthz", views.healthz),
]
