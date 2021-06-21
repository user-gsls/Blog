import re

from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError
from django.forms import Form, forms, ModelForm, EmailField
from django import forms

from .models import UserProfile, Wordcloud


#使用Form方法定义、查找 注册 字段
class UserRegisterForm(Form):
    username = forms.CharField(max_length=50,min_length=1,required=True,error_messages={'min_leagth':'名称长度至少一位'},label='用户名')
    email = forms.EmailField(required=True,error_messages={'require':'必须填写邮箱信息'},label="邮箱")
    #密码框（但一般用char，然后用插件定义passwordInput）
    password = forms.CharField(required=True,error_messages={'require':'必须填写密码'},label="密码",widget=forms.widgets.PasswordInput)
    # repassword = forms.CharField(required=True, error_messages={'require': '必须填写确认密码'}, label="确认密码",
    #                            widget=forms.widgets.PasswordInput)

    #校验username的条件
    def clean_username(self):
        username = self.clean_data.get('username')
        result = re.match(r'\w+{1,}',username)#正则表达式，username第一位必须是字母
        if not result:
            raise ValidationError('用户名必须字母开头')
        return username

#使用MobelForm方法定义、查找 注册 字段
class RegisterForm(ModelForm):
    repassword = forms.CharField(required=True, error_messages={'require': '必须填写确认密码'}, label="确认密码",
                                widget=forms.widgets.PasswordInput)
    class Meta:
        model = UserProfile#引入模型
        fields = ['username','email','password']


    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     result = re.match(r'\w{1,}',username)#正则表达式，username第一位必须是字母
    #     if not result:
    #         raise ValidationError('用户名必须字母开头')
    #     return username

#定义、查找 登录字段
class LoginForm(Form):
    email = forms.EmailField(required=True, error_messages={'require': '必须填写邮箱信息'}, label="邮箱")
    password = forms.CharField(required=True, error_messages={'require': '必须填写密码'}, label="密码",
                               widget=forms.widgets.PasswordInput)
    # class Meta:
    #     model = UserProfile
    #     fields = ['email','password']

    # def clean(self):
    #     email = self.cleaned_data.get('email')
    #     password = self.cleaned_data.get('password')
    #     if not UserProfile.objects.filter(email=email,password=password).exists():
    #         if not UserProfile.objects.filter(email=email).exists():
    #             raise  ValidationError('用户不存在!')
    #         else:
    #             raise ValidationError('密码错误!')
    #     else:
    #         pass
    #     return email

#验证码captcha的form
class CaptchaTestForm(forms.Form):
    email = EmailField(required=True,error_messages={'require':'必须填写邮箱信息'},label="邮箱")
    captcha = CaptchaField()

#词云的Form
class WordcloudForm(forms.ModelForm):
    # content = forms.CharField(required=True,label="内容")
    # background = forms.ImageField(required=False,label="背景")
    color1 = forms.CharField(required=True,label="起始色")
    color2 = forms.CharField(required=True, label="结束色")


    class Meta:
        model = Wordcloud
        fields = ['background','content']


        # 定义widgets，设置表单字段的CSS样式
        # widgets={
        #     'title':forms.TextInput(attrs={'class':'form-control','placeholder':'标题'}),
        #     'desc': forms.TextInput(attrs={'class':'form-control','placeholder':'简介'}),
        #     'tags':forms.SelectMultiple(attrs={'class':'form-control'}),
        # }


