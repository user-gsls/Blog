

#发送邮件
import uuid
# from locale import str


from django.core.mail import send_mail

from Blog.settings import EMAIL_HOST_USER
from .models import UserProfile


def send_email(email,request):
    subject='找回密码'
    user = UserProfile.objects.filter(email=email).first()
    ran_code = uuid.uuid4()#产生随机数码
    ran_code = str(ran_code)
    ran_code= ran_code.replace('-','')
    request.session[ran_code]=user.id

    message = '''
    尊敬的用户：
            您好！此链接找回密码，请点击链接: http://127.0.0.1:8000/user/update_pwd?c=%s 更新密码
            
            
    '''%(ran_code)
    result = send_mail(subject,message,EMAIL_HOST_USER,[email,])
    return result
