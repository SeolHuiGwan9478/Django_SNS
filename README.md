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
## Chapter3. Login & Logout API
## Chapter4. Register API
## Chapter5. Contents & Image
## Chapter6. Following & Unfollowing
## Chapter7. Search User function
