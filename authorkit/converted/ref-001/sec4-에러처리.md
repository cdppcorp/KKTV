
**제4절 에러처리**

에러를 처리하지 않거나 불충분하게 처리하여 에러 정보에 중요정보(시스템 내부정보 등)가 포함될 때 발생
할 수 있는 보안약점이다.
1. 오류 메시지 정보노출
가. 개요
응용 프로그램이 실행환경, 사용자 등 관련 데이터에 대한 민감한 정보를 포함하는 오류 메시지를 생성해
외부에 제공하는 경우 공격자의 악성 행위로 이어질 수 있다. 예외발생 시 예외 이름이나 추적 메시지
(traceback)를 출력하는 경우 프로그램 내부 구조를 쉽게 파악할 수 있기 때문이다.
Django 프레임워크와 Flask 프레임워크는 HTTP 오류 코드가 있는 요청을 처리하기 위한 사용자 에러 페이지
핸들러를 제공한다.
나. 안전한 코딩기법
오류 메시지는 정해진 사용자에게 유용한 최소한의 정보만 포함하도록 한다. 소스코드에서 예외 상황은 내부적
으로 처리하고 사용자에게 시스템 내부 정보 등 민감한 정보를 포함하는 오류를 출력하지 않고 미리 정의된
메시지를 제공하도록 설정한다.
Django 프레임워크에서는 urls.py에 사용자 정의 에러 페이지 핸들러를 정의할 수 있다.

![p131 이미지](images/p131_img0.png)

다. 코드예제
사용자 요청을 정상적으로 처리할 수 없는 경우 에러 페이지에 디버그 정보 또는 서버의 정보가 노출될 수
있다. 어플리케이션 배포 시 DEBUG 모드를 True로 설정하고 배포할 경우에 아래와 같이 시스템의 주요 정보가
노출될 수도 있다. Django는 DEBUG 모드를 False로 배포했을 경우 아래와 같이 사용자 에러 페이지를 설정
하지 않으면 Django 기본 에러 페이지가 출력된다.

**안전하지 않은 코드 예시**

1:
2:
# config/urls.py
# 별도의 에러 페이지를 선언하지 않아 django의 기본 에러 페이지를 출력한다
제공되는 에러 페이지 핸들러를 이용해 별도의 에러 페이지를 생성하여 사용자에게 표현하고 서버의 정보노출을
최소화해야 한다.

![p132 이미지](images/p132_img1.png)


![p132 이미지](images/p132_img2.png)


![p132 이미지](images/p132_img3.png)


**안전한 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
# config/urls.py
from django.conf.urls import handler400, handler403, handler404, handler500
# 사용자 정의 에러 페이지를 지정하고
# views.py에 사용자 정의 에러 페이지에 대한 코드를 구현하여 사용한다
handler400 = "blog.views.error400"
handler403 = "blog.views.error403"
handler404 = "blog.views.error404"
handler500 = "blog.views.error500“
아래는 traceback을 사용하여 에러 스택을 표준 출력으로 표시해 정보가 노출되는 예제를 보여 준다.

**안전하지 않은 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
11:
12:
13:
14:
15:
import traceback
def fetch_url(url, useragent, referer=None, retries=1, dimension=False):
......
try:
response = requests.get(
url,
stream=True,
timeout=5,
headers={ 'User-Agent': useragent, 'Referer': referer },
)
......
except IOError:
# 에러메시지를 통해 스택 정보가 노출.
traceback.print_exc()

![p133 이미지](images/p133_img1.png)


![p133 이미지](images/p133_img2.png)


![p133 이미지](images/p133_img4.png)


![p133 이미지](images/p133_img5.png)

오류 처리 시 아래와 같이 에러 이름이나 에러 추적 정보가 노출되지 않도록 한다.

**안전한 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
11:
12:
13:
import logging
def fetch_url(url, useragent, referer=None, retries=1, dimension=False):
......
try:
response = requests.get(url, stream=True, timeout=5, headers={
'User-Agent': useragent,
'Referer': referer,
})
  ......
except IOError:
# 에러 코드와 정보를 별도로 정의하고 최소 정보만 로깅
logger.error('ERROR-01:통신에러')
라. 참고자료
① CWE-209: Generation of Error Message Containing Sensitive Information, MITRE
https://cwe.mitre.org/data/definitions/209.html
② Improper Error Handling, OWASP,
https://owasp.org/www-community/Improper_Error_Handling
③ Errors and Exceptions, Python Software Foundation,
https://docs.python.org/3/tutorial/errors.html
➃ Django Error views, Django Software Foundation,
https://docs.djangoproject.com/en/3.2/ref/views/#error-views
➄ Flask Error Handlers, Flask
https://flask.palletsprojects.com/en/2.0.x/errorhandling/#error-handlers

![p134 이미지](images/p134_img1.png)


![p134 이미지](images/p134_img2.png)

2. 오류상황 대응 부재
가. 개요
오류가 발생할 수 있는 부분을 확인하였으나 이러한 오류에 대해 예외 처리를 하지 않을 경우 공격자는 오류
상황을 악용해 개발자가 의도하지 않은 방향으로 프로그램이 동작하도록 할 수 있다.
예외처리는 코드를 견고하게 만들고 프로그램 제어 실패로 인해 의도치 않은 중단으로 이어지는 잠재적인
오류를 방지하는데 도움이 된다.
나. 안전한 코딩기법
오류가 발생할 수 있는 부분에 대하여 제어문(try-except)을 사용해 적절하게 예외 처리한다.
다. 코드예제
다음 예제는 try 블록에서 발생하는 오류를 포착(except)하고 있지만 그 오류에 대해서 아무 조치를 하지
않는 상황을 보여준다. 아무 조치가 없으므로 프로그램이 계속 실행되기 때문에 개발자가 의도하지 않은 방향
으로 프로그램이 동작할 수 있다.

![p135 이미지](images/p135_img0.png)


**안전하지 않은 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
11:
12:
13:
14:
15:
16:
17:
18:
19:
20:
21:
22:
23:
24:
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
static_keys=[
{'key' : b'\xb9J\xfd\xa9\xd2\xefD\x0b\x7f\xb2\xbcy\x9c\xf7\x9c',
‘iv'  : b'\xf1BZ\x06\x03TP\xd1\x8a\xad"\xdc\xc3\x08\x88\xda'},
{'key' : b'Z\x01$.:\xd4u3~\xb6TS(\x08\xcc\xfc',
'iv'  : b'\xa1a=:\xba\xfczv]\xca\x83\x9485\x14\x17'},
]
def encryption(key_id, plain_text):
static_key = {'key':b'0000000000000000', 'iv':b'0000000000000000'}
try:
static_key = static_keys[key_id]
except IndexError:
# key 선택 중 오류 발생 시 기본으로 설정된 암호화 키인
# ‘0000000000000000’ 으로 암호화가 수행된다.
pass
cipher_aes = AES.new(static_key['key'],AES.MODE_CBC,static_key['iv'])
encrypted_data = base64.b64encode(cipher_aes.encrypt(pad(plain_text.encode(), 32)))
return encrypted_data.decode('ASCII')
예외상황 발생 시에 프로그램이 개발자의 의도와 다르게 동작하지 않도록 반드시 예외 처리 구문을 추가해야 한다.

![p136 이미지](images/p136_img1.png)


![p136 이미지](images/p136_img2.png)


**안전한 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
11:
12:
13:
14:
15:
16:
17:
18:
19:
20:
21:
22:
23:
24:
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
static_keys=[
{'key' : b'\xb9J\xfd\xa9\xd2\xefD\x0b\x7f\xb2\xbcy\x9c\xf7\x9c',
‘iv'  : b'\xf1BZ\x06\x03TP\xd1\x8a\xad"\xdc\xc3\x08\x88\xda'},
{'key' : b'Z\x01$.:\xd4u3~\xb6TS(\x08\xcc\xfc',
'iv'  : b'\xa1a=:\xba\xfczv]\xca\x83\x9485\x14\x17'},
]
def encryption(key_id, plain_text):
static_key = {'key':b'0000000000000000', 'iv':b'0000000000000000'}
try:
static_key = static_keys[key_id]
except IndexError:
# key 선택 중 오류 발생 시 랜덤으로 암호화 키를 생성하도록 설정
static_key = {'key': secrets.token_bytes(16), 'iv': secrets.token_bytes(16)}
static_keys.append(static_key)
cipher_aes = AES.new(static_key['key'],AES.MODE_CBC,static_key['iv'])
encrypted_data = base64.b64encode(cipher_aes.encrypt(pad(plain_text.encode(), 32)))
return encrypted_data.decode('ASCII')
라. 참고자료
① CWE-390: Detection of Error Condition Without Action, MITRE,
https://cwe.mitre.org/data/definitions/390.html
② Errors and Exceptions, Python Software Foundation,
https://docs.python.org/3/tutorial/errors.html
➂ Built-in Exceptions, Python Software Foundation,
https://docs.python.org/3/library/exceptions.html

![p137 이미지](images/p137_img1.png)


![p137 이미지](images/p137_img2.png)

3. 부적절한 예외 처리
가. 개요
프로그램 수행 중에 함수의 결과 값에 대한 적절한 처리 또는 예외 상황에 대한 조건을 적절하게 검사 하지
않을 경우 예기치 않은 문제를 야기할 수 있다.
나. 안전한 코딩기법
값을 반환하는 모든 함수의 결과값을 검사해야 한다. 결과값이 개발자가 의도했던 값인지 검사하고 예외 처리를
사용하는 경우에 광범위한 예외 처리 대신 구체적인 예외 처리를 수행한다.
다. 코드예제
다음 예제는 다양한 예외가 발생할 수 있음에도 불구하고 광범위한 예외 처리로 예외상황에 따른 적절한
조치가 부적절한 사례를 보여 준다.

**안전하지 않은 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
11:
import sys
def get_content():
try:
f = open('myfile.txt')
s = f.readline()
i = int(s.strip())
# 예외처리를 세분화 할 수 있음에도 광범위하게 사용하여 예기치 않은
# 문제가 발생할 수 있다
except:
print("Unexpected error ")
다음은 발생 가능한 예외를 세분화한 후 예외상황에 따라 적합한 처리한 예시를 보여 준다.

![p138 이미지](images/p138_img1.png)


![p138 이미지](images/p138_img2.png)


**안전한 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
11:
12:
13:
def get_content():
try:
f = open('myfile.txt')
s = f.readline()
i = int(s.strip())
# 발생할 수 있는 오류의 종류와 순서에 맞춰서 예외 처리 한다.
except FileNotFoundError:
print("file is not found")
except OSError:
print("cannot open file")
except ValueError:
print("Could not convert data to an integer.")
라. 참고자료
① CWE-754: Improper Check for Unusual or Exceptional Conditions, MITRE,
https://cwe.mitre.org/data/definitions/754.html
② Errors and Exceptions, Python Software Foundation,
https://docs.python.org/3/tutorial/errors.html
➂ Built-in Exceptions, Python Software Foundation,
https://docs.python.org/3/library/exceptions.html

![p139 이미지](images/p139_img1.png)


![p139 이미지](images/p139_img2.png)
