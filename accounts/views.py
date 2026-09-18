from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import CreateView

from .forms import UserRegistrationForm


@login_required
def dashboard(request):
    return render(request, "registration/dashboard.html", {"section": "dashboard"})


class RegisterView(CreateView):
    template_name = "registration/register.html"
    form_class = UserRegistrationForm

    def form_valid(self, form):
        new_user = form.save()
        return render(
            self.request, "registration/register_done.html", {"new_user": new_user}
        )
