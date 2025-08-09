from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
import time

from .models import Ride, Location
from .serializers import RideSerializer
from utils.permissions import IsDriver
from utils.locationiq import get_distance_and_time, get_address_from_coords


# Create your views here.
class RideViewSet(viewsets.ViewSet):

    http_method_names = ["get", "post", "patch"]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        try:
            rides = []
            if request.user.role == "rider":
                rides = Ride.objects.filter(rider=request.user)
            else:
                rides = Ride.objects.filter(driver=request.user)
            serializer = RideSerializer(rides, many=True)
            return Response({"status": "Success", "data": serializer.data})
        except Exception as e:
            return Response(
                {"status": "Error", "data": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, pk=None):
        try:
            try:
                ride = Ride.objects.select_related(
                    "pickup_location", "dropoff_location"
                ).get(id=pk)
            except Ride.DoesNotExist:
                return Response(
                    {"status": "Error", "message": "Not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = RideSerializer(ride)
            return Response({"status": "Success", "data": serializer.data})
        except Exception as e:
            return Response(
                {"status": "Error", "data": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request):
        try:
            pickup = request.data.get("pickup_location")
            if not pickup:
                return Response(
                    {"status": "Error", "message": "Pickup value missing"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            pickup_latitude = pickup.get("latitude")
            pickup_longitude = pickup.get("longitude")
            if not (pickup_latitude and pickup_longitude):
                return Response(
                    {"status": "Error", "message": "Pickup value missing"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            pickup_location, pickup_created = Location.objects.get_or_create(
                latitude=pickup_latitude, longitude=pickup_longitude
            )

            dropoff = request.data.get("dropoff_location")
            if not dropoff:
                return Response(
                    {"status": "Error", "message": "Dropoff value missing"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            dropoff_latitude = request.data.get("dropoff_location").get("latitude")
            dropoff_longitude = request.data.get("dropoff_location").get("longitude")
            if not (dropoff_latitude and dropoff_longitude):
                return Response(
                    {"status": "Error", "message": "Dropoff value missing"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            dropoff_location, dropoff_created = Location.objects.get_or_create(
                latitude=dropoff_latitude, longitude=dropoff_longitude
            )

            Ride.objects.create(
                rider=request.user,
                pickup_location=pickup_location,
                dropoff_location=dropoff_location,
            )
            return Response(
                {"status": "Success", "message": "Ride Created"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"status": "Error", "data": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def partial_update(self, request, pk=None):
        try:
            try:
                ride = Ride.objects.get(id=pk)
            except Ride.DoesNotExist:
                return Response(
                    {"status": "Error", "message": "Not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            status_list = ["not_started", "started", "completed", "cancelled"]
            request_status = request.GET.get("status", "").lower()
            if request_status not in status_list:
                return Response(
                    {"status": "Error", "message": "Status not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            if request.user.role == "rider":
                if not (request_status == "cancelled" and ride.status == "not_started"):
                    return Response(
                        {
                            "status": "Error",
                            "message": "Not Authorized to change status",
                        },
                        status=status.HTTP_404_NOT_FOUND,
                    )
            elif request.user.role == "driver" and request_status == "cancelled":
                return Response(
                    {"status": "Error", "message": "Not Authorized to change status"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            elif ride.status == "not_started" and request_status == "completed":
                return Response(
                    {
                        "status": "Error",
                        "message": "Can't change status from not_started to completed",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            ride.status = request_status
            ride.save()
            return Response({"status": "Success", "message": "Status updated"})
        except Exception as e:
            return Response(
                {"status": "Error", "data": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DriverViewSet(viewsets.ViewSet):

    http_method_names = ["get", "patch"]
    permission_classes = [IsDriver]

    def list(self, request):
        try:
            driver_location_lat = request.GET.get("lat")
            driver_location_lon = request.GET.get("lon")
            if not (driver_location_lat and driver_location_lon):
                return Response(
                    {"status": "Error", "message": "Location required"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            driver_location_lat = float(driver_location_lat)
            driver_location_lon = float(driver_location_lon)
            rides = Ride.objects.select_related("pickup_location").filter(
                status="not_started", driver__isnull=True
            )
            available_rides = []
            for ride in rides:
                distance, time_taken = get_distance_and_time(
                    driver_location_lat,
                    driver_location_lon,
                    ride.pickup_location.latitude,
                    ride.pickup_location.longitude,
                )
                time.sleep(1)
                data = {
                    "ride_id": ride.id,
                    "pickup_location": get_address_from_coords(
                        ride.pickup_location.latitude, ride.pickup_location.longitude
                    ),
                    "dropoff_location": get_address_from_coords(
                        ride.dropoff_location.latitude, ride.dropoff_location.longitude
                    ),
                    "distance_to_pickup_location": distance,
                }
                available_rides.append(data)
            available_rides.sort(key=lambda ride: ride["distance_to_pickup_location"])
            return Response({"status": "Success", "data": available_rides})
        except Exception as e:
            return Response(
                {"status": "Error", "data": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def partial_update(self, request, pk=None):
        try:
            try:
                ride = Ride.objects.get(id=pk)
            except Ride.DoesNotExist:
                return Response(
                    {"status": "Error", "message": "Not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            if not (ride.status == "not_started" and ride.driver is None):
                return Response(
                    {"status": "Error", "message": "This ride is not available"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            ride.driver = request.user
            ride.save()
            return Response({"status": "Success", "message": "Ride Accepted"})
        except Exception as e:
            return Response(
                {"status": "Error", "data": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def ride_tracker(request, id):
    try:
        try:
            ride = Ride.objects.select_related("dropoff_location").get(id=id)
        except Ride.DoesNotExist:
            return Response(
                {"status": "Error", "message": "Not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if ride.status != "started":
            return Response(
                {"status": "Error", "message": "Ride has not been started"},
                status=status.HTTP_404_NOT_FOUND,
            )
        ride_location_lat = request.GET.get("lat")
        ride_location_lon = request.GET.get("lon")
        if not (ride_location_lat and ride_location_lon):
            return Response(
                {"status": "Error", "message": "Location required"},
                status=status.HTTP_404_NOT_FOUND,
            )
        ride_location_lat = float(ride_location_lat)
        ride_location_lon = float(ride_location_lon)
        distance, time_taken = get_distance_and_time(
            ride_location_lat,
            ride_location_lon,
            ride.dropoff_location.latitude,
            ride.dropoff_location.longitude,
        )
        return Response(
            {
                "status": "Success",
                "remaining_distance": distance,
                "remaining_time_estimate": time_taken,
            }
        )
    except Exception as e:
        return Response(
            {"status": "Error", "data": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
