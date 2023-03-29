from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

from django.urls import reverse


class Author(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    subscribed_to_categories = models.ManyToManyField('Category', related_name='subscribers', blank=True)

    def update_rating(self):
        for post in Post.objects.filter(author=self):
            self.rating += Post.rating*3
            for comment in Comment.objects.filter(post=post):
                self.rating += comment.rating
        for comment in Comment.objects.filter(user=self.name):
            self.rating += comment.rating
        self.save()

    def __str__(self):
        return f"{self.name}"


class Category(models.Model):
    category_name = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return f"{self.category_name}"


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    POST_CHOICES = [
        ('AR', 'Article'),
        ('NW', 'News')
    ]
    title = models.CharField(max_length=50, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type_choice = models.CharField(choices=POST_CHOICES, default='News', max_length=10)
    time_created = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    content = models.TextField(null=True, blank=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        self.content = self.content[0:50] + '...'
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.ForeignKey(Author, on_delete=models.CASCADE)
    text = models.CharField(default='An Upvote comment', max_length=255)
    time_created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class Subscription(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)