from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from news.filters import NewsFilter
from news.forms import PostForm
from news.models import Post, PostCategory, Category, Subscription


@login_required
def subscribe(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        subscription = Subscription(user=request.user.author, category=category)
        subscription.save()
        messages.success(request, f"You have subscribed to {category.category_name} category.")
        return redirect('subscribe')

    categories = Category.objects.all()
    subscriptions = Subscription.objects.filter(user=request.user.author)

    context = {
        'categories': categories,
        'subscriptions': subscriptions
    }

    return render(request, 'subscribe.html', context)


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

        # Send email notification to subscribers of the category
        for author in category.subscribers.all():
            send_mail(
                    subject='New post in subscribed category',
                    message=f'A new post "{self.object.title}" has been created in the category "{category.category_name}".',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[author.name.email],
                )

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

