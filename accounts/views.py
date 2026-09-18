from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView

from .forms import ProfileEditForm, UserEditForm, UserRegistrationForm
from .models import Profile


@login_required
def dashboard(request):
    return render(request, "registration/dashboard.html", {"section": "dashboard"})


class RegisterView(CreateView):
    template_name = "registration/register.html"
    form_class = UserRegistrationForm

    def form_valid(self, form):
        new_user = form.save()
        Profile.objects.create(user=new_user)
        return render(
            self.request, "registration/register_done.html", {"new_user": new_user}
        )


class EditView(LoginRequiredMixin, View):
    template_name = "registration/edit.html"

    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

        return render(
            request,
            self.template_name,
            {
                "user_form": user_form,
                "profile_form": profile_form,
            },
        )

    def post(self, request):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("dashboard")

        return render(
            request,
            self.template_name,
            {
                "user_form": user_form,
                "profile_form": profile_form,
            },
        )
