# -*-coding:utf-8 -*-
# from builtins import Exception

from captcha.models import CaptchaStore
from django.contrib import auth
from django.contrib.auth import logout, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect



from django.contrib.auth import get_user_model

from article.models import Article,Tag
from matplotlib import colors

UserModel = get_user_model()


# Create your views here.


from django.urls import reverse
from .forms import UserRegisterForm, WordcloudForm

from .forms import RegisterForm

from .models import UserProfile
from .tool import send_email
from .forms import LoginForm, CaptchaTestForm,WordcloudForm

#制作词云所需库
import os
import jieba
import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS

#网站主页
def home(request):
    return render(request,'home.html')

# 博客主页
def index(request):
    far_articles = Article.objects.all().order_by('-click_num')[:5]#点击量前五
    dararticles = Article.objects.all().order_by('-date')#按时间排序
    paginator = Paginator(dararticles,6)#分页器，每5个一页（对象列表，每页几条记录）
    # paginator.count #总的记录数
    # paginator.num_pages#可以分页的数量
    # paginator.page_range#页面的范围
    tags = Tag.objects.filter()

    page = request.GET.get('page',1)
    page = paginator.get_page(page)
    # page.has_next()#判断有没有下一页
    # page.has_previous()#判断有没有上一页
    # page.next_page_number()#获取下一页的页码数
    # page.previous_page_number()#获取上一页的页码数

    #page属性
    #object_list 当前页的所有对象
    # number     当前的页码书
    #paginator   分页器对象

    return render(request, 'index.html',context={'page':page,
                                                 'far_articles':far_articles,
                                                 'dararticles':dararticles,
                                                 'tags':tags})


# 用户的注册
def user_register(request):
    if request.method == 'GET':
        reform = RegisterForm()
        return render(request, 'user/register.html')

    else:
        reform = RegisterForm(request.POST)  # 使用form获取数据
        # 校验username，user\forms.clean_username
        if reform.is_valid():
            # 从干净的数据中取值
            username = reform.cleaned_data.get('username')
            email = reform.cleaned_data.get('email')
            # mobile = reform.cleaned_data.get('mobile')
            password = reform.cleaned_data.get('password')
            # 查询数据库是否已经存在账号
            if not UserProfile.objects.filter(Q(username=username) | Q(email=email)).exists():
                # 注册到数据库
                password = make_password(password)#对密码进行加密
                user = UserProfile.objects.create(username=username, password=password, email=email)
                if user:
                    return redirect(reverse('user:login'))
            else:
                return render(request, 'user/register.html', context={'msg': '名称或邮箱已存在！'})

        return render(request, 'user/register.html', context={'msg': '名称或邮箱已存在！'})


# 用户的登录
def user_login(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')
    else:
        reform = LoginForm(request.POST)
        if reform.is_valid():
            email = reform.cleaned_data.get('email')
            password = reform.cleaned_data.get('password')
            # 进行数据库的查询，校验密码
             #第一种方法
            # user = UserProfile.objects.filter(email=email).first()
            # print(user,user.password)
            # flag = check_password(password, user.password)  # 密码校验
            # print(flag,"123")
            # if flag:
            #     #保存session信息，提取用户名称
            #     username = user.username
            #     email = user.email
            #     icon = str(user.icon)
            #     request.session['username'] = username
            #     request.session['email'] = email
            #     request.session['icon'] = icon
            # 方式二 前提是继承了AbstracUser
            authentication = CustomModelBackend()
            user = authentication.authenticate(request,username=email, password=password)
            if user:
                login(request, user)  # 将用户对象保存在底层的request中
                return redirect(reverse('home'))
            return render(request, 'user/login.html', context={'error': "密码错误！"})
        return render(request, 'user/login.html', context={'error': "用户不存在！"})


# 用户的注销
def user_logout(request):
    # request.session.clean()#删除字典
    # request.session.flush()#删除django_session+cookie+字典
    logout(request)  # 底层已经封装好
    return redirect(reverse('home'))


# 忘记密码
def forget_password(request):
    if request.method == 'GET':
        form = CaptchaTestForm()
        return render(request, 'user/forget_pwd.html', context={'form': form})
    else:
        # 获取提交的邮箱，发送邮件，通过发送的邮箱链接设置新的密码
        email = request.POST.get('email')
        # 给此邮件地址发送邮件
        result = send_email(email, request)
        if result:
            return HttpResponse("邮件发送成功！赶快去邮箱修改密码<a href='/'>返回首页>>></a>")


# 更新密码
def update_pwd(request):
    if request.method == 'GET':
        c = request.GET.get('c')
        return render(request, 'user/update_pwd.html', context={'c': c})
    else:
        code = request.POST.get('code')
        print(code)
        uid = request.session.get(code)
        print(uid)
        user = UserProfile.objects.get(pk=uid)
        # 获取密码
        pwd = request.POST.get('password')
        repwd = request.POST.get('repassword')
        if pwd == repwd and user:
            pwd = make_password(pwd)
            user.password = pwd
            user.save()
            return render(request, 'user/update_pwd1.html', context={'msg': '密码更新成功!'})
        else:
            return render(request, 'user/update_pwd.html', context={'msg': '更新失败！请重试'})


# 定义一个路由验证验证码
def valide_code(request):
    if request.is_ajax():
        key = request.GET.get('key')
        code = request.GET.get('code')

        captcha = CaptchaStore.objects.get(hashkey=key)
        # captcha1 = model_to_dict(captcha)
        # print(captcha,type(captcha))
        if captcha.response == code.lower():
            # 正确
            data = {'status': 1}
        else:
            # 错误
            data = {'status': 0}
        return JsonResponse(data)


# 用户中心
@login_required
def user_center(request):
    user = request.user
    id = user.id
    articles = Article.objects.filter(user_id=id)

    # 将用户相关的标签全部找出
    tag_list=[]
    for article in articles:
        tags_all = article.tags.all()
        for tag in tags_all:
            if tag not in tag_list:
                tag_list.append(tag)

    paginator = Paginator(articles, 4)
    page = request.GET.get('page', 1)
    page = paginator.get_page(page)

    return render(request, 'user/user_center.html',context={"user": user,
                                                            'page':page,
                                                            'tag_list':tag_list,})


# 关于我
def about_myself(request):
    user = request.user
    return render(request,'about_myself.html',context={"user": user})


# 用户修改个人信息
@login_required
def user_change(request):
    user = request.user
    if request.method == 'GET':

        return render(request, 'user/user_change.html', context={"user": user})
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        job = request.POST.get('job')
        description = request.POST.get('description')
        icon = request.FILES.get('icon')

        user.username= username
        user.email = email
        user.description = description
        user.job = job
        user.icon = icon
        user.save()
        return render(request, 'user/user_center.html', context={"user": user})

#关于标签的文章页面
def tag_articles(request):
    tid = request.GET.get("tid",'')#null
    id = tid[:1]
    if tid:
        tag = Tag.objects.get(pk=tid)
        articles = tag.article_set.all()
    else:
        articles = Article.objects.all()

    tag_name = tag.name
    paginator = Paginator(articles, 4)
    page = request.GET.get('page', 1)
    page = paginator.get_page(page)


    return render(request,'article/tag_articles.html',context={'page':page,'tag_name':tag_name,'tid':id})


#share页面
def share(request):
    far_articles = Article.objects.all().order_by('-click_num')[:5]# 点击量前五
    tags = Tag.objects.filter()
    return render(request,'share.html',context={'far_articles':far_articles,'tags':tags})

#音乐播放器
def music(request):
    return render(request,'share/music.html')

#旋转特效
def overturn(request):
    return render(request,'share/overturn.html')

#波纹小球
def ball(request):
    return render(request,'share/ball.html')

#界面词云生成
def wordcloud(request):
    if request.method == 'GET':
        return render(request, 'share/wordcloud.html')
    else:
        form = WordcloudForm(request.POST)
        # print(form)
        if form.is_valid():
            form = form.cleaned_data
            text = str(form.get('content'))
            background = os.path.realpath(form.get('background'))#获取背景相对路径
            color1 = str(form.get('color1'))
            color2 = str(form.get('color2'))
            print(color1,color2)
            mask = np.array(Image.open(background))
            word_list = jieba.cut(text,cut_all=True)#分词
            result = " ".join(word_list)

            color_list = [color1, color2]  # 建立颜色数组
            colormap = colors.ListedColormap(color_list)  # 调用
            ##词云
            wordcloud = WordCloud(
                mask=mask,
                font_path="C:\Windows\Fonts\STXINGKA.TTF",
                background_color='white',
                max_words=2000,
                max_font_size=1000,
                # min_font_size=40,
                # random_state=42,
                # prefer_horizontal=0.8,
                colormap =colormap,
            ).generate(result)
            name = text[:2]
            path = os.path.dirname(background)
            wordcloud.to_file(path + '/' + name +'.jpg')
            return render(request,'share/wordcloud.html',context={'name':name})
        else:
            print('发表失败')
            return render(request,'share/wordcloud.html',context={'msg':'操作失败！'})





#自定义authenticate
class CustomModelBackend(ModelBackend):  # 继承ModelBackend类，重写authenticate()方法
    """
    自定义用户验证后端：支持用户名或邮箱登录。
    """
    def authenticate(self,request,username=None, password=None,**kwargs): # 参数username实际是用户输入的登录账号
        try:
            # Q(username=username) | Q(email=username)，的意思是起到并集作用，只要第一个查到就不会查第二个，第一个没查到就会查第二个
            user = UserProfile.objects.get(email=username)
            # print(user, user.password)
            flag = check_password(password, user.password)  # 密码校验
            print(user.username,user.password,flag)
            if flag:
                return user
        except Exception as e:
            return None

