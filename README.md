#[JSON Schema](https://spacetelescope.github.io/understanding-json-schema/index.html)

![문어그림](https://spacetelescope.github.io/understanding-json-schema/_images/octopus.svg)

JSON 스키마는 XML 스키마와 유사하게 JSON 으로 표현된 JSON 객체의 검증을 하기 위한 표현 방법이라 생각하면 됩니다. (역자주)

## 스키마란?

만약 RelaxNG 또는 ASN.1 과 같은 XML 스키마를 알고 있다면 JSON 스키마를 동일한 개념으로 이해해도 됩니다. 우선 JSON 스키마를 정의하기 위해서는 JSON이 무엇인지 알 필요가 있습니다.
[JSON(JavaScript Object Notation)](http://www.json.org/json-ko.html)은 JavaScript를 이용한 경량의 데이터 교환 형식입니다. 

### 자료형

다음과 같은 종류의 JSON 데이터 구조가 존재합니다.

* object

``` json
{ "key1": "value1", "key2": "value2" }
```

* number

``` json
42
3.1415926
```

* string

``` json
"This is a string"
```

> 파이썬의 문자열은 ' 및 " 로 모두 문자열 지정이 가능하지만 JSON에서는 " 만 허용됩니다.

* boolean

``` json
true
false
```

* null

``` json
null
```

JSON과 파이썬은 아주 유사하게 1:1 표현이 가능하며 쉽게 이용할 수 있습니다.


### 첫번째 예제

이런 방식을 이용하여 다음과 같은 여러가지 방식의 자료를 표현할 수 있습니다.

``` json
{
  "name": "George Washington",
  "birthday": "February 22, 1732",
  "address": "Mount Vernon, Virginia, United States"
}

{
  "first_name": "George",
  "last_name": "Washington",
  "birthday": "1732-02-22",
  "address": {
    "street_address": "3200 Mount Vernon Memorial Highway",
    "city": "Mount Vernon",
    "state": "Virginia",
    "country": "United States"
  }
}
```

이제 맛보기로 스키마가 어떻게 생겼나 보겠습니다.

``` json
{
  "type": "object",
  "properties": {
    "first_name": { "type": "string" },
    "last_name": { "type": "string" },
    "birthday": { "type": "string", "format": "date-time" },
    "address": {
      "type": "object",
      "properties": {
        "street_address": { "type": "string" },
        "city": { "type": "string" },
        "state": { "type": "string" },
        "country": { "type" : "string" }
      }
    }
  }
}
```

첫번째 데이터를 검증해보면 실패할 것이고,

``` json
{
  "name": "George Washington",
  "birthday": "February 22, 1732",
  "address": "Mount Vernon, Virginia, United States"
}
```

두번째 데이터는 검증에 성공할 것입니다.

``` json
{
  "first_name": "George",
  "last_name": "Washington",
  "birthday": "22-02-1732",
  "address": {
    "street_address": "3200 Mount Vernon Memorial Highway",
    "city": "Mount Vernon",
    "state": "Virginia",
    "country": "United States"
  }
}
```

## 기본

### 시작하기

만약 JSON 스키마가

``` json
{ }
```
과 같다면 어떤일이 벌어질까요?

단순 JSON 자료형 혹은 JSON 이라면 해당 결과는 모두 검증에 성공합니다.

> 42
> 
> "I'm a string"
> 
> { "an": [ "arbitrarily", "nested" ], "data": "structure" }

위에 세 가지 경우 모두 검증에 성공합니다.


### `type` 키워드

JSON 형식에서 특정 형식의 데이터만 오도록 지정하기 위하여 `type` 키워드를 이용합니다.

만약 

``` json
{ "type": "string" }
```
라고 JSON 스키마를 지정했다면

> "I'm a string"

는 성공할 것이고

> 42

는 실패합니다.

### JSON 스키마 선언

JSON 스키마 또한 JSON 이기 떄문에 해당 스키마가 단순 JSON 데이터 인지 아니면 스키마 인지 알 수 없는 경우가 있습니다. 이런 경우 다음과 같이 `$schema` 라는 것을 지정해 줍니다.

```json
{ "$schema": "http://json-schema.org/schema#" }
```

### 고유 식별자 선언

`id`라는 식별자를 각각의 스키마에 고유하게 지정할 수 있습니다. 각각은 공유 URL을 지정해 줍니다.

```json
{ "id": "http://yourdomain.com/schemas/myschema.json" }
```

## JSON 스키마 참조

### 자료형에 따른 키워드


#### 파이썬과의 자료형 비교

다음은 JSON으로 표현되는 javascript의 개체와 Python의 자료형에 대한 비교표 입니다.

| 언어 | JavaScript | Python |
|---|---|---|
| *문자열* | string | string [^1] |
| *숫자* | number | int/float [^2] |
| *사전형* | object | dict |
| *목록* | array | list |
| *불리언* | boolean | bool [^3] |
| *널* | null | None |


[^1]: 파이썬 2.x에서는 `unicode`, 파이썬 3.x 에서는 `str` 과 같은 데이터 형식
[^2]: 파이썬에는 int 형과 float 형이 개별로 존재하지만 javascript에는 별도 형식이 존재하지 않습니다. 또한 파이썬 2.x는 int 외에 long 형이 개별로 존재하였지만 파이썬 3.x에서는 int 형만 존재합니다.
[^3]: javascript에서는 `true/false` 로 구분되고 파이썬에서는 `True/False` 가 불리언 상수입니다.


`type` 키워드 자체는 문자열 이거나 목록 입니다.
* 만약 문자열이면 위의 JavaScript 에 정의된 자료형 중에 하나가 올 수 있습니다.
* 만약 목록이라면 문자열의 목록이 나타나는데 각 문자열 역시 위에 JavaScript에 정의된 자료형 입니다.

``` json
{ "type": "number" }
```
라고 스키마가 정의되면,

> 42
> 42.0

등은 검증에서 성공하고,

> "42"

는 검증에서 실패합니다.

그런데 다음과 같이

``` json
{ "type": ["number", "string"] }
```

와 같이 목록으로 하나 이상의 자료형으로 정의되어 있다면

> 42
> "Life, the universe, and everythin"

은 검증에 성공하지만,

> ["Life", "the universe", "and everything"]

는 실패할 것입니다.  ("array" 가 목록에 포함되어야 성공 합니다)

### string

`string` 자료형은 문자열을 나타냅니다.

``` json
{ "type": "string" }
```

> "This is a string"

> "Déjà vu"
 
> ""
 
> "42"

등은 모두 성공할 것이고

> 42

는 문자열이 아니기 때문에 (number 자료형) 실패합니다.

#### Length
문자열은 각각 `minLength` 및 `maxLength` 키워드에 의하여 다음과 같이 그 길이를 제한할 수 있습니다.

``` json
{
  "type": "string",
  "minLength": 2,
  "maxLength": 3
}
```

> "AB"

> "ABC"

는 각각 검증에 성공하는데 반해

> "A"

및 

> "ABCD"

는 검증에 실패합니다.

#### 정규식

`pattern` 키워드를 이용하여 문자열의 정규식 매칭을 통한 검증이 가능하빈다. 정규식 문법은 JavaScript([ECMA 262](http://www.ecma-international.org/publications/standards/Ecma-262.htm))에 정의된 정규식을 따릅니다. 정규식에 대한 더 자세한 설명은 [정규식](https://spacetelescope.github.io/understanding-json-schema/reference/regular_expressions.html#regular-expressions)을 참조하십시오.

``` json
{
   "type": "string",
   "pattern": "^(\\([0-9]{3}\\))?[0-9]{3}-[0-9]{4}$"
}
```
위와 같이 스키마를 설정하면,

> "555-1212"
 
> "(888)555-1212"

는 검증에 성공하지만,

> "(888)555-1212 ext. 532"

또는

> "(800)FLOWERS"

등은 검증에 실패합니다.

#### format

`format` 키워드는 시각, 이메일 등과 같이 일반적으로 사용되는 문자열에 대한 검증용으로 이용됩니다.

> 노트: JSON 스키마를 구현하는데 있어 이 부분은 꼭 구현해야하는 것이 아니며 실제 열 구현체 들이 이 스펙을 구현하지 않고 있으므로 구현체를 확인하십시오.

##### 미리 정의된 format

다음과 같은 문자열에 대하여 사전 정의된 format이 존재 합니다.

* `"date-time"`: [RFC 3339, section 5.6](https://tools.ietf.org/html/rfc3339)에 정의된 날짜 표현
* `"email"`: [RFC 5322, section 3.4.1](https://tools.ietf.org/html/rfc5322)에 정의된 이메일 표현
* `"hostname"`: [RFC 1034, section 3.1](https://tools.ietf.org/html/rfc1034)에 정의된 호스트명 표현
* `"ipv4"`: [RFC 2673, section 3.2](https://tools.ietf.org/html/rfc2673)에 정의된 IPv4 주소 표현
* `"ipv6"`: [RFC 2373, section 2.2](hhttps://tools.ietf.org/html/rfc2373#section-2.2)에 정의된 IPv6 주소 표현
* `"uri"`: [RFC3986](https://tools.ietf.org/html/rfc3986)에 정의된 ​universal resource identifier 표현


### 숫자형

JSON 스키마에서 정의된 숫자형으로 `integer`와 `number` 가 있습니다.

#### integer
`integer` 정수형을 나타냅니다.

```json
{ "type": "integer" }
```
과 같이 JSON 스키마가 정의되어 있으면

> 42

> -1

은 검증에 성공하고,

> 3.14

> "42"

등은 실패합니다.

#### number

정수형 또는 실수형을 표현하기 위하여 `number` 형을 이용합니다.

``` json
{ "type": "number" }
```

> 42
>
> -1

과 같은 정수형 뿐만 아니라

> 5.0
> 
> 2.99792458e8

과 같은 실수형 모두 검증에 성공하지만,

> "42"

와 같은 문자열은 실패합니다.

#### multiples

`multipleOf` 키워드를 이용하여 특정 정수 또는 실수의 배수만 허용하도록 할 수 있습니다.

``` json
{
    "type"       : "number",
    "multipleOf" : 10
}
```
라고 JSON 스키마를 지정하면,

> 0
> 
> 10
> 
> 20

등은 검증에 성공하는 반면,

> 23

은 검증에 실패합니다.

#### Range
숫자 값이 특정 영역에 속해있는가를 표현하는 `minimum`, `maximum` 과 `exclusiveMinimum` 및  `exclusiveMaximum` 키워드가 있습니다.

* `minimum`는 최소 허용값을 나타냅니다.
* `exclusiveMinimum`는 불리언 값을 가지는데 `true`이면 최소값을 허용하지 않고 (x > min) `false`이면 최소값을 포함합니다. (x >= min) 디폴트는 `false` 입니다.
* `maximum`는 최대 허용값을 나타냅니다.
* `exclusiveMaximum`는 불리언 값을 가지는데 `true`이면 최대값을 허용하지 않고 (x < max) `false`이면 최대값을 포함합니다. (x <= max) 디폴트는 `false` 입니다.

다음과 같이,

``` json
{
  "type": "number",
  "minimum": 0,
  "maximum": 100,
  "exclusiveMaximum": true
}
```
JSON 스키마가 정의되어 있으면,

> -1

과 같이 최소값보다 작은 것은 검증에 실패하고

> 0
> 
> 10
> 
> 99

등은 검증에 성공합니다.

그런데 ​`exclusiveMaximum`가 `true` 이므로

> 100

은 실패합니다.


### object
파이썬의 dict와 같은 형식입니다. 이것은 중첩(nested) 자료형을 의미합니다.

```json
{ "type": "object" }
```
와 같이 JSON 스키마가 정의 되어 있다면,

```json
{
   "key"         : "value",
   "another_key" : "another_value"
}
```

및 

```json
{
    "Sun"     : 1.9891e30,
    "Jupiter" : 1.8986e27,
    "Saturn"  : 5.6846e26,
    "Neptune" : 10.243e25,
    "Uranus"  : 8.6810e25,
    "Earth"   : 5.9736e24,
    "Venus"   : 4.8685e24,
    "Mars"    : 6.4185e23,
    "Mercury" : 3.3022e23,
    "Moon"    : 7.349e22,
    "Pluto"   : 1.25e22
}
```

는 검증에 성공할 것이고

다음과 같은,

```json
{
    0.01 : "cm"
    1    : "m",
    1000 : "km"
}
```

> `키`는 숫자가 아니라 문자열이어야 함

```json
"Not an object"
```
> 단순 문자열은 object (dict) 가 아님

``` json
["An", "array", "not", "an", "object"]
```

> array (list)는 object(dict)가 아님


#### Properties

키-값의 쌍을 속성 (Properties) 라고 하는데 객체는 이 `properties` 키워드로 정의합니다. `properties` 값은 object이며 각각의 키는 객체의 키가 되고 그 값은 자료형을 나타내는 정의가 됩니다.

예를 들어,

``` json
{
  "type": "object",
  "properties": {
    "number":      { "type": "number" },
    "street_name": { "type": "string" },
    "street_type": { "type": "string",
                     "enum": ["Street", "Avenue", "Boulevard"]
                   }
  }
}
```
와 같은 JSON 스키마가 정의 되어 있다면

> { "number": 1600, "street_name": "Pennsylvania", "street_type": "Avenue" }

는 검증이 성공하는데 반해

> { "number": "1600", "street_name": "Pennsylvania", "street_type": "Avenue" }

는 검증에 실패합니다. ("number" 키가 숫자 1600이 아니라 문자열 "1600" 임)

그런데 아래와 같이,

> { "number": 1600, "street_name": "Pennsylvania" }

해당 키가 삭제되어도 성공입니다. (해당 키는 선택적으로 빠질 수 있습니다만 `required` 속성을 지정하면 꼭 등장해야 합니다)

따라서,

>  {}

도 검증에 성공합니다.

다음과 같은

> ​{ "number": 1600, "street_name": "Pennsylvania", "street_type": "Avenue",  "direction": "NW" }

JSON object도 검증에 성공하는데 `"direction":"NW"` 라는 속성이 추가되어도 문법에는 이상이 없습니다. 하지만 다음과 같이

```json
{
  "type": "object",
  "properties": {
    "number":      { "type": "number" },
    "street_name": { "type": "string" },
    "street_type": { "type": "string",
                     "enum": ["Street", "Avenue", "Boulevard"]
                   }
  },
  "additionalProperties": false
}
```

`additionalProperties` 라는 속성을 `false`라고 주면 위의

> ​{ "number": 1600, "street_name": "Pennsylvania", "street_type": "Avenue",  "direction": "NW" }

검증은 실패할 것입니다.

그런데 다음과 같이 `additionalProperties` 의 값이 불리언이 아니라 object 이면,

```json
{
  "type": "object",
  "properties": {
    "number":      { "type": "number" },
    "street_name": { "type": "string" },
    "street_type": { "type": "string",
                     "enum": ["Street", "Avenue", "Boulevard"]
                   }
  },
  "additionalProperties": { "type": "string" }
}
```

> { "number": 1600, "street_name": "Pennsylvania", "street_type": "Avenue" }

또는

> { "number": 1600, "street_name": "Pennsylvania", "street_type": "Avenue", "direction": "NW" }

는 검증에 성공하지만,

> { "number": 1600, "street_name": "Pennsylvania", "street_type": "Avenue", "office_number": 201  }

는 실패합니다. 부가적인 속성 ​`"office_number"`의 값이 201 이라는 숫자이기 때문입니다.

#### required 속성

위에서 언급하였듯이 `properties`에서 지정한 속성은 꼭 있어야 할 필요가 없습니다. 하지만 `required` 키워드를 이용하여 꼭 있어야 하는 속성을 키-값을 지정할 수 있습니다.

```json
{
  "type": "object",
  "properties": {
    "name":      { "type": "string" },
    "email":     { "type": "string" },
    "address":   { "type": "string" },
    "telephone": { "type": "string" }
  },
  "required": ["name", "email"]
}
``` 

이라는 JSON 스키마가 존재하면

``` json
{
  "name": "William Shakespeare",
  "email": "bill@stratford-upon-avon.co.uk"
}
```

과 

```json
{
  "name": "William Shakespeare",
  "email": "bill@stratford-upon-avon.co.uk",
  "address": "Henley Street, Stratford-upon-Avon, Warwickshire, England",
  "authorship": "in question"
}
```

는 검증에 성공하지만,

``` json
{
  "name": "William Shakespeare",
  "address": "Henley Street, Stratford-upon-Avon, Warwickshire, England",
}
```

는 검증에 실패합니다.

꼭 나타나야 하는 `"email"` 키가 없기 때문입니다.

#### size

`minProperties` 과 `maxProperties` 키워드를 통하여 키-값의 개수를 지정할 수 있습니다.

예를 들어,

``` json
{
  "type": "object",
  "minProperties": 2,
  "maxProperties": 3
}
```
라고 JSON 스키마를 지정하면

> {}
> 
> { "a": 0 }
> 
> { "a": 0, "b": 1, "c": 2, "d": 3 }

는 검증에 실패할 것이지만

> { "a": 0, "b": 1 }
> 
> { "a": 0, "b": 1, "c": 2 }

는 검증에 성공합니다.

#### 의존성(Dependencies)

> 주의: 이부분은 JSON 스키마의 세세한 정의로 계속 발전할 수 있습니다.

`dependencies` 키워드는 어느 특정 속성이 존재하여야 하는 것을 정의합니다.

다음과 같이 두가지 종류의 ​`dependencies` 가 있습니다.

* `Property dependencies`는 주어진 속성이 존재한다면 다른 어떤 속성이 존재해야 함을 의미
* `Schema dependencies`는 주어진 속성이 존재한다면 스카마가 변경됨을 선언합니다.

##### 속성 의존성 (Property dependencies)

```json
{
  "type": "object",

  "properties": {
    "name": { "type": "string" },
    "credit_card": { "type": "number" },
    "billing_address": { "type": "string" }
  },

  "required": ["name"],

  "dependencies": {
    "credit_card": ["billing_address"]
  }
}
```

위와 같이 JSON 스키마가 정의되어 있습니다. 이는 *고객* 을 담고 있다고 가정합니다. 그런데 위에서 보면 `"name"` 이라는 속성은 꼭 나와야 하는데 `"credit_card"` 라는 속성은 나올 수도 있고 안 나올 수도 있습니다. 그런데 만약  `"credit_card"` 속성이 존재한다면 꼭 `"billing_address"` 속성이 나와야 한다고 정할 필요가 있는데 그것을 위에서 처럼 `"dependencies"`에 정의한 것입니다.

따라서 다음과 같이,

```json
{
  "name": "John Doe"
}
```

는  `"credit_card"` 속성과 `"billing_address"`  속성 모두 없으므로 검증에 성공합니다.

또한,

```json
{
  "name": "John Doe",
  "credit_card": 5555555555555555,
  "billing_address": "555 Debtor's Lane"
}
```

는  `"credit_card"` 속성과 `"billing_address"`  속성이 모두 있으므로 검증에 성공합니다.

마찬가지로

```json
{
  "name": "John Doe",
  "billing_address": "555 Debtor's Lane"
}
```

 `"billing_address"`  속성만 있어도 검증에 성공합니다.
 
 대신,
 
```json
{
  "name": "John Doe",
  "credit_card": 5555555555555555
}
```

과 같은 경우는 ​ `"credit_card"` 속성이 존재하지만 `"billing_address"`  속성이 없으므로 검증에 실패합니다.

그런데 여기에서 `"billing_address"`  속성이 나왔을 때에도  `"credit_card"` 속성이 존재해만 한다면,

```json
{
  "type": "object",

  "properties": {
    "name": { "type": "string" },
    "credit_card": { "type": "number" },
    "billing_address": { "type": "string" }
  },

  "required": ["name"],

  "dependencies": {
    "credit_card": ["billing_address"],
    "billing_address": ["credit_card"]
  }
}
```

과 같이 상호 `"dependencies"` 를 주어 해결할 수 있습니다.

##### 스키마 의존성 (Schema dependencies)

스키마 의존성은 위의 속성 의존성과 달리 별도의 `properties` 선언을 포함합니다.

다음과 같이,

```json
{
  "type": "object",

  "properties": {
    "name": { "type": "string" },
    "credit_card": { "type": "number" }
  },

  "required": ["name"],

  "dependencies": {
    "credit_card": {
      "properties": {
        "billing_address": { "type": "string" }
      },
      "required": ["billing_address"]
    }
  }
}
```
JSON 스키마가 정의되어 있다면,

```json
{
  "name": "John Doe",
  "credit_card": 5555555555555555,
  "billing_address": "555 Debtor's Lane"
}
```

또는

``` Json
{
  "name": "John Doe",
  "billing_address": "555 Debtor's Lane"
}
```

는 검증에 성공하고,

```json
{
  "name": "John Doe",
  "credit_card": 5555555555555555
}
```
는 검증에 실패합니다.

#### 패턴 속성 (Pattern Properties)

`additionalProperties`에서 확인한 것과 같이 추가적인 속성이 나올 수 없도록 제한하거나 그 형식을 제한 하는 것과 유사하게 `patternProperties` 키워드를 이용하여 특정 패턴의 키가 오도록 제한 할 수 있습니다.

다음의 예제에서는 키가 `S_`로 시작하는 경우에는 문자열 값이, `I_`로 시작하는 경우에는 정수값이 오도록 제한하는 것을 보여줍니다.

```json
{
  "type": "object",
  "patternProperties": {
    "^S_": { "type": "string" },
    "^I_": { "type": "integer" }
  },
  "additionalProperties": false
}
```

그러면,

> { "S_25": "This is a string" }
> 
> { "I_0": 42 }

는 검증에 성공하지만,

> { "S_0": 42 }
> 
> { "I_42": "This is a string" }
> 
> { "keyword": "value" }

는 검증에 실패합니다.

하지만 스키마가

```json
{
  "type": "object",
  "properties": {
    "builtin": { "type": "number" }
  },
  "patternProperties": {
    "^S_": { "type": "string" },
    "^I_": { "type": "integer" }
  },
  "additionalProperties": { "type": "string" }
}
```

와 같이 `additionalProperties`에 문자열이 오도록 제한을 가했을 경우에는

> { "builtin": 42 }
> 
> { "keyword": "value" }

는 검증에 성공하지만,

> { "keyword": 42 }

는 검증에 실패합니다.


### 목록 (array) 자료형

목록은 순서데로 값을 가지고 있는 내용입니다. JSON에서 각 항목은 서로 다른 자료형일 수 있습니다.

```json
{ "type": "array" }
```
이라는 JSON 스키마가 있다면

> [1, 2, 3, 4, 5]
> 
> [3, "different", { "types" : "of values" }]

은 검증에 성공하는 반면,

> {"Not": "an array"}

는 실패합니다.

#### 항목 (items)

목록은 `items`와 `additionalItems` 키워드를 통하여 스키마를 정의합니다.
일반적으로 다음과 같은 두가지 방식의 목록이 있습니다.
* 목록 검증 (List validation): 동일한 자료형이 각 항목으로 존재하도록 규약
* 튜플 검증 (Tuple validation): 각각의 항목이 서로 다른 자료형이 존재할 때 규약 (파이썬의 `tuple`과 유사하지만 꼭 그 갯수를 맞출 필요는 없습니다) 

##### 목록 검증 (List validation)

목록 검증은 임의의 길이를 갖는 동일한 자료형의 목록을 정의하는 스키마입니다. 

> 노트: `items` 은 한번만 나오는 것이며 `additionalItems`는 의미 없게 됩니다.

```json
{
  "type": "array",
  "items": {
    "type": "number"
  }
}
```
위와 같은 JSON 스키마가 있다면

> [1, 2, 3, 4, 5]

은 검증에 성공하지만,

> [1, 2, "3", 4, 5]

는 실패합니다.

##### 튜플 검증 (Tuple validation)

튜플 검증은 특정 자료형을 갖는 목록을 지정할 수 있습니다.

예를 들어 다음과 같은
> [1600, "Pennsylvania", "Avenue", "NW"]

라고 주소를 

> [number, street_name, street_type, direction]

의 4개 항목으로 표현한다면,

* `number`: 거리 숫자
* `​street_name`: 거리명으로 문자
* `street_type`: 거리 형태, 문자
* `direction`: 방향, 문자

위와 같은 경우,

```json
{
  "type": "array",
  "items": [
    {
      "type": "number"
    },
    {
      "type": "string"
    },
    {
      "type": "string",
      "enum": ["Street", "Avenue", "Boulevard"]
    },
    {
      "type": "string",
      "enum": ["NW", "NE", "SW", "SE"]
    }
  ]
}
```
이라고 스키마를 지정하면,

> [1600, "Pennsylvania", "Avenue", "NW"]

는 검증에 성공하지만,

> [24, "Sussex", "Drive"]

또는 

> ["Palais de l'Élysée"]

는 모두 실패합니다.

하지만 각 항목의 갯수를 맞출 필요는 없습니다.

> [10, "Downing", "Street"]

네번째 항목이 빠져도 성공이고,

> [1600, "Pennsylvania", "Avenue", "NW", "Washington"]

항목이 하나 더 나와도 성공입니다.

여기서 `additionalItems`가 사용될 수 있습니다.

```json
{
  "type": "array",
  "items": [
    {
      "type": "number"
    },
    {
      "type": "string"
    },
    {
      "type": "string",
      "enum": ["Street", "Avenue", "Boulevard"]
    },
    {
      "type": "string",
      "enum": ["NW", "NE", "SW", "SE"]
    }
  ],
  "additionalItems": false
}
```

`"additionalItems"` 항목이 `false`라면 

> [1600, "Pennsylvania", "Avenue", "NW"]
> 
> ​[1600, "Pennsylvania", "Avenue"]

정확히 4개인 항목과 하나 부족한 것은 검증에 성공하지만,

> [1600, "Pennsylvania", "Avenue", "NW", "Washington"]

하나 더 많은 것은 실패하게 됩니다.

##### Length

목록의 길이는 `minItems` 와 `maxItems`로 지정할 수 있습니다.

```json
{
  "type": "array",
  "minItems": 2,
  "maxItems": 3
}
```

> [1, 2]
> 
> [1, 2, 3]

는 검증에 성공하지만,

> []
> 
> [1]
> 
> [1,2,3,4]

는 검증에 실패합니다.


##### Uniqueness

목록에 각 항목의 내용이 중복되지 않도록 하는 것으로 `uniqueItems` 키워드를 `true`로 설정하여 이용할 수 있습니다.

``` json
{
  "type": "array",
  "uniqueItems": true
}
```
라는 JSON 스키마가 있다면,

> [1, 2, 3, 4, 5]
> 
> []

빈 목록을 포함하여 검증에 성공하지만,

> [1, 2, 3, 3, 4]

는 중복된 항목 3이 있으므로 실패합니다.


### boolean

블리언 형식은 `true` 또는 `false`를 갖는 형식입니다. (파이썬의 `True` 및 `False` 와는 달리 모두 소문자 임을 주의합니다)

```json
{ "type": "boolean" }
```

> true
> 
> false

는 검증에 성공하고

> "true"
> 
> 0

은 실패합니다.


### null

null 형식은 아무런 값도 가지고 있지 않다라는 것을 나타냅니다. (파이썬의 None 객체와 유사하다 생각하면 됩니다. JavaScript의 null 의미입니다)

```json
{ "type": "null" }
```
라고 JSON 스키마가 정의되어 있다면

> null

은 성공하지만,

> false
> 
> 0
> 
> ""

등은 모두 실패합니다.


## Generic keywords

이곳에서는 JSON 형식에서 가능한 기타 키워드 등을 기술합니다.

### Metadata

JSON 스키마에는 `title`, `description`, 및 `default`라는 키워드가 있어 직접 검증에 이용되지는 않지만 스키마의 일부분을 정의하는 메타 속성을 정의합니다.

`title` 과 `description` 키워드는 문자열 값을 가집니다. 해당 스키마의 제목과 설명을 기술하면 됩니다.

`defaul` 키워드는 해당 속성의 디폴트 값을 지정합니다. 아직 많은 JSON 스키마 검증 프로그램이 이 키워드를 제대로 지원하지 않지만 특정 키-값이 빠졌을 때 디폴트 값을 갖는 키-값 이 적용되도록  JSON 처리기가 동작하도록 할 수 있습니다.

다음과 같이 적용됩니다.

```json
{
  "title" : "Match anything",
  "description" : "This is a schema that matches anything.",
  "default" : "Default value"
}
```

### 열거형 값 (Enumerated values)

`enum` 키워드는 주어진 세트의 값으로만 구성될 때 이용할 수 있습니다. 중복되지 않으며 적어도 하나 이상의 값을 가지고 있는 목록으로 기술됩니다.

``` json
{
  "type": "string",
  "enum": ["red", "amber", "green"]
}
```

> "red"

는 검증에 성공하지만,

> "blue"

는 검증에 실패합니다.

`type`을 가지지 않고 `enum` 만을 이용하여 서로 다른 자료형의 값 세트를 정할 수 있습니다.

```json
{
  "enum": ["red", "amber", "green", null, 42]
}
```
이라고 JSON 스키마가 있다면

> "red"
>  
> null
> 
> 42

는 모두 검증에 성공하지만,

> 0

은 검증에 실패합니다.

```json
{
  "type": "string",
  "enum": ["red", "amber", "green", null]
}
```
와 같이 섞여 있는 경우도 있는데

> "red"

는 검증에 성공하지만,

> null

이 오면 `"type": "string"` 에 의해 검증은 실패하게 됩니다.


### 스키마 결합

JSON 스키마는 스키마 정의를 결합아여 사용할 수 있습니다. 이것은 여러 JSON 스키마 파일이나 JSON 트리를 서로 결합하는 것을 의미하지 않고 대신 여러 정의 어떤 식으로 이용하는가를 정의합니다.

예를 들어 다음과 같은 `anyOf` 라는 키워드를 이용하여

```json
{
  "anyOf": [
    { "type": "string", "maxLength": 5 },
    { "type": "number", "minimum": 0 }
  ]
}
```
라고 JSON 스키마를 지정하면 두 개의 조건을 만족하는 것이면 모두 검증에 성공합니다.

즉,

> "short"
> 
> 12

는 두 조건에 모두 만족하는 것이므로 검증에 성공하지만,

> "too long"
> 
> -5
는 두 조건에 만족하지 않으므로 검증에 실패합니다.

이런 결합 키워드로는 다음과 같이 세 가지가 있습니다.

* `allOf`: 결합된 하위 스키마 모두를 만족해야 검증에 성공합니다
* `anyOf`: 결합된 하위 스키마 중에 하나로도 만족하면 검증에 성공합니다.
* `oneOf`: 결합된 하위 스키마 중에 단 하나의 조건에만 만족해야 검증에 성공합니다.

또한 

* `not`: 주어진 스키마가 거짓인 경우 검증에 성공합니다

#### allOf

```json
{
  "allOf": [
    { "type": "string" },
    { "maxLength": 5 }
  ]
}
```
위와 같은 JSON 스키마가 있으면

> "short"

은 검증에 성공하고

> "too long"

은 검증에 실패합니다.

그런데 만약

```json
{
  "allOf": [
    { "type": "string" },
    { "type": "number" }
  ]
}
```
라고 주었다면

> "No way"
> 
> -1

모두 조건을 동시에 만족하지 않으므로 검증에 실패합니다.

`allOf`, `anyOf` 또는 `oneOf`에 기술된 하위 스키마 목록에서 서로 서로 관계가 없다는 것을 알 필요가 있다.  반면 `allOf` 스키마 결합이 객체 지향 프로그램에서의 상속과 같은 개념으로 확장에 이용된지 않음을 알아야 한다. 예를 들어 다음과 같이 `definitions` 섹션에서 주소 스키마를 가지고 있고 주소 type이 또한 필요하다면,

``` json
{
  "definitions": {
    "address": {
      "type": "object",
      "properties": {
        "street_address": { "type": "string" },
        "city":           { "type": "string" },
        "state":          { "type": "string" }
      },
      "required": ["street_address", "city", "state"]
    }
  },

  "allOf": [
    { "$ref": "#/definitions/address" },
    { "properties": {
        "type": { "enum": [ "residential", "business" ] }
      }
    }
  ]
}
```

와 같이 JSON 스키마가 만들어져 있고,

```json
{
   "street_address": "1600 Pennsylvania Avenue NW",
   "city": "Washington",
   "state": "DC",
   "type": "business"
}
```
는 검증에 성공합니다.

하지만,

```json
{
  "definitions": {
    "address": {
      "type": "object",
      "properties": {
        "street_address": { "type": "string" },
        "city":           { "type": "string" },
        "state":          { "type": "string" }
      },
      "required": ["street_address", "city", "state"]
    }
  },

  "allOf": [
    { "$ref": "#/definitions/address" },
    { "properties": {
        "type": { "enum": [ "residential", "business" ] }
      }
    }
  ],

  "additionalProperties": false
}
```
와 같이 ` "additionalProperties": false`가 포함되면 위에 성공했던 JSON 자료는 실패하게 됩니다. 뿐만 아니라 어떤 JSON 데이터도 모두 실패합니다.

#### anyOf

```json
{
  "anyOf": [
    { "type": "string" },
    { "type": "number" }
  ]
}
```
위와 같이 `anyOf`를 사용하면

> "Yes"
> 
> 42

는 검증에 성공하고

> { "Not a": "string or number" }

는 object 이므로 검증에 실패합니다.

#### oneOf

``` json
{
  "oneOf": [
    { "type": "number", "multipleOf": 5 },
    { "type": "number", "multipleOf": 3 }
  ]
}
```
이면 

> 10
> 
> 9

는 5의 배수 이거나 3의 배수라 검증에 성공하지만,

> 2

는 5와 3의 배수가 모두 아니므로 실패하고,

> 15

는 5와 3의 배수가 동시에 되므로 (하나만 만족하는 조건에 위배되어) 실패합니다.

위의 스키마는 다음과 같이 표현될 수도 있습니다.

```json
{
  "type": "number",
  "oneOf": [
    { "multipleOf": 5 },
    { "multipleOf": 3 }
  ]
}
```

#### not

``` json
{ "not": { "type": "string" } }
```
라는 JSON 스키마가 정의되어 있다면,

> 42
> 
> { "key": "value" }

는 문자열이 아니므로 검증에 성공하지만

> "I am a string"

는 문자열이라 검증에 실패합니다.

### $schema 키워드

JSON 스키마의 표준 혹은 버전 등을 명시하는데 사용됩니다. 모든 JSON 스키마는 `$schema` 를 시작에 포함하도록 권고됩니다.

```json
"$schema": "http://json-schema.org/schema#"
```

### 정규식

``` json
{
   "type": "string",
   "pattern": "^(\\([0-9]{3}\\))?[0-9]{3}-[0-9]{4}$"
}
```
라고 하면

> "555-1212"
> 
> "(888)555-1212"

은 검증에 성공하고

> "(888)555-1212 ext. 532"
> 
> "(800)FLOWERS"

은 검증에 실패합니다.


## 복잡한 스키마 구성

일반 프로그램을 작성할 때에도 재사용할 함수나 코드를 잘 구조화하고 이를 이용하는 것 처럼 JSON 스키마도 구성할 수 있습니다. 이런 방식을 잘 사용하여 복잡하고 어려운 구조도 보다 잘 구조화 할 수 있습니다.

### Reuse

다음과 같이 일반 고객을 담고 있는 스키마를 구성하고 있습니다.

> 노트: 재사용은 draft 3에는 없고 draft 4에 나타납니다.

```json
{
  "type": "object",
  "properties": {
    "street_address": { "type": "string" },
    "city":           { "type": "string" },
    "state":          { "type": "string" }
  },
  "required": ["street_address", "city", "state"]
}
```
재사용을 목적으로 하면 `definitions` 키워드를 이용합니다.

``` json
{
  "definitions": {
    "address": {
      "type": "object",
      "properties": {
        "street_address": { "type": "string" },
        "city":           { "type": "string" },
        "state":          { "type": "string" }
      },
      "required": ["street_address", "city", "state"]
    }
  }
}
```

그러면 `$ref` 키워드를 이용하여 해당 스키마를 사용합니다.

```json
{ "$ref": "#/definitions/address" }
```

`$ref`의 값은 JSON 포인터라고 불리우는 해당 스키마의 위치를 나타냅니다.

> 노트: JSON 포인터는 XML에서의 XPath와 같은 목적으로 사용되지만 문법은 차이가 있습니다.

`#` 기호는 현재 문서를 나타내고 각 구분자는 `/` 기호를 이용합니다. 따라서 `"#/definitions/address"`가 의미하는 것은

1. 현재 문서의 최상위로 간다
2. `"definitions"` 이라는 키를 찾아 들어간다
3. 그 아래에 `"address"`라는 키를 가진 객체에 위치한다

`$ref`는 또는 URI와 같은 기술이 가능합니다. 따라서 

```json
{ "$ref": "definitions.json#/address" }
```
라고 하여 `definitions.json` 파일에서 최상위 (`#`)에서 `address` 키의 값을 참조합니다.

```json
{
  "$schema": "http://json-schema.org/draft-04/schema#",

  "definitions": {
    "address": {
      "type": "object",
      "properties": {
        "street_address": { "type": "string" },
        "city":           { "type": "string" },
        "state":          { "type": "string" }
      },
      "required": ["street_address", "city", "state"]
    }
  },

  "type": "object",

  "properties": {
    "billing_address": { "$ref": "#/definitions/address" },
    "shipping_address": { "$ref": "#/definitions/address" }
  }
}
```

위와 같이 정의하면, ​` "billing_address"` 및 `"shipping_address"`의 키가 해당 address의 object 구조를 갖습니다.

``` json
{
  "shipping_address": {
    "street_address": "1600 Pennsylvania Avenue NW",
    "city": "Washington",
    "state": "DC"
  },
  "billing_address": {
    "street_address": "1st Street SE",
    "city": "Washington",
    "state": "DC"
  }
}
```

위의 내용은 검증에 성공합니다.

### id 속성

`id` 속성은 두 가지 목적을 갖습니다.
* 특정 스키마의 고유한 ID를 정의합니다
* `$ref` 로 URL에 정의되어 질 수 있는 base가 됩니다

만약 `foo.bar` 라는 도메인을 가지고 있다면 다음과 같이 고유한  `id`를 URL 형식으로 가지고 있을 수 있습니다.

```json
"id": "http://foo.bar/schemas/address.json"
```

위의 것은 어디에서 다운로드 받을 수 있는가를 나타내는 URL 정보 뿐만 아니라 특정 스키마의 고유 정보를 나타냅니다.

그리고 또 다른 활용 방법으로써 `id` 속성을 이용하여 상대 경로의 내용을 `$ref`로 이용할 수 있습니다.

예를 들어,

```json
{ "$ref": "person.json" }
```
라고 지정하면 address.json 이 있었던 위치에서 person.json을 참조합니다. 즉, `http://foo.bar/schemas/person.json`를 참조합니다. (로컬에 있었어도 마찬가지 입니다)


### 확장 (Extending)

`$ref`의 진정한 확장성은 `allOf`, `anyOf` 및 `oneOf`과 같은 스키마 결합 기능과 함께 사용하면 더 배가됩니다.

위의 예에서 처럼,

``` json
"shipping_address": { "$ref": "#/definitions/address" }
```
라고 참조하는 대신

```json
"shipping_address": {
  "allOf": [
    // Here, we include our "core" address schema...
    { "$ref": "#/definitions/address" },

    // ...and then extend it with stuff specific to a shipping
    // address
    { "properties": {
        "type": { "enum": [ "residential", "business" ] }
      },
      "required": ["type"]
    }
  ]
}
```
위와 같이 `allOf` 키워드를 이용하여 기존의 `address` 에 `type` 이라는 것을 더 확장할 수 있습니다.

위에 이야기 한 것을 모두 하나의 스키마로 표현해 보면,

```json
{
  "$schema": "http://json-schema.org/draft-04/schema#",

  "definitions": {
    "address": {
      "type": "object",
      "properties": {
        "street_address": { "type": "string" },
        "city":           { "type": "string" },
        "state":          { "type": "string" }
      },
      "required": ["street_address", "city", "state"]
    }
  },

  "type": "object",

  "properties": {
    "billing_address": { "$ref": "#/definitions/address" },
    "shipping_address": {
      "allOf": [
        { "$ref": "#/definitions/address" },
        { "properties":
          { "type": { "enum": [ "residential", "business" ] } },
          "required": ["type"]
        }
      ]
    }
  }
}
```
과 같이 확장 스키마를 정할 수 있으며,

```json
{
  "shipping_address": {
    "street_address": "1600 Pennsylvania Avenue NW",
    "city": "Washington",
    "state": "DC",
    "type": "business"
  }
}
```
과 같은 JSON 데이터는 검증에 성공하지만,

```json
{
  "shipping_address": {
    "street_address": "1600 Pennsylvania Avenue NW",
    "city": "Washington",
    "state": "DC"
  }
}
```
과 같은 결과는 검증에 실패합니다.

## [관련 저자](https://spacetelescope.github.io/understanding-json-schema/credits.html)

## 역자정보 [채문창](https://www.facebook.com/mcchae)

어느분께는 도움이 되셨기를...
