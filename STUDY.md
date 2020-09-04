# Air bnb clone - app

## django rest framework

- REST API rule
- https://www.swipe.to/4287nc?p=Z4h7dGZHX
- insomnia - REST Api testing app

- django와 비슷해서.. 딱히 적을 내용은 없고
- object를 json으로 바꾸는 함수.

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

## Graphql Python
