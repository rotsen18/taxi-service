from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license_number(number):
    if not len(number) == 8:
        raise ValidationError("License number should consist of 8 characters")
    elif not number[:3].isupper() or not number[:3].isalpha():
        raise ValidationError("First 3 characters should be uppercase letters")
    elif not number[3:].isdigit():
        raise ValidationError("Last 5 characters should be digits")

    return number


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class DriverCreateForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("username", "first_name", "last_name", "license_number")

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class DriverSearchForm(forms.Form):
    search = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username..."})
    )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
