from django import forms

from .models import Comment, Post


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content", "published_at", "status", "tags")


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content", "published_at", "status", "tags")


class PostShareForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    to = forms.EmailField()
    message = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)


class PostSearchForm(forms.Form):
    query = forms.CharField()
