from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from news.filters import NewsFilter
from news.forms import PostForm
from news.models import Post


class PostsList(ListView):
    model = Post
    ordering = 'time_created'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostsDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    def form_valid(self, form):
        if self.request.path.endswith('create/article/'):
            form.instance.type_choice = Post.ARTICLE
        if self.request.path.endswith('create/news/'):
            form.instance.type_choice = Post.NEWS

        response = super().form_valid(form)

        return response


class PostsUpdate(UpdateView):
    model = Post
    fields = ['content', 'title']
    template_name = 'post_create.html'
    success_url = "/"


class PostsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
