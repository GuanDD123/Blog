from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser, Profile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "is_staff")

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )
    fieldsets = UserAdmin.fieldsets + (
        ("Relationships", {"fields": ("following_list",)}),
    )

    def following_list(self, obj):
        return ", ".join(user.username for user in obj.following.all())

    following_list.short_description = "Following"
    readonly_fields = ("following_list",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "date_of_birth", "photo")
    autocomplete_fields = ("user",)
