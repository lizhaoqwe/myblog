from rest_framework import serializers
from .models import Articles,ArticleCategory
from apps.userauth.serializers import UserSerializers

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = ['id', 'name']


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer()
    author = UserSerializers()
    class Meta:
        model = Articles
        fields = ['id','title','desc','thumbnail','category','pub_time','author']
