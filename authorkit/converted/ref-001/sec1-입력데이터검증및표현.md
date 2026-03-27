
# 시큐어코딩


# 가이드


**제1절 입력데이터 검증 및 표현**

프로그램 입력값에 대한 검증 누락 또는 부적절한 검증, 데이터의 잘못된 형식지정, 일관되지 않은 언어셋
사용 등으로 인해 발생되는 보안약점으로 SQL 삽입, 크로스사이트 스크립트(XSS) 등의 공격을 유발할 수 있다.
1. SQL 삽입
가. 개요
데이터베이스(DB)와 연동된 웹 응용프로그램에서 입력된 데이터에 대한 유효성 검증을 하지 않을 경우 공격자가
입력 폼 및 URL 입력란에 SQL 문을 삽입하여 DB로부터 정보를 열람하거나 조작할 수 있는 보안약점을 말한다.
취약한 웹 응용프로그램에서는 사용자로부터 입력된 값을 검증 없이 넘겨받아 동적쿼리(Dynamic Query)를
생성하기 때문에 개발자가 의도하지 않은 쿼리가 실행되어 정보유출에 악용될 수 있다.

![p14 이미지](images/p14_img0.png)


![p14 이미지](images/p14_img1.png)

파이썬에서는 데이터베이스에 엑세스에 사용되는 다양한 파이썬 모듈간의 일관성을 장려하기 위해 DB-API를
정의하고 있고 각 데이터베이스마다 별도의 DB 모듈을 이용해 데이터베이스에 엑세스하게 된다. DB-API 외에도
파이썬에서는 Django, SQLAlchemy, Storm등의 ORM(Object Relational Mapping)을 사용하여 데이터
베이스에 엑세스할 수 있다.
파이썬에서 지원하는 다양한 ORM을 이용하여 보다 안전하게 DB를 사용할 수 있지만 일부 복잡한 조건의
쿼리문 생성 어려움, 성능저하 등의 이유로 직접 원시 SQL 실행이 필요한 경우가 있다. ORM 대신 원시 쿼리를
사용하는 경우 검증되지 않은 외부 입력값으로 인해 SQL 삽입 공격이 발생할 수 있다.
나. 안전한 코딩기법
DB API 사용 시 인자화된 쿼리2)를 통해 외부 입력값을 바인딩해서 사용하면 SQL 삽입 공격으로부터 안전하게
보호할 수 있다.
파이썬에서 많이 사용되는 ORM 프레임워크로는 Django의 querySets, SQLAlchemy, Storm등이 있다.
ORM 프레임워크는 기본적으로 모든 쿼리문에 인자화된 쿼리문을 사용하므로 SQL 삽입 공격으로부터 안전하다.
ORM 프레임워크 내에서 원시 SQL을 사용할 경우에도 외부 입력값을 인자화된 쿼리문의 바인딩 변수로 사용
하면 안전한 코드를 작성할 수 있다.
다. 코드 예제
가) DB API 사용 예제
다음은 MySQL, PostgreSQL의 DB API를 사용해 입력값을 받아 처리 하는 안전하지 않은 코드 예시다.
외부 입력값을 입력 받아 변수 name과 content_id에 할당하고(line 8-9), 이 name과 content_id 값에 대한
별도의 검증 없이 쿼리문의 인자 값으로 사용하는 단순 문자열 결합을 통해 쿼리를 생성하고 있다(line 12-15).
이 경우 content_id 값으로 ‘a’ or ‘a’ = ‘a와 같은 공격 문자열을 입력하면 조건절이 content_id = ‘a’ or
‘a’ = ‘a’로 바뀌고, 그 결과 board 테이블 전체 레코드의 name 컬럼의 내용이 공격자가 전달한 name의
값으로 변경된다.
2) 사용자가 전달한 입력값을 그대로 쿼리 문자열로 만들지 않고, DB API에서 제공하는 기능을 사용해 쿼리
내에 사용자 입력값을 구성하는 방법을 의미

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
from django.shortcuts import render
from django.db import connection
def update_board(request):
......
dbconn = connection
with dbconn.cursor() as curs:
# 외부로부터 입력받은 값을 검증 없이 사용할 경우 안전하지 않다
name = request.POST.get('name', '')
content_id = request.POST.get('content_id', '')
# 사용자의 검증되지 않은 입력값을 사용해 동적 쿼리문 생성
sql_query = "update board set name='" + name + "' where content_id='“ + content_id + "'"
# 외부 입력값이 검증 없이 쿼리로 포함되어 안전하지 않다
curs.execute(sql_query)
dbconn.commit()
return render(request, '/success.html')
다음은 이를 안전한 코드로 변환한 예시를 보여준다. 앞선 예제와 달리 입력 받은 외부 입력값을 그대로
사용하지 않고 인자화된 쿼리 생성 후(line 11) execute() 메서드의 두 번째 인자 값으로 이 값을 바인딩 해서
쿼리문을 실행한다(line 15). 이렇게 매개변수 바인딩을 통해 execute() 함수를 호출하면 공격자가 쿼리를 변조
하는 값을 삽입하더라도 해당 값이 바인딩된 매개변수의 값으로만 사용되기 때문에 안전하다.

![p16 이미지](images/p16_img1.png)


![p16 이미지](images/p16_img2.png)


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
from django.shortcuts import render
from django.db import connection
def update_board(request):
......
dbconn = connection
with dbconn.cursor() as curs:
name = request.POST.get('name', '')
content_id = request.POST.get('content_id', '')
# 외부 입력값 조작으로부터 안전한 인자화된 쿼리를 생성한다.
sql_query = 'update board set name=%s where content_id=%s'
# 사용자의 입력값이 인자화된 쿼리에 바인딩 후 실행되므로 안전하다.
curs.execute(sql_query, (name, content_id))
dbconn.commit()
return render(request, '/success.html')
SQLite DB API 사용 시에도 동일하게 정적인 쿼리문을 사전에 생성하고 사용자 입력을 바인딩하는 방법을
적용해야 한다. SQLite에서는 인자화된 쿼리를 만들기 위해 “?”를 Placeholder로 사용하거나 “:name”처럼
Named Placeholder를 사용하는 방법 2가지를 적용 가능하다.
나) ORM 사용 예제
Django의 querysets는 쿼리 인자화를 사용해 쿼리를 구성하기 때문에 SQL 삽입 공격으로부터 안전하다.
부득이하게 원시 SQL 또는 사용자 정의 SQL을 사용할 경우에도 외부 입력값을 인자화된 쿼리의 바인딩 변수로
사용하면 된다.
아래는 Django의 원시 SQL을 사용하는 예시를 보여 준다. Django의 ORM 프레임워크는 원시 SQL 쿼리를
수행하기 위해 Manager.raw() 기능을 제공한다. 외부로부터 입력받은 외부 입력값(line 6)을 쿼리문 생성에
문자열 조합으로 사용해 쿼리문을 구성하고 있다(line 11).

![p17 이미지](images/p17_img1.png)


![p17 이미지](images/p17_img2.png)


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
from django.shortcuts import render
from app.models import Member
def member_search(request):
name = request.POST.get('name', '')
# 입력값을 검증 없이 쿼리문 생성에 사용해 안전하지 않다
query=“select * from member where name=‘” + name + “’”
# 외부 입력값을 검증 없이 사용한 쿼리문을 raw()함수로 실행하면 안전하지 않다
data = Member.objects.raw(query)
return render(request, '/member_list.html', {'member_list':data})
다음 코드에서는 Django에서 원시 코드 실행 시에도 인자화된 쿼리와 params 인수를 raw() 함수의 바인딩
변수로 사용하는 안전한 예시를 보여 준다. 외부 입력값을 포함하는 쿼리문 생성 자체를 인자화된 쿼리 형식으로
생성하고(line 10), raw() 메소드에서 두 번째 인자의 바인딩 변수로 사용했다.

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
from django.shortcuts import render
from app.models import Member
def member_search(request):
name = request.POST.get('name', '')
# 외부 입력값을 raw() 함수 실행 시 바인딩 변수로 사용하여 쿼리 구조가
# 변경되지 않도록 한다.(list 형은 %s, dictionary 형은 %(key)s를 사용)
query='select * from member where name=%s'
# 인자화된 쿼리문을 사용하여 raw() 함수를 호출해 안전하다
data = Member.objects.raw(query, [name])
return render(request, '/member_list.html', {'member_list':data})

![p18 이미지](images/p18_img1.png)


![p18 이미지](images/p18_img2.png)


![p18 이미지](images/p18_img4.png)


![p18 이미지](images/p18_img5.png)

라. 참고자료
① CWE-89: Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection'), MITRE,
https://cwe.mitre.org/data/definitions/89.html
② SQL Injection Prevention Cheat Sheet, OWASP
https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
③ Sqlite3 DB-API, Python, Python Software Foundation,
https://docs.python.org/ko/3/library/sqlite3.html
④ MySQL, Python Coding Examples, Oracle Corporation
https://dev.mysql.com/doc/connector-python/en/connector-python-examples.html
⑤ Django QuerySet API reference, Django Software Foundation,
https://docs.djangoproject.com/en/3.2/ref/models/querysets/
⑥ Django Performing raw SQL queries, Django Software Foundation,
https://docs.djangoproject.com/en/3.2/topics/db/sql/
⑦ SQL Expression Language Tutorial, SQLAlchemy,
https://docs.sqlalchemy.org/en/14/core/tutorial.html#using-textual-sql
2. 코드 삽입
가. 개요
공격자가 소프트웨어의 의도된 동작을 변경하도록 임의 코드를 삽입해 소프트웨어가 비정상적으로 동작하도록
하는 보안약점을 말한다. 코드 삽입은 프로그래밍 언어 자체의 기능에 한해 이뤄진다는 점에서 운영체제 명령어
삽입과 다르다. 프로그램에서 사용자의 입력값 내에 코드가 포함되는 것을 허용할 경우 공격자는 개발자가 의도
하지 않은 코드를 실행해 권한을 탈취하거나 인증 우회, 시스템 명령어 실행 등을 할 수 있다.
파이썬에서 코드 삽입 공격을 유발할 수 있는 함수로는 eval(), exec() 등이 있다. 해당 함수의 인자를 면밀히
검증하지 않는 경우 공격자가 전달한 코드가 그대로 실행될 수 있다.
나. 안전한 코딩기법
동적코드를 실행할 수 있는 함수를 사용하지 않는다. 필요 시, 실행 가능한 동적 코드를 입력값으로 받지
않도록 외부 입력값에 대해 화이트리스트 기반 검증을 수행해야 한다. 유효한 문자만 포함하도록 동적 코드에
사용되는 사용자 입력값을 필터링 하는 방법도 있다.
다. 코드예제
가) eval()함수 사용 예제
다음은 안전하지 않은 코드로 eval()을 사용해 사용자로부터 입력받은 값을 실행하여 결과를 반환 하는 예제다.
외부로부터 입력 받은 값을 아무런 검증 없이 eval() 함수의 인자로 사용하고 있다(line 10).

![p20 이미지](images/p20_img0.png)

외부 입력값을 검증 없이 사용할 경우 공격자는 파이썬 코드를 통해 악성 기능 실행을 위한 라이브러리 로드
및 원격 대화형 쉘 등을 실행할 수도 있다. 예를 들어 공격자가 다음과 같은 코드를 입력할 경우 20초 동안
응용 프로그램이 sleep 상태에 빠질 수 있다.
예시) “compile(‘for x in range(1):\n import time\n time.sleep(20)’,’a’,’single’)”

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
from django.shortcuts import render
def route(request):
# 외부에서 입력받은 값을 검증 없이 사용하면 안전하지 않다
message = request.POST.get('message', '')
# 외부 입력값을 검증 없이 eval 함수에 전달할 경우 의도하지 않은 코드가
# 실행될 수 있어 위험하다
ret = eval(message)
return render(request, '/success.html', {'data':ret})
다음은 안전한 코드로 변환한 예제를 보여 준다. 외부 입력값 내에 포함된 (파이썬 코드를 실행할 수 있는)
특수 문자 등을 필터링 하는 사전 검증 코드를 추가하면 코드 삽입 공격 위험을 완화할 수 있다. 아래 코드는
입력 받은 외부 입력값(line 4)을 eval() 함수의 인자 값으로 사용하기 전에 입력값이 영문과 숫자만으로 입력
되었는지 검증 후(line 9) 사용하도록 하고 있다.

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
from django.shortcuts import render
def route(request):
message = request.POST.get('message', '')
# 사용자 입력을 영문, 숫자로 제한하며, 만약 입력값 내에 특수문자가 포함되어
# 있을 경우 에러 메시지를 반환 한다
if message.isalnum():
ret = eval(message)
return render(request, '/success.html', {'data':ret})
return render(request, '/error.html')

![p21 이미지](images/p21_img1.png)


![p21 이미지](images/p21_img2.png)


![p21 이미지](images/p21_img4.png)


![p21 이미지](images/p21_img5.png)

파이썬은 다양한 String 메소드를 제공하고 있다. 필요한 경우 적절한 메소드를 사용해 외부 입력값에 대한
검증을 수행해야 한다. 아래는 파이썬에서 제공하는 입력값 검증용 String 메소드 예시를 보여 준다.
⦁str.isalpha() : 문자열 내의 모든 문자가 알파벳이고, 적어도 하나의 문자가 존재하는 경우 True를 반환
⦁str.isdecimal() : 문자열 내의 모든 문자가 십진수 문자이고, 적어도 하나의 문자가 존재하는 경우 True를 반환
⦁str.isdigit() : 문자열 내의 모든 문자가 숫자이고, 적어도 하나의 문자가 존재하는 경우 True를 반환,
십진수 문자와 호환되는 위 첨자 숫자와 같은 숫자도 포함. ex) ‘52’ 는 True를 반환
입력값 검증 시 외부 입력값이 특정 형식을 따라야 하는 경우 정규 표현식을 이용해 검증을 할 수 있다.
파이썬에서는 re 라이브러리를 사용해 정규식 기반 검증이 가능하다. 예를 들어 이메일 형식의 입력만 허용하고
싶은 경우 다음과 같은 정규식을 사용하면 된다.
ex) prog = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
나) exec()함수 사용 예제
다음은 exec() 함수를 사용한 안전하지 않은 코드 예제를 보여 준다. 외부 입력값을 검증 없이 exec 함수의
인자로 사용하고 있다(line 9). 이렇게 되면 중요 데이터 탈취 및 서버의 권한 탈취, 액세스 거부, 심지어 완전한
호스트 탈취로도 이어질 수 있다.

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
from django.shortcuts import render
def request_rest_api(request):
function_name = request.POST.get('function_name', '')
# 사용자에게 전달받은 함수명을 검증하지 않고 실행
# 입력값으로 “__import__(‘platform’).system()” 등을 입력 시
# 시스템 정보 노출 위험이 있다
exec('{}()'.format(function_name))
return render(request, '/success.html')

![p22 이미지](images/p22_img1.png)


![p22 이미지](images/p22_img2.png)

다음은 위 코드를 안전하게 변환한 예제다. 우선 외부로부터 입력 받은 문자열 내부에서 발견된 라이브러리
이름이 사전에 정의한 화이트리스트에 포함되는지 확인하고 리스트에 없는 경우엔 에러 페이지를 반환한다.

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
from django.shortcuts import render
WHITE_LIST = ['get_friends_list', 'get_address', 'get_phone_number']
def request_rest_api(request):
function_name = request.POST.get('function_name', '')
# 사용 가능한 함수를 화이트리스트 목록 내의 함수로 제한
if function_name in WHITE_LIST:
exec('{}()'.format(function_name))
return render(request, '/success.html')
return render(request, '/error.html', {'error':'허용되지 않은 함수입니다.'})
라. 참고자료
① CWE-94: Improper Control of Generation of Code ('Code Injection'), MITRE,
https://cwe.mitre.org/data/definitions/94.html
② CWE-95: Improper Neutralization of Directives in Dynamically Evaluated Code ('Eval Injection'), MITRE,
https://cwe.mitre.org/data/definitions/95.html
③ Code Injection, OWASP,
https://owasp.org/www-community/attacks/Code_Injection
④ Python Built-in Functions - eval(), exec(), compile(), Python Software Foundation,
https://docs.python.org/3/library/functions.html#eval
https://docs.python.org/3/library/functions.html#exec
https://docs.python.org/3/library/functions.html#compile
⑤ Python Built-in Types – isalnum(), Python Software Foundation,
https://docs.python.org/3/library/stdtypes.html
⑥ Reqular expression operations, Python Software Foundation,
https://docs.python.org/3/library/re.html#module-re

![p23 이미지](images/p23_img1.png)


![p23 이미지](images/p23_img2.png)

3. 경로 조작 및 자원 삽입
가. 개요
검증되지 않은 외부 입력값을 통해 파일 및 서버 등 시스템 자원(파일, 소켓의 포트 등)에 대한 접근 혹은
식별을 허용할 경우 입력값 조작으로 시스템이 보호하는 자원에 임의로 접근할 수 있는 보안약점이다. 경로조작
및 자원삽입 약점을 이용해 공격자는 자원 수정·삭제, 시스템 정보누출, 시스템 자원 간 충돌로 인한 서비스
장애 등을 유발시킬 수 있다. 또한 경로 조작 및 자원 삽입을 통해서 공격자가 허용되지 않은 권한을 획득해
설정 파일을 변경하거나 실행시킬 수 있다.
파이썬에서는 subprocess.popen()과 같이 프로세스를 여는 함수, os.pipe()처럼 파이프를 여는 함수,
socket 연결 등에서 외부 입력값을 검증 없이 사용할 경우 경로 조작 및 자원 삽입의 취약점이 발생할 수 있다.
나. 안전한 코딩기법
외부로부터 받은 입력값을 자원(파일, 소켓의 포트 등)의 식별자로 사용하는 경우 적절한 검증을 거치도록
하거나 사전에 정의된 리스트에 포함된 식별자만 사용하도록 해야 한다. 특히 외부의 입력이 파일명인 경우에는
필터를 적용해 경로순회(directory traversal) 공격의 위험이 있는 문자( /, \, .. 등)를 제거해야 한다.
다. 코드예제
가) 경로 조작 예제
다음은 외부 입력값으로 파일 경로 등을 입력받아 파일을 여는 예시를 보여 준다. 만약 공격자가
‘../../../../etc/passwd’ 와 같은 값을 전달하면 사용자 계정 및 패스워드 정보가 담긴 파일의 내용이 클라이언트
측에 표시되어 의도치 않은 시스템 정보노출 문제가 발생한다.

![p24 이미지](images/p24_img0.png)


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
import os
from django.shortcuts import render
def get_info(request):
# 외부 입력값으로부터 파일명을 입력 받는다
request_file = request.POST.get('request_file')
(filename, file_ext) = os.path.splitext(request_file)
file_ext = file_ext.lower()
if file_ext not in ['.txt', '.csv']:
return render(request, '/error.html', {'error':'파일을 열 수 없습니다.'})
# 입력값을 검증 없이 파일 처리에 사용했다
with open(request_file) as f:
data = f.read()
return render(request, '/success.html', {'data':data})
외부 입력값에서 경로 조작 문자열 ( /, \, .. 등)을 제거한 후 파일의 경로 설정에 사용하면 코드를 안전하게
만들 수 있다. replace 함수 외에도 re.sub, filter 함수를 사용해 특수문자를 필터링 하는 것도 가능하다.

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
import os
from django.shortcuts import render
def get_info(request):
request_file = request.POST.get('request_file')
(filename, file_ext) = os.path.splitext(request_file)
file_ext = file_ext.lower()
# 외부 입력값으로 받은 파일 이름은 검증하여 사용한다.
if file_ext not in ['.txt', '.csv']:
return render(request, '/error.html', {'error':'파일을 열수 없습니다.'})
# 파일 명에서 경로 조작 문자열을 필터링 한다.
filename = filename.replace('.', '')
filename = filename.replace('/', '')
filename = filename.replace('\\', '')

![p25 이미지](images/p25_img1.png)


![p25 이미지](images/p25_img2.png)


![p25 이미지](images/p25_img4.png)


![p25 이미지](images/p25_img5.png)


**안전한 코드 예시**

17:
18:
19:
21:
22:
23:
24:
25:
26:
27:
try:
with open(filename + file_ext) as f:
data = f.read()
except:
return render(
request, "/error.html", {"error": "파일이 존재하지 않거나 열 수 없는 파일입니다."}
)
return render(request, '/success.html', {'data':data})
나) 자원 삽입 예제
다음은 안전하지 않은 코드 예시로, 외부 입력을 소켓 포트 번호로 그대로 사용하고 있다. 외부 입력값을
검증 없이 사용할 경우 기존 자원과의 충돌로 의도치 않은 에러가 발생할 수 있다.

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
import socket
from django.shortcuts import render
def get_info(request):
port = int(request.POST.get('port'))
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
# 외부로부터 입력받은 검증되지 않은 포트 번호를 이용하여
# 소켓을 바인딩하여 사용하고 있어 안전하지 않다
s.bind(('127.0.0.1', port))
...
return render(request, '/success.html')
return render(request, '/error.html', {'error':'소켓연결 실패'})
다음은 안전한 예제를 보여 준다. 내부 자원에 접근 시 외부에서 입력 받은 값을 포트 번호와 같은 식별자로
그대로 사용하는 것은 바람직하지 않으며, 꼭 필요한 경우엔 허용 가능한 목록을 설정한 후 목록 내에 포함된
포트만 할당되도록 코드를 작성해야 한다.

![p26 이미지](images/p26_img1.png)


![p26 이미지](images/p26_img2.png)


![p26 이미지](images/p26_img4.png)


![p26 이미지](images/p26_img5.png)


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
import socket
from django.shortcuts import render
ALLOW_PORT = [4000, 6000, 9000]
def get_info(request):
port = int(request.POST.get('port'))
# 사용 가능한 포트 번호를 화이트리스트 내의 포트로 제한
if port not in ALLOW_PORT:
return render(request, '/error.html', {'error':'소켓연결 실패'})
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
s.bind(('127.0.0.1', port))
......
return render(request, '/success.html')
라. 참고자료
① CWE-22: Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal'), MITRE,
https://cwe.mitre.org/data/definitions/22.html
② CWE-99: Improper Control of Resource Identifiers ('Resource Injection'), MITRE,
https://cwe.mitre.org/data/definitions/99.html
③ Path Traversal, OWASP,
https://owasp.org/www-community/attacks/Path_Traversal
④ Resource Injection, OWASP,
https://owasp.org/www-community/attacks/Resource_Injection
⑤ File Uploads, Django Software Foundation,
https://docs.djangoproject.com/en/3.2/topics/http/file-uploads/
⑥ HTML Helpers, Werkzeug,
https://werkzeug.palletsprojects.com/en/2.0.x/utils/#module-werkzeug.utils

![p27 이미지](images/p27_img1.png)


![p27 이미지](images/p27_img2.png)

4. 크로스사이트 스크립트(XSS)
가. 개요
크로스사이트 스크립트 공격(Cross-site scripting Attacks)은 웹사이트에 악성 코드를 삽입하는 공격 방법
이다. 공격자는 대상 웹 응용프로그램의 결함을 이용해 악성코드(일반적으로 클라이언트 측 JavaScript 사용)를
사용자에게 보낸다. XSS공격은 일반적으로 애플리케이션 호스트 자체보다 사용자를 목표로 삼는다.
XSS는 공격자가 웹 응용프로그램을 속여 브라우저에서 실행될 수 있는 형식의 데이터(코드)를 다른 사용자
에게 전달할 때 발생한다. 공격자가 임의로 구성한 기본 웹 코드 외에도 악성코드 다운로드, 플러그인 또는
미디어 콘텐츠를 이용할 수도 있다. 사용자가 폼 양식에 입력한 데이터 또는 서버에서 클라이언트 단말(브라우저)
전달된 데이터가 적절한 검증 없이 사용자에게 표시되도록 허용되는 경우 발생한다.
XSS공격에는 크게 세 가지 유형의 공격방법이 있다.
⦁유형 1 : Reflective XSS (or Non-persistent XSS)

![p28 이미지](images/p28_img0.png)


![p28 이미지](images/p28_img1.png)

- Reflective XSS는 공격 코드를 사용자의 HTTP 요청에 삽입한 후, 해당 공격 코드를 서버 응답 내용에
그대로 반사 (Reflected)시켜 브라우저에서 실행하는 공격기법이다. Reflective XSS 공격을 수행하려면
사용자로 하여금 공격자가 만든 서버로 데이터를 보내도록 해야 한다. 이 방법은 보통 악의적으로 제작된
링크를 사용자가 클릭하도록 유도하는 방식을 수반한다. 공격자는 피해자가 취약한 사이트를 참조하는
URL을 방문하도록 유도하고, 피해자가 링크를 방문하면 스크립트가 피해자의 브라우저에서 자동으로 실행
된다. 대부분의 경우 Reflective XSS 공격 메커니즘은 공개 게시판, 피싱(Phishing) 이메일, 단축 URL
또는 실제와 유사한 URL을 사용한다.
⦁유형 2 : Persistent XSS (or Stored XSS)
- Persistent XSS는 신뢰할 수 없거나 확인되지 않은 사용자 입력(코드)이 서버에 저장되고, 이 데이터가
다른 사용자들에게 전달될 때 발생한다. Persistent XSS는 게시글 및 댓글 또는 방문자 로그 기능에서
발생할 수 있다. 해당 기능을 통해 공격자의 악성 콘텐츠를 다른 사용자들이 열람할 수 있다. 소셜 미디어
사이트 및 회원 그룹에서 흔히 볼 수 있는 것과 같이 공개적으로 표시되는 프로필 페이지는 Persistent
XSS의 대표적인 공격 대상 중 하나다. 공격자는 프로필 입력 폼에 악성 스크립트를 주입해 다른 사용자가
프로필을 방문하면 브라우저에서 자동으로 코드가 실행되도록 할 수 있다.
⦁유형 3 : DOM XSS (or Client-Side XSS)
- DOM XSS은 웹 페이지에 있는 사용자 입력값을 적절하게 처리하기 위한 JavaScript의 검증 로직을 무효화
하는 것을 목표로 한다. 공격 스크립트가 포함된 악성 URL을 통해 전달된다는 관점에서 Reflective XSS와
유사하다고 볼 수 있다. 그러나 신뢰할 수 있는 사이트의 HTTP 응답에 페이로드를 포함하는 대신 DOM
또는 문서 개체 모델을 수정해 브라우저와 독립적인 공격을 실행한다는 점에서 차이가 있다.

![p29 이미지](images/p29_img0.png)

- 공격자는 DOM XSS 공격을 통해 세션 및 개인 정보를 포함한 쿠키 데이터를 피해자의 컴퓨터에서 공격자
시스템으로 전송할 수 있다. 이 정보를 사용해 특정 웹사이트에 악의적인 요청을 보낼 수 있으며, 피해자가
해당 사이트를 관리 할 수 있는 관리자 권한이 있는 경우 심각한 위협을 초래할 수도 있다. 또한 신뢰할
수 있는 웹 사이트를 모방하고 피해자가 암호를 입력하도록 속여 공격자가 해당 웹 사이트에서 피해자의
계정을 손상시키는 피싱(Phishing) 공격으로도 이어질 수 있다.
- 파이썬에서 가장 많이 사용하고 있는 Django 프레임워크와 Flask 프레임워크에서는 각각 Django 템플릿과
Jinja2 템플릿을 사용할 시 XSS 공격에 악용될 수 있는 위험한 HTML 문자들을 HTML 특수문자 (HTML
Entities)로 치환하는 기능을 제공하고 있어 프레임워크에서 제공하는 템플릿을 사용하는 경우 위협을 최소화
할 수 있다.
나. 안전한 코딩기법
외부 입력값 또는 출력값에 스크립트가 삽입되지 못하도록 문자열 치환 함수를 사용하여 &<>*‘/() 등을
&amp; &lt; &gt; &quot; &#x27; &#x2F; &#x28; &#x29;로 치환하거나, html라이브러리의 escape()를
사용해 문자열을 변환해야 한다. HTML 태그를 허용해야 하는 게시판에서는 허용할 HTML 태그들을 화이트
리스트로 만들어 해당 태그만 지원하도록 한다.
파이썬에서 가장 많이 사용하는 프레임워크인 Django, Flask 등을 사용하는 경우 외부 입력값에 악의적인
스크립트가 삽입되지 못하도록 프레임워크 자체에서 XSS 공격에 사용될 수 있는 문자를 HTML 특수문자
(HTML Entities)로 치환하여 응답 페이지를 생성하므로 XSS 공격으로부터 안전하다.

![p30 이미지](images/p30_img0.png)

프레임워크 자체에서 XSS 공격으로부터 보호해 주는 기능이 있더라도 완전하지 않은 경우도 있고 개발자의
실수로 보호기능이 무효화 되는 경우가 있으므로 주의를 기울여야 한다.
다. 코드예제
가) Django 예제
Django 프레임워크는 XSS 공격에 대한 보안기능을 내장하고 있지만 유의해야 할 사항이 몇 가지 있다.
Django의 “safestring(django.utils.safestring)”의 기능을 오용할 경우 Django의 XSS 공격에 대한 보호
정책이 무력화 될 수 있다.

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
from django.shortcuts import render
from django.utils.safestring import mark_safe
def profile_link(request):
# 외부 입력값을 검증 없이 HTML 태그 생성의 인자로 사용
profile_url = request.POST.get('profile_url')
profile_name = requst.POST.get('profile_name')
object_link = '<a href="{}">{}</a>'.format(profile_url, profile_name)
# mark_safe함수는 Django의 XSS escape 정책을 따르지 않는다
object_link = mark_safe(object_link)
return render(request, 'my_profile.html',{'object_link':object_link})
Django 프레임워크는 템플릿 생성 시 HTML에서 위험한 것으로 간주되는 특수 문자(“<”, “>”, “‘”, “””,
“&”)를 모두 HTML 엔티티로 치환 하지만 mark_safe를 사용할 경우 이 정책을 따르지 않는다. 따라서
mark_safe 함수를 사용할 경우에는 각별한 주의가 필요하고 신뢰할 수 없는 데이터에 대해서는 mark_safe
함수를 사용하지 않아야 한다.

![p31 이미지](images/p31_img1.png)


![p31 이미지](images/p31_img2.png)


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
from django.shortcuts import render
def profile_link(request):
# 외부 입력값을 검증 없이 HTML 태그 생성의 인자로 사용
profile_url = request.POST.get('profile_url')
profile_name = requst.POST.get('profile_name')
object_link = '<a href="{}">{}</a>'.format(profile_url, profile_name)
# 신뢰할 수 없는 데이터에 대해서는 mark_safe 함수를 사용해선 안 된다
return render(request, 'my_profile.html',{'object_link':object_link})
다음은 또 다른 Django 프레임워크 템플릿 예제를 보여 준다. autoescape 블록 사용 시 설정값을 off로
할 경우와 개별 변수에 대해서 safe 필터를 사용할 경우 크로스사이트 스크립트 공격에 노출될 수 있다.

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
<!doctype html>
<html>
<body>
<div class="content">
{% autoescape off %}
<!-- autoescape off로 설정하면 해당 블록내의 데이터는 XSS 공격에
노출될 수 있다 -->
{{ content }}
{% endautoescape %}
</div>
<div class="content2">
<!-- safe 필터 사용으로 XSS 공격에 노출될 수 있다 -->
{{ content | safe }}
</div>
</body>
</html>
신뢰할 수 없는 입력값 또는 동적 데이터에 대해서는 autoescape 옵션 값을 on으로 설정해야 하며, safe
필터를 부득이 하게 사용할 경우에는 추가적인 보안대책이 필요하다.

![p32 이미지](images/p32_img1.png)


![p32 이미지](images/p32_img2.png)


![p32 이미지](images/p32_img4.png)


![p32 이미지](images/p32_img5.png)


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
<!doctype html>
<html>
<body>
<div class="content">
{% autoescape on %}
<!--autoescape on으로 해당 블록내의 데이터는 XSS 공격에 노출되지 않음. -->
{{ content }}
{% endautoescape %}
</div>
<div class="content2">
<!-- 검증되지 않은 데이터에는 safe 필터를 사용하지 않는다. -->
{{ content }}
</div>
</body>
</html>
autoescape 블록을 사용할 경우 많은 주의를 기울여야 한다. autoescape 옵션값을 off로 설정한 템플릿
페이지를 include 또는 extends하는 템플릿까지 영향이 확장된다. 공통적으로 사용하는 템플릿페이지에 off로
설정할 경우 템플릿 페이지가 XSS 공격에 노출될 수 있다.
나) Flask에서의 예제
사용자의 요청에 포함된 값, DB에 저장된 값 또는 내부의 연산을 통해서 생성된 값을 포함한 데이터를 동적
웹페이지 생성에 사용하는 경우 XSS 공격이 발생할 가능성이 있어 위험하다. 아래 예제는 Flask 프레임워크를
사용한 안전하지 않은 사례를 보여 준다.

**안전하지 않은 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
from flask import Flask, request, render_template
@app.route('/search', methods=['POST'])
def search():
search_keyword = request.form.get('search_keyword')
# 사용자의 입력을 아무런 검증 또는 치환 없이 동적 웹페이지에 사용하고 있어
# XSS 공격이 발생할 수 있다
return render_template('search.html', search_keyword=search_keyword)

![p33 이미지](images/p33_img1.png)


![p33 이미지](images/p33_img2.png)


![p33 이미지](images/p33_img4.png)


![p33 이미지](images/p33_img5.png)

동적 웹 페이지 생성에 사용하는 데이터를 HTML 엔티티 코드 (Entity Code)로 치환하여 안전하게 표현해야
한다. html.escape 메소드는 문자열의 &, < 및 > 특수문자를 HTML에서 안전한 값으로 변환한다. quote
옵션 값이 True이면 문자 (“)와 (‘)도 변환된다. <a href=”…“>에서처럼 따옴표로 구분된 HTML 속성
(attribute) 값이 들어간 문자열을 포함할 경우에도 사용할 수 있다.

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
import html
from flask import Flask, request, render_template
@app.route('/search', methods=['POST'])
def search():
search_keyword = request.form.get('search_keyword')
# 동적 웹페이지 생성에 사용되는 데이터는
# HTML 엔티티코드로 치환하여 표현해야 한다
escape_keyword = html.escape(search_keyword)
return render_template('search.html', search_keyword=escape_keyword)
라. 참고자료
① CWE-79: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting'), MITRE,
https://cwe.mitre.org/data/definitions/79.html
② Cross Site Scripting (XSS), OWASP,
https://owasp.org/www-community/attacks/xss/
③ html - HyperText Markup Language support, Python Software Foundation,
https://docs.python.org/3/library/html.html
④ Flask Security Considerations Cross-Site Scripting (XSS), Flask docs,
https://flask-docs-kr.readthedocs.io/ko/latest/security.html
⑤ Django Security in Django Cross site scripting (XSS) protection, Django Software Foundation,
https://docs.djangoproject.com/en/3.2/topics/security/

![p34 이미지](images/p34_img1.png)


![p34 이미지](images/p34_img2.png)

5. 운영체제 명령어 삽입
가. 개요
적절한 검증 절차를 거치지 않은 사용자 입력값이 운영체제 명령어의 일부 또는 전부로 구성되어 실행되는
경우 의도하지 않은 시스템 명령어가 실행돼 부적절하게 권한이 변경되거나 시스템 동작 및 운영에 악영향을
미칠 수 있다.
명령어 라인의 파라미터나 스트림 입력 등 외부 입력을 사용해 시스템 명령어를 생성 하는 프로그램을 많이
찾아볼 수 있다. 이 경우 프로그램 외부로부터 받은 입력 문자열은 기본적으로 신뢰할 수 없기 때문에 적절한
처리를 해주지 않으면 공격으로 이어질 수 있다.
파이썬에서 eval() 함수와 exec() 함수는 내부에서 문자열을 실행하기에 편리하지만, String 형식의 표현된
식을 인수로 받아 반환하는 eval() 함수와 인수로 받은 문자열을 실행하는 exec()를 같이 사용하면 여러 변수들에
동적으로 값을 할당해 사용할 수 있어 명령어 삽입(Command Injection) 공격에 취약하다.
나. 안전한 코딩기법
외부 입력값 내에 시스템 명령어를 포함하는 경우 |, ;, &, :, >, <, `(backtick), \, ! 과 같이 멀티라인 및
리다이렉트 문자 등을 필터링 하고 명령을 수행할 파일명과 옵션을 제한해 인자로만 사용될 수 있도록 해야
한다. 외부 입력에 따라 명령어를 생성하거나 선택이 필요한 경우에는 명령어 생성에 필요한 값들을 미리 지정해
놓고 사용해야 한다.

![p35 이미지](images/p35_img0.png)

다. 코드예제
다음 예제는 os.system을 이용해 외부로부터 받은 입력값을 통해 프로그램을 실행하며, 외부에서 전달되는
인자값은 명령어의 생성에 사용된다. 하지만 해당 프로그램에서 실행할 프로그램을 제한하지 않고 있기 때문에
외부의 공격자는 원하는 모든 프로그램을 실행할 수 있다.

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
import os
from django.shortcuts import render
def execute_command(request):
app_name_string = request.POST.get('app_name','')
# 입력 파라미터를 제한하지 않아 외부 입력값으로 전달된
# 모든 프로그램이 실행될 수 있음
os.system(app_name_string)
return render(request, '/success.html')
외부에서 입력받은 값이 명령어의 인자로 사용되지 않고 명령어 그 자체로 사용될 경우에는 사전에 화이트
리스트 파라미터 배열을 정의한 후 외부의 입력에 따라 적절한 파라미터를 선택하도록 하여 외부의 부적절한
입력이 명령어로 사용되는 것을 금지해야 한다.

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
import os
from django.shortcuts import render
ALLOW_PROGRAM = ['notepad', 'calc']
def execute_command(request):
app_name_string = request.POST.get('app_name','')
# 입력받은 파라미터가 허용된 시스템 명령어 목록에 포함되는지 검사
if app_name_string not in ALLOW_PROGRAM:
return render(request, '/error.html', {'error':'허용되지 않은 프로그램입니다.'})
os.system(app_name_string)
return render(request, '/success.html')

![p36 이미지](images/p36_img1.png)


![p36 이미지](images/p36_img2.png)


![p36 이미지](images/p36_img4.png)


![p36 이미지](images/p36_img5.png)

다음은 subprocess() 함수를 사용해 별도의 프로세스로 응용 프로그램을 실행하는 안전하지 않은 예제다.
외부 입력값으로 받은 파라미터를 별도의 검증 없이 subprocess의 인자 값으로 사용하고 있다.

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
import subprocess
from django.shortcuts import render
def execute_command(request):
date = request.POST.get('date','')
# 입력받은 파라미터를 제한하지 않아 전달된 모든 프로그램이 실행될 수 있음
cmd_str = “cmd /c backuplog.bat ” + date
subprocess.run(cmd_str, shell=True)
return render(request, '/success.html')
운영체제 명령어 실행 시에는 외부에서 들어오는 값에 의하여 멀티라인을 지원하는 특수문자(|, ;, &, :, `,
\, !)나 파일 리다이렉트 특수문자( >, >> )등을 제거하여 원하지 않는 운영체제 명령어가 실행될 수 없도록
필터링을 수행한다.
명령어 라인을 구문 분석하고 escape 하는 기능을 제공하는 모듈인 shlex 모듈을 사용해 필터링을 수행할
수 있다. subprocess의 옵션 값 중 shell를 True로 설정할 경우 중간 프로세스에 의해 명령이 실행되고 파일
이름, 와일드카드(*), 환경변수 확장 등의 쉘 기능을 검증 없이 실행하게 되므로 shell의 옵션은 삭제해야 한다
(기본값은 False).

![p37 이미지](images/p37_img1.png)


![p37 이미지](images/p37_img2.png)


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
import subprocess
from django.shortcuts import render
def execute_command(request):
date = request.POST.get('date','')
# 명령어를 추가로 실행 또는 또 다른 명령이 실행될 수 있는 키워드에
# 대한 예외처리
for word in ['|', ';', '&', ':', '>', '<', '`', '\\', '!']:
date = date.replace(word, “”)
# re.sub 함수를 사용해 특수문자를 제거하는 방법도 있다
# date = re.sub('[|;&:><`\\\!]', '', date)
# shell=True 옵션은 제거 하고 명령과 인자를 배열로 입력
subprocess.run(["cmd", "/c", "backuplog.bat", date])
return render(request, '/success.html')
라. 참고자료
① CWE-78: Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection'), MITRE,
https://cwe.mitre.org/data/definitions/78.html
② Command Injection, OWASP
https://owasp.org/www-community/attacks/Command_Injection
③ OS Command Injection Defense Cheat Sheet, OWASP
https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html
④ Miscellaneous operating system interfaces - os.system(), Python Software Foundation
https://docs.python.org/3.10/library/os.html?highlight=os%20system#module-os
⑤ Subprocess management, Python Software Foundation,
https://docs.python.org/ko/3/library/subprocess.html#security-considerations
⑥ Regular expression operations, Python Software Foundation,
https://docs.python.org/3/library/re.html

![p38 이미지](images/p38_img1.png)


![p38 이미지](images/p38_img2.png)

6. 위험한 형식 파일 업로드
가. 개요
서버 측에서 실행 가능한 스크립트 파일(asp, jsp, php, sh 파일 등)이 업로드 가능하고 이 파일을 공격자가
웹을 통해 직접 실행시킬 수 있는 경우 시스템 내부 명령어를 실행하거나 외부와 연결해 시스템을 제어할 수
있는 보안약점이다.
공격자가 실행 가능한 파일을 서버에 업로드 하면 파이썬에서 String 형식으로 표현된 표현식을 인수로 받아
반환하는 eval() 함수와 인수로 받은 문자열을 실행하는 exec()를 같이 사용해 여러 변수들을 동적으로 값을
할당받아 실행될 수 있어 웹쉘(Web Shell) 공격에 취약하다.
나. 안전한 코딩기법
파일 업로드 공격을 방지하기 위해서 특정 파일 유형만 허용하도록 화이트리스트 방식으로 파일 유형을 제한
해야 한다. 이때 파일의 확장자 및 업로드 된 파일의 Content-Type도 함께 확인해야 한다. 또한 파일 크기
및 파일 개수를 제한하여 시스템 자원 고갈 등으로 서비스 거부 공격이 발생하지 않도록 제한해야 한다. 업로드
된 파일을 웹 루트 폴더 외부에 저장해 공격자가 URL을 통해 파일을 실행할 수 없도록 해야 하며, 가능하면
업로드 된 파일의 이름은 공격자가 추측할 수 없는 무작위한 이름으로 변경 후 저장하는 것이 안전하다. 또한
업로드 된 파일을 저장할 경우에는 최소 권한만 부여하는 것이 안전하고 실행 여부를 확인하여 실행 권한을
삭제해야 한다.

![p39 이미지](images/p39_img0.png)

다. 코드예제
업로드 대상 파일 개수, 크기, 확장자 등의 유효성 검사를 하지 않고 파일 시스템에 그대로 저장할 경우
공격자에 의해 악성코드, 쉘코드 등 위험한 형식의 파일이 시스템에 업로드 될 수 있다.

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
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
def file_upload(request):
if request.FILES['upload_file']:
# 사용자가 업로드하는 파일을 검증 없이 저장하고 있어
# 안전하지 않다
upload_file = request.FILES['upload_file']
fs = FileSystemStorage(location='media/screenshot', base_url='media/screenshot')
# 업로드 하는 파일에 대한 크기, 개수, 확장자 등을 검증하지 않음
filename = fs.save(upload_file.name, upload_file)
return render(request, '/success.html', {'filename':filename})
return render(request, '/error.html', {'error':'파일 업로드 실패'})
아래 코드는 업로드 하는 파일의 개수, 크기, 파일 확장자 등을 검사해 업로드를 제한하고 있다. 파일 타입
확인은 MIME 타입을 확인하는 과정으로 파일 이름에서 확장자만 검사할 경우 변조된 확장자를 통해 업로드
제한을 회피할 수 있어 파일자체의 시그니처를 확인하는 과정을 보여 준다.

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
import os
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
# 업로드 하는 파일 개수, 크기, 확장자 제한
FILE_COUNT_LIMIT = 5
# 업로드 하는 파일의 최대 사이즈 제한 예 ) 5MB - 5*1024*1024
FILE_SIZE_LIMIT = 5242880
# 허용하는 확장자는 화이트리스트로 관리한다.
WHITE_LIST_EXT = [
'.jpg',
'.jpeg'
]

![p40 이미지](images/p40_img1.png)


![p40 이미지](images/p40_img2.png)


![p40 이미지](images/p40_img4.png)


![p40 이미지](images/p40_img5.png)


**안전한 코드 예시**

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
25:
26:
27:
28:
29:
30:
31:
32:
33:
34:
35:
36:
37:
def file_upload(request):
# 파일 개수 제한
if len(request.FILES) == 0 or len(request.FILES) > FILE_COUNT_LIMIT:
return render(request, '/error.html', {'error': '파일 개수 초과'})
for filename, upload_file in request.FILES.items():
# 파일 타입 체크
if upload_file.content_type != 'image/jpeg':
return render(request, '/error.html', {'error': '파일 타입 오류'})
# 파일 크기 제한
if upload_file.size > FILE_SIZE_LIMIT:
return render(request, '/error.html', {'error': '파일사이즈 오류'})
# 파일 확장자 검사
file_name, file_ext = os.path.splitext(upload_file.name)
if file_ext.lower() not in WHITE_LIST_EXT:
return render(request, '/error.html', {'error': '파일 타입 오류'})
fs = FileSystemStorage(location='media/screenshot', base_url = 'media/screenshot')
for upload_file in request.FILES.values():
filename = fs.save(upload_file.name, upload_file)
filename_list.append(filename)
return render(request, "/success.html", {"filename_list": filename_list})
라. 참고자료
① CWE-434: Unrestricted Upload of File with Dangerous Type, MITRE,
https://cwe.mitre.org/data/definitions/434.html
② Unrestricted File Upload, OWASP,
https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload
③ User-uploaded content, Django Software Foundation,
https://docs.djangoproject.com/en/3.2/topics/security/#user-uploaded-content-security

![p41 이미지](images/p41_img1.png)


![p41 이미지](images/p41_img2.png)

7. 신뢰되지 않은 URL주소로 자동접속 연결
가. 개요
사용자가 입력하는 값을 외부 사이트 주소로 사용해 해당 사이트로 자동 접속하는 서버 프로그램은 피싱
(Phishing) 공격에 노출되는 취약점을 가진다. 클라이언트에서 전송된 URL 주소로 연결하기 때문에 안전하다고
생각할 수 있으나, 공격자는 정상적인 폼 요청을 변조해 사용자가 위험한 URL로 접속할 수 있도록 공격할 수 있다.
파이썬 프레임워크의 redirect 함수를 사용할 때에도 해당 프레임워크 버전에서 알려진 취약점이 있는지
확인해야 한다. Flask 프레임워크의 Flask-Security-Too 라이브러리의 경우 get_post_logout_redirect 함수와
get_post_login_redirect 함수가 4.1.0 이전 버전에서 URL 유효성 검사를 우회하고 사용자를 임의의 URL로
리다이렉션 할 수 있는 취약점이 존재한다.
나. 안전한 코딩기법
리다이렉션을 허용하는 모든 URL을 서버 측 화이트리스트로 관리하고 사용자 입력값을 리다이렉션 할
URL이 존재하는지 검증해야 한다.
만약 사용자 입력값이 화이트리스트로 관리가 불가능하고 리다이렉션 URL의 인자 값으로 사용되어야만 하는
경우는 모든 리다이렉션에서 프로토콜과 host 정보가 들어가지 않는 상대 URL(relative)을 사용 및 검증해야
한다. 또는 절대 URL(absoute URL)을 사용할 경우 리다이렉션을 실행하기 전에 사용자 입력 URL이
https://myhompage.com/ 처럼 서비스하고 있는 URL로 시작하는지를 확인해야 한다.

![p42 이미지](images/p42_img0.png)

다. 코드예제
다음은 안전하지 않은 예제로 사용자로부터 입력받은 URL 주소를 검증 없이 redirect 함수의 인자로 사용
하고 있다. 이 경우 사용자가 의도하지 않은 사이트로 접근하도록 하거나 피싱(Phishing)공격에 노출될 수 있다.

**안전하지 않은 코드 예시**

1:
2:
3:
4:
5:
6:
7:
from django.shortcuts import redirect
def redirect_url(request):
url_string = request.POST.get('url', '')
# 사용자 입력에 포함된 URL 주소로 리다이렉트 하는 경우
# 피싱 사이트로 접속되는 등 사용자가 피싱 공격에 노출될 수 있다
return redirect(url_string)
다음은 안전한 코드 예제로 사용자로부터 주소를 입력받아 리다이렉트하고 있는 코드로 위험한 도메인이
포함될 수 있기 때문에 화이트리스트로 사전에 정의된 안전한 웹사이트에 한하여 리다이렉트 할 수 있도록 한다.

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
from django.shortcuts import render, redirect
ALLOW_URL_LIST = [
'127.0.0.1',
'192.168.0.1',
'192.168.0.100',
'https://login.myservice.com',
'/notice',
]
def redirect_url(request):
url_string = request.POST.get('url', '')
# 이동할 수 있는 URL 범위를 제한하여
# 위험한 사이트의 접근을 차단하고 있다
if url_string not in ALLOW_URL_LIST:
return render(request, '/error.html', {'error':'허용되지 않는 주소입니다.'})
return redirect(url_string)

![p43 이미지](images/p43_img1.png)


![p43 이미지](images/p43_img2.png)


![p43 이미지](images/p43_img4.png)


![p43 이미지](images/p43_img5.png)

라. 참고자료
① CWE-601: URL Redirection to Untrusted Site ('Open Redirect'), MITRE,
https://cwe.mitre.org/data/definitions/601.html
② Unvalidated Redirects and Forwards Cheat Sheet, OWASP
https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html
③ Django shortcut functions – redirect, Django Sowftware Foundation,
https://docs.djangoproject.com/en/3.2/topics/http/shortcuts/
④ Redirects and Errors, Flask,
https://flask.palletsprojects.com/en/2.0.x/quickstart/#redirects-and-errors
8. 부적절한 XML 외부 개체 참조
가. 개요
XML 문서에는 DTD(Document Type Definition)를 포함할 수 있으며 DTD는 XML 엔티티(entitiy)를
정의한다. 부적절한 XML 외부개체 참조 보안약점은 서버에서 XML 외부 엔티티를 처리할 수 있도록 설정된
경우에 발생할 수 있다.
취약한 XML parser가 외부값을 참조하는 XML을 처리할 때 공격자가 삽입한 공격 구문이 동작되어 서버
파일 접근, 불필요한 자원 사용, 인증 우회, 정보 노출 등이 발생할 수 있다.
파이썬에서는 간단한 XML 데이터 구문 분석 및 조작에 사용할 수 있는 기본 XML 파서가 제공된다. 이 파서는
유효성 검사와 같은 고급 XML 기능은 지원하지 않는다. 기본으로 제공되는 XML 파서는 외부 엔티티를 지원
하지 않지만 다른 유형의 XML 공격에 취약할 수 있다. 기본으로 제공되는 파서의 기능 외에 더 많은 기능이
필요한 경우에 lxml과 같은 라이브러리를 사용하게 되는데, 이 라이브러리에서는 기본적으로 외부 엔티티의
구문 분석이 활성화 되어 있다.
나. 안전한 코딩기법
로컬 정적 DTD를 사용하도록 설정하고 외부에서 전송된 XML 문서에 포함된 DTD를 완전하게 비활성화해야
한다. 비활성화를 할 수 없는 경우에는 외부 엔티티 및 외부 문서 유형 선언을 각 파서에 맞는 고유한 방식으로
비활성화 한다.
외부 라이브러리를 사용할 경우 기본적으로 외부 엔티티에 대한 구문 분석 기능을 제공하는지 확인하고 제공이
되는 경우 해당 기능을 비활성화 할 수 있는 방법을 확인해 외부 엔티티 구문 분석 기능을 비활성화 한다.

![p45 이미지](images/p45_img0.png)

많이 사용하는 XML 파서의 한 종류인 lxml의 경우 외부 엔티티 구문 분석 옵션인 resolve_entities 옵션을
비활성화 해야 한다. 또한 외부 문서 조회 시 네트워크 액세스를 방지하는 no_network 옵션이 활성화(True)
되어 있는지도 확인해야 한다.
다. 코드예제
다음 예제는 XML 소스를 읽어와 분석하는 코드다. 공격자는 아래와 같이 XML 외부 엔티티를 참조하는
xxe.xml 데이터를 전송하고 이를 파싱할 때 /etc/passwd 파일을 참조할 수 있다.
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [
<!ELEMENT foo ANY >
<!ENTITY xxe1 SYSTEM "file:///etc/passwd" >
<!ENTITY xxe2 SYSTEM "http://attacker.com/text.txt">
]>
<foo>&xxe1;&xxe2;</foo>

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
from xml.sax import make_parser
from xml.sax.handler import feature_external_ges
from xml.dom.pulldom import parseString, START_ELEMENT
from django.shortcuts import render
from .model import comments
def get_xml(request):
if request.method == “GET”:
data = comments.objects.all()
com = data[0].comment
return render(request, '/xml_view.html', {'com':com})
elif request.method == “POST”:
parser = make_parser()
# 외부 일반 엔티티를 포함하는 설정을 True로 적용할 경우 취약하다
parser.setFeature(feature_external_ges, True)
doc = parseString(request.body.decode(‘utf-8’), parser=parser)
for event, node in doc:
if event == START_ELEMENT and node.tagName == “foo”:
doc.expandNode(node)
text = node.toxml()
comments.objects.filter(id=1).update(comment=text)
return render(request, '/xml_view.html')

![p46 이미지](images/p46_img1.png)


![p46 이미지](images/p46_img2.png)

만약 sax 패키지를 사용해 XML을 파싱할 경우 외부 엔티티를 처리하는 방식의 옵션(feature_external_ges)을
False로 설정해야 한다.

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
from xml.sax import make_parser
from xml.sax.handler import feature_external_ges
from xml.dom.pulldom import parseString, START_ELEMENT
from django.shortcuts import render
from .model import comments
def get_xml(request):
if request.method == “GET”:
data = comments.objects.all()
com = data[0].comment
return render(request, '/xml_view.html', {'com':com})
elif request.method == “POST”:
parser = make_parser()
parser.setFeature(feature_external_ges, False)
doc = parseString(request.body.decode(‘utf-8’), parser=parser)
for event, node in doc:
if event == START_ELEMENT and node.tagName == “foo”:
doc.expandNode(node)
text = node.toxml()
comments.objects.filter(id=1).update(comment=text);
return render(request, '/xml_view.html')
라. 참고자료
① CWE-611: Improper Restriction of XML External Entity Reference, MITRE,
https://cwe.mitre.org/data/definitions/611.html
② XML External Entity (XXE) Processing, OWASP,
https://owasp.org/www-community/vulnerabilities/XML_External_Entity_(XXE)_ Processing
③ XML External Entity Prevention Cheat Sheet, OWASP,
https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html
④ XML vulnerabilities, Python Software Foundation,
https://docs.python.org/3/library/xml.html#xml-vulnerabilities
⑤ lxml API, lxml library,
https://lxml.de/api/lxml.etree.XMLParser-class.html
⑥ PyGoat, OWASP,
https://github.com/adeyosemanputra/pygoat

![p47 이미지](images/p47_img1.png)


![p47 이미지](images/p47_img2.png)

9. XML 삽입
가. 개요
검증되지 않은 외부 입력값이 XQuery 또는 XPath 쿼리문을 생성하는 문자열로 사용되어 공격자가 쿼리문의
구조를 임의로 변경하고 임의의 쿼리를 실행해 허가되지 않은 데이터를 열람하거나 인증절차를 우회할 수 있는
보안약점이다.
나. 안전한 코딩기법
XQuery 또는 XPath 쿼리에 사용되는 외부 입력 데이터에 대하여 특수문자 및 쿼리 예약어를 필터링 하고
인자화된 쿼리문을 지원하는 XQuery를 사용해야 한다.
다. 코드예제
다음 예제는 파이썬에서 XML 데이터를 처리하기 위한 기본 모듈인 xml.etree.ElementTree를 이용하여
사용자 정보를 가져오는 예제다. xml.etree.ElementTree 모듈은 제한적인 Xpath 기능을 제공하며 Xpath
표현식을 인자화해서 사용하는 방법을 제공하지 않는다.

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
from django.shortcuts import render
from lxml import etree
def parse_xml(request):
user_name = request.POST.get('user_name', '')
parser = etree.XMLParser(resolve_entities=False)
tree = etree.parse('user.xml', parser)
root = tree.getroot()
# 검증되지 않은 외부 입력값 user_name을 사용한 안전하지 않은
# 질의문이 query 변수에 저장
query = "/collection/users/user[@name='" + user_name + "']/home/text()"
elmts = root.xpath(query)
return render(request, 'parse_xml.html', {'xml_element':elmts})

![p48 이미지](images/p48_img1.png)


![p48 이미지](images/p48_img2.png)


![p48 이미지](images/p48_img3.png)

파이썬 3.3 이후 보안상의 이유로 금지된 xml.etree.ElementTree 모듈 대신 lxml 라이브러리를 사용하고
외부 입력값은 인자화해서 사용한다.

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
from lxml import etree
def parse_xml(request):
user_name = request.POST.get('user_name', '')
parser = etree.XMLParser(resolve_entities=False)
tree = etree.parse('user.xml', parser)
root = tree.getroot()
# 외부 입력값을 paramname으로 인자화 해서 사용
query = '/collection/users/user[@name = $paramname]/home/text()'
elmts = root.xpath(query, paramname=user_name)
return render(request, 'parse_xml.html', {'xml_element':elmts})
라. 참고자료
① CWE-643: Improper Neutralization of Data within XPath Expressions ('XPath Injection'), MITRE,
https://cwe.mitre.org/data/definitions/643.html
② XPATH Injection, OWASP,
https://owasp.org/www-community/attacks/XPATH_Injection
③ XML vulnerabilities, Python Software Foundation,
https://docs.python.org/3/library/xml.html#xml-vulnerabilities

![p49 이미지](images/p49_img1.png)


![p49 이미지](images/p49_img2.png)

10. LDAP 삽입
가. 개요
외부 입력값을 적절한 처리 없이 LDAP 쿼리문이나 결과의 일부로 사용하는 경우 LDAP 쿼리문이 실행될 때
공격자는 LDAP 쿼리문의 내용을 마음대로 변경할 수 있다. 이로 인해 프로세스가 명령을 실행한 컴포넌트와
동일한 권한(Permission)을 가지고 동작하게 된다.
파이썬에는 파이썬-ldap 및 ldap3라는 두 개의 라이브러리가 있다. ldap3가 python-ldap 보다 더 현대적인
라이브러리다. ldap3 모듈은 파이썬 2.6부터 모든 파이썬 3 버전에 호환된다. ldap3에서는 좀 더 파이썬적인
방식으로 LDAP서버와 상호 작용할 수 있는 완전한 기능의 추상화 계층이 포함되어 있다. python-ldap은
OpenLDAP에서 만든 파이썬2의 패키지로 파이썬3에서는 ldap3 라이브러리를 사용하는 것이 권장된다.
나. 안전한 코딩기법
다른 삽입 공격들과 마찬가지로 LDAP 삽입에 대한 기본적인 방어 방법은 적절한 유효성 검사이다.
⦁올바른 인코딩(Encoding) 함수를 사용해 모든 변수 이스케이프(Escape) 처리
⦁화이트리스트 방식의 입력값 유효성 검사
⦁사용자 패스워드와 같은 민감한 정보가 포함된 필드 인덱싱
⦁LDAP 바인딩 계정에 할당된 권한 최소화

![p50 이미지](images/p50_img0.png)

다. 코드예제
사용자의 입력을 그대로 LDAP 질의문에 사용하고 있으며 이 경우 권한 상승 등의 공격에 노출될 수 있다.

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
25:
26:
27:
28:
from  ldap3 import  Connection, Server, ALL
from django.shortcuts import render
config = {
"bind_dn": "cn=read-only-admin,dc=example,dc=com",
"password": "password",
}
def ldap_query(request):
search_keyword = request.POST.get('search_keyword','')
dn = config['bind_dn']
password = config['password']
address = 'ldap.badSoruce.com'
server = Server(address, get_info=ALL)
conn = Connection(server, user=dn, password, auto_bind=True )
# 사용자 입력을 필터링 하지 않는 경우 공격자의 권한 상승으로
# 이어질 수 있다
search_str = '(&(objectclass=%s))' % search_keyword
conn.search(
'dc=company,dc=com',
search_str,
attributes=['sn', 'cn', 'address', 'mail', 'mobile', 'uid'],
)
return render(request, '/ldap_query_response.html', {'ldap':conn.entries})

![p51 이미지](images/p51_img1.png)


![p51 이미지](images/p51_img2.png)

사용자의 입력 중 LDAP 질의문에 사용될 변수를 이스케이프 하여 질의문 실행 시 공격에 노출되는 것을
예방할 수 있다.

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
19:
20:
21:
22:
23:
24:
25:
26:
27:
28:
29:
30:
31:
from  ldap3 import  Connection, Server, ALL
from  ldap3.utils.conv import  escape_filter_chars
from django.shortcuts import render
config = {
"bind_dn": "cn=read-only-admin,dc=example,dc=com",
"password": "password",
}
def ldap_query(request):
search_keyword = request.POST.get('search_keyword','')
dn = config['bind_dn']
password = config['password']
address = 'ldap.goodsource.com'
server = Server(address, get_info=ALL)
conn = Connection(server, dn, password, auto_bind=True )
# 사용자의 입력에 필터링을 적용하여 공격에 사용될 수 있는 문자를
# 이스케이프하고 있다
escpae_keyword = escape_filter_chars(search_keyword)
search_str = '(&(objectclass=%s))' % escpae_keyword
conn.search(
'dc=company,dc=com',
search_str,
attributes=['sn', 'cn', 'address', 'mail', 'mobile', 'uid'],
)
return render(request, '/ldap_query_response.html', {'ldap':conn.entries})

![p52 이미지](images/p52_img1.png)


![p52 이미지](images/p52_img2.png)

라. 참고자료
① CWE-90: Improper Neutralization of Special Elements used in an LDAP Query ('LDAP Injection'), MITRE,
https://cwe.mitre.org/data/definitions/90.html
② LDAP Injection Prevention Cheat Sheet, OWASP,
https://cheatsheetseries.owasp.org/cheatsheets/LDAP_Injection_Prevention_Cheat_ Sheet.html
③ LDAP filter handling, python-ldap project team
https://www.python-ldap.org/en/python-ldap-3.3.0/reference/ldap-filter.html
11. 크로스사이트 요청 위조(CSRF)
가. 개요
특정 웹사이트에 대해 사용자가 인지하지 못한 상황에서 사용자의 의도와는 무관하게 공격자가 의도한 행위
(수정, 삭제, 등록 등)를 요청하게 하는 공격을 말한다. 웹 응용프로그램이 사용자로부터 받은 요청이 해당 사용자가
의도한 대로 작성되고 전송된 것인지 확인하지 않는 경우 발생 가능하다. 특히 사용자가 관리자 권한을 가지는
경우 사용자 권한관리, 게시물 삭제, 사용자 등록 등 관리자 권한으로만 수행 가능한 기능을 공격자의 의도대로
실행시킬 수 있게 된다. 공격자는 사용자가 인증한 세션이 특정 동작을 수행해도 계속 유지되어 정상적인 요청과
비정상적인 요청을 구분하지 못하는 점을 악용한다.
파이썬에서 가장 많이 사용하고 있는 Django 프레임워크와 Flask 프레임워크에서는 각각 CSRF(Cross-Site
Request Forgery) 토큰 기능을 지원하고 있으며, Django는 {% csrf token %} 태그를 이용해 CSRF 토큰
기능 제공하고 Flask에서는 Flask-WTF 확장 라이브러리를 통해 {{form.csrf_token}} 태그를 이용한 CSRF
토큰 기능을 제공해 태그를 사용하는 경우 CSRF 공격에 대비할 수 있다.
나. 안전한 코딩기법
해당 요청이 정상적인 사용자의 정상적인 절차에 의한 요청인지를 구분하기 위해 세션별로 CSRF 토큰을
생성하여 세션에 저장하고 사용자가 작업 페이지를 요청할 때마다 hidden 값으로 클라이언트에게 토큰을 전달한 뒤,
해당 클라이언트의 데이터 처리 요청 시 전달되는 CSRF 토큰값을 체크하여 요청의 유효성을 검사하도록 한다.

![p54 이미지](images/p54_img0.png)

Django 프레임워크와 Flask 프레임워크는 미들웨어와 프레임워크에서 기본적으로 CSRF Token을 사용해서
CSRF 공격으로부터 보호하는 기능을 가지고 있다. 해당 기능을 사용하기 위해 form 태그 내부에 csrf_token을
사용해야 한다.
다. 코드예제
가) Django 프레임워크 사용
Django 프레임워크에서는 1.2 버전부터 CSRF 취약점을 방지 기능을 기본으로 제공하고 있다. 미들웨어의
CSRF 옵션을 비활성하거나 템플릿에서 csrf_exempt decorator를 사용하는 경우 CSRF 공격에 노출될 수 있다.
⦁Django 미들웨어 설정(settings.py) 사례

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
MIDDLEWARE = [
'django.contrib.sessions.middleware.SessionMiddleware',
# MIDDLEWARE 목록에서 CSRF 항목을 삭제 또는 주석처리 하면
# Django 앱에서 CSRF 유효성 검사가 전역적으로 제거된다
# 'django.middleware.csrf.CsrfViewMiddleware',
'django.contrib.auth.middleware.AuthenticationMiddleware',
'django.contrib.messages.middleware.MessageMiddleware',
'django.middleware.locale.LocaleMiddleware',
......
]
다음은 Django의 CSRF 기능을 활성화하기 위한 안전한 미들웨어 설정 예제를 보여 준다. 미들웨어의
CSRF 기능을 주석 또는 삭제 처리하지 않아야 한다. 템플릿 페이지에는 csrf_token을 form 태그 안에 명시
해야 미들웨어에서 정상적으로 CSRF 기능을 사용할 수 있다.

![p55 이미지](images/p55_img1.png)


![p55 이미지](images/p55_img2.png)


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
MIDDLEWARE = [
'django.contrib.sessions.middleware.SessionMiddleware',
# MIDDLEWARE 목록에서 CSRF 항목을 활성화 한다
'django.middleware.csrf.CsrfViewMiddleware',
'django.contrib.auth.middleware.AuthenticationMiddleware',
'django.contrib.messages.middleware.MessageMiddleware',
'django.middleware.locale.LocaleMiddleware',
......
]
⦁Django 뷰 기능 설정(views.py) 사례
미들웨어에 CSRF 검증 기능이 활성화 되어 있어도 View에서 CSRF 기능을 해제하는 경우에는 해당 요청에
대해서 CSRF 검증 기능을 사용하지 않게 된다. 다음은 Function-Based View에서 CSRF 검증 기능을 비활성화
하는 예제를 보여 준다.

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
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# csrf.exempt 데코레이터로 미들웨어에서 보호되는 CSRF 기능을 해제한다
@csrf.exempt
def pay_to_point(request):
user_id = request.POST.get('user_id', '')
pay = request.POST.get('pay', '')
product_info = request.POST.get('product_info', '')
ret = handle_pay(user_id, pay, product_info)
return render(request, '/view_wallet.html', {'wallet':ret})

![p56 이미지](images/p56_img1.png)


![p56 이미지](images/p56_img2.png)


![p56 이미지](images/p56_img4.png)


![p56 이미지](images/p56_img5.png)

Django는 기본적으로 CSRF 기능을 강제하고 있지만, 부득이하게 CSRF 기능을 해제해야 하는 경우는 미들
웨어의 CSRF 기능을 전역적으로 비활성화 하기 보다는 미들웨어의 CSRF 기능은 활성화 하고 필요한 요청에
대해서만 csrf_exempt 데코레이터를 사용하여야 하고 이 경우에 크로스사이트 요청 위조의 위협에 노출될
수 있으므로 주의를 기울여야 한다.

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
from django.shortcuts import render
from django.template import RequestContext
# csrf_exempt 데코레이터를 삭제하거나 주석 처리한다.
# @csrf_exempt
def pay_to_point(request):
user_id = request.POST.get('user_id', '')
pay = request.POST.get('pay', '')
product_info = request.POST.get('product_info', '')
ret = handle_pay(user_id, pay, product_info)
return render(request, '/view_wallet.html', {'wallet':ret})
⦁Django 템플릿 설정 사례
미들웨어에서 CSRF 기능을 활성화해도 템플릿 페이지에 CSRF 토큰을 명시하지 않을 경우 CSRF 검증
기능을 사용할 수 없다.

**안전하지 않은 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
<!--html page-->
<form action="" method="POST">
<!-- form 태그 내부에 csrf_token 미적용-->
<table>
{{form.as_table}}
</table>
<input type="submit"/>
</form>

![p57 이미지](images/p57_img1.png)


![p57 이미지](images/p57_img2.png)


![p57 이미지](images/p57_img4.png)


![p57 이미지](images/p57_img5.png)

미들웨어에서 CSRF 기능을 활성화한 후에 템플릿 페이지에서는 csrf_token 값을 명시하여야만 정상적인
CSRF 검증 기능을 사용할 수 있다.

**안전한 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
<!--html page-->
<form action="" method="POST">
{% csrf_token %}  <!--csrf_token 사용->
<table>
{{form.as_table}}
</table>
<input type="submit"/>
</form>
나) Flask 프레임워크 사용
⦁Flask app 설정 사례
Flask의 WTF 패키지를 사용하면 CSRF 보호 기법을 사용할 수 있다. 아래 예제 코드는 CSRF 설정이 되지
않은 상태를 보여 준다.

**안전하지 않은 코드 예시**

1:
2:
3:
from flask import Flask
app = Flask(__name__)
Flask 프레임워크를 사용해 웹 애플리케이션을 구축하는 경우 CSRF를 방지하려면 Flask-WTF extension의
CSRFProtect를 사용해야 한다. 다음과 같이 app에 설정하고 HTML(템플릿) 페이지에는 CSRF 토큰을 추가
해야 한다.

![p58 이미지](images/p58_img1.png)


![p58 이미지](images/p58_img2.png)


![p58 이미지](images/p58_img4.png)


![p58 이미지](images/p58_img5.png)


**안전한 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
from flask import Flask
from flask_wtf.csrf import CSRFProtect
# CSRF 설정 추가
csrf = CSRFProtect(app)
app = Flask(__name__)
app.config[‘SECRET_KEY’] = os.environ.get('SECRET_KEY')
csrf.init_app(app)
⦁Flask 템플릿 설정 사례
위 코드처럼 함수에 CSRF 기능을 활성화 해도 HTML 파일에 csrf_token을 명시하지 않을 경우 CSRF
검증 기능을 사용할 수 없다.

**안전하지 않은 코드 예시**

1:
2:
3:
4:
5:
6:
7:
<form action="" method="POST">
<!-- form 태그 내부에 csrf_token 미적용-->
<table>
{{as_table}}
</table>
<input type="submit"/>
</form>
템플릿 페이지에도 csrf_token 값을 명시해줘야 정상적인 CSRF 검증이 수행된다.
FlaskForm 사용 시에는 {{ form.csrf_token }}을 명시해야 하고 템플릿에 FlaskForm을 사용하지 않을
경우에는 form 태그 안에 hidden input 값으로 {{ csrf_token }} 값을 명시해야 한다.

![p59 이미지](images/p59_img1.png)


![p59 이미지](images/p59_img2.png)


![p59 이미지](images/p59_img4.png)


![p59 이미지](images/p59_img5.png)


**안전한 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
<form action="" method="POST">
<!-- form 태그 내부에 csrf_token 적용-->
<input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />
<table>
{{table}}
</table>
<input type="submit"/>
</form>
라. 참고자료
① CWE-352: Cross-Site Request Forgery (CSRF), MITRE,
https://cwe.mitre.org/data/definitions/352.html
② Cross Site Request Forgery (CSRF), OWASP,
https://owasp.org/www-community/attacks/csrf
③ Cross-Site Request Forgery Prevention Cheat Sheet, OWASP
https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
④ Cross Site Request Forgery protection, Django Software Foundation
https://docs.djangoproject.com/en/3.2/ref/csrf/
⑤ CSRF Protection, WTForms
https://flask-wtf.readthedocs.io/en/0.15.x/csrf/

![p60 이미지](images/p60_img1.png)


![p60 이미지](images/p60_img2.png)

12. 서버사이드 요청 위조
가. 개요
적절한 검증 절차를 거치지 않은 사용자 입력값을 내부 서버간의 요청에 사용해 악의적인 행위가 발생할 수
있는 보안약점이다. 외부에 노출된 웹 서버가 취약한 애플리케이션을 포함하는 경우 공격자는 URL 또는 요청문을
위조해 접근통제를 우회하는 방식으로 비정상적인 동작을 유도하거나 신뢰된 네트워크에 있는 데이터를 획득
할 수 있다.
나. 안전한 코딩기법
식별 가능한 범위 내에서 사용자의 입력값을 다른 시스템의 서비스 호출에 사용하는 경우, 사용자의 입력값을
화이트리스트 방식으로 필터링한다.
부득이하게 사용자가 지정하는 무작위의 URL을 받아들여야 하는 경우라면 내부 URL을 블랙리스트로 지정
하여 필터링 한다. 또한 동일한 내부 네트워크에 있더라도 기기 인증, 접근권한을 확인하여 요청이 이루어질
수 있도록 한다.

![p61 이미지](images/p61_img0.png)

다. 코드예제

**<참고 : 삽입 코드의 예>**

설명
삽입 코드의 예
내부망 중요 정보 획득
http://sample_site.com/connect?url=http://192.168.0.45/member/list.json
외부 접근 차단된
admin 페이지 접근
http://sample_site.com/connect?url=http://192.168.0.45/admin
도메인 체크를 우회하여
중요 정보 획득
http://sample_site.com/connect?url=http://sample_site.com:x@192.168.0.45/member/
list.json
단축 URL을 이용한
Filter 우회
http://sample_site.com/connect?url=http://bit.ly/sdjk3kjhkl3
도메인을 사설IP로 설정해
중요정보 획득
http://sample_site.com/connect?url=http://192.168.0.45/member/list.json
서버내 파일 열람
http://sample_site.com/connect?url=file:///etc/passwd
다음 예제는 안전하지 않은 코드를 보여 준다. 사용자로부터 입력된 URL 주소를 검증 없이 사용하면 의도하지
않은 다른 서버의 자원에 접근할 수 있게 된다.

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
from django.shortcuts import render
import requests
def call_third_party_api(request):
addr = request.POST.get('address', '')
# 사용자가 입력한 주소를 검증하지 않고 HTTP 요청을 보낸 후
# 응답을 사용자에게 반환
result = requests.get(addr).text
return render(request, '/result.html', {'result':result})
다음과 같이 안전한 코드를 작성하면 사전에 정의된 서버 목록을 정의하고 매칭되는 URL만 사용할 수 있으므로
URL 값을 임의로 조작할 수 없다.

![p62 이미지](images/p62_img1.png)


![p62 이미지](images/p62_img2.png)


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
from django.shortcuts import render
import requests
# 허용하는 도메인을 화이트리스트에 정의할 경우 DNS rebinding 공격 등에
# 노출될 위험이 있어 신뢰할 수 있는 자원에 대한 IP를 사용해
# 검증하는 것이 조금 더 안전하다
ALLOW_SERVER_LIST = [
'https://127.0.0.1/latest/',
'https://192.168.0.1/user_data',
'https://192.168.0.100/v1/public',
]
def call_third_party_api(request):
addr = request.POST.get('address', '')
# 사용자가 입력한 URL을 화이트리스트로 검증한 후 그 결과를 반환하여
# 검증되지 않은 주소로 요청을 보내지 않도록 제한한다
if addr not in ALLOW_SERVER_LIST:
return render(request, '/error.html', {‘error’ = '허용되지 않은 서버입니다.'})
result = requests.get(addr).text
return render(request, '/result.html', {'result':result})
라. 참고자료
① CWE-918: Server-Side Request Forgery (SSRF), MITRE
https://cwe.mitre.org/data/definitions/918.html
② Server Side Request Forgery, OWASP
https://owasp.org/www-community/attacks/Server_Side_Request_Forgery
③ Server-Side Request Forgery Prevention Cheat Sheet, OWASP
https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html

![p63 이미지](images/p63_img1.png)


![p63 이미지](images/p63_img2.png)

13. HTTP 응답분할
가. 개요
HTTP 요청 내의 파라미터(Parameter)가 HTTP 응답 헤더에 포함되어 사용자에게 다시 전달될 때 입력값에
CR(Carriage Return)이나 LF(Line Feed)와 같은 개행문자가 존재하면 HTTP 응답이 2개 이상으로 분리될
수 있다. 이 경우 공격자는 개행문자를 이용해 첫 번째 응답을 종료 시키고 두 번째 응답에 악의적인 코드를
주입해 XSS 및 캐시훼손(Cache Poisoning) 공격 등을 수행할 수 있다.
파이썬 3.9.5+ 버전에서의 URLValidator에서 HTTP 응답분할 취약점이 보고되기도 했고 해당 라이브러리를
사용하는 Django버전에도 영향이 있다. HTTP 응답분할 공격으로부터 어플리케이션을 안전하게 지키려면 최신
버전의 라이브러리, 프레임워크를 사용하고 외부 입력값에 대해서는 철저한 검증 작업을 수행해야 한다.
나. 안전한 코딩기법
요청 파라미터의 값을 HTTP 응답 헤더(예를 들어, Set-Cookie 등)에 포함시킬 경우 CR(\r), LF(\n)와
같은 개행문자를 제거해야 한다. 외부 입력값이 헤더, 쿠키, 로그 등에 사용될 경우에는 항상 개행문자를 검증
하고 가능하다면 헤더에 사용되는 예약어 등을 화이트리스트로 제한해야 한다.

![p64 이미지](images/p64_img0.png)

다. 코드예제
사용자 요청에 포함된 값을 필터링 및 검증 없이 응답에 사용하는 경우 개행문자로 인해 여러 개의 응답으로
분할되어 사용자에게 전달될 수 있다.

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
from django.http import HttpResponse
def route(request):
content_type = request.POST.get('content-type')
# 외부 입력값을 검증 또는 필터링 하지 않고
# 응답 헤더의 값으로 포함시켜 회신한다
......
res = HttpResponse()
res['Content-Type'] = content_type
return res
응답 분할을 예방하기 위해 \r, \n과 같은 문자에 대해 치환 또는 예외처리를 적용해 응답분할이 발생하지
않도록 예방해야 한다.

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
from django.http import HttpResponse
def route(request):
content_type = request.POST.get('content-type')
# 응답헤더에 포함될 수 있는 외부 입력값 내의 개행 문자를 제거한다
content_type = content_type.replace('\r', '')
content_type = content_type.replace('\n', '')
......
res = HttpResponse()
res['Content-Type'] = content_type
return res

![p65 이미지](images/p65_img1.png)


![p65 이미지](images/p65_img2.png)


![p65 이미지](images/p65_img4.png)


![p65 이미지](images/p65_img5.png)

라. 참고자료
① CWE-113: Improper Neutralization of CRLF Sequences in HTTP Headers ('HTTP Response Splitting'), MITRE,
https://cwe.mitre.org/data/definitions/113.html
② HTTP Response Splitting, OWASP,
https://owasp.org/www-community/attacks/HTTP_Response_Splitting
③ Django security releases issued, Django Software Foundation,
https://www.djangoproject.com/weblog/2021/may/06/security-releases/
14. 정수형 오버플로우
가. 개요
정수형 오버플로우는 정수형 크기가 고정된 상태에서 변수가 저장할 수 있는 범위를 넘어선 값을 저장하려
할 때 실제 저장되는 값이 의도치 않게 아주 작은 수 또는 음수가 되어 프로그램이 예기치 않게 동작하게 되는
취약점이다. 특히 반복문 제어, 메모리 할당, 메모리 복사 등을 위한 조건으로 사용자가 제공하는 입력값을
사용하고 그 과정에서 정수형 오버플로우가 발생하는 경우 보안상 문제를 유발할 수 있다.
파이썬 2.x에서는 int 타입 변수의 값이 표현 가능한 범위를 넘어서게 되면 자동으로 long으로 타입을 변경해
범위를 확장한다. 파이썬 3.x에서는 long 타입을 없애고 int 타입만 유지하되, 정수 타입의 자료형에
‘Arbitrary-precision arithmetic’ 방식을 사용해 오버플로우를 발생하지 않는다. 하지만 파이썬 3.x에서도
기존의 pydata stack을 사용하는 패키지를 사용할 때는 C언어와 동일하게 정수형 데이터가 처리되므로 오버
플로우 발생에 유의해야 한다. 이처럼 언어 자체에서는 안정성을 보장하지만 특정 취약점에 취약한 패키지 또는
라이브러리를 사용하는 것에 주의해야 한다.
나. 안전한 코딩기법
기본 파이썬 자료형을 사용하지 않고 패키지에서 제공하는 데이터 타입을 사용할 경우 해당 패키지에서 제공
하는 데이터 타입의 표현 방식과 최대 크기를 반드시 확인해야 한다. numpy에서는 기본적으로 64비트 길이의
정수형 변수를 사용하며, 변수가 표현할 수 없는 큰 크기의 숫자는 문자열 형식(object)으로 변환하는 기능을
제공한다. 하지만 64비트를 넘어서는 크기의 숫자는 제대로 처리하지 못한다. 따라서 변수에 값 할당 전에
반드시 변수의 최소 및 최대값을 확인하고 범위를 넘어서는 값을 할당하지 않는지 테스트해야 한다.

![p67 이미지](images/p67_img0.png)

다. 코드예제
다음은 거듭제곱을 계산해 그 결과를 반환하는 함수 예시로, 계산 가능한 숫자에 대한 검증이 없어 에러는
발생하지 않지만 반환값을 처리하는 함수에서 예기치 않은 오류가 발생할 수 있다.

**안전하지 않은 코드 예시**

1:
2:
3:
4:
5:
6:
import numpy as np
def handle_data(number, pow):
res = np.power(number, pow, dtype=np.int64)
# 64비트를 넘어서는 숫자와 지수가 입력될 경우 오버플로우가 발생해 결과값이 0이 된다
return res
오버플로우 발생을 예방하려면 입력하는 값이 사용하는 데이터 타입의 최소보다 크거나 최대보다 작은지
확인해야 한다. 만약 위 코드 예시처럼 값을 계산해야 하는 경우 오버플로우가 발생하지 않는 파이썬 기본 자료형에
계산 결과값을 저장한 후 그 값을 검사해 오버플로우 여부를 확인해야 한다.

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
import numpy as np
MAX_NUMBER = np.iinfo(np.int64).max
MIN_NUMBER = np.iinfo(np.int64).min
def handle_data(number, pow):
calculated = number ** pow
# 파이썬 기본 자료형으로 큰 수를 계산한 후 이를 검사해 오버플로우 탐지
if calculated > MAX_NUMBER or calculated < MIN_NUMBER:
# 오버플로우 탐지 시 비정상 종료를 나타내는 –1 값 반환
return –1
res = np.power(number, pow, dtype=np.int64)
return res

![p68 이미지](images/p68_img1.png)


![p68 이미지](images/p68_img2.png)


![p68 이미지](images/p68_img4.png)


![p68 이미지](images/p68_img5.png)

라. 참고자료
① CWE-190: Integer Overflow or Wraparound, MITRE
https://cwe.mitre.org/data/definitions/190.html
② Integer Overflow Error, ZAP,
https://www.zaproxy.org/docs/alerts/30003/
③ Arbitrary-precision arithmetic,
https://en.wikipedia.org/wiki/Arbitrary-precision_arithmetic
④ PEP 237 – Unifying Long Integers and Integers,
https://peps.python.org/pep-0237/
⑤ Numpy Types
https://numpy.org/doc/stable/user/basics.types.html?highlight=s
15. 보안기능 결정에 사용되는 부적절한 입력값
가. 개요
응용 프로그램이 외부 입력값에 대한 신뢰를 전제로 보호 메커니즘을 사용하는 경우 공격자가 입력값을 조작
할 수 있다면 보호 메커니즘을 우회할 수 있게 된다.
개발자들이 흔히 쿠키, 환경변수 또는 히든필드와 같은 입력값이 조작될 수 없다고 가정하지만 공격자는 다양한
방법을 통해 이러한 입력값들을 변경할 수 있고 조작된 내용은 탐지되지 않을 수 있다. 인증이나 인가와 같은
보안 결정이 이런 입력값(쿠키, 환경변수, 히든필드 등)에 기반을 두어 수행되는 경우 공격자는 입력값을 조작해
응용프로그램의 보안을 우회할 수 있다. 따라서 충분한 암호화, 무결성 체크를 수행하고 이와 같은 메커니즘이
없는 경우엔 외부 사용자에 의한 입력값을 신뢰해서는 안 된다.
파이썬의 Django 프레임워크에서 세션을 관리하는 기능을 제공하고 있으며, 해당 기능 사용 시에는 세션쿠키의
만료 시점을 설정해 사용할 수 있으며 DRF(Django Rest Framework)에서 제공하는 토큰 및 세션 기능을
사용해 안전하게 구성할 수 있다.

![p70 이미지](images/p70_img0.png)

나. 안전한 코딩기법
상태 정보나 민감한 데이터 특히 사용자 세션 정보와 같은 중요 정보는 서버에 저장하고 보안확인 절차도
서버에서 실행한다. 보안설계 관점에서 신뢰할 수 없는 입력값이 응용 프로그램 내부로 들어올 수 있는 지점을
검토하고 민감한 보안 기능 실행에 사용되는 입력값을 식별해 입력값에 대한 의존성을 없애는 구조로 변경
가능한지 분석한다.
다. 코드예제
다음은 안전하지 않은 코드로 쿠키에 저장된 권한 등급을 가져와 관리자인지 확인 후에 사용자의 패스워드를
초기화 하고 메일을 보내는 예제다. 쿠키에서 등급을 가져와 관리자 여부를 확인한다.

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
from django.shortcuts import render
def init_password(request):
# 쿠키에서 권한 정보를 가져 온다
role = request.COOKIE['role']
request_id = request.POST.get('user_id', '')
request_mail = request.POST.get('user_email','')
# 쿠키에서 가져온 권한이 관리자인지 비교
if role == 'admin':
# 사용자의 패스워드 초기화 및 메일 발송 처리
password_init_and_sendmail(request_id, request_mail)
return render(request, '/success.html')
else:
return render(request, '/failed.html')

![p71 이미지](images/p71_img1.png)


![p71 이미지](images/p71_img2.png)

중요 기능 수행을 위한 데이터는 위변조 가능성이 높은 쿠키보다 세션에 저장하도록 한다.

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
from django.shortcuts import render
def init_password(request):
# 세션에서 권한 정보를 가져옴
role = request.session['role']
request_id = request.POST.get('user_id', '')
request_mail = request.POST.get('user_email','')
# 세션에서 가져온 권한이 관리자인지 비교
if role == ‘admin’:
# 사용자의 패스워드 초기화 및 메일 발송 처리
password_init_and_sendmail(request_id, request_mail)
return render(request, '/sucess.html')
else:
return render(request, '/failed.html')
라. 참고자료
① CWE-807: Reliance on Untrusted Inputs in a Security Decision, MITRE,
https://cwe.mitre.org/data/definitions/807.html
② How to use sessions, Django Software Foundation,
https://docs.djangoproject.com/en/3.2/topics/http/sessions/
③ Flask Sessions,
https://flask-session.readthedocs.io/en/latest/

![p72 이미지](images/p72_img1.png)


![p72 이미지](images/p72_img2.png)

16. 포맷 스트링 삽입
가. 개요
외부로부터 입력된 값을 검증하지 않고 입·출력 함수의 포맷 문자열로 그대로 사용하는 경우 발생할 수 있는
보안약점이다. 공격자는 포맷 문자열을 이용해 취약한 프로세스를 공격하거나 메모리 내용을 읽고 쓸 수 있다.
이를 통해 취약한 프로세스의 권한을 취득해 임의의 코드를 실행 할 수 있다.
파이썬에서는 문자열의 포맷팅 방법으로 “% formatting”, “str.format”, “f-string” 과 같이 세 가지 문자열
포맷팅 방식을 제공하고 있다(f-string 은 파이썬 3.6 버전부터 사용 가능하다). 공격자는 포맷 문자열을 이용해
내부 정보를 문자열로 만들 수 있으며, 이를 그대로 사용하는 경우 중요 정보 유출로 이어질 수 있다.
나. 안전한 코딩기법
포맷 문자열을 처리하는 함수 사용 시 사용자 입력값을 직접적으로 포맷 문자열로 사용하거나 포맷 문자열
생성에 포함시키지 않아야 한다. 사용자로부터 입력 받은 데이터를 포맷 문자열로 사용하고자 하는 경우에는
서식 지정자를 포함하지 않거나 파이썬의 내장함수 또는 내장변수 등이 포함되지 않도록 해야 한다.
다. 코드예제
아래 예시에서는 외부에서 입력받은 문자열을 바로 포맷스트링으로 사용하고 있는데, 이는 내부 정보가 외부로
노출될 수 있는 문제를 내포하고 있다.
공격자가 # {user.__init__.__globals__[AUTHENTICATE_KEY]} 형식의 문자열 입력 시 전역 변수에 접근
하여 AUTHENTICATE_KEY의 값을 탈취 할 수 있다.

![p73 이미지](images/p73_img0.png)


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
from django.shortcuts import render
AUTHENTICATE_KEY = 'Passw0rd'
def make_user_message(request):
user_info = get_user_info(request.POST.get('user_id', ''))
format_string = request.POST.get('msg_format', '')
# 내부의 민감한 정보가 외부로 노출될 수 있다.
# 사용자가 입력한 문자열을 포맷 문자열로 사용하고 있어 안전하지 않다
message = format_string.format(user=user_info)
return render(request, '/user_page.html', {'message':message})
외부에서 입력 받은 문자열은 반드시 포맷 지정자를 이용해 바인딩 후 사용해야 하며 직접적으로 포맷문자열로
사용해서는 안 된다.

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
from django.shortcuts import render
AUTHENTICATE_KEY = 'Passw0rd'
def make_user_message(request):
user_info = get_user_info(request.POST.get('user_id', ''))
# 사용자가 입력한 문자열을 포맷 문자열로 사용하지 않아 안전하다
message = 'user name is {}'.format(user_info.name)
return render(request, '/user_page.html', {'message':message})
라. 참고자료
① CWE-134: Use of Externally-Controlled Format String, MITRE,
https://cwe.mitre.org/data/definitions/134.html
② Format string attack, OWASP,
https://owasp.org/www-community/attacks/Format_string_attack
③ 파이썬 format, Python Software Foundation,
https://docs.python.org/3/library/functions.html#format
④ Format String Syntax, Python Software Foundation,
https://docs.python.org/3/library/string.html#format-string-syntax

![p74 이미지](images/p74_img1.png)


![p74 이미지](images/p74_img2.png)


![p74 이미지](images/p74_img4.png)


![p74 이미지](images/p74_img5.png)
