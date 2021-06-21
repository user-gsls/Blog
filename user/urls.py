from django.urls import path
from . import views
app_name='User'

urlpatterns = [
    path('register',views.user_register,name = 'register'),
    path('login',views.user_login,name = 'login'),
    path('logout',views.user_logout,name='logout'),
    path('forget_pwd',views.forget_password,name='forget_pwd'),
    path('valide_code',views.valide_code,name='valide_code'),
    path('update_pwd',views.update_pwd,name='update_pwd'),
    path('user_center',views.user_center,name='user_center'),
    path('user_change',views.user_change,name='user_change'),
    path('tag_articles',views.tag_articles,name='tag_articles'),
    path('music',views.music,name='music'),
    path('overturn',views.overturn,name='overturn'),
    path('ball',views.ball,name='ball'),
    path('wordcloud',views.wordcloud,name='wordcloud'),

]