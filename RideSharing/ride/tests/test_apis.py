from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from ride.models import Ride, Location
from user.models import CustomUser


class RideViewSetTest(APITestCase):

    def setUp(self):
        self.rider = CustomUser.objects.create_user(
            username="rider", password="rider", role="rider"
        )
        self.driver = CustomUser.objects.create_user(
            username="driver", password="driver", role="driver"
        )
        self.pickup_location = Location.objects.create(
            latitude=11.27045525, longitude=75.775141946119
        )
        self.dropoff_location = Location.objects.create(
            latitude=11.2653898, longitude=75.7804253
        )
        self.client = APIClient()
        self.ride = Ride.objects.create(
            rider=self.rider,
            pickup_location=self.pickup_location,
            dropoff_location=self.dropoff_location,
        )

    def test_list_rides_for_rider(self):
        self.client.force_authenticate(user=self.rider)
        response = self.client.get("/rides/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Success")

    def test_create_ride(self):
        self.client.force_authenticate(user=self.rider)
        data = {
            "pickup_location": {"latitude": 11.27045525, "longitude": 75.775141946119},
            "dropoff_location": {"latitude": 11.2653898, "longitude": 75.7804253},
        }
        response = self.client.post("/rides/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Ride Created")

    def test_update_ride_status_cancelled_by_rider(self):
        self.client.force_authenticate(user=self.rider)
        ride = Ride.objects.create(
            rider=self.rider,
            pickup_location=self.pickup_location,
            dropoff_location=self.dropoff_location,
        )
        url = f"/rides/{ride.id}/?status=cancelled"
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_ride(self):
        self.client.force_authenticate(user=self.rider)
        url = f"/rides/{self.ride.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DriverViewSetTest(APITestCase):

    def setUp(self):
        self.rider = CustomUser.objects.create_user(
            username="rider", password="rider", role="rider"
        )
        self.driver = CustomUser.objects.create_user(
            username="driver", password="driver", role="driver"
        )
        self.client = APIClient()
        self.pickup_location = Location.objects.create(
            latitude=11.27045525, longitude=75.775141946119
        )
        self.dropoff_location = Location.objects.create(
            latitude=11.2653898, longitude=75.7804253
        )
        self.ride = Ride.objects.create(
            rider=self.rider,
            pickup_location=self.pickup_location,
            dropoff_location=self.dropoff_location,
            status="not_started",
        )

    def test_list_available_rides(self):
        self.client.force_authenticate(user=self.driver)
        response = self.client.get(f"/available_rides/?lat=11.2710633&lon=75.7757265")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Success")

    def test_accept_ride(self):
        self.client.force_authenticate(user=self.driver)
        url = f"/available_rides/{self.ride.id}/"
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Ride Accepted")


class RideTrackerTest(APITestCase):

    def setUp(self):
        self.rider = CustomUser.objects.create_user(
            username="rider", password="rider", role="rider"
        )
        self.driver = CustomUser.objects.create_user(
            username="driver", password="driver", role="driver"
        )
        self.client = APIClient()
        self.pickup = Location.objects.create(
            latitude=11.27045525, longitude=75.775141946119
        )
        self.dropoff = Location.objects.create(
            latitude=11.2653898, longitude=75.7804253
        )
        self.ride = Ride.objects.create(
            rider=self.rider,
            driver=self.driver,
            pickup_location=self.pickup,
            dropoff_location=self.dropoff,
            status="started",
        )

    def test_track_ride(self):
        self.client.force_authenticate(user=self.rider)
        response = self.client.get(
            f"/track_ride/{self.ride.id}?lat=11.2685991&lon=75.7775674"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("remaining_distance", response.data)
