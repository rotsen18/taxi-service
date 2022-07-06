from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer


class PublicCarTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_list_login_required(self):
        response = self.client.get(reverse("taxi:car-list"))

        self.assertNotEqual(response.status_code, 200)

    def test_create_and_edit_login_required(self):
        response = self.client.get(reverse("taxi:car-form"))

        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            license_number="AAA12345",
            first_name="Test first",
            last_name="test last",
            password="Test12345678$"
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        manufacturer_1 = Manufacturer.objects.create(
            name="test_name_1",
            country="country_1"
        )
        Car.objects.create(model="model_name_1", manufacturer=manufacturer_1)
        Car.objects.create(model="model_name_2", manufacturer=manufacturer_1)

        response = self.client.get(reverse("taxi:car-list"))
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    # def test_create_car(self):
    #     manufacturer = Manufacturer.objects.create(
    #         name="test_name_1",
    #         country="country_1"
    #     )
    #     car_data = {
    #         "model": "test_model_name",
    #         "manufacturer_id": manufacturer.id
    #     }
    #     self.client.post(reverse("taxi:car-form"), car_data, follow=True)
    #     # Car.objects.create(**car_data)
    #     print(Car.objects.all())
    #     self.assertTrue(
    #         Car.objects.filter(
    #             model=car_data["model"],
    #             manufacturer__id=car_data["manufacturer_id"]
    #         ).exists()
    #     )

    # def test_update_car(self):
    #     manufacturer = Manufacturer.objects.create(
    #         name="test_name_1",
    #         country="country_1"
    #     )
    #     old_data = {"model": "test_name_1", "manufacturer": manufacturer}
    #     car = Car.objects.create(**old_data)
    #
    #     new_data = {"model": "changed_name_1", "manufacturer": manufacturer}
    #     self.client.post(
    #         reverse("taxi:car-form",
    #                 args=[car.id]), new_data
    #     )
    #
    #     updated_car = Car.objects.get(id=manufacturer.id)
    #
    #     self.assertEqual(new_data["model"], updated_car.model)

    def test_delete_car(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name_1",
            country="country_1"
        )
        car = Car.objects.create(
            model="test_name_1",
            manufacturer=manufacturer
        )

        self.client.post(
            reverse("taxi:car-delete", args=[car.id])
        )

        self.assertFalse(
            Car.objects.filter(id=car.id).exists()
        )

    def test_detail_car(self):
        driver = get_user_model().objects.create_user(
            username="test23",
            license_number="AAA12225",
            first_name="Test first",
            last_name="test last",
            password="Test12345678$"
        )
        manufacturer = Manufacturer.objects.create(
            name="test_name_1",
            country="country_1"
        )
        car = Car.objects.create(
            model="test_name_1",
            manufacturer=manufacturer
        )
        car.drivers.add(driver)

        response = self.client.get(reverse("taxi:car-detail", args=[car.id]))

        self.assertContains(response, car.drivers.first())