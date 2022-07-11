from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer


class PublicCarTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_list_login_required(self):
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertNotEqual(response.status_code, 200)

    def test_create_and_edit_login_required(self):
        response = self.client.get(reverse("taxi:driver-create"))

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            license_number="AAA12345",
            first_name="Test first",
            last_name="test last",
            password="Test12345678$"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        Driver.objects.create(
            username="test_username",
            license_number="CCC12345"
        )
        response = self.client.get(reverse("taxi:driver-list"))
        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_create_driver(self):
        driver_data = {
            "username": "test_username",
            "password": "Test_12345",
            "license_number": "BBB87675"
        }

        self.client.post(reverse("taxi:driver-create"), driver_data)
        print(Driver.objects.all())
        self.assertTrue(
            Driver.objects.filter(username=driver_data["username"]).exists()
        )

    def test_driver_update_license_number(self):
        driver = Driver.objects.create(
            username="test_username",
            license_number="CCC12345"
        )
        new_data = {
            "license_number": "DDD12345"
        }

        self.client.post(
            reverse("taxi:driver-update", args=[driver.id]), new_data
        )
        updated_driver = Driver.objects.get(id=driver.id)

        self.assertEqual(
            updated_driver.license_number, new_data["license_number"]
        )

    def test_delete_driver(self):
        driver = Driver.objects.create(
            username="test_username",
            license_number="CCC12345"
        )

        self.client.post(
            reverse("taxi:driver-delete", args=[driver.id])
        )

        self.assertFalse(
            Driver.objects.filter(id=driver.id).exists()
        )

    def test_detail_car(self):
        driver = Driver.objects.create(
            username="test23",
            license_number="EEE12225",
        )
        manufacturer = Manufacturer.objects.create(
            name="test_name_1",
            country="country_1"
        )
        car = Car.objects.create(
            model="test_name_1",
            manufacturer=manufacturer
        )
        driver.cars.add(car)

        response = self.client.get(
            reverse("taxi:driver-detail", args=[driver.id])
        )

        self.assertContains(response, driver.cars.first())
        self.assertContains(response, driver.license_number)
        self.assertContains(response, driver.username)

    def test_driver_search(self):
        for salt in "1234":
            Driver.objects.create(
                username="test" + salt,
                license_number="DDD1222" + salt,
            )

        response = self.client.get(reverse("taxi:driver-list") + "?search=1")
        drivers = Driver.objects.filter(username__contains="1")

        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
