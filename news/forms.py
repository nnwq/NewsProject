from django import forms
from django.core.exceptions import ValidationError
from news.models import Post, Category


class PostForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Post
        fields = ('title', 'author', 'type_choice', 'content')

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if title is not None and len(title) < 5:
            raise ValidationError({
                "description": "Title cannot contain less than 5 symbols."
            })

        return cleaned_data

    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()
            self.save_m2m()
        return post


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name',)
