
**제3절 시간 및 상태**

동시 또는 거의 동시에 여러 코드 수행을 지원하는 병렬 시스템이나 하나 이상의 프로세스가 동작되는 환경에서
시간 및 상태를 부적절하게 관리하여 발생할 수 있는 보안약점이다.
1. 경쟁조건: 검사시점과 사용시점(TOCTOU)
가. 개요
병렬시스템(멀티프로세스로 구현한 응용프로그램)에서는 자원(파일, 소켓 등)을 사용하기에 앞서 자원의 상태를
검사한다. 하지만 자원을 사용하는 시점과 검사하는 시점이 다르기 때문에 검사하는 시점(Time Of Check)에
존재하던 자원이 사용하던 시점(Time Of Use)에 사라지는 등 자원의 상태가 변하는 경우가 발생한다.
예를 들어 프로세스 A와 B가 존재하는 병렬시스템 환경에서 프로세스 A는 자원사용(파일 읽기)에 앞서 해당
자원(파일)의 존재 여부를 검사(TOC) 한다. 이때는 프로세스 B가 해당 자원(파일)을 아직 사용(삭제)하지 않았기
때문에 프로세스 A는 해당 자원(파일)이 존재한다고 판단한다. 그러나 프로세스 A가 자원 사용(파일읽기)을
시도하는 시점(TOU)에 해당 자원(파일)은 사용불가능 상태이기 때문에 오류 등이 발생할 수 있다.

![p125 이미지](images/p125_img0.png)

이와 같이 하나의 자원에 대해 동시에 검사시점과 사용시점이 달라 생기는 보안약점으로 인해 동기화 오류뿐만
아니라 교착상태 등과 같은 문제점이 발생할 수 있다.
파이썬에서는 멀티스레드 환경에서 공유 자원에 여러 쓰레드가 접근하는 것을 막기 위해 Lock 객체를 제공
한다(자원의 상태를 잠금으로 변경하는 acquire() 메서드와 사용 중인 자원을 해제하는 release() 메서드).
나. 안전한 코딩기법
변수, 파일과 같은 공유자원을 여러 프로세스가 접근하여 사용할 경우 동기화 구문을 사용하여 한 번에 하나의
프로세스만 접근 가능하도록 해야 하며 성능에 미치는 영향을 최소화하기 위해 임계영역(critical section) 주변만
동기화 구문을 사용한다.
파이썬의 Lock 객체 사용 시 lock.acquire()로 자원을 잠그고 lock.release()로 자원을 해제해야 하며 이
부분을 with 문을 사용해 간단하게 표현할 수 있다.
다. 코드예제
다음 예제는 공유된 파일을 사용할 때 파일을 불러온 후 실제로 파일을 사용하는 부분이 실행되기 전 짧은
시간에도 다른 사용자 또는 프로그램에 의해 파일이 사라져 원하는 기능을 실행할 수 없는 경우를 보여 준다.

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
import os
import io
import datetime
import threading
def write_shared_file(filename, content):
# 멀티스레드 환경에서는 다른 사용자들의 작업에 따라 파일이 사라질 수
# 있기 때문에 공유 자원에 대해서는 검사와 사용을 동시에 해야 한다.
if os.path.isfile(filename) is True:
f = open(filename, 'w')
f.seek(0, io.SEEK_END)
f.write(content)
f.close()
def start():
filename = ‘./temp.txt’
content = f“start time is {datetime.datetime.now()}”
my_thread = threading.Thread(target=write_shared_file, args=(filename, content))
my_thread.start()

![p126 이미지](images/p126_img1.png)


![p126 이미지](images/p126_img2.png)

다음은 파일 검사 후 파일이 삭제되거나 변동되는 것을 예방하기 위해 lock을 사용하여 각 쓰레드에서 공유
자원에 접근하는 것을 통제 하는 예제 코드를 보여 준다. lock을 acquire하면 해당 쓰레드만 공유 데이터에
접근 할 수 있고 lock을 release 해야만 다른 쓰레드에서 공유 데이터에 접근 할 수 있다.

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
import os
import io
import datetime
import threading
lock = threading.Lock()
def write_shared_file(filename, content):
# lock을 이용하여 여러 사용자가 동시에 파일에 접근하지 못하도록 제한
with lock:
if os.path.isfile(filename) is True:
f = open(filename, 'w')
f.seek(0, io.SEEK_END)
f.write(content)
f.close()
def start():
filename = ‘./temp.txt’
content = f“start time is {datetime.datetime.now()}”
my_thread = threading.Thread(target=write_shared_file, args=(filename, content))
my_thread.start()
라. 참고자료
① CWE-367: Time-of-check Time-of-use (TOCTOU) Race Condition, MITRE,
https://cwe.mitre.org/data/definitions/367.html
② Thread-based parallelism, Python Software Foundation,
https://docs.python.org/3/library/threading.html

![p127 이미지](images/p127_img1.png)


![p127 이미지](images/p127_img2.png)

2. 종료되지 않는 반복문 또는 재귀 함수
가. 개요
재귀 함수의 순환 횟수를 제어하지 못해 할당된 메모리나 프로그램 스택 등의 자원을 개발자가 의도한 범위를
과도하게 초과해 사용하면 위험하다. 대부분의 경우 기본 케이스(Base Case4))가 정의되어 있지 않은 재귀
함수는 무한 루프에 빠져들게 되고 자원고갈을 유발함으로써 시스템의 정상적인 서비스를 제공할 수 없게 한다.
파이썬에서는 재귀 함수의 재귀 반복 제한(Recursion Depth Limit)이 적용되어 있어 무한루프가 발생하지
않으나, setrecursionlimit() 함수를 사용해 임의로 최대 깊이를 변경해 사용하는 경우 재귀 함수 호출 횟수가
과도하게 많아지지 않도록 주의해야 한다.
나. 안전한 코딩기법
모든 재귀 호출 시 호출 횟수를 제한하거나 재귀 함수 종료 조건을 명확히 정의해 호출을 제어해야 한다.
파이썬의 recursionlimit 제한은 스택 오버플로우 발생을 막기 위한 방법으로, recursionlimit 값을 과도하게
큰 값으로 설정하지 않아야 한다.
다. 코드예제
다음 코드 예시의 factorial 함수는 함수 내부에서 자신을 호출하는 함수로 재귀문을 빠져 나오는 조건을
정의하고 있지 않아 시스템 장애를 유발할 수 있다.
4) 기본 케이스(Base Case)는 재귀 호출을 하지 않고 반환하는 방법을 의미한다.

![p128 이미지](images/p128_img0.png)


**안전하지 않은 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
def factorial(num):
# 재귀함수 탈출조건을 설정하지 않아 동작 중 에러 발생
return num * factorial(num – 1)
if __name__ == '__main__':
itr = 5
result = factorial(itr)
print(str(itr) + ' 팩토리얼 값은 : ' + str(result))
특정 조건 또는 횟수에 따라 재귀 코드 실행을 중단해 프로그램이 무한 반복에 빠지지 않도록 한다.

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
def factorial(num):
# 재귀함수 사용 시에는 탈출 조건을 명시해야 한다.
if (num == 0):
return 1
else:
return num * factorial(num - 1)
if __name__ == '__main__':
itr = 5
result = factorial(itr)
print(str(itr) + ' 팩토리얼 값은 : ' + str(result))
파이썬의 재귀 반복 제한은 기본이 1000으로 설정되어 있다. Anaconda의 경우는 기본 값이 2000이다.
이 값을 과도하게 변경하지 않아야 한다.

**안전한 코드 예시**

1:
2:
3:
import sys
sys.setrecursionlimit(1000)

![p129 이미지](images/p129_img1.png)


![p129 이미지](images/p129_img2.png)


![p129 이미지](images/p129_img4.png)


![p129 이미지](images/p129_img5.png)

라. 참고자료
① CWE-674: Uncontrolled Recursion, MITRE,
https://cwe.mitre.org/data/definitions/674.html
② CWE-835: Loop with Unreachable Exit Condition ('Infinite Loop'), MITRE,
https://cwe.mitre.org/data/definitions/835.html
③ sys.setrecursionlimit, Python Software Foundation,
https://docs.python.org/3/library/sys.html#sys.setrecursionlimit