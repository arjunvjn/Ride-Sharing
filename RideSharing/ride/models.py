from django.db import models

from user.models import CustomUser


# Create your models here.
class Location(models.Model):

    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"lat:{self.latitude} and lon:{self.longitude}"


class Ride(models.Model):

    class RideStatus(models.TextChoices):
        NOT_STARTED = "not_started"
        STARTED = "started"
        COMPLETED = "completed"
        CANCELLED = "cancelled"

    rider = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, related_name="rider_rides"
    )
    driver = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, related_name="driver_rides"
    )
    pickup_location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="pickup_rides"
    )
    dropoff_location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="dropoff_rides"
    )
    status = models.CharField(
        max_length=20, choices=RideStatus.choices, default=RideStatus.NOT_STARTED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.created_at)
