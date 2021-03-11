from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db import IntegrityError 
from django.core.validators import validate_email, ValidationError
from django.contrib.auth import authenticate, login, logout
#IntegritError는 user model이 null 값을 가지고 있을 때를 의미한다.
# Create your views here.

class BasicView(View):
    @staticmethod
    def response(data={}, message='', status=200):
        result = {
            'data':data,
            'message': message,
        }
        return JsonResponse(result, status=status)

class UserCreateView(BasicView):
    #이것을 써주면 csrf_token으로 따로 써줄 필요가 없다.
    @method_decorator(csrf_exempt)

    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView,self).dispatch(request, *args, **kwargs)

    def post(self, request):
        #dictionary 메소드 .get의 두번째 인자는 default 값을 의미한다.
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        email = request.POST.get('email','')

        if not username:
            return self.response(message='아이디를 입력해주세요.', status=400)
        
        if not password:
            return self.response(message='비밀번호를 입력해주세요.', status=400)

        try:
            validate_email(email)
        except ValidationError:
            self.response(message='올바른 이메일을 입력해주세요.', status=400)

        try:
            user = User.objects.create_user(username, email, password)
        except IntegrityError:
            return self.response(message="이미 존재하는 아이디입니다.", status=400)

        return self.response({'user_id': user.id})

class UserLoginView(BasicView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(UserLoginView,self).dispatch(request, *args, **kwargs)
        
    def post(self, request):
        username = request.POST.get('username', '')
        if not username:
            return self.response(message='아이디를 입력해주세요.', status=400)
        password = request.POST.get('password', '')
        if not password:
            return self.response(message='비밀번호를 입력해주세요.', status=400)
        user = authenticate(request, username=username, password=password)

        if user is None:
            return self.response(message='입력 정보를 확인해주세요', status=400)
        login(request, user)

        return self.response()

class UserLogoutView(BasicView):
    def get(self, request):
        logout(request)
        return self.response()
