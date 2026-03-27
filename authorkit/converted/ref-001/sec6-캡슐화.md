
**제6절 캡슐화**

중요한 데이터 또는 기능성을 불충분하게 캡슐화하거나 잘못 사용함으로써 발생하는 보안약점으로 정보노출,
권한 문제 등이 발생할 수 있다.
1. 잘못된 세션에 의한 데이터 정보 노출
가. 개요
다중 스레드 환경에서는 싱글톤(Singleton) 객체 필드에 경쟁조건(Race Condition)이 발생할 수 있다. 따라서
다중 스레드 환경에서는 정보를 저장하는 전역 변수가 포함되지 않도록 코드를 작성해 서로 다른 세션에서
데이터를 공유하지 않도록 해야 한다.
나. 안전한 코딩기법
싱글톤 패턴을 사용하는 경우 변수 범위(Scope)에 주의를 기울여야 한다. 특히 다중 스레드 환경에서 클래스
변수의 값은 하위 메소드와 공유되므로 필요한 경우 인스턴스 변수로 선언하여 사용한다.

![p149 이미지](images/p149_img0.png)

다. 코드예제
다중 스레드 환경에서 파이썬의 클래스 변수는 스레드 간 서로 공유하게 된다. 클래스 변수에 값을 할당할
경우 서로 다른 세션 간에 데이터가 공유되어 의도하지 않은 데이터가 전달될 수 있다.

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
from django.shortcuts import render
class UserDescription:
user_name = ''
def get_user_profile(self):
result = self.get_user_discription(UserDescription.user_name)
......
return result
def show_user_profile(self, request):
# 클래스변수는 다른 세션과 공유되는 값이기 때문에 멀티스레드
# 환경에서 공유되지 않아야 할 자원을 사용하는 경우
# 다른 스레드 세션에 의해 데이터가 노출될 수 있다
UserDescription.user_name = request.POST.get(‘name’, ‘’)
self.user_profile = self.get_user_profile()
return render(request, 'profile.html', {'profile':self.user_profile})
공유가 금지된 변수는 인스턴스 변수로 선언하여 세션 간에 공유되지 않도록 한다.

![p150 이미지](images/p150_img1.png)


![p150 이미지](images/p150_img2.png)


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
from django.shortcuts import render
class UserDescription:
def get_user_profile(self):
result = self.get_user_discription(self.user_name)
......
return result
def show_user_profile(self, name):
# 인스턴스 변수로 사용해 스레드 간 공유되지 않도록 한다
self.user_name = request.POST.get(‘name’, ‘’)
self.user_profile = self.get_user_profile()
return render(request, 'profile.html', {'profile':self.user_profile})
라. 참고자료
① CWE-488: Exposure of Data Element to Wrong Session, MITRE,
https://cwe.mitre.org/data/definitions/488.html
② CWE-543: Use of Singleton Pattern Without Synchronization in a Multithreaded Context, MITRE,
https://cwe.mitre.org/data/definitions/543.html
➂ The global statement, Python Software Foundation,
https://docs.python.org/3/reference/simple_stmts.html#global

![p151 이미지](images/p151_img1.png)


![p151 이미지](images/p151_img2.png)

2. 제거되지 않고 남은 디버그 코드
가. 개요
디버깅 목적으로 삽입된 코드는 개발이 완료되면 제거해야 한다. 디버그 코드는 설정 등의 민감한 정보 또는
의도하지 않은 시스템 제어로 이어질 수 있는 정보를 담고 있을 수 있다. 만일 디버그 코드가 남겨진 채로
배포될 경우 공격자가 식별 과정을 우회하거나 의도하지 않은 정보 노출로 이어질 수 있다.
Django 프레임워크, Flask 프레임워크는 전역 수준에서 DEBUG 모드를 설정할 수 있다. DEBUG 모드를
사용하면 브라우저에서 임의의 파이썬 코드를 실행할 수도 있고 파이썬에서 발생한 모든 오류가 출력되어 정보
노출의 위험이 있다. 어플리케이션을 배포 전에 반드시 DEBUG 모드를 비활성화 해야 한다.
나. 안전한 코딩기법
소프트웨어 배포 전 반드시 디버그 코드를 확인 및 삭제한다. Django 프레임워크의 경우 전역 수준에서
DEBUG 모드를 비활성화 하려면 settings.py 파일에 설정을 하고 Flask 프레임워크는 app_run() 전에
debug = False로 설정하면 된다.

![p152 이미지](images/p152_img0.png)


![p152 이미지](images/p152_img1.png)

다. 코드예제
다음은 Django의 미들웨어 세팅 파일인 settings.py 파일 예시로, 개발 시 사용된 DEBUG 옵션이 True로
설정되어 있어 정보 노출의 위험이 있다.
가) Django 예제

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
from django.urls import reverse_lazy
from django.utils.text import format_lazy
DEBUG = True
ROOT_URLCONF = 'test.urls'
SITE_ID = 1
DATABASES = {
'default': {
'ENGINE': 'django.db.backends.sqlite3',
'NAME': ':memory:',
}
}
개발이 끝난 소스코드를 배포 및 운영할 경우에는 반드시 DEBUG 옵션을 False로 변경해야 한다.

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
from django.urls import reverse_lazy
from django.utils.text import format_lazy
DEBUG = False
ROOT_URLCONF = 'test.urls'
SITE_ID = 1
DATABASES = {
'default': {
'ENGINE': 'django.db.backends.sqlite3',
'NAME': ':memory:',
}
}

![p153 이미지](images/p153_img1.png)


![p153 이미지](images/p153_img2.png)


![p153 이미지](images/p153_img4.png)


![p153 이미지](images/p153_img5.png)

나) Flask 예제
다음은 Flask의 예제로, debug 모드가 True로 설정되어 정보 노출의 위험이 있다.

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
from flask import Flask
app = Flask(__name__)
# 디버그 모드 설정 방법1
app.debug = True
@app.route('/')
def hello_world():
return 'Hello World!'
if __name__ == '__main__':
app.run()
# 디버그 모드 설정 방법2
app.run(debug=True)
마찬가지로 개발이 끝난 소스코드를 배포 및 운영 시 반드시 debug 옵션을 False로 변경해야 한다.

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
from flask import Flask
app = Flask(__name__)
app.debug = False
@app.route('/')
def hello_world():
return 'Hello World!'
if __name__ == '__main__':
app.run()
app.run(debug=False)

![p154 이미지](images/p154_img1.png)


![p154 이미지](images/p154_img2.png)


![p154 이미지](images/p154_img4.png)


![p154 이미지](images/p154_img5.png)

라. 참고자료
① CWE-489: Active Debug Code, MITRE,
https://cwe.mitre.org/data/definitions/489.html
② Settings, Django Software Foundation,
https://docs.djangoproject.com/en/3.2/ref/settings/#debug
➂ Debug Mode, Flask,
https://flask.palletsprojects.com/en/2.0.x/quickstart/#debug-mode
3. Public 메소드로부터 반환된 Private 배열
가. 개요
파이썬은 명시적인 private 선언이 없다. 하지만 대부분의 파이썬 코드가 따르는 규칙으로 이름 앞에 밑줄
(예:__spam)로 시작하면 private 로 처리된다. public으로 선언된 메소드에서 배열을 반환하면 해당 배열의
참조 객체가 외부에 공개되어 외부에서 배열 수정과 객체 속성 변경이 가능해진다. 이러한 속성은 배열 뿐만
아니라 변경 가능한(mutable) 모든 객체에 해당된다.
구분
표시 방법
public
attribute, method는 기본적으로 public
protect
attribute, method 앞에 _(single underscore)를 붙여서 표시 함.
실제 제약 보다는 관례적임.
private
attribute, method 앞에 __(double underscore)를 붙여서 표시 함.
파이썬은 네임 맹글링(name mangling)으로 private 멤버에 _class__member로 접근은 가능하지만
바람직하지 않음.
나. 안전한 코딩기법
private로 선언된 배열을 public으로 선언된 메소드로 반환하지 않도록 한다. private 배열에 대한 복사본을
반환하도록 하고 배열의 원소에 대해서는 clone() 메소드를 통해 복사된 원소를 저장하도록 해서 private 선언된
배열과 객체 속성에 대한 의도치 않은 수정을 방지한다. 만약 배열의 원소가 String 타입 등과 같이 변경이
되지 않는 경우(immutable)에는 private 배열의 복사본을 만들고 이를 반환하도록 작성한다.
다. 코드예제
다음 예제는 private 변수를 생성하고 이를 반환하는 public 메소드를 사용하는 예시를 보여 준다. 이 경우
외부에서 클래스 내에 숨겨져 있는 private 배열 값에 접근할 수 있는 문제점이 발생한다.

![p156 이미지](images/p156_img0.png)


**안전하지 않은 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
class UserObj:
__private_variable = []
def __init__(self):
pass
# private 배열을 리턴하는 public 메소드를 사용하는 경우 취약함
def get_private_member(self):
return self.__private_variable
아래 예제는 내부와 외부의 배열이 서로 참조되는 것을 예방하기 위해 [:]로 새로운 객체를 생성하여 값을
반환하고 있다.

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
class UserObj:
__private_variable = []
def __init__(self):
pass
# private 배열을 반환하는 경우 [:]를 사용하여 외부와 내부의
# 배열이 서로 참조되지 않도록 해야 한다
def get_private_member(self):
return self.__private_variable[:]
라. 참고자료
① CWE-495: Private Data Structure Returned From A Public Method, MITRE,
https://cwe.mitre.org/data/definitions/495.html
② Do not return references to private mutable class members, CERT,
https://wiki.sei.cmu.edu/confluence/display/java/OBJ05-J.+Do+not+return+references+to+private+mutable
+class+members
③ Shallow and deep copy operations, Python Software Foundation,
https://docs.python.org/3/library/copy.html

![p157 이미지](images/p157_img1.png)


![p157 이미지](images/p157_img2.png)


![p157 이미지](images/p157_img4.png)


![p157 이미지](images/p157_img5.png)

4. Private 배열에 Public 데이터 할당
가. 개요
public으로 선언된 메소드의 인자가 private로 선언된 배열에 저장되면 private 배열을 외부에서 접근하여
배열 수정과 객체 속성 변경이 가능해진다.
나. 안전한 코딩기법
public으로 선언된 메소드의 인자를 private 로 선언된 배열에 저장하지 않도록 한다. 사용자가 전달한 값으로
클래스 외부에서 private 값을 변경해서는 안 되며, 필요한 경우 별도의 인스턴스 변수로 정의하거나 의도한
기능이라면 전달된 값의 정상 여부를 검증한 후 적용해야 한다.
다. 코드예제
다음 예제는 __를 이용해서 파이썬의 내부 배열을 생성하고 외부 값을 대입하는 public 메소드를 사용하는
예시를 보여 준다. 이 경우 특정 배열 타입에 따라 외부에서 private 배열을 변조할 수 있는 문제를 내포하고 있다.

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
class UserObj:
__private_variable = []
def __init__(self):
pass
# private 배열에 외부 값을 바로 대입하는 public 메소드를 사용하는
# 경우 취약하다
def set_private_member(self, input_list):
self.__private_variable = input_list

![p158 이미지](images/p158_img1.png)


![p158 이미지](images/p158_img2.png)


![p158 이미지](images/p158_img3.png)

아래 예제는 내부와 외부의 배열이 서로 참조되는 것을 예방하기 위해 [:]로 새로운 객체를 생성하여 값을
대입하고 있다.

**안전한 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
class UserObj:
def __init__(self):
self.__privateVariable = []
# private 배열에 외부 값을 바로 대입하는 경우 [:]를 사용하여
# 외부와 내부의 배열이 서로 참조되지 않도록 해야 한다
def set_private_member(self, input_list):
self.__privateVariable = input_list[:]
라. 참고자료
① CWE-496: Public Data Assigned to Private Array-Typed Field, MITRE,
https://cwe.mitre.org/data/definitions/496.html
② Shallow and deep copy operations, Python Software Foundation,
https://docs.python.org/3/library/copy.html
➂ Private Variables, Python Software Foundation,
https://docs.python.org/3/tutorial/classes.html#private-variables

![p159 이미지](images/p159_img1.png)


![p159 이미지](images/p159_img2.png)
