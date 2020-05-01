
from django.contrib import admin
from django.urls import path,include
from . import views
app_name = 'cms'
urlpatterns = [
    path('index/',views.index, name='index'),
    path('write_articles/',views.ArticlesView.as_view(), name='write_articles'),
    path('category/',views.CategoryView.as_view(), name='category'),
    path('articles_list/',views.ArticleList.as_view(), name='articles_list'),
    path('login/',views.login_view, name='login'),
    path('upload/',views.upload, name='upload'),
    path('delete/',views.delete, name='delete'),
    path('edit/<article_id>', views.EditArticle.as_view(), name='edit')

]
