from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Profile


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email")


class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email")


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("date_of_birth", "photo")
