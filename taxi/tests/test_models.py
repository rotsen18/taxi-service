from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )

        self.assertEqual(str(manufacturer), manufacturer.name)

    def test_driver_str(self):
        driver = Driver.objects.create(
            username="test",
            license_number="AAA12345",
            first_name="Test first",
            last_name="test last"
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer
        )

        self.assertEqual(str(car), car.model)

    def test_create_driver_as_user_with_license_number(self):
        username = "test"
        license_number = "AAA12345"
        first_name = "Test first"
        last_name = "test last"
        password = "Test12345678$"

        driver = Driver.objects.create_user(
            username=username,
            license_number=license_number,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        self.assertEqual(driver.username, username)
        self.assertEqual(driver.first_name, first_name)
        self.assertEqual(driver.last_name, last_name)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))

