from django.shortcuts import render
from utils import restful
from .models import Articles,ArticleCategory
from django.conf import settings
from .serializers import ArticleSerializer
def index(request):
    count = settings.ARTICLE_PAGE
    articles = Articles.objects.all()[0:count]
    categories = ArticleCategory.objects.all()
    context = {
        'articles': articles,
        'categories': categories
    }
    return render(request, 'front/index.html',context=context)
def article_list(request):
    page = int(request.GET.get('p',1))
    category_id = int(request.GET.get('category_id',0))
    print(category_id)
    start = (page-1)*settings.ARTICLE_PAGE
    end = start + settings.ARTICLE_PAGE
    if category_id == 0:
        articles = Articles.objects.all()[start: end]
    else:
        articles = Articles.objects.filter(category_id=category_id)[start:end]
    serializer = ArticleSerializer(articles,many=True)
    print(serializer.data)
    return restful.result(data=serializer.data)

def blog(request):
    return render(request, 'front/blog.html')

def detail(request,article_id):
    article = Articles.objects.get(pk=article_id)
    categories = ArticleCategory.objects.all()
    context = {
        'article': article,
        'categories': categories
    }
    return render(request, 'front/post.html', context=context)