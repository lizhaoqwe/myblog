from django.db import models
from apps.userauth.models import User



class ArticleCategory(models.Model):
    name = models.CharField(max_length=100)


class Articles(models.Model):
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    thumbnail = models.URLField()
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('ArticleCategory',on_delete=models.SET_NULL,null=True)
    author = models.ForeignKey('userauth.User',on_delete=models.SET_NULL,null=True)
    class Meta:
        ordering = ['-pub_time']

class Comment(models.Model):
    pub_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    author = models.ForeignKey('userauth.User',on_delete=models.CASCADE)
    article = models.ForeignKey('Articles',on_delete=models.CASCADE)
    class Meta:
        ordering = ['-pub_time']