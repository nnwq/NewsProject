from django_filters import FilterSet
from news.models import Post


class NewsFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'category': ['icontains'],
        }
