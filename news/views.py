from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from news.filters import NewsFilter
from news.forms import PostForm
from news.models import Post, PostCategory, Category


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


class PostsDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostsCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    def form_valid(self, form):
        if self.request.path.endswith('create/article/'):
            form.instance.type_choice = Post.ARTICLE
        if self.request.path.endswith('create/news/'):
            form.instance.type_choice = Post.NEWS

        response = super().form_valid(form)

        categories = self.request.POST.getlist('category')

        for category_id in categories:
            category = Category.objects.get(id=category_id)
            self.object.category.add(category)

        return response


class PostsUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['content', 'title']
    template_name = 'post_create.html'
    success_url = reverse_lazy('post_list')


class PostsDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

