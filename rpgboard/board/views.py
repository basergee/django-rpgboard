from django.shortcuts import render
from django.views.generic import ListView

from .models import Post


class IndexView(ListView):
    template_name = 'default.html'
    model = Post
    context_object_name = 'posts_list'
    # Ограничиваем количество новостей на странице
    paginate_by = 10
