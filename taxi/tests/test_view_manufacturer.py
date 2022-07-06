from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer


class PublicManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_list_login_required(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertNotEqual(response.status_code, 200)

    def test_create_and_edit_login_required(self):
        response = self.client.get(reverse("taxi:manufacturer-form"))

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            license_number="AAA12345",
            first_name="Test first",
            last_name="test last",
            password="Test12345678$"
        )
        self.client.force_login(self.user)

    def test_create_manufacturer(self):
        manufacturer_data = {
            "name": "test_name",
            "country": "test_country"
        }

        self.client.post(reverse("taxi:manufacturer-form"), manufacturer_data)

        self.assertTrue(
            Manufacturer.objects.filter(
                name=manufacturer_data["name"],
                country=manufacturer_data["country"]
            ).exists()
        )

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="test_name_1", country="country_1")
        Manufacturer.objects.create(name="test_name_2", country="country_2")

        response = self.client.get(reverse("taxi:manufacturer-list"))
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_update_manufacturer(self):
        old_data = {"name": "test_name_1", "country": "country_1"}
        manufacturer = Manufacturer.objects.create(**old_data)

        new_data = {"name": "changed_name_1", "country": "new_country_1"}
        self.client.post(
            reverse("taxi:manufacturer-form",
                    args=[manufacturer.id]), new_data
        )

        updated_manufacturer = Manufacturer.objects.get(id=manufacturer.id)

        self.assertEqual(new_data["name"], updated_manufacturer.name)
        self.assertEqual(new_data["country"], updated_manufacturer.country)

    def test_delete_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name_1",
            country="country_1"
        )

        self.client.post(
            reverse("taxi:manufacturer-delete", args=[manufacturer.id])
        )

        self.assertFalse(
            Manufacturer.objects.filter(id=manufacturer.id).exists()
        )
