from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db import IntegrityError 
from django.core.validators import validate_email, ValidationError
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from contents.models import Content, Image, FollowRelation
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

class NoneUserTemplateView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            return redirect('content_home')
        return super(NoneUserTemplateView, self).dispatch(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class ContentCreateView(BasicView):
    def post(self, request):
        text = request.POST.get('text','').strip()
        content = Content.objects.create(user=request.user, text=text)
        for idx, file in enumerate(request.FILES.values()):
            Image.objects.create(content=content, image=file, order=idx)
        
        return self.response()

@method_decorator(login_required, name='dispatch')
class RelationView(TemplateView):

    template_name = 'relation.html'

    def get_context_data(self, **kwargs):
        context = super(RelationView, self).get_context_data(**kwargs)

        user = self.request.user

        # 내가 팔로우하는 사람들
        try:
            followees = FollowRelation.objects.get(follower=user).followee.all()
            context['followees'] = followees
            context['followees_ids'] = list(followees.values_list('id', flat=True))
            
        except FollowRelation.DoesNotExist:
            pass

        try:
            context['followers'] = FollowRelation.objects.filter(followee=user)
        except FollowRelation.DoesNotExist:
            pass

        return context

@method_decorator(login_required, name='dispatch')
class RelationCreateView(BasicView):
    def post(self, request):
        try:
            user_id = request.POST.get('id','')
        except ValueError:
            return self.response(message='잘못된 요청입니다.', status=400)
    
        try:
            relation = FollowRelation.objects.get(follower=request.user)
        except FollowRelation.DoesNotExist:
            relation = FollowRelation.objects.create(follower=request.user)

        try:
            if user_id == request.user.id:
                # 자기 자신은 팔로우 안됨.
                raise IntegrityError
            relation.followee.add(user_id)
            relation.save()
        except IntegrityError:
            return self.response(message='잘못된 요청입니다.')

        return self.response({})


@method_decorator(login_required, name='dispatch')
class RelationDeleteView(BasicView):
    def post(self, request):
        try:
            user_id = request.POST.get('id','')
        except ValueError:
            return self.response(message="잘못된 요청입니다.", status=400)
        
        try:
            relation = FollowRelation.objects.get(follower=request.user)
        except FollowRelation.DoesNotExist:
            return self.response(message='잘못된 요청입니다.', status=400)
        
        try:
            if user_id == request.user.id:
                raise IntegrityError
            relation.followee.remove(user_id)
            relation.save()
        except IntegrityError:
            return self.response(message="잘못된 요청입니다.", status=400)

        return self.response({})