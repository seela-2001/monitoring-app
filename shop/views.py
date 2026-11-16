import logging
import random
import time

from django.http import JsonResponse
from rest_framework import viewsets

from .metrics import ITEMS_CREATED
from .models import Item
from .serializers import ItemSerializer

logger = logging.getLogger(__name__)


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by("-id")
    serializer_class = ItemSerializer

    def perform_create(self, serializer):
        item = serializer.save()
        ITEMS_CREATED.inc()
        logger.info("item created", extra={"item_id": item.id})


def health(request):
    return JsonResponse({"status": "ok"})


def slow(request):
    delay = random.uniform(0.5, 3)
    time.sleep(delay)
    return JsonResponse({"delay_seconds": round(delay, 2)})


def error(request):
    logger.error("intentional error triggered")
    return JsonResponse({"error": "boom"}, status=500)


def flaky(request):
    rate = float(request.GET.get("rate", 0.3))
    if random.random() < rate:
        logger.error("flaky endpoint failed")
        return JsonResponse({"error": "random failure"}, status=500)
    return JsonResponse({"ok": True})
