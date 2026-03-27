# Chapter 14. 코드 오류 — 개발자가 놓치기 쉬운 함정들

완벽해 보이는 코드에도 미묘한 오류가 숨어 있을 수 있습니다. 변수가 `None`인지 확인하지 않거나, 파일이나 데이터베이스 연결을 제대로 닫지 않거나, 외부에서 전달된 데이터를 검증 없이 역직렬화하는 것은 모두 심각한 보안 사고로 이어질 수 있는 코드 오류(Code Quality)입니다. AI가 생성한 코드에서 특히 자주 발견되는 세 가지 패턴을 살펴봅니다.

---

## 14-1. Null Pointer 역참조

### 개요

Null Pointer 역참조(Null Pointer Dereference)는 객체가 존재하지 않는 상태, 즉 `None` 상태에서 해당 객체의 속성이나 메서드에 접근하려 할 때 발생합니다. 파이썬에서는 C/C++과 같은 포인터 개념이 없지만, `None` 값을 참조하는 동일한 유형의 오류가 발생합니다. 이 오류는 `AttributeError`나 `TypeError`를 발생시키며, 프로그램이 예기치 않게 중단되거나 공격자가 오류 정보를 활용할 수 있습니다.

### 왜 위험한가

바이브 코딩으로 웹 폼(Form) 처리 코드를 생성하면, AI는 `request.POST.get('field_name')`으로 값을 가져온 뒤 바로 문자열 메서드를 호출하는 코드를 만들곤 합니다. 사용자가 해당 필드를 비워두고 전송하면 반환값이 `None`이 되고, `None.strip()`이나 `None.split()` 같은 호출에서 프로그램이 중단됩니다. 공격자는 의도적으로 필수 파라미터를 누락시켜 이러한 예외를 유발하고, 노출되는 에러 메시지에서 시스템 정보를 수집합니다.

### ❌ 취약한 코드

```python
from django.shortcuts import render

def parse_input(request):
    username = request.POST.get('username')
    # username이 None일 경우 AttributeError 발생
    if username.strip() == "":
        return render(request, '/error.html', {'error': '이름을 입력하세요.'})

    # 이후 처리 로직
    return render(request, '/success.html', {'name': username})
```

`request.POST.get('username')`은 해당 키가 없으면 `None`을 반환합니다. `None` 객체에 `.strip()`을 호출하면 `AttributeError: 'NoneType' object has no attribute 'strip'`이 발생합니다.

### ✅ 안전한 코드

```python
from django.shortcuts import render

def parse_input(request):
    username = request.POST.get('username')

    # None 체크를 먼저 수행
    if username is None or username.strip() == "":
        return render(request, '/error.html', {'error': '이름을 입력하세요.'})

    # 안전하게 사용 가능
    username = username.strip()
    return render(request, '/success.html', {'name': username})
```

`is None` 검사를 먼저 수행하고, 파이썬의 단축 평가(Short-circuit Evaluation) 덕분에 `username`이 `None`이면 `or` 뒤의 `.strip()` 호출은 실행되지 않습니다.

> **💡 팁:** `request.POST.get('field', '')`처럼 기본값을 빈 문자열로 지정하면 `None` 반환을 원천적으로 방지할 수 있습니다. JavaScript/TypeScript에서는 옵셔널 체이닝(Optional Chaining) `?.` 연산자를 활용합니다.

---

## 14-2. 부적절한 자원 해제

### 개요

파일 핸들(File Handle), 데이터베이스 연결(Database Connection), 네트워크 소켓(Socket) 등은 유한한 시스템 자원입니다. 사용이 끝난 자원을 적절히 반환하지 않으면 자원이 고갈되어 프로그램이 새로운 요청을 처리할 수 없게 됩니다. 이를 부적절한 자원 해제(Improper Resource Shutdown or Release)라고 합니다.

### 왜 위험한가

AI가 생성한 코드에서 파일을 열고 `close()`를 호출하는 패턴은 흔합니다. 하지만 `open()`과 `close()` 사이에서 예외가 발생하면 `close()`가 실행되지 않습니다. 웹 서버에서 이 패턴이 반복되면 열린 파일 핸들이 계속 쌓여 운영체제의 파일 디스크립터(File Descriptor) 한도에 도달하고, 새로운 파일을 열거나 새로운 네트워크 연결을 받을 수 없는 상태가 됩니다. 데이터베이스 연결도 마찬가지로, 연결 풀(Connection Pool)이 고갈되면 전체 서비스가 마비됩니다.

### ❌ 취약한 코드

```python
def get_config():
    lines = None
    try:
        f = open('config.cfg')
        lines = f.readlines()
        # 여기서 예외가 발생하면 f.close()가 실행되지 않음
        process_data(lines)
        f.close()  # 예외 발생 시 도달 불가
        return lines
    except Exception as e:
        return ''
```

`process_data(lines)`에서 예외가 발생하면 `f.close()`는 실행되지 않고, 파일 핸들이 반환되지 않은 채 남게 됩니다.

### ✅ 안전한 코드

**방법 1: `with` 문 사용 (권장)**

```python
def get_config():
    try:
        # with 문이 블록 종료 시 자동으로 파일을 닫아줌
        with open('config.cfg') as f:
            lines = f.readlines()
            process_data(lines)
            return lines
    except FileNotFoundError:
        logging.error("설정 파일을 찾을 수 없습니다.")
        return ''
    except Exception as e:
        logging.error(f"설정 파일 처리 중 오류: {e}")
        return ''
```

**방법 2: `finally` 블록 사용**

```python
def get_config():
    f = None
    try:
        f = open('config.cfg')
        lines = f.readlines()
        return lines
    except Exception as e:
        logging.error(f"오류 발생: {e}")
        return ''
    finally:
        # 예외 발생 여부와 관계없이 항상 실행
        if f is not None:
            f.close()
```

**데이터베이스 연결 — 컨텍스트 매니저(Context Manager) 활용**

```python
import sqlite3

def get_user(user_id):
    # with 문으로 커넥션과 커서 모두 자동 관리
    with sqlite3.connect('app.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()
```

> **💡 팁:** 파이썬의 `with` 문(컨텍스트 매니저, Context Manager)은 자원 해제를 자동으로 보장합니다. 파일, 데이터베이스 연결, 네트워크 소켓 등 `close()`가 필요한 모든 자원에 `with` 문을 사용하는 것을 습관으로 만드십시오.

---

## 14-3. 신뢰할 수 없는 데이터의 역직렬화

### 개요

직렬화(Serialization)는 객체의 상태를 바이트 스트림(Byte Stream)으로 변환하는 과정이며, 역직렬화(Deserialization)는 그 반대 과정입니다. 파이썬의 `pickle` 모듈은 편리한 직렬화 도구이지만, 역직렬화 과정에서 임의 코드 실행(Arbitrary Code Execution)이 가능한 심각한 보안 위험을 내포하고 있습니다.

### 왜 위험한가

`pickle.loads()`는 바이트 스트림을 객체로 복원하면서 `__reduce__` 메서드를 호출합니다. 공격자는 이를 악용하여 `os.system("rm -rf /")` 같은 악성 명령을 포함한 pickle 데이터를 구성할 수 있습니다. AI가 "객체를 파일에 저장하고 불러오는 코드를 만들어줘"라고 요청받으면 가장 먼저 `pickle`을 사용하는 코드를 생성하는 경향이 있어 매우 주의가 필요합니다.

실제 공격 시나리오를 살펴보면, 사용자가 업로드한 파일이나 쿠키, API 요청 본문(Body)에 악의적으로 조작된 pickle 데이터가 포함될 수 있습니다. 서버가 이를 `pickle.loads()`로 역직렬화하는 순간 공격자의 코드가 서버에서 실행됩니다.

### ❌ 취약한 코드

```python
import pickle
from django.shortcuts import render

def load_user_object(request):
    # 사용자 입력을 직접 pickle로 역직렬화 — 원격 코드 실행 위험
    user_data = request.POST.get('userinfo', '')
    user_obj = pickle.loads(user_data.encode())
    return render(request, '/profile.html', {'user': user_obj})
```

사용자가 전송한 데이터를 검증 없이 `pickle.loads()`로 역직렬화하고 있습니다. 공격자는 서버에서 임의 명령을 실행할 수 있습니다.

### ✅ 안전한 코드

**방법 1: JSON 사용 (권장)**

```python
import json
from django.shortcuts import render

def load_user_object(request):
    try:
        # JSON은 데이터만 파싱하므로 코드 실행 위험 없음
        user_data = request.POST.get('userinfo', '{}')
        user_obj = json.loads(user_data)
        return render(request, '/profile.html', {'user': user_obj})
    except json.JSONDecodeError:
        return render(request, '/error.html', {'error': '잘못된 데이터 형식입니다.'})
```

**방법 2: HMAC 서명 검증 후 역직렬화 (pickle이 반드시 필요한 경우)**

```python
import hmac
import hashlib
import pickle
import os
from django.shortcuts import render

SECRET_KEY = os.environ.get('PICKLE_SECRET_KEY')

def load_user_object(request):
    received_signature = request.POST.get('signature', '')
    pickled_data = request.POST.get('userinfo', '').encode()

    # HMAC으로 데이터 무결성 검증
    expected_signature = hmac.new(
        SECRET_KEY.encode(), pickled_data, hashlib.sha256
    ).hexdigest()

    if hmac.compare_digest(expected_signature, received_signature):
        user_obj = pickle.loads(pickled_data)
        return render(request, '/profile.html', {'user': user_obj})
    else:
        return render(request, '/error.html', {'error': '데이터 검증에 실패했습니다.'})
```

> **⚠️ 주의:** 파이썬 공식 문서에도 명시되어 있듯이, `pickle` 모듈은 **신뢰할 수 없는 데이터에 대해 안전하지 않습니다**. 외부 입력 데이터에는 반드시 `json.loads()`를 사용하고, 내부 시스템 간 통신에서 `pickle`이 꼭 필요한 경우에만 HMAC 서명 검증과 함께 사용해야 합니다.

### 바이브 코딩 시 체크포인트

| 점검 항목 | 확인 방법 |
|-----------|-----------|
| `None` 체크 누락 | `request.POST.get()`, `request.GET.get()` 반환값 사용 전 `is None` 검사 여부 |
| 기본값 미설정 | `.get('key')` 대신 `.get('key', '')` 사용 여부 확인 |
| `with` 문 사용 | 파일, DB 연결, 소켓 등에 `with` 문 사용 여부 확인 |
| `close()` 누락 | `finally` 블록 없이 `open()` 후 `close()`를 호출하는 패턴 검색 |
| `pickle.loads()` 사용 | 코드베이스에서 `pickle` 모듈 사용 검색, 외부 데이터 역직렬화 여부 확인 |
| JSON 대체 가능성 | `pickle` 대신 `json` 모듈로 대체할 수 있는지 검토 |
| DB 연결 풀 설정 | Django `CONN_MAX_AGE` 또는 SQLAlchemy 풀 설정 확인 |
