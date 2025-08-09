from rest_framework import serializers
import time

from .models import Ride, Location
from user.serializers import CustomUserSerializer
from utils.locationiq import get_distance_and_time


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        required_fields = kwargs.pop("fields", None)
        super().__init__(*args, **kwargs)
        if required_fields:
            # Drop any fields that are not specified
            allowed = set(required_fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class RideSerializer(serializers.ModelSerializer):
    rider = CustomUserSerializer(fields=["id", "username", "phone"], read_only=True)
    driver = CustomUserSerializer(fields=["id", "username", "phone"], read_only=True)

    pickup_location = LocationSerializer(read_only=True)
    dropoff_location = LocationSerializer(read_only=True)
    distance = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Ride
        fields = [
            "id",
            "rider",
            "driver",
            "pickup_location",
            "dropoff_location",
            "status",
            "created_at",
            "updated_at",
            "distance",
        ]

    def __init__(self, *args, **kwargs):
        required_fields = kwargs.pop("fields", None)
        super().__init__(*args, **kwargs)

        if required_fields:
            allowed = set(required_fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_distance(self, obj):
        distance, time_taken = get_distance_and_time(
            obj.pickup_location.latitude,
            obj.pickup_location.longitude,
            obj.dropoff_location.latitude,
            obj.dropoff_location.longitude,
        )
        time.sleep(1)
        return distance
