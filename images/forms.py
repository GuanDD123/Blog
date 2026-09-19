from typing import ClassVar

import requests
from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify

from .models import Image


class ImageURLForm(forms.Form):
    url = forms.URLField()


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("title", "url", "description")
        widgets: ClassVar[dict[str, forms.Widget]] = {"url": forms.HiddenInput}

    def clean_url(self):
        url = self.cleaned_data["url"]
        valid_extentions = ("jpg", "jpeg", "png")
        extentions = url.rsplit(".", 1)[1].lower()
        if extentions not in valid_extentions:
            raise forms.ValidationError("Invalid image extension.")
        return url

    def save(self, commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data["url"]
        name = slugify(image.title)
        extension = image_url.rsplit(".", 1)[1].lower()
        image_name = f"{name}.{extension}"
        response = requests.get(image_url)
        image.image.save(image_name, ContentFile(response.content), save=False)
        if commit:
            image.save()
        return image
