from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (ListView, CreateView, UpdateView, DeleteView,
                                  FormView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

from .models import Post, UserReply
from .forms import ReplyForm, PostForm, UserSignupForm, UserConfirmCodeForm


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
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.reply_author = self.request.user
        post_id = int(self.request.path.split('/')[-1])
        reply.post = Post.objects.get(pk=post_id)
        response = super().form_valid(form)
        return response


class DeleteUserReplyView(DeleteView):
    model = UserReply
    template_name = 'reply_delete.html'
    success_url = reverse_lazy('profile')


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'
    success_url = reverse_lazy('index')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        response = super().form_valid(form)
        return response


class EditPostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'
    success_url = reverse_lazy('index')
    login_url = reverse_lazy('login')

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


class UserSignupView(CreateView):
    model = User
    form_class = UserSignupForm
    template_name = 'signup.html'
    success_url = reverse_lazy('confirm_code')


class UserConfirmCodeView(FormView):
    template_name = 'confirm.html'
    form_class = UserConfirmCodeForm
    success_url = reverse_lazy('index')


class UserProfileView(LoginRequiredMixin, ListView):
    template_name = 'profile.html'
    context_object_name = 'replies_list'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        # Показать отклики на посты, у которых пользователь является автором
        logged_user = self.request.user
        return UserReply.objects.filter(post__author=logged_user)


def accept_reply(request, **kwargs):
    reply_id = request.path.split('/')[-1]
    reply = UserReply.objects.get(pk=reply_id)
    reply.is_accepted = True
    reply.save()
    return redirect('profile')
