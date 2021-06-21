from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from user.models import UserProfile


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='标签名')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tag'
        verbose_name = '标签表'
        verbose_name_plural = verbose_name


class Article(models.Model):

    def __str__(self):
        return self.title

    title = models.CharField(max_length=100, verbose_name="标题")
    desc = models.CharField(max_length=256, verbose_name="简介")
    content = RichTextUploadingField(verbose_name="内容")
    date = models.DateField(auto_now_add=True, verbose_name='发表时间')
    click_num = models.IntegerField(default=0, verbose_name='点击量')
    love_num = models.IntegerField(default=0, verbose_name='点赞量')
    image = models.ImageField(upload_to='uploads/article/%y/%m/%d', verbose_name='文章图片',default="uploads/article/article.jpg")

    tags = models.ManyToManyField(to=Tag)
    user = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = 'article'
        verbose_name = '文章表'
        verbose_name_plural = verbose_name

#评论的模型
class Comment(models.Model):
    nickname = models.CharField(max_length=50,verbose_name='昵称')
    content = models.TextField(verbose_name="内容")
    date = models.DateTimeField(auto_now=True,verbose_name='评论时间')
    image = models.ImageField(upload_to='uploads/comment/', verbose_name='评论图片',
                              default='uploads/comment/mine1.jpg')

    article = models.ForeignKey(to=Article,on_delete=models.CASCADE,verbose_name='文章')

    def __str__(self):
        return self.nickname

    class Meta:
        db_table = 'comment'
        verbose_name = '评论表'
        verbose_name_plural = verbose_name
