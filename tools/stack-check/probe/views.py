from django.http import HttpResponse, JsonResponse
from rest_framework import serializers, viewsets

from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "name", "kind"]


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.order_by("id")
    serializer_class = ItemSerializer
    filterset_fields = ["kind"]


def page(request):
    return HttpResponse(
        "<!doctype html><title>stack-check</title>"
        '<link rel="stylesheet" href="/static/probe/site.css">'
        '<h1 id="h">ok</h1><script>document.getElementById("h").dataset.js = "ran"</script>'
    )


def healthz(request):
    return JsonResponse({"status": "ok"})
