from django.views.generic import DetailView, ListView

from .models import Post


class PostListView(ListView):
    model = Post
    template_name = "blog/post/list.html"
    context_object_name = "posts"
    paginate_by = 3

    def get_queryset(self):
        return Post.published.all()


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post/detail.html"
    context_object_name = "post"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Post.objects.filter(
            status=Post.Status.PUBLISHED,
            published_at__year=self.kwargs["year"],
            published_at__month=self.kwargs["month"],
            published_at__day=self.kwargs["day"],
        )
