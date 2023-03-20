from django.contrib import admin
from news.forms import PostForm, CategoryForm

from news.models import Post, Category


class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm


class PostAdmin(admin.ModelAdmin):
    form = PostForm
    filter_horizontal = ('category',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
