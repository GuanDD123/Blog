from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView

from .forms import ImageCreateForm
from .models import Image


class ImageCreateView(LoginRequiredMixin, CreateView):
    model = Image
    form_class = ImageCreateForm
    template_name = "images/create.html"
    success_message = "Image added successfully"

    def get_initial(self):
        initial = super().get_initial()
        initial["url"] = self.request.GET.get("url", "")
        initial["title"] = self.request.GET.get("title", "")
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, "images/detail.html", {"section": "images", "image": image})
