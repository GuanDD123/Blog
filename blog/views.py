from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
    TrigramSimilarity,
)
from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from taggit.models import Tag

from .forms import CommentForm, EmailPostForm, SearchForm
from .models import Comment, Post


class PostListView(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "blog/list.html"
    paginate_by = 3

    def get_queryset(self):
        queryset = Post.published.all()

        tag_slug = self.kwargs.get("tag_slug")
        if tag_slug:
            self.tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags__in=[self.tag])
        else:
            self.tag = None

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["section"] = "blog"
        context["tag"] = self.tag
        return context


class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "blog/detail.html"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Post.objects.filter(
            published_at__year=self.kwargs["year"],
            published_at__month=self.kwargs["month"],
            published_at__day=self.kwargs["day"],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["section"] = "blog"
        context["comments"] = self.object.comments.filter(active=True)
        post_tags_pks = self.object.tags.values_list("pk", flat=True)
        similar_posts = (
            Post.published.filter(tags__in=post_tags_pks)
            .exclude(pk=self.object.pk)
            .annotate(same_tags=Count("tags"))
            .order_by("-same_tags", "-published_at")
        )
        context["similar_posts"] = similar_posts[:3]

        context["form"] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    context_object_name = "post"
    template_name = "blog/new.html"
    fields = ("title", "content", "published_at", "status", "tags")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    context_object_name = "post"
    template_name = "blog/edit.html"
    fields = ("title", "content", "published_at", "status", "tags")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    context_object_name = "post"
    template_name = "blog/delete.html"
    success_url = reverse_lazy("blog:post_list")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostShareView(LoginRequiredMixin, FormView):
    form_class = EmailPostForm
    template_name = "blog/share.html"

    def dispatch(self, request, *args, **kwargs):
        self.post_obj = get_object_or_404(
            Post,
            pk=kwargs["pk"],
            status=Post.Status.PUBLISHED,
        )
        self.post_url = request.build_absolute_uri(self.post_obj.get_absolute_url())
        self.sent = False
        self.recipient = None
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = self.post_obj
        context["sent"] = self.sent
        context["recipient"] = self.recipient
        return context

    def form_valid(self, form):
        cd = form.cleaned_data
        subject = f"{cd['name']} ({cd['email']})"
        message = (
            f"Read {self.post_obj.title} at {self.post_url}\n\n"
            f"{cd['name']}'s message: {cd['message']}"
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=cd["email"],
            recipient_list=[cd["to"]],
        )
        self.sent = True
        self.recipient = cd["to"]
        return self.render_to_response(self.get_context_data(form=form))


class PostCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment.html"

    def dispatch(self, request, *args, **kwargs):
        self.post_obj = get_object_or_404(
            Post,
            pk=kwargs["pk"],
            status=Post.Status.PUBLISHED,
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["section"] = "blog"
        context["post"] = self.post_obj
        return context

    def form_valid(self, form):
        form.instance.post = self.post_obj
        form.instance.name = self.request.user.username
        form.instance.email = self.request.user.email
        return super().form_valid(form)

    def get_success_url(self):
        return self.post_obj.get_absolute_url()


class PostSearch(View):
    form_class = SearchForm
    template_name = "blog/search.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.GET or None)

        if form.is_valid():
            cd = form.cleaned_data

            search_vector = SearchVector(
                "title", weight="A", config="english"
            ) + SearchVector("content", weight="B", config="english")
            search_query = SearchQuery(cd["query"], config="english")
            results = (
                Post.published.annotate(
                    search=search_vector, rank=SearchRank(search_vector, search_query)
                )
                .filter(rank__gte=0.1)
                .order_by("-rank")
            )

            return render(
                request,
                self.template_name,
                {"query": cd["query"], "results": results, "section": "blog"},
            )

        return render(request, self.template_name, {"form": form, "section": "blog"})


class PostSearchTrigramSimilarity(View):
    form_class = SearchForm
    template_name = "blog/search.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.GET or None)

        if form.is_valid():
            cd = form.cleaned_data

            results = (
                Post.published.annotate(
                    similarity=TrigramSimilarity("title", cd["query"])
                )
                .filter(similarity__gt=0.1)
                .order_by("-similarity")
            )

            return render(
                request,
                self.template_name,
                {"query": cd["query"], "results": results, "section": "blog"},
            )

        return render(request, self.template_name, {"form": form, "section": "blog"})
