from django.test import TestCase

from ride.models import Location, Ride
from user.models import CustomUser


class LocationModelTest(TestCase):

    def test_create_location(self):
        loc = Location.objects.create(latitude=12.34, longitude=56.78)
        self.assertEqual(loc.latitude, 12.34)
        self.assertEqual(loc.longitude, 56.78)


class RideModelTest(TestCase):

    def setUp(self):
        self.rider = CustomUser.objects.create_user(
            username="rider", password="rider", role="rider"
        )
        self.driver = CustomUser.objects.create_user(
            username="driver", password="driver", role="driver"
        )

        self.pickup = Location.objects.create(latitude=10.0, longitude=20.0)
        self.dropoff = Location.objects.create(latitude=30.0, longitude=40.0)

    def test_create_ride(self):
        ride = Ride.objects.create(
            rider=self.rider,
            driver=self.driver,
            pickup_location=self.pickup,
            dropoff_location=self.dropoff,
            status=Ride.RideStatus.NOT_STARTED,
        )
        self.assertEqual(ride.rider.username, "rider")
        self.assertEqual(ride.driver.username, "driver")
        self.assertEqual(ride.pickup_location.latitude, 10.0)
        self.assertEqual(ride.dropoff_location.longitude, 40.0)
        self.assertEqual(ride.status, Ride.RideStatus.NOT_STARTED)
