## Social NetWork Service(SNS) Web
## Chapter1. Base API View
#### apis/models.py
- 대부분의 모델 클래스들이 공통적인 모델 요소들을 가질 때 매번 모델의 필드를 선언해주는 것 보다는 BaseModel을 만들어 다른 모델 클래스에서 상속받는 것이 더 좋은 방법이다.
```python
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```
- 클래스 내부의 Meta 클래스는 클래스를 만드는 Inner Class 이다. Meta 클래스에 abstract = True 를 해줌으로서 BaseModel 클래스는 추상클래스로 취급된다. 추상클래스는 메서드의 목록만 가진 클래스이며 상속받는 클래스에서 메서드 구현을 강제하기 위해 사용된다.
#### apis/views.py
```python
class BasicView(View):
    @staticmethod
    def response(data={}, message='', status=200):
        result = {
            'data':data,
            'message': message,
        }
        return JsonResponse(result, status=status)
```
- 이번 SNS 프로젝트에서는 BLOG 프로젝트와 달리 FBV(Function-Based View)가 아닌 CBV(Class-Based View) 방식을 사용하였다.
- jQuery를 이용하여 Template에 데이터를 전달해주었기 때문에 HttpResponse의 Subclass인 JsonResponse를 이용하였다. 
#### JSON 외 HttpResponse, HttpRequest 란?
- Django는 request와 response 객체를 통해 서버와 클라이언트 사이에 통신한다.
- django.http 모듈에서 HttpRequest와 HttpResponse API를 제공한다.
- 통신절차
1. 클라이언트가 요청하면, 장고는 요청 시 데이터를 포함하는 HttpRequest 객체를 생성
2. 장고는 urls.py에서 정의한 특정 View 클래스/함수에 첫 번째 인자로 reqeust 객체를 전달해준다.
3. 해당 View는 결과 값을 HttpRespnse 혹은 JsonResponse 객체에 담아 전달한다.
- HttpRequest 객체의 주요 속성
```
HttpRequest.body #reqeust의 body 객체
HttpRequest.headers # request의 headers 객체
HttpRequest.COOKIES # 모든 쿠키를 담고 있는 딕셔너리 객체
HttpRequest.method # request의 메소드 타입
HttpRequest.GET # GET 파라미터를 담고 있는 딕셔너리 같은 객체
HttpRequest.POST # POST 파라미터를 담고 있는 딕셔너리 같은 객체
```
- HttpRedirect: 별다른 response를 하지 않고, 지정된 url 페이지로 redirect 함
- HttpResponse: response를 반환하는 가장 기본적인 함수, 주로 html를 반환
- Render: httpResponse 객체를 반환하는 함수로 template를 context와 함께 httpResponse로 반환해주는 함수. template_name 인자에 불러오고 싶은 템플릿 명을 적고, context에는 View에서 사용하던 변수를 html 템플릿에 전달하는 역할을 한다. 딕셔너리 형태로 context를 전달해주어야 한다. key 값이 템플릿에서 사용할 변수이름, value 값이 파이썬 변수가 된다.
- 출처: https://velog.io/@jcinsh/Django-request-response
#### CBV vs FBV
1. CBV(클래스 뷰)
- 프로젝트 내부의 App의 views.py 파일을 `Class`를 기반으로 구현한 것을 말한다.
- 쉽게 확장하고 재사용하기 쉬움
- mixin(다중상속)과 같은 기능 사용가능
- 별도의 클래스 메소드로 HTTP 메소드 처리
- Django에서 제공하는 Genric View 사용
* 데코레이터 사용하기 위해서 별도의 @method decorator를 import 해주어야 함.
2. FBV(함수 뷰)
- 프로젝트 내부의 App의 views.py 파일을 `Function`을 기반으로 구현한 것을 말한다.
- 간단한 구현
- 읽기 쉽다
- 명시적 코드흐름
- 데코레이터의 간단한 사용법
* 조건문을 이용한 HTTP 메소드 처리
* 확장과 재사용에 어려움

## Chapter2. User API
#### apis/views.py
```python
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
```
#### csrf_exempt와 method_decorator
- csrf_exempt 는 csrf token을 생성해주는 decorator 이다. 하지만 이번 프로젝트에서는 FBV가 아닌 CBV를 사용하기 때문에 view의 함수들이 클래스로 선언되어 있다. 클래스로 선언되어 있기 때문에 method_decorator 라는 것을 import해서 클래스 view의 dispatch 함수에 csrf_exempt를 적용시켜 주어야 한다.
#### 클래스형 뷰의 동작방식
- 클래스형 뷰는 클래스로 진입하기 위한 진입 메소드 as_view() 메소드를 제공한다. 
- as_view() 메소드에서 클래스의 인스턴스를 생성한다.
- 생성된 인스턴스의 dispatch() 메소드를 호출한다.
- diapatch() 메소드는 요청을 검사해서 HTTP이 메소드(GET,POST)를 알아낸다.
- 인스턴스 내에 해당 이름을 갖는 메소드로 요청을 중계한다.
- 해당 메소드가 정의되어 있지 않으면, HTTPResponseNotAllowed 예외를 발생시킨다.

## Chapter3. Login & Logout API
## Chapter4. Register API
## Chapter5. Contents & Image
## Chapter6. Following & Unfollowing
## Chapter7. Search User function
