import redis
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, View
from django.views.generic.edit import DeleteView

from actions.utils import create_action

from .forms import ImageCreateForm, ImageURLForm
from .models import Image

r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    password=settings.REDIS_PASSWORD,
)


class ImageListView(ListView):
    model = Image
    context_object_name = "images"
    template_name = "images/list.html"
    paginate_by = 8

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            if request.GET.get("images_only"):
                return HttpResponse("")
            raise

    def get_template_names(self):
        if self.request.GET.get("images_only"):
            return ["images/include/list_images.html"]
        return self.template_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["section"] = "images"
        return context


class ImageDetailView(DetailView):
    model = Image
    context_object_name = "image"
    template_name = "images/detail.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Image, pk=self.kwargs["pk"], slug=self.kwargs["slug"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_views = r.incr(f"image:{self.object.pk}:views")
        r.zincrby("image_ranking", 1, self.object.pk)

        context["section"] = "images"
        context["total_views"] = total_views

        return context


class ImageRankingView(ListView):
    model = Image
    context_object_name = "most_viewed"
    template_name = "images/ranking.html"

    def get_queryset(self):
        image_ranking = r.zrange("image_ranking", 0, 9, desc=True)
        image_ranking_pks = [int(pk) for pk in image_ranking]

        most_viewed = list(Image.objects.filter(pk__in=image_ranking_pks))
        most_viewed.sort(key=lambda image: image_ranking_pks.index(image.pk))
        return most_viewed
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["section"] = "images"
        return context


class ImageCreateView(LoginRequiredMixin, CreateView):
    model = Image
    context_object_name = "image"
    form_class = ImageCreateForm
    template_name = "images/create.html"
    success_message = "Image added successfully"

    def get_initial(self):
        initial = super().get_initial()
        initial["url"] = self.request.GET.get("url", "")
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["url_form"] = ImageURLForm(self.request.GET or None)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        create_action(self.request.user, "created image", self.object)
        return response


class ImageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Image
    context_object_name = "image"
    template_name = "images/delete.html"
    success_url = reverse_lazy("images:list")

    def test_func(self):
        return self.request.user == self.get_object().user

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        create_action(request.user, "deleted image", self.object)
        return super().delete(request, *args, **kwargs)


class ImageLikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        image_pk = request.POST.get("pk")
        action = request.POST.get("action")

        if not image_pk or not action:
            return JsonResponse({"status": "error"})

        image = get_object_or_404(Image, pk=image_pk)

        if action == "like":
            image.users_like.add(request.user)
            create_action(request.user, "liked image", image)
        elif action == "unlike":
            image.users_like.remove(request.user)
            create_action(request.user, "unliked image", image)
        else:
            return JsonResponse({"status": "error"})

        return JsonResponse({"status": "ok"})
