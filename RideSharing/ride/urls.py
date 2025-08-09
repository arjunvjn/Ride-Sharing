from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RideViewSet, DriverViewSet, ride_tracker

router = DefaultRouter()
router.register(r"rides", RideViewSet, basename="rides")
router.register(r"available_rides", DriverViewSet, basename="drivers")

urlpatterns = [
    path("", include(router.urls)),
    path("track_ride/<int:id>", ride_tracker, name="ride_tracker"),
]
