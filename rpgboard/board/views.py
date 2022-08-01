from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from .models import Post, UserReply
from .forms import ReplyForm, PostForm


class IndexView(ListView):
    template_name = 'default.html'
    model = Post
    context_object_name = 'posts_list'
    # Ограничиваем количество новостей на странице
    paginate_by = 10


class CreateUserReplyView(CreateView):
    model = UserReply
    form_class = ReplyForm
    template_name = 'reply_create.html'
    success_url = '/'

    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.reply_author = self.request.user
        post_id = int(self.request.path.split('/')[-1])
        reply.post = Post.objects.get(pk=post_id)
        response = super().form_valid(form)
        return response


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'
    success_url = '/'
    login_url = '/login/'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        response = super().form_valid(form)
        return response


class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'
    success_url = '/'
    login_url = '/login/'
