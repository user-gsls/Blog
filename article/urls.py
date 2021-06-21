from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from article import views

app_name='article'


urlpatterns = [
    path('datail',views.article_details,name='detail'),
    path('write',views.write_article,name='write'),
    path('comment',views.article_comment,name='comment'),
    path('search',views.search,name='search'),
]