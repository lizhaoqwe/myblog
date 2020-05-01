from django.shortcuts import render
from django.views import View
from apps.articles.models import ArticleCategory,Articles,Comment
from utils import restful
import os
from django.conf import settings
from .forms import WriteArticlesForm
from django.views.decorators.http import require_POST,require_GET
from apps.articles.serializers import ArticleSerializer
from datetime import datetime
from django.utils.timezone import make_aware
from django.core.paginator import Paginator
from urllib import parse


def login_view(request):
    return render(request, 'cms/login.html')

def index(request):
    return render(request, 'cms/index.html')

class ArticleList(View):
    def get(self,request):
        page = int(request.GET.get('p', 1))
        start = request.GET.get('start')
        end = request.GET.get('end')
        title = request.GET.get('title')
        category_id = int(request.GET.get('category',0) or 0)
        articles = Articles.objects.all()
        if start or end:
            if start:
                starttime = datetime.strptime(start, '%Y/%m/%d')
            else:
                starttime = datetime(year=2020, month=4, day=14)
            if end:
                endtime = datetime.strptime(end, '%Y/%m/%d')
            else:
                endtime = datetime.today()
            articles = articles.filter(pub_time__range=(make_aware(starttime), make_aware(endtime)))
        if title:
            articles = articles.filter(title__icontains=title)
        if category_id:
            articles = articles.filter(category_id=category_id)
        paginator = Paginator(articles, 10)
        page_obj = paginator.page(page)
        context_obj = self.get_pagination_data(paginator, page_obj, 10)
        categories = ArticleCategory.objects.all()
        context = {
            'start': start,
            'end': end,
            'title': title,
            'category': category_id,
            'articles': page_obj.object_list,
            'categories': categories,
            'page_obj': page_obj,
            'paginator': paginator,
            'url_query': '&'+parse.urlencode({
                'start': start or '',
                'end': end or '',
                'title': title or '',
                'category': category_id or ''
            })
        }
        context.update(context_obj)
        return render(request, 'cms/articles_list.html',context=context)
    def get_pagination_data(self,paginator,page_obj,around_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages
        left_has_more = False
        right_has_more = False

        if current_page <= around_count +2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page-around_count,current_page)
        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page+1,num_pages+1)
        else:
            right_has_more = True
            right_pages = range(current_page+1,current_page+around_count+1)
        return {
            'current_page':current_page,
            'left_pages': left_pages,
            'right_pages': right_pages,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'num_pages': num_pages
        }

class ArticlesView(View):
    def get(self,request):
        categories = ArticleCategory.objects.all()
        articles = Articles.objects.all()
        context = {
            'categories': categories,
            'articles': articles,
        }
        return render(request, 'cms/write_articles.html', context=context)
    def post(self,request):
        form = WriteArticlesForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            category_id = form.cleaned_data.get('category')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            Articles.objects.create(title=title,category_id=category_id,desc=desc,thumbnail=thumbnail,content=content,author=request.user)
            return restful.ok()
        else:
            return restful.params_error(form.get_errors())


class CategoryView(View):
    def get(self,request):
        categories = ArticleCategory.objects.all()
        context = {
            'categories': categories
        }
        return render(request, 'cms/category.html', context=context)
    def post(self,request):
        name = request.POST.get('name')
        if name:
            ArticleCategory.objects.create(name=name)
            return restful.ok()
        else:
            return restful.params_error(message='没有获取到分类名称')

@require_POST
def upload(request):
    file = request.FILES.get('file')
    name = file.name
    with open(os.path.join(settings.MEDIA_ROOT, name), 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)
    url = request.build_absolute_uri(settings.MEDIA_URL + name)
    return restful.result(data={'url': url})

def delete(request):
    article_id = request.POST.get('news_id')
    Articles.objects.get(pk=article_id).delete()
    return restful.ok()


class EditArticle(View):
    def get(self,request,article_id):
        article = Articles.objects.get(pk=article_id)
        category = ArticleCategory.objects.all()
        context = {
            'article':article,
            'category': category
        }
        return render(request, 'cms/write_articles.html',context=context)
    def post(self,request,article_id):
        form = WriteArticlesForm(request.POST)
        print(form.errors)
        if form.is_valid():
            print(111)
            pk = form.cleaned_data.get('pk')
            title = form.cleaned_data.get('title')
            category_id = form.cleaned_data.get('category')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            Articles.objects.filter(pk=pk).update(title=title,
                                                          category_id=category_id,
                                                          desc=desc,
                                                          thumbnail=thumbnail,
                                                          content=content,
                                                          author=request.user)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())