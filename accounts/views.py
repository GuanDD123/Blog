from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import CreateView, DetailView, ListView

from actions.models import Action
from actions.utils import create_action
from blog.models import Post

from .forms import ProfileEditForm, UserEditForm, UserRegistrationForm
from .models import Contact, Profile
from .tasks import user_registed


class DashBoard(LoginRequiredMixin, ListView):
    model = Action
    context_object_name = "actions"
    template_name = "registration/dashboard.html"

    def get_queryset(self):
        if following_pks := self.request.user.following.values_list("pk", flat=True):
            actions = (
                Action.objects.exclude(user=self.request.user)
                .filter(user_id__in=following_pks)
                .select_related("user", "user__profile")
                .prefetch_related("target")
                .order_by("-created_at")
            )[:20]
        else:
            actions = Action.objects.none()
        return actions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["section"] = "dashboard"
        return context


class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = "registration/register.html"

    def form_valid(self, form):
        new_user = form.save()

        Profile.objects.create(user=new_user)
        create_action(new_user, "created account")
        user_registed.delay(new_user.pk)

        return render(self.request, "registration/register_done.html")


class EditView(LoginRequiredMixin, View):
    template_name = "registration/edit.html"

    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

        return render(
            request,
            self.template_name,
            {"user_form": user_form, "profile_form": profile_form},
        )

    def post(self, request):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("dashboard")
        else:
            messages.error(request, "Error updating profile.")
            return render(
                request,
                self.template_name,
                {"user_form": user_form, "profile_form": profile_form},
            )


class UserListView(LoginRequiredMixin, ListView):
    model = get_user_model()
    context_object_name = "users"
    template_name = "registration/user/list.html"
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["section"] = "people"
        context["page"] = context["page_obj"]
        return context


class UserDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    context_object_name = "user"
    template_name = "registration/user/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["section"] = "people"

        category = self.request.GET.get("category")
        if (not category) or (category in ("all", "images")):
            context["user_images"] = self.object.images_created.all()
        else:
            context["user_images"] = None
        if (not category) or (category in ("all", "posts")):
            context["user_posts"] = self.object.blog_posts.filter(
                status=Post.Status.PUBLISHED
            )
        else:
            context["user_posts"] = None
        return context


class UserFollowView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user_pk = request.POST.get("pk")
        action = request.POST.get("action")

        if (not user_pk) or (not action):
            return JsonResponse({"status": "error"})

        user = get_object_or_404(get_user_model(), pk=user_pk)
        if action == "follow":
            Contact.objects.get_or_create(user_from=request.user, user_to=user)
            create_action(request.user, "followed user", user)
        elif action == "unfollow":
            Contact.objects.filter(user_from=request.user, user_to=user).delete()
            create_action(request.user, "unfollowed user", user)
        else:
            return JsonResponse({"status": "error"})

        return JsonResponse({"status": "ok"})
