from django import forms
from django.core.exceptions import ValidationError
from news.models import Post, Category


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'author', 'type_choice', 'category', 'content')

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if title is not None and len(title) < 5:
            raise ValidationError({
                "description": "Title cannot contain less than 5 symbols."
            })

        return cleaned_data


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name',)
