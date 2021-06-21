
from django.contrib import admin

# Register your models here.
from .models import Article, Tag,Comment

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['user','title','date','love_num','click_num']#显示的文章信息
    search_fields = ['id','title']#可以根据标签进行检索
    list_editable = ['click_num','love_num']#对标签进行编辑
    list_filter = ['date']#过滤器

class CommentAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'content', 'date']

admin.site.register(Article,ArticleAdmin)
admin.site.register(Tag)
admin.site.register(Comment,CommentAdmin)
