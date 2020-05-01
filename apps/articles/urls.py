
from django.contrib import admin
from django.urls import path,include
from . import views
app_name = 'article'
urlpatterns = [
    path('blog/', views.blog,name='blog'),
    path('detail/<int:article_id>', views.detail,name='detail'),
    path('article_list/', views.article_list,name='article_list'),
]
