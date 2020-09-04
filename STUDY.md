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

## Graphql Python
