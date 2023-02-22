from django.shortcuts import render
from django.views.generic import ListView, DetailView

from news.models import Post


class PostsList(ListView):
    model = Post
    ordering = 'time_created'
    template_name = 'news.html'
    context_object_name = 'news'


class PostsDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
