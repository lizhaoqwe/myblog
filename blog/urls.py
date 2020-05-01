from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from apps.articles import views
urlpatterns = [
    path('', views.index,name='index'),
    path('articles/', include('apps.articles.urls') ),
    path('cms/', include('apps.cms.urls')),
    path('auth/', include('apps.userauth.urls')),
    path('ueditor/', include('apps.ueditor.urls')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
