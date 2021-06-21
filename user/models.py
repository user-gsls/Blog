from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class UserProfile(AbstractUser):
    description = models.CharField(max_length=50,verbose_name="个人介绍",default=" ")
    job = models.CharField(max_length=10,verbose_name="职业",default=" ")
    icon = models.ImageField(upload_to='uploads/%Y/%M/%D',default='uploads/comment/mine1.jpg')

    class Meta:
        db_table = 'userprofile'
        verbose_name = "用户表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

class Wordcloud(models.Model):

    content = models.TextField(verbose_name="内容")
    background = models.ImageField(upload_to='uploads/wordcloud/background', verbose_name='背景图片',default="media/uploads/wordcloud/cy.jpg")


    class Meta:
        db_table = 'wordcloud'
        verbose_name = '词云表'
        verbose_name_plural = verbose_name