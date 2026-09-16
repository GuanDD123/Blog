from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, FormView, ListView

from .forms import CommentForm, EmailPostForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.filter(active=True)
        context["form"] = CommentForm()
        return context


class PostShareView(FormView):
    template_name = "blog/post/share.html"
    form_class = EmailPostForm

    def dispatch(self, request, *args, **kwargs):
        self.post_obj = get_object_or_404(
            Post,
            id=kwargs["post_id"],
            status=Post.Status.PUBLISHED,
        )
        self.post_url = request.build_absolute_uri(self.post_obj.get_absolute_url())
        self.sent = False
        self.recipient = None
        return super().dispatch(request, *args, **kwargs)

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = self.post_obj
        context["sent"] = self.sent
        context["recipient"] = self.recipient
        return context


class PostCommentView(FormView):
    template_name = "blog/post/comment.html"
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.post_obj = get_object_or_404(
            Post,
            id=kwargs["post_id"],
            status=Post.Status.PUBLISHED,
        )
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.post_obj.get_absolute_url()

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.post_obj
        comment.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = self.post_obj
        return context
