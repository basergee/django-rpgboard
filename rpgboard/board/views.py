from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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


class EditPostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'
    success_url = '/'
    login_url = '/login/'

    # Запрещаем авторизованному пользователю править объявления других
    # пользователей. Без этого пользователь мог указать ключ другого
    # пользователя в url и получить доступ к его объявлению.
    # Путь к странице имеет вид: /edit/5/, где 5 -- это ключ в
    # базе объявлений. Авторизованный пользователь должен иметь возможность
    # изменить только собственные объявления. Если он пробует получить доступ
    # к чужому, то будет ошибка '403 Forbidden'
    def test_func(self):
        # Узнаем ключ объявления, которое пытаемся редактировать
        post_id = int(self.request.path.split('/')[-1])

        # Получим все посты авторизованного в данный момент пользователя
        logged_user_posts = Post.objects.filter(author=self.request.user)

        # Если пост с ключом post_id есть среди них, разрешаем редактирование
        return logged_user_posts.filter(pk=post_id).exists()
