from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Profile


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email")

    def clean_email(self):
        data = self.cleaned_data["email"]
        if self.Meta.model.objects.filter(email=data).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return data


class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email")

    def clean_email(self):
        data = self.cleaned_data["email"]
        if (
            self.Meta.model.objects.exclude(id=self.instance.id)
            .filter(email=data)
            .exists()
        ):
            raise forms.ValidationError("A user with that email already exists.")
        return data


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("date_of_birth", "photo")
