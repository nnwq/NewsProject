from django.urls import path
from news.views import PostsList, PostsDetail, PostsCreate

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('<int:pk>/', PostsDetail.as_view(), name='post_detail'),
    path('create/article/', PostsCreate.as_view(), name='post_create_article'),
    path('create/news/', PostsCreate.as_view(), name='post_create_news'),
]
