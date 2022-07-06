from django.test import TestCase

from taxi.forms import DriverCreateForm, DriverLicenseUpdateForm


class FormsDriverTests(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "test_username",
            "first_name": "test first",
            "last_name": "test last",
            "license_number": "BBB87675"
        }
        form = DriverCreateForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_validate_license_has_8_characters_create_form(self):
        form_data = {
            "username": "test_username",
            "first_name": "test first",
            "last_name": "test last",
            "license_number": "BBB123456"
        }

        form_to_long = DriverCreateForm(data=form_data)
        self.assertFalse(form_to_long.is_valid())

        form_data["license_number"] = "BBB12"

        form_to_short = DriverCreateForm(data=form_data)
        self.assertFalse(form_to_short.is_valid())

    def test_validate_license_first_3_characters_uppercase_create_form(self):
        form_data = {
            "username": "test_username",
            "first_name": "test first",
            "last_name": "test last",
            "license_number": "22212345"
        }

        form_no_letters = DriverCreateForm(data=form_data)
        self.assertFalse(form_no_letters.is_valid())

        form_data["license_number"] = "bbb12345"

        form_lower_case = DriverCreateForm(data=form_data)
        self.assertFalse(form_lower_case.is_valid())

    def test_validate_license_last_5_characters_are_digit_create_form(self):
        form_data = {
            "username": "test_username",
            "first_name": "test first",
            "last_name": "test last",
            "license_number": "BBBaaaaa"
        }

        form_no_digits = DriverCreateForm(data=form_data)
        self.assertFalse(form_no_digits.is_valid())

    def test_driver_license_update_form(self):
        form_data = {
            "license_number": "BBB87675"
        }
        form = DriverLicenseUpdateForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_validate_license_has_8_characters_update_form(self):
        form_data = {
            "license_number": "BBB123456"
        }

        form_to_long = DriverCreateForm(data=form_data)
        self.assertFalse(form_to_long.is_valid())

        form_data["license_number"] = "BBB12"

        form_to_short = DriverCreateForm(data=form_data)
        self.assertFalse(form_to_short.is_valid())

    def test_validate_license_first_3_characters_uppercase_update_form(self):
        form_data = {
            "license_number": "22212345"
        }

        form_no_letters = DriverCreateForm(data=form_data)
        self.assertFalse(form_no_letters.is_valid())

        form_data["license_number"] = "bbb12345"

        form_lower_case = DriverCreateForm(data=form_data)
        self.assertFalse(form_lower_case.is_valid())

    def test_validate_license_last_5_characters_are_digit_update_form(self):
        form_data = {
            "license_number": "BBBaaaaa"
        }

        form_no_digits = DriverCreateForm(data=form_data)
        self.assertFalse(form_no_digits.is_valid())
