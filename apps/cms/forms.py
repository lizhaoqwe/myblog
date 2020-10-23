from django import forms
from django.forms.models import ModelForm
from apps.forms import FormMixMin
from apps.articles.models import Articles,ArticleCategory
from apps.articles.serializers import CategorySerializer



class WriteArticlesForm(ModelForm,FormMixMin):
    category = forms.IntegerField()
    class Meta:
        model = Articles
        exclude = ['author','pub_time','category']
