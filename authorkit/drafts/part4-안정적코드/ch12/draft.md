# Chapter 12. 시간 및 상태 — 타이밍이 만드는 버그

여러 작업이 동시에 실행되는 환경에서는 "언제" 코드가 실행되는지가 "무엇을" 실행하는지만큼 중요합니다. AI가 생성한 코드는 단일 스레드 환경에서는 잘 동작하지만, 실제 서버 환경에서 동시에 여러 요청이 들어올 때 예상치 못한 충돌을 일으킬 수 있습니다. 이 장에서는 시간과 상태(Time and State) 관련 보안약점을 살펴봅니다.

---

## 12-1. 경쟁 조건: 검사 시점과 사용 시점(TOCTOU)

### 개요

경쟁 조건(Race Condition)이란 두 개 이상의 프로세스나 스레드가 공유 자원에 동시에 접근할 때 실행 순서에 따라 결과가 달라지는 현상을 말합니다. 그중에서도 **TOCTOU(Time Of Check, Time Of Use)** 는 자원의 상태를 검사하는 시점(Check)과 실제로 사용하는 시점(Use) 사이의 시간 차이를 악용하는 대표적인 보안약점입니다.

예를 들어, 파일이 존재하는지 확인한 뒤 해당 파일을 열어서 쓰는 코드가 있다고 가정합니다. 검사 시점에는 파일이 분명히 존재했지만, 실제로 파일을 열려는 그 찰나에 다른 프로세스가 해당 파일을 삭제하거나 심볼릭 링크(Symbolic Link)로 교체할 수 있습니다. 이 간극이 바로 공격자가 노리는 지점입니다.

### 왜 위험한가

바이브 코딩(Vibe Coding)으로 "파일 업로드 후 처리" 기능을 만들 때 AI는 보통 다음과 같은 흐름을 생성합니다: 파일 존재 여부 확인 → 파일 읽기 또는 쓰기. 단일 사용자 테스트에서는 문제가 없지만, 운영 환경에서 수십 명이 동시에 파일을 업로드하면 한 사용자의 파일이 다른 사용자의 요청에 의해 덮어씌워지거나 삭제될 수 있습니다. 최악의 경우, 공격자가 검사와 사용 사이의 틈을 이용해 시스템 파일에 접근하는 권한 상승(Privilege Escalation) 공격으로 이어질 수 있습니다.

### ❌ 취약한 코드

```python
import os
import threading

def write_shared_file(filename, content):
    # 파일 존재 여부를 먼저 검사(TOC)
    if os.path.isfile(filename):
        # 검사와 사용 사이에 다른 스레드가 파일을 삭제할 수 있음
        f = open(filename, 'w')  # 사용 시점(TOU)
        f.write(content)
        f.close()

def start():
    filename = './temp.txt'
    content = "user data"
    t = threading.Thread(target=write_shared_file, args=(filename, content))
    t.start()
```

위 코드에서 `os.path.isfile()`로 파일을 확인한 직후, 다른 스레드가 해당 파일을 삭제하면 `open()` 호출 시 `FileNotFoundError`가 발생합니다. 반대로 공격자가 파일을 심볼릭 링크로 교체하면 의도하지 않은 경로에 데이터가 기록될 수 있습니다.

### ✅ 안전한 코드

```python
import os
import threading

lock = threading.Lock()

def write_shared_file(filename, content):
    # Lock을 사용해 한 번에 하나의 스레드만 접근하도록 보호
    with lock:
        if os.path.isfile(filename):
            f = open(filename, 'w')
            f.write(content)
            f.close()

def start():
    filename = './temp.txt'
    content = "user data"
    t = threading.Thread(target=write_shared_file, args=(filename, content))
    t.start()
```

`threading.Lock()`을 사용하면 `with lock:` 블록 안의 코드는 한 번에 하나의 스레드만 실행할 수 있습니다. 검사와 사용이 원자적(Atomic)으로 이루어지므로 TOCTOU 문제를 방지할 수 있습니다.

> **💡 팁:** 웹 프레임워크에서 파일을 다룰 때는 데이터베이스 레코드와 함께 트랜잭션(Transaction)으로 묶거나, 고유한 파일명(UUID 기반)을 생성하여 충돌 자체를 원천적으로 방지하는 것이 더 실용적입니다.

---

## 12-2. 종료되지 않는 반복문 또는 재귀 함수

### 개요

재귀 함수(Recursive Function)는 자기 자신을 호출하는 함수입니다. 종료 조건인 기본 케이스(Base Case)가 없거나 잘못 정의되면 함수가 무한히 자신을 호출하게 됩니다. 마찬가지로, 반복문(Loop)의 탈출 조건이 도달 불가능하면 무한 루프(Infinite Loop)에 빠지게 됩니다. 이는 서버의 메모리와 CPU를 고갈시켜 서비스 거부(DoS, Denial of Service) 상태를 유발합니다.

### 왜 위험한가

AI 코드 생성 도구에 "팩토리얼 함수를 만들어줘"라고 요청하면 대부분 올바른 코드를 생성합니다. 하지만 복잡한 비즈니스 로직에서 재귀를 사용할 때, AI가 기본 케이스를 누락하거나 경계 조건(Edge Case)을 잘못 처리하는 경우가 발생합니다. 특히 트리 구조 탐색, 중첩 카테고리 조회, 댓글의 대댓글 처리 등에서 이 문제가 자주 나타납니다.

파이썬은 기본적으로 재귀 깊이 제한(Recursion Depth Limit)이 1,000으로 설정되어 있어 스택 오버플로우(Stack Overflow)를 방지합니다. 그러나 AI가 `sys.setrecursionlimit()`을 사용해 이 제한을 임의로 늘리는 코드를 생성하는 경우가 있으며, 이는 시스템 전체를 위험에 빠뜨릴 수 있습니다.

### ❌ 취약한 코드

```python
import sys

# AI가 "재귀 제한 에러를 해결해줘"라는 요청에 생성할 수 있는 위험한 코드
sys.setrecursionlimit(100000)

def factorial(num):
    # 기본 케이스(Base Case)가 없어 무한 재귀 발생
    return num * factorial(num - 1)

result = factorial(5)
```

기본 케이스가 없으므로 `num`이 0 아래로 계속 내려가면서 무한히 재귀 호출됩니다. `setrecursionlimit`을 극단적으로 높인 경우 파이썬 프로세스가 시스템 메모리를 소진할 때까지 계속 실행됩니다.

### ✅ 안전한 코드

```python
def factorial(num):
    # 명확한 기본 케이스 정의
    if num <= 0:
        return 1
    return num * factorial(num - 1)

result = factorial(5)
print(f"5 팩토리얼 값은: {result}")  # 출력: 120
```

기본 케이스를 `num <= 0`으로 명확히 정의하여 재귀가 반드시 종료되도록 합니다. 더 안전한 방법은 재귀 대신 반복문을 사용하는 것입니다.

```python
import math

# 내장 함수 사용 — 가장 안전하고 효율적
result = math.factorial(5)
```

> **⚠️ 주의:** AI가 `RecursionError`를 해결하기 위해 `sys.setrecursionlimit()`을 제안하면 주의해야 합니다. 이는 근본적인 해결이 아니라 시한폭탄의 타이머를 늘리는 것과 같습니다. 재귀 깊이 에러가 발생하면 알고리즘 자체를 반복문으로 변경하거나 로직을 재설계하는 것이 올바른 접근입니다.

### 바이브 코딩 시 체크포인트

| 점검 항목 | 확인 방법 |
|-----------|-----------|
| 공유 자원에 Lock 사용 여부 | 파일, 전역 변수 접근 시 `threading.Lock()` 또는 데이터베이스 트랜잭션 사용 확인 |
| 파일명 충돌 방지 | 사용자 업로드 파일에 UUID 기반 고유 파일명 사용 여부 확인 |
| 재귀 함수의 기본 케이스 | 모든 재귀 함수에 명확한 종료 조건이 있는지 확인 |
| `setrecursionlimit` 사용 여부 | 코드베이스에서 해당 함수 호출을 검색하여 불필요한 사용 제거 |
| 반복문 탈출 조건 | `while True` 패턴 사용 시 `break` 조건이 반드시 도달 가능한지 확인 |
| 재귀 대신 반복문 검토 | 깊은 재귀가 예상되는 경우 반복문이나 내장 함수로 대체 가능한지 검토 |
