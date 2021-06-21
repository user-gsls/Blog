from django.utils.deprecation import MiddlewareMixin

login_list=['user/center',]

class MiddleWare1(MiddlewareMixin):
    def process_request(selfself,request):
