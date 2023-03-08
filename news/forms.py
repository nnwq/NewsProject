from django import forms
from django.core.exceptions import ValidationError
from news.models import Post, Category


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'author', 'type_choice', 'category', 'content')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name',)
