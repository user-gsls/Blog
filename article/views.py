from django.contrib.auth.decorators import login_required
from django.core.checks import Tags
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from user.models import UserProfile
from .forms import ArticleForm
from .models import Article, Tag, Comment


# 文章详情
def article_details(request):
    far_articles = Article.objects.all().order_by('-click_num')[:3]  # 点击量前五
    # tags = Tag.objects.filter()
    id = request.GET.get('id')
    article = Article.objects.get(pk=id)
    author_id = article.user_id
    author = UserProfile.objects.get(id=author_id)
    # print(article.title)
    article.click_num += 1
    article.save()
    # 查询相关文章
    tags_all = article.tags.all()  # 获取文章相关的标签
    list_about = []  # 存放文章的列表
    for tag in tags_all:
        for article1 in tag.article_set.all():
            if article1 not in list_about and len(list_about) < 6:
                list_about.append(article1)

    # 评论
    comments = Comment.objects.filter(article_id=id)


    return render(request, 'article/info.html', context={'article': article,
                                                         'list_about': list_about,
                                                         'comments':comments,
                                                         'far_articles':far_articles,
                                                         'tags_all':tags_all,
                                                         'author':author,})


# 文章分页
# def article_show(request):
#     id = request.GET.get('id')
#     articles = Article.objects.all().get(pk=id)
#     tags = Tag.objects.all()[:6]
#     # articles = Article.objects.all()
#     return render(request, 'user/user_center.html', context={'articles': articles, 'tags': tags})


# 博客编写页面
@login_required
def write_article(request):
    if request.method == 'GET':
        aform = ArticleForm()

        return render(request, 'article/write.html', context={'form': aform})
    else:
        aform = ArticleForm(request.POST)
        print(aform)
        if aform.is_valid():
            data = aform.cleaned_data
            article1 = Article()
            article1.title = data.get('title')
            article1.desc = data.get('desc')
            article1.content = data.get('content')
            # article.click_num = data.get('click_num')
            # article.love_num = data.get('love_num')
            article1.image = data.get('image')
            article1.user = request.user  # 一对多 直接赋值
            article1.save()

            # 数据库多对多，且保存之后才添加
            article1.tags.set(data.get('tags'))
            return redirect(reverse('index'))
        else:
            print('发表失败')
        return HttpResponse("failure")


# 文章评论
def article_comment(request):
    # 直接接受
    content = request.GET.get('saytext')
    if content== '':
        return 0
    aid = request.GET.get('aid')
    nickname = request.user
    image = request.user.icon

    comment = Comment.objects.create(nickname=nickname, content=content, article_id=aid,image = image)

    if comment:
        data = {'status': 1}
    else:
        data = {'status': 0}
    # print(data)
    return JsonResponse(data)

#搜索界面
def search(request):
    q = request.GET.get('search_word')
    error_msg = ''
    articles = []

    if Tag.objects.filter(Q(name=q)).exists() or Article.objects.filter(Q(title__icontains=q)).exists():
        if Tag.objects.filter(Q(name=q)).exists():
            tag = Tag.objects.get(name=q)
            articles1 = tag.article_set.all()
            articles.extend(articles1)
        if Article.objects.filter(Q(title__icontains=q)).exists():
            articles2 = Article.objects.filter(title__icontains=q)
            print(articles2)
            articles.extend(articles2)
    else:
        error_msg = '无搜索结果，请重新搜索！'
    return render(request, 'article/search_articles.html', {'error_msg': error_msg,'articles':articles,'search_word':q})
