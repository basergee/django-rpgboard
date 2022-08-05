import logging
from datetime import datetime, timezone

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (ListView, CreateView, UpdateView, DeleteView,
                                  FormView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

from .models import Post, UserReply, UserConfirmCodes
from .forms import ReplyForm, PostForm, UserSignupForm, UserConfirmCodeForm
from .filters import UserReplyFilter


logger = logging.getLogger(__name__)


class IndexView(ListView):
    template_name = 'index.html'
    model = Post
    context_object_name = 'posts_list'
    # Ограничиваем количество новостей на странице
    paginate_by = 2
    ordering = '-creation_time'


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
        post.upload = self.request.FILES.get('upload')
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

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        logger.info("Подтвердите регистрацию, введя код из письма")
        return super().form_valid(form)


class UserConfirmCodeView(FormView):
    template_name = 'confirm.html'
    form_class = UserConfirmCodeForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        entered_code = form.cleaned_data['code']
        if UserConfirmCodes.objects.filter(code=entered_code).exists():
            code_obj = UserConfirmCodes.objects.get(code=entered_code)
            user = UserConfirmCodes.objects.get(code=entered_code).user
            if datetime.now(timezone.utc) <= code_obj.code_expires:
                # Активируем пользователя, для которого создан код
                user.is_confirmed = True
                user.is_active = True
                user.save()
                logger.info(user)
                logger.info('Регистрация прошла успешно')
            else:
                logger.info('Код подтверждения истек')
                # Удалим пользователя с этим кодом. Это решение принято для
                # простоты. В будущем стоит создавать новый код. Сейчас система
                # не даст отправить новый код, потому что пользователь уже
                # существует в базе
                logger.info(f'Удаляем неактивированного пользователя '
                            f'{user.username}')
                user.delete()
        else:
            logger.info('*** Неправильный код подтверждения ***')
        return super().form_valid(form)


class UserProfileView(LoginRequiredMixin, ListView):
    template_name = 'profile.html'
    context_object_name = 'replies_list'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        # Показать отклики на посты, у которых пользователь является автором
        logged_user = self.request.user
        queryset = UserReply.objects.filter(post__author=logged_user)

        # Даем возможность фильтровать отклики по статусы "принят/не принят"
        self.filterset = UserReplyFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


def accept_reply(request, **kwargs):
    reply_id = request.path.split('/')[-1]
    reply = UserReply.objects.get(pk=reply_id)
    reply.is_accepted = True
    reply.save()
    return redirect('profile')
