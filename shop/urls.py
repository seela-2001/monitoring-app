from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("items", views.ItemViewSet, basename="item")

urlpatterns = [
    path("health", views.health),
    path("slow", views.slow),
    path("error", views.error),
    path("flaky", views.flaky),
    path("", include(router.urls)),
]
