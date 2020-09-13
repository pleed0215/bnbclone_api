# Air bnb clone - app

## django rest framework

- REST API rule
- https://www.swipe.to/4287nc?p=Z4h7dGZHX
- insomnia - REST Api testing app

### 1. Serialization

- django와 비슷해서.. 딱히 적을 내용은 없고
- object를 json으로 바꾸는 과정.

  ```python
      import json
      from django.core import serializer
      from .models import Room

      data = serializers.seralize("json", Room.objects.all())
      #json_data = json.dumps(data)
  ```

  - 강의에서는 json.dumps를 먼저 이야기 해줬는데, 결국에는 사용 안해도 되는 것..
  - json data를 확인을 해보면, foreign key 관련된 내용에 대해서는 pk만 나와있다.
    - 그래서 serialization만으로는 부족..
    - documentation을 확인해보면, deserialization을 할 수 있다. 즉, json, xml 등을 django query set으로 바꿀 수도 있다.
    - deserialize, serialize는 직렬화면 시켜주는 것들과 관게 된 작업만 해줄 뿐, data 검증은 해주지 않는다.
      - data 검증은 그래서 꼭 프로그래머가 해줘야 할 일이다.
      - 강의는 조금 왔다갔다 하는 편인데, 왜냐하면 기본을 알려주고 나서 왜 이런 프레임워크를 사용해야 하는지 알려주기 때문에...
      - serialization django rest framework 에서는 조금 달라지는 모양이라 위의 내용을 사용하지 않을 것 같다.
      - djangoframework를 pipenv, pip 등을 통해 install 해주고, config.setting에 가서 INSTALLED_APP에 추가해줘야 한다.

### 2. version control

- version control 방법으로 여러가지를 재시해줬다.
  - 가장 추천하는 방법은 api 폴더를 만들어서 v1, v2를 따로 관리하라는 것..

### 3. django rest framework

- rest_framework가 기본 경로.
- rest_framework function based view를 시작하려면 먼저 decorator를 가져와서 사용해주면 된다.
  - decorator에는 method를 추가해줘야 한다.
  - django의 HttpResponse로 리턴을 해줘도 되지만, rest_framework.response.Response로 응답을 해주자.

```python
  from rest_framework.decorators import api_view
  from rest_framework.response import Resonpse

  @api_view(["GET"])
  def room_list(req):
    ...
    return Response()
```

- django rest framework의 목표중 하나가 browsable api이기 때문에 page를 제공해준다.

  #### rest_framework.serializers

  - serializers.Serializer 클래스를 상속 받아 serializer를 custom시키면 된다.

    - in serializers.py

    ```python
    from rest_framework import serializers

    class RoomSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=200)
        price = serializers.IntegerField(default=1)
        bedrooms = serializers.IntegerField(default=1)
        bathrooms = serializers.IntegerField(default=1)
    ```

    - in views.py

    ```python
    from .serializers import RoomSerializer
    from .models import Room
    @api_view(["GET"])
    def room_list(req):
      rooms = Room.objects.all()
      rooms_serialized = RoomSerializer(rooms)
      return Response(data=rooms_serialized.data)
    ```

    - rooms_serialized.data property를 data에 넣어줘야 한다.
    - many=True, agument를 RoomSerializer에 초기화 속성으로 넘겨주지 않으면, 에러가 발생한다.
      - 이유는 RoomSerializer는 하나의 방에 대한 내용이지만, 넘겨준 rooms는 여러가지의 QuerySet이기 때문에..
      - 다행히도 many=True 하나만 넘겨주면 된다.

  #### Easy way in serializing

  - 그냥 코드를 보자.
  - serializers.ModelSerializer를 상속받자..

  ```python
    from rest_framework import serializers
    from .models import Room

    class RoomSerializer(serializers.ModelSerializer):
      class Meta:
        model = Room
        fields = '__all__' # 모든 필드를 넣고 싶으면 이렇게 하면 된다.
  ```

  - 여전히 user 필드를 보면, pk만 나와있는 것을 볼 수 있는데..
  - users에도 serializer를 만들어 준 후에 user필드를 위 클래스에서 만들어서 serializer에 연결을 해주면 된다.

  ```python
    from users.serializers import UserSerializer
    class RoomSerializer(serializers.ModelSerializer):
      user = UserSerializer()
      class Meta:
        model = Room
        fields = '__all__' # 모든 필드를 넣고 싶으면 이렇게 하면 된다.
  ```

### 4. Class Based View

- django와 마찬가지로 django rest framework에도 view class가 있다.

  - 기본적인 django의 View와 마찬가지인 view class로는 APIView(rest_franework.views.APIView)가 있다.
    - Custom Logic을 사용해야 할 때 보통 사용.
  - 물론 필요한 작업들을 위해 미리 만들어진 Generic View와 같은 View가 역시나 존재한다.
  - 위의 room_list를 class로 만들면 아래와 같다.
    ```python
    class ListRoomView(APIView):
      def get(self, request):
          rooms = Room.objects.all()
          rooms_serialized = RoomSerializer(rooms, many=True)
          return Response(data=rooms_serialized.data)
    ```
  - 위의 코드를 Generic view 중 하나인 ListAPIView로 recap해보면..

  ```python
    class ListRoomView(ListAPIView):
      queryset = Room.objects.all()
      serializer_class = RoomSerializer
  ```

- 참고사항
  - django generic views들이 여러가지 클래스들을 상속 받다보니, 그 구조를 한눈에 보기 어려워서 ccbv.co.uk라는 사이트를 참고했었다.
  - django rest framework에도 마찬가지로 여러가지 클래스들을 상속받아 generic view들의 구조를 한눈에 파악하기가 쉽지 않다.
  - https://cdrf.co
    - 여기로 가면 ccbv.co.uk처럼 rest framework generic view의 구조를 확인할 수 있다.

### 5. Pagination

- config.settings에 추가해줄 것이 좀 있다.

```python
    REST_FRAMEWORK = {
      'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
      'PAGE_SIZE': 100
    }
```

- 항상 그렇듯.. 이러한 내용은 공식 documentation에 다 있는 내용.

  - DEFAULT_PAGINATION_CLASS
    - 위에 documentation에서 긁어온 class는 offset과 limit를 url에 query로 넘겨줘서 pagination 범위를 정해주는 클래스.
    - PageNumberPagination
      - rest_framework.pagination.PageNumberPagination
      - URL에서는 이런식으로 작동한다.
        <code>GET https://api.example.org/accounts/?page=4</code>

- 각 view에도 pagination_class attribute를 지정하여 pagination을 custom할 수 있다.

### 6. RetrieveAPIView

- api/vi/rooms/\<id:pk\>형식으로 된 view를 만들고 싶을 때 사용하면 된다.
- 기본적으로 ListAPIView와 비슷하게 만들어주면 된다.
  ```python
  class SeeRoomView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
  ```
- 참 재밌는 부분은 queryset에 특정 부분을 filtering 하도록 하는 것이 아니라, 모든 queryset을 다 준다는 것..
  - rest framework가 알아서 다 해주는 것.
  - lookup_field, lookup_rul_kwargs 라는 것이 있는데, 이것이 기본적으로 pk로 되어 있기 때문.

### 7. ModelViewSet

- 일단 viewset.py를 만들어준다.
  ```python
    from rest_framework import viewsets
    class RoomViewset(viewsets.ModelViewSet):
      queryset = Room.objects.all()
      serializer_class = RoomSerializer
  ```
  - 사실은 ListAPIView 등에서 했던 방법들과 똑같다.
- url pattern도 제공해주는 부분이 있으므로, urls.py도 새로 만들어 줘야 한다.

  ```python
    from rest_framework.routers import DefaultRouter

    router = DefaultRouter()
    router.register ("", viewsets.RoomViewset, basename="room")

    urlpatterns = router.urls
  ```

  - 이렇게 해주면 위에서 했던 내용과 거의 똑같이 작동한다.
  - 문제는 보안.
    - CRUD를 모두 다룰 수 있도록 해주기 때문에 이런 부분은 설정이 필요하다.

## POST method

- 강의에 뭔가 일관되지 않다. 이유는 어려운 방법부터 알려줘야 나중에 framework 라이브러리 사용의 이유를 알 수 있다 하여서..

  - 니코 강의는 항상 이런식이긴 하다. 근데 이번엔 조금 많이 왔다 갔다 한다.

- 다시 function based view

  - POST method와 GET method용 serializer가 각각 다르다.
  - serializers.ModelSerializer는 READ 전용이라 봐야 하나..? 이유를 잘 모르겠다.
  - WRITE 전용 serializer는 normal Serializer를 사용해야 한다.

### 1. Validation, Create & Save

- Generic View를 사용하지 않고 직접 만들어주려면, data validation도 직접 해줘야 할 필요가 있다.

  - django form과 굉장히 유사하다.

  ```python
    if serializer.is_valid():
              return Response(status=status.HTTP_200_OK)
          else:
              return Response(status=status.HTTP_400_BAD_REQUEST)
  ```

- serializer에서 기억해야 할 3가지 method.

  - 이 세가지를 알면 영원히 django framework을 만족할 거라는데...?? 그정도.로..?

    - create, update, save
    - create method
      ```python
        class RoomSerializer(serailizers.Serializer):
          ...
          def create(self, validated_data):
            Room.objects.create(**validated_data)
      ```
    - create method는 직접적으로 호출해서는 안된다. save method를 호출해야 한다.
    - save method를 room 만들 때 사용하면 error가 발생하는데, user id가 없어서이다.
    - save method에 user(Foreign Key)를 넘겨줘야 한다.
      <code>serializer.save(user=req.user)</code>

  - validation은 django form의 clean과 굉장히 유사하다. clean*(form element)한 것처럼, validate*(element)로 데이터 검증을 하면 된다.

    - error handling: raise serializers.ValidationError().
      - 사용할 때에는.. return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  - field를 한 개씩만 validation을 할 때에는 위의 방법으로 하면 되지만, data가 연계되어 있다고 하면, validate 함수를 overriding을 해야 한다.

- updating

  - instance, validate_data 두가지를 argument로 받는다.
  - Serializer에 partial argument -> 내가 원하는 data만 보내겠다라는 뜻..

    - 수정할 때 data valid error가 나는데, 이것을 해결하려면 partial argument True로 넘겨주면 된다.
    - data를 수정하고 싶은데 전체를 다 보낼 순 없잖어..
    - 아직 에러가 수정되지 않는데, 그 이유는 수정 때에도 validation이 실행되기 때문에.
    - Serializer에 instance attribute가 None이 아니면, updating 중이라.. validation에서 한 번 걸러줘야 한다.

      - 각각 data를 validation하려는, validation\_{field} 방법은 사용하지 말아야 겠다.
      - 왜냐하면, instance 거르는 작업에서 막힌다.
      - validate 사용하기 위해서는, is_valid를 호출해야 한다.

      ```python
            if room_serialized.is_valid():
                room_serialized.save()
      ```

      - 호출 후에는 data validation이 확인된 것이기 때문에, serializer의 save method를 호출한다.
      - save method가 호출되면 곧, serializer의 update method가 호출된다.
      - update method

        ```python
        class WriterSerializer(serializers.Serializer):
          ...
          def update(self, instance, validated_data):
            instance.field1 = validated_data.get("field1", instance.field1)
            ...

            instance.save()
            return instance
        ```

        - validated_data에는 validated된 data가 들어가는데, data update 할 때에는 어떤 데이터가 update될지는 모르므로,
          - 모든 field에 대해 update한다고 가정하면 된다.
          ```python
            instance.field1 = validated_data.get("field1", instance.field1)
            ....
          ```
          - validated_data에 필드가 없다면, update하려는 속성이 아니므로, skip 하면된다. get 함수 사용 시 key값이 없다면 None이되므로, 위와 같이 해준 것.

  - magic way
    - ModelSerializer를 사용해도 된다.

- Authenticate

  - rest_framework.permission.IsAuthenticated
  - APIView에서 <code>permission_classses = [IsAuthenticated]</code> 등으로 사용하면 된다.
    - 그럼 request.user.is_authenticated 등으로 사용하지 않아도 사용할 수 있다.

- Read / Write Serializer

  - ModelSerializer 하나로 통일 할 수 있다.
  - field 중에 edit하면 안되는 field는 read_only_fields 사용하면 된다.
    - 위 속성에 넣어준 필드는 validation에 빠진다.

- Write only field
  - password를 만들 때, serializer에 어쩔 수 없이 password field를 포함시켜줘야 하는데,
  - 문제는 다른 사람들이 패스워드를 볼 수도 있다는 것..
  - 그래서 password를 write_only field로 만들어주면 된다.
    - <code>password = serializers.CharField(write_only=True)</code>

## Graphql Python
