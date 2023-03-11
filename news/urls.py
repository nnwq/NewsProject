from django.urls import path
from news.views import PostsList, PostsDetail, PostsCreate, PostsUpdate, PostsDelete

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('<int:pk>/', PostsDetail.as_view(), name='post_detail'),
    path('create/article/', PostsCreate.as_view(), name='post_create_article'),
    path('create/news/', PostsCreate.as_view(), name='post_create_news'),
    path('update/news/<int:pk>', PostsUpdate.as_view(), name='post_update_news'),
    path('update/articles/<int:pk>', PostsUpdate.as_view(), name='post_update_article'),
    path('delete/news/<int:pk>', PostsDelete.as_view(), name='post_delete_news'),
    path('delete/articles/<int:pk>', PostsDelete.as_view(), name='post_delete_article')
]
