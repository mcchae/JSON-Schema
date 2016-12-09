# JSON과 PYTHON API의 만남

이 세상 어떤 발명물이던지 새롭게 하루아침에 없었던 것이 갑자기 만들어 지는 것은 없습니다. 모두 이전의 생각과 사상이 다음 아이디어에 영향을 미치고 전달되고 하고 더 위대한 무언가가 만들어지기 마련입니다. 마찬가지로 어떤 기술이던지 새롭게 하루아침에 태어난 것은 없습니다.

[JSON (JavaScript Object Notation)](https://ko.wikipedia.org/wiki/JSON)은 현재 어떤 자료 전송에 있어 거의 표준이 되어 버렸습니다. 한때 XML이 그랬었고 그 이전에도 자료의 표준화 등의 시도는 있어왔죠.

그럼 왜 JavaScript 일까요? 저는 굳이 JavaScript로 Full-Stack 프로그램을 하려하지 않습니다만 Front-End에서는 JavaScript 말고는 더 다른 것을 표현할 길이 없을 만큼이나 그 스스로 표준 개발 언어가 되어 버렸습니다.

Back-End 에서는 nodejs와 같은 JavaScript를 이용한 개발도 있을 수 있고, Java를 이용할 수도, 또는 PHP 등을 이용할 수도 있지만 저는 파이썬 이라는 언어를 제일 좋아하고 사랑합니다. (지금껏 열가지 이상의 프로그래밍 언어를 했었던 것 같은데 이렇게 사랑한다 라고 고백한 것은 파이썬이 처음 인듯 합니다)

이런 점에서 파이썬 역시 JSON 과 궁합이 잘 맞습니다. 1:1 이라고는 할 수 없지만 파이썬의 dict 라는 자료형과 JSON은 거의 동등하게 생각해도 좋을 만큼 서로 궁합이 맞습니다. 그 외에 NoSQL 중에 하나인 mongoDB 역시 [BSON (Binary JSON)](https://en.wikipedia.org/wiki/BSON) 이라고 하여  JSON과 거의 동일한 자료가 저장소까지 그대로 갔다가 다시 Back-End 파이썬을 거쳐 Front-End 까지 그대로 자료 왔다리 갔다리 할 수 있는 장점이 있습니다.

이를 RDB에 있었던 Schema 라는 개념이 NoSQL로 오면서 Schema-less 라는 것이 부곽되었죠. 즉 자유롭게 중첩가능한 '키-값' 및 어레이와 같은 어떤 데이터가 있고 필요시 어떤 값도 새롭게 넣고 뺄 수 있는 등의 자유도는 기존 RDB에 연결하여 작업하던 개발자에게는 엄청난 잇점 처럼 보이고 이를 행복하게 생각해 왔습니다.

*그런데 말입니다*, 다시한번 API 라는 다른 관점에서 바라보기 바랍니다.
다시 처음으로 돌아가서 API 라는 것은 호출 가능한 함수에서 출발하고 함수는 패러미터와 그 결과값을 리턴합니다. 이런 함수가 원격 함수로 발전하면서 RPC 라는 것이 나왔고 (ONC RPC, DEC RPC 등이 있었고 각자 NFS, DCOM 등이 파생되었죠) XML이 자료형으로 유명할 때부터 XML-RPC라는 원격 API 호출이 있었습니다. 그러던 것이 HTTP를 통해 API를 전달하고 결과를 받는 곳에서 WebService를 거쳐 SOAP이 대세가 되었다가 이제는 RestfulAPI가 대세처럼 보입니다. 

어찌되었던 간에,

``` python
ret = func(param1, param2, param3)
```
과 같은 API 가 있다고 하면 그것을 JSON 으로 표현해 보면 다음과 유사할 수 있습니다.

우선 패러미터는 

``` json
{
	"param1": 1,
	"param2": "abc",
	"param3": [1, 3, { 'a":333 }]
}
```
과 같이 표현될 수 있고,

결과는

```json
{
	"ok": true,
	"result": 0
}
```

과 같이 나타낼 수 있습니다.

다시한번 *그런데 말입니다*, API 라는 관점에서 위와 같이 패러미터나 결과의 return 값 (Scalar 값이 아닌 JSON 객체와 같은 구조체가 리턴될 수도 있습니다) 을 바라봅시다.

`사용자` 라는 데이터는

``` json
{
	"name" : "홍길동",
	"cellphone": "010-1345-7764",
	"address": "​이상국 행복리 234",
	"age": 33
}
```
와 같이 표현된다고 하였을 때, 이 사용자를 시스템에 저장하는 add_user 라는 함수를 아래와 같이 표현할 수 있습니다.

```python
param_json = {
	"name" : "홍길동",
	"cellphone": "010-1345-7764",
	"address": "​이상국 행복리 234",
	"age": 33
}

ret_json = add_user(param_Json)
```

세번째 *그런데 말입니다*. 위와 같이 패러미터가 API로 전달된다고 할 때 그 자료형이 무조건 자유롭다... 라고 생각하면 힘들어지는 부분이 발생합니다. JSON이 어떤 구조의 자료도 모두 표현된다고 하고 하더라도 사용자는 이렇게 표현된다... 라는 것이 없으면 이 API를 처리하는 부분에서는 그 값의 정당성 등을 제대로 파악할 수 없게 됩니다. 말하고 싶은 것은 저장소에 저장할 때 RDB에 스키마를 저장하듯이 결국 이런 API를 작성할 때는 어떤 자료의 형식을 갖추어 어떤 값이 오고 그 값의 유효성은 어떠하며 어떻게 해야 정당하다는 데이터 스키마를 지정해야만 합니다. (경우에 따라서는 그 결과를 받는 부분에서는 또 그 유효성을 검증해야 합니다)

약간 다른 논점에서 과거에 모놀리틱 구조의 프로그램에서는 제일 먼저 어떤 형식의 데이터를 정의하는 것이 제일 중요했습니다. 그러나 현재와 같이 [마이크로서비스 아키텍쳐](http://guruble.com/?p=951)와 같은 개념의 소프트웨어에서는 어디에 어떻게 저장되는 관점 보다는 어디에서 어떤 API 들이 있고 이를 어떻게 사용하여 원하는 서비스를 하는가가 주안점이 되고 있습니다.

따라서 오늘의 결론은

"[JSON 스키마](JSON-Schema.md)"를 이용하여 API의 패러미터에 들어갈 데이터 형식과 결과의 형식을 지정하고 API 내부에서는 해당 자료가 올바른지 JSON 스키마를 통해 검증을 하며 해당 JSON 자료를 가지고 처리하다가 결과의 JSON에 값을 넣으면 그 결과를 받아 처리하는 부분 역시 (Client-Side JavaScript 일 수도 있고, 아니면 RestfulAPI를 호출하는 외부 API 일 수도 있습니다) 그 결과가 올바른 형식인지 알 필요가 있습니다.

UI에서 조금 더 생각을 확장하면 JSON 스키마를 이용하여 해당 자료가 입력 폼은 어떻게 구성된다든지 또한 데이터 그리드는 어떤 형식인지, 또 검색할 항목은 어떤 것들이 있는 지 등등의 것들을 충분히 자동화할 수 있습니다. (데이터 그리드에는 표시하지 말라는 등의 부가 옵션 등이 있을 수 있겠네요.) 실지로 과거 2009년 정도에는 C#으로 유사하게 자동화를 부분 적용한 적도 있습니다.

그러면 오늘의 본론인 어떻게 하면 파이썬 API에서 JSON 스키마와 JSON 데이터를 처리할 것인가를 살펴보겠습니다.

## 1 테스트에 필요한 패키지 설치

우선 아래에 하나씩 설명을 하겠지만,
다음과 같은 패키지를 우선 설치합시다.

> requirements.txt 라는 파일을 다음과 같이 만듭니다.

``` txt
genson==0.2.0
jsonschema==2.5.1
apitools==0.1.4
rstr==2.2.5
```

> pip install -r requirements.txt

## 2 JSON 스키마 생성

[JSON 스키마](JSON-Schema.md)에 정의된 것처럼 만들기란 쉽지 않습니다. 그런데 거꾸로 생각해 봅시다. 위에 기술했던,

```python
param_json = {
	"name" : "홍길동",
	"cellphone": "010-1345-7764",
	"address": "​이상국 행복리 234",
	"age": 33
}
```
과 같이 저런 데이터가 패러미터로 들어가겠구나... 하는 것은 어렵지 않게 생성할 수 있습니다.

그러면 머리 좋은 누군가는 

> 아하! 그럼 JSON 데이터를 넣고 JSON 스키마를 자동으로 맹글어 (만들어의 사투리 입니다 ^^) 주는 무언가가 있지 않을까?
> 
> 구글 신께 여쭈어 봐야지~~~

그래서 찾은 [GenSON](https://github.com/wolverdude/genson/) 되시겠습니다. 뭐 다들 최신 Draft 4을 지원한다고들 합니다.

설치는 

> pip install genson  # VirtualEnv 인 경우
> 
> sudo pip install genson

``` bash
$ genson --help
usage: genson [-h] [-a] [-d DELIM] [-i SPACES] [-s SCHEMA] ...

Generate one, unified JSON Schema from one or more JSON objects and/or JSON
Schemas. (uses Draft 4 - http://json-schema.org/draft-04/schema)

positional arguments:
  object                files containing JSON objects (defaults to stdin if no
                        arguments are passed and the -s option is not present)

optional arguments:
  -h, --help            show this help message and exit
  -a, --no-merge-arrays
                        generate a different subschema for each element in an
                        array rather than merging them all into one
  -d DELIM, --delimiter DELIM
                        set a delimiter - Use this option if the input files
                        contain multiple JSON objects/schemas. You can pass
                        any string. A few cases ('newline', 'tab', 'space')
                        will get converted to a whitespace character, and if
                        empty string ('') is passed, the parser will try to
                        auto-detect where the boundary is.
  -i SPACES, --indent SPACES
                        pretty-print the output, indenting SPACES spaces
  -s SCHEMA, --schema SCHEMA
                        file containing a JSON Schema (can be specified
                        mutliple times to merge schemas)
```

라고 도움말이 나오는데,

```bash
$ cat user.json 
{
	"name" : "홍길동",
	"cellphone": "010-1345-7764",
	"address": "​이상국 행복리 234",
	"age": 33
}
```
라고 파일이 있으면

이를 genson으로

```bash
$ genson user.json 
{"required": ["address", "age", "cellphone", "name"], "type": "object", "properties": {"cellphone": {"type": "string"}, "age": {"type": "integer"}, "name": {"type": "string"}, "address": {"type": "string"}}}
```

라고 스키마가 나옵니다.

그런데 이쁘게 (pprint) 출력하려면 `-i 4` 라고 옵션을 추가해봅니다.

```bash
$ genson -i 4 user.json 
{
    "required": [
        "address", 
        "age", 
        "cellphone", 
        "name"
    ], 
    "type": "object", 
    "properties": {
        "cellphone": {
            "type": "string"
        }, 
        "age": {
            "type": "integer"
        }, 
        "name": {
            "type": "string"
        }, 
        "address": {
            "type": "string"
        }
    }
}
```

**와우!** 잘 되는군요. 위에 `"required"` 는 꼭 나와야 하는 것을 지정하는 부분입니다.
각 문자열에서의 세세한 설정부분은 [string](JSON-Schema.md#string) 에서 `length`, `정규식`, `format` 을 참조합니다.

진짜 필요한 항목이나 아니면 선택 사항등을 수정합니다. 이부분은 [JSON 스키마](JSON-Schema.md)를 일독하고 잘 사용하시기를 바랍니다.

약간 더 수정을 하여 다음과 같이 해 보았습니다.

```bash
$ cat user-schema.json
{
    "type": "object", 
    "properties": {
        "cellphone": {
            "type": "string",
            "pattern": "^[01]{3}-[0-9]{4}-[0-9]{4}$"
        }, 
        "age": {
            "type": "integer",
            "minimum": 0,
            "maximum": 150
        }, 
        "name": {
            "type": "string"
        }, 
        "address": {
            "type": "string",
            "maxLength": 50
        }
    },
    "required": [
        "age", 
        "name"
    ]
}
```

다음과 같이 변경하였습니다.

* `"age"`와 `"name"` 은 꼭 나오고 다른 항목은 선택적으로 나올 수도 있고 안 나올 수도 있습니다.
* `"cellphone"` 에 `"pattern"`을 주어 010-1111-3829 와 같이 나오면 성공하도록 정규식 패턴을 추가하였습니다.
* 0 <= `"age"` <= 150 사이의 값이 나오도록 `minimum` 및 `maximum`을 지정하였습니다.
* `"address"`의 최대 길이를 50으로 제한합니다.

그 밖에도 object 등을 그 안에 정해서 중첩시킬 수도 있습니다.


## 3 특정 JSON 데이터가 해당 스키마에 맞는지 검증

파이썬에 [jsonschema](https://github.com/Julian/jsonschema) 라는 모듈을 이용하면 JSON의 데이터가 해당 스키마와 맞는지 검증해 봅니다.

이제 `user_validate.py` 라는 파이썬 파일을 만들어 보았습니다.

```python
#!/usr/bin/env python
# coding=utf-8

import sys
from jsonschema import validate
from jsonschema.exceptions import ValidationError

schema = {
    "type": "object",
    "properties": {
        "cellphone": {
            "type": "string",
            "pattern": "^[01]{3}-[0-9]{4}-[0-9]{4}$"
        },
        "age": {
            "type": "integer",
            "minimum": 0,
            "maximum": 150
        },
        "name": {
            "type": "string"
        },
        "address": {
            "type": "string",
            "maxLength": 50
        }
    },
    "required": [
        "age",
        "name"
    ]
}

data = [
    {
        "name": "홍길동",
        "cellphone": "010-1345-7764",
        "address": "​이상국 행복리 234",
        "age": 33
    },
    {
        "name": "홍길동",
        "age": 33
    },
    {
        "name": "홍길동",
        "address": "​이상국 행복리 234",
    },
    {
        "name": "홍길동",
        "cellphone": "012-1345-7764",
        "age": 33
    }
]

print("Validating the input data using jsonschema:")
for idx, item in enumerate(data):
    try:
        validate(item, schema)
        sys.stdout.write("Record #{}: OK\n".format(idx))
    except ValidationError as ve:
        sys.stderr.write("Record #{}: ERROR\n".format(idx))
        sys.stderr.write(str(ve) + "\n")
```

이 결과를 확인하면,

```sh
Validating the input data using jsonschema:
Record #0: OK
Record #1: OK
Record #2: ERROR
'age' is a required property

Failed validating 'required' in schema:
    {'properties': {'address': {'maxLength': 50, 'type': 'string'},
                    'age': {'maximum': 150,
                            'minimum': 0,
                            'type': 'integer'},
                    'cellphone': {'pattern': '^[01]{3}-[0-9]{4}-[0-9]{4}$',
                                  'type': 'string'},
                    'name': {'type': 'string'}},
     'required': ['age', 'name'],
     'type': 'object'}

On instance:
    {'address': '\xe2\x80\x8b\xec\x9d\xb4\xec\x83\x81\xea\xb5\xad \xed\x96\x89\xeb\xb3\xb5\xeb\xa6\xac 234',
     'name': '\xed\x99\x8d\xea\xb8\xb8\xeb\x8f\x99'}
Record #3: ERROR
'012-1345-7764' does not match '^[01]{3}-[0-9]{4}-[0-9]{4}$'

Failed validating 'pattern' in schema['properties']['cellphone']:
    {'pattern': '^[01]{3}-[0-9]{4}-[0-9]{4}$', 'type': 'string'}

On instance['cellphone']:
    '012-1345-7764'
```

**우와~~!!** 이렇게 성공과 실패도 잡아내는 것도 신통하지만 정확하게 왜 검증에 틀렸는가를 정확하게 알려줍니다. 그 메시지를 거의 그대로 사용자에게 보여줘도 될 만 합니다. (대신 영어로 나오네요~ ^^)

위에 파이썬 모듈을 확인해 보았지만 [언어별 JSON 스키마 검증](http://json-schema.org/implementations.html)을 보면 많은 언어에서도 모두 지원되는 모듈들이 있음을 알 수 있습니다.

특히 Client-Side의 JavaScript에서 이용할 만한 [ajv](https://github.com/epoberezkin/ajv)가 있습니다. 이제는 사용자가 입력한 자료로 JSON으로 만들어 이 JSON 스키마 검증 모듈로 미리 체크할 수도 있고, 또 API 안에서도 체크할 수 있고...

지금까지 이런 검증 코드를 하나 하나 노가다를 뛰며 했었던 것을 생각해 보면...

역시 손발이 게으른 개발자가 이런 훌륭한 방안을 고안하고 구현하고 하는 듯 합니다. 
우리 같은 일반 개발자는 이런 것을 잘 사용하는 것 만으로도 훨씬 효과적이고 경제적인 코드를 할 수 있다고 확신합니다.

## 4 해당 스키마에 맞는 자동 데이터 생성

이제 다른 요구 사항이 생겼습니다. RPC 세계에서 STUB 라는 dummy 코드라는 개념이 있었습니다. 비슷한 개념인데 Front-End와 Back-End 에서 일을 하는데 위와 같은 API 를 먼저 설계하고 여이~ 땅 작업을 시작한다고 하면 dummy API 코드를 생성해서 작업을 한다고 가정합시다.

그러면 위와 같은 JSON 스키마를 가지고 거꾸로 해당 스키마를 만족하는 랜덤 JSON 데이터를 뽑아낼 필요가 있습니다. API 패러미터 입장에서는 외부에서 해당 JSON 스키마를 만족하는 랜덤 데이터를 갖는 JSON 데이터 자동으로 생산하고 또한 결과의 JSON 또한 JSON 스키마를 정해놓고 거기에 맞는 결과가 나오도록 JSON 데이터를 자동 생성하면 우리는 해당 코드의 실제 코드 없이도 이미 패러미터 검증 및 그 결과를 가짜로 만들어 넘겨줌으로써 호출하는 곳에서 해당 API가 이미 되었다고 생각하고 작업을 할 수 있을 수 있습니다.

그래서 이런 모듈이 있을까 확인해 보았더니...

[apitools](https://github.com/hamstah/apitools) 라는 모듈이 있습니다. 자세히는 못 보았지만 정확히 JSON 스키마를 넣고 임의 JSON 데이터를 만들 수 있습니다.

``` txt
apitools==0.1.4
rstr==2.2.5
```
apitools 를 선택하는데 rstr 이라는 정규식에서 일치하는 랜덤 데이터를 생성하는 모듈 또한 설치해야 합니다.

> gen_jsondata.py

라는 파이썬 파일을 다음과 같이 만들어 테스트를 해 보았습니다.

``` python
#!/usr/bin/env python
# coding=utf-8

import sys
from apitools.datagenerator import DataGenerator
from jsonschema import validate
from jsonschema.exceptions import ValidationError

generator = DataGenerator()

user_schema = {
    "type": "object",
    "properties": {
        "cellphone": {
            "type": "string",
            "pattern": "^[01]{3}-[0-9]{4}-[0-9]{4}$"
        },
        "age": {
            "type": "integer",
            "minimum": 0,
            "maximum": 150
        },
        "name": {
            "type": "string"
        },
        "address": {
            "type": "string",
            "maxLength": 50
        }
    },
    "required": [
        "age",
        "name"
    ]
}

while True:
    r = generator.random_value(user_schema)
    try:
        validate(r, user_schema)
        break
    except ValidationError as ve:
        sys.stderr.write(str(ve) + "\n")
print(r)
```

해당 결과를 돌려보면

```sh
$ python gen_jsondata.py 
'age' is a required property

Failed validating 'required' in schema:
    {'properties': {'address': {'maxLength': 50, 'type': 'string'},
                    'age': {'maximum': 150,
                            'minimum': 0,
                            'type': 'integer'},
                    'cellphone': {'pattern': '^[01]{3}-[0-9]{4}-[0-9]{4}$',
                                  'type': 'string'},
                    'name': {'type': 'string'}},
     'required': ['age', 'name'],
     'type': 'object'}

On instance:
    {'cellphone': u'001-0033-5228'}
'age' is a required property

Failed validating 'required' in schema:
    {'properties': {'address': {'maxLength': 50, 'type': 'string'},
                    'age': {'maximum': 150,
                            'minimum': 0,
                            'type': 'integer'},
                    'cellphone': {'pattern': '^[01]{3}-[0-9]{4}-[0-9]{4}$',
                                  'type': 'string'},
                    'name': {'type': 'string'}},
     'required': ['age', 'name'],
     'type': 'object'}

On instance:
    {'address': 'aXfUmZWMhZ9q7QXAQoWpBzZYjORMjVCzfO1BLmbIE',
     'name': 'hFOxGGOh'}
'age' is a required property

Failed validating 'required' in schema:
    {'properties': {'address': {'maxLength': 50, 'type': 'string'},
                    'age': {'maximum': 150,
                            'minimum': 0,
                            'type': 'integer'},
                    'cellphone': {'pattern': '^[01]{3}-[0-9]{4}-[0-9]{4}$',
                                  'type': 'string'},
                    'name': {'type': 'string'}},
     'required': ['age', 'name'],
     'type': 'object'}

On instance:
    {}
{'age': 12, 'name': 'nYk4PlSoQxx'}
```

아직 `"required"` 속성을 제대로 인식 못하는 것 같은데... 좀더 확인을 해 봐야 되겠습니다.

`apitools` 라는 이름이 의미하듯이 JSON 스키마를 통하여 RestfulAPI 같이 테스트 API 서버 기능도 제공하는것 같습니다.


## 5 기타 필요 모듈

파이썬에서 JSON 스키마를 받아들이고 이를 바탕으로 자동 파이썬 클래스화 해 주는 모듈이 있습니다.

* [python-jsonschema-objects](https://github.com/cwacek/python-jsonschema-objects)
* [warlock](https://github.com/bcwaldon/warlock)

나중에 필요에 따라 이용하면 좋겠다는 느낌이 들었습니다. python-jsonschema-objects 가 좀 더 나아 보입니다.


## 6 TODO

API 들에 대한 정보를 넣고 그 목록을 자동으로 API (RestFulAPI)를 생성하는데 JSON 스키마를 가지고 이용하도록 합니다. API Stub 내용을 넣는데 해당 패러미터와 리턴 JSON 데이터가 맞는지 Validation을 하고 Return 값을 자동으로 만들어 리턴하도록 하는 자동 함수 generation를 만들어 사용하면 좋을 듯 합니다.
