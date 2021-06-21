from django import forms

from .models import Article


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = '__all__'
        exclude = ['click_num','love_num','user']
        # labels设置HTML元素控件的label标签

        # 定义widgets，设置表单字段的CSS样式
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'标题'}),
            'desc': forms.TextInput(attrs={'class':'form-control','placeholder':'简介'}),
            'tags':forms.SelectMultiple(attrs={'class':'form-control'}),
        }
