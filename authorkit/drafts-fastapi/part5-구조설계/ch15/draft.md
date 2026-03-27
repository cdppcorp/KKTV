# Chapter 15. 캡슐화 — 보여서는 안 되는 것들

캡슐화(Encapsulation)란 데이터와 기능을 적절히 감싸서 외부에 불필요하게 노출되지 않도록 하는 설계 원칙입니다. 이 원칙이 깨지면 서로 다른 사용자의 데이터가 섞이거나, 개발 과정의 흔적이 운영 환경에 그대로 남아 공격의 단서가 됩니다. FastAPI 기반 바이브 코딩에서 특히 주의해야 할 두 가지 캡슐화 문제를 다루겠습니다.

---

## 15-1. 잘못된 세션에 의한 데이터 정보 노출

### 개요

비동기(Async) 환경에서 모듈 수준 변수나 클래스 변수(Class Variable)에 사용자별 데이터를 저장하면, 서로 다른 세션(Session) 간에 데이터가 공유되는 문제가 발생합니다. 이를 잘못된 세션에 의한 데이터 정보 노출(Exposure of Data Element to Wrong Session)이라고 합니다.

### 왜 위험한가

FastAPI는 단일 프로세스 내에서 여러 요청을 비동기적으로 처리합니다. AI가 생성한 코드에서 모듈 수준 변수에 사용자 정보를 저장하면, 사용자 A의 요청을 처리하는 중 `await` 지점에서 사용자 B의 요청이 같은 변수를 덮어쓸 수 있습니다. 그 결과 사용자 A가 사용자 B의 개인정보를 보게 되는 심각한 개인정보 유출 사고가 발생합니다.

이 문제는 특히 AI가 간단한 클래스 구조를 생성할 때 빈번하게 나타납니다. AI는 데이터를 모듈 수준이나 클래스 수준에 선언하는 것이 편리하다고 판단하지만, 비동기 환경에서의 부작용까지는 고려하지 못하는 경우가 많습니다.

### ❌ 취약한 코드

```python
from fastapi import FastAPI, Request

app = FastAPI()

# 모듈 수준 변수 — 모든 요청이 공유
current_user_name = ""

class UserService:
    # 클래스 변수 — 모든 인스턴스와 요청이 공유
    user_name = ""

    def get_user_profile(self):
        result = self.get_user_description(UserService.user_name)
        return result

service = UserService()

@app.post("/profile")
async def show_user_profile(request: Request):
    form = await request.form()
    # 모듈 수준 변수에 사용자별 데이터를 저장 — 요청 간 데이터 오염
    global current_user_name
    current_user_name = form.get("name", "")

    # 클래스 변수에도 동일한 문제
    UserService.user_name = current_user_name

    # await 시점에서 다른 요청이 current_user_name을 덮어쓸 수 있음
    profile = await fetch_profile_from_db(current_user_name)
    return {"profile": profile}
```

`current_user_name`은 모듈 수준 변수이고 `UserService.user_name`은 클래스 변수이므로 모든 요청에서 공유됩니다. 동시에 두 사용자가 이 엔드포인트에 접근하면 한 사용자의 이름이 다른 사용자의 프로필 조회에 사용될 수 있습니다.

### ✅ 안전한 코드

**방법 1: 함수 기반 엔드포인트 — 지역 변수 사용**

```python
from fastapi import FastAPI, Form

app = FastAPI()

# 함수 기반 엔드포인트 — 각 요청이 독립적인 지역 변수를 사용
@app.post("/profile")
async def show_user_profile(name: str = Form(...)):
    # 지역 변수는 요청마다 독립적
    profile = await fetch_profile_from_db(name)
    return {"profile": profile}
```

**방법 2: Depends()를 활용한 의존성 주입**

```python
from fastapi import FastAPI, Depends, Form

app = FastAPI()

class UserService:
    """요청마다 새로운 인스턴스가 생성되어 데이터 격리 보장"""
    def __init__(self, user_name: str):
        # 인스턴스 변수 — 요청마다 독립적
        self.user_name = user_name

    async def get_profile(self):
        return await fetch_profile_from_db(self.user_name)

# Depends()로 요청마다 새로운 서비스 인스턴스 생성
async def get_user_service(name: str = Form(...)) -> UserService:
    return UserService(user_name=name)

@app.post("/profile")
async def show_user_profile(service: UserService = Depends(get_user_service)):
    profile = await service.get_profile()
    return {"profile": profile}
```

FastAPI의 `Depends()`를 사용하면 요청마다 새로운 인스턴스가 생성되어 데이터가 자연스럽게 격리됩니다. 클래스 변수 대신 인스턴스 변수를 사용하고, 의존성 주입 패턴을 활용하면 스레드 안전성 문제를 원천적으로 방지할 수 있습니다.

> **💡 팁:** FastAPI에서는 `Depends()`를 활용한 의존성 주입이 가장 안전한 패턴입니다. 사용자별 데이터는 반드시 함수의 지역 변수나 `Depends()`로 주입된 인스턴스에 보관하십시오. 모듈 수준 변수에는 설정값이나 상수만 저장해야 합니다.

---

## 15-2. 제거되지 않고 남은 디버그 코드

### 개요

개발 과정에서 삽입한 디버그 코드(Debug Code)가 운영 환경에 그대로 배포되는 것은 가장 흔하면서도 가장 위험한 보안약점 중 하나입니다. `print()` 문, `console.log()`, 디버그용 API 엔드포인트(Endpoint), 하드코딩된 테스트 계정 등이 여기에 해당합니다.

### 왜 위험한가

**이 항목은 바이브 코딩에서 특히 높은 우선순위로 점검해야 합니다.** AI 코드 생성 도구는 생성한 코드의 동작을 보여주기 위해 `print()` 문을 자주 포함합니다. 또한 "테스트 계정을 추가해줘", "디버그 모드를 켜줘" 같은 개발 중 요청에 응답하면서 생성된 코드가 최종 배포본에 남아 있는 경우가 많습니다.

디버그 코드가 남아 있으면 다음과 같은 위험이 발생합니다:

1. **`print()` 문의 민감 정보 노출**: 사용자 비밀번호, API 키, 데이터베이스 쿼리 등이 서버 로그에 평문으로 기록됩니다. 로그 파일이 유출되면 대규모 정보 유출로 이어집니다.
2. **`console.log()`의 클라이언트 정보 노출**: 브라우저 개발자 도구에서 누구나 확인할 수 있습니다. 인증 토큰(Token), 사용자 ID, 내부 API 경로 등이 노출됩니다.
3. **디버그 엔드포인트 방치**: `/debug`, `/test`, `/admin-backdoor` 같은 테스트용 URL이 남아 있으면 공격자가 인증 없이 시스템 내부에 접근할 수 있습니다.
4. **FastAPI 디버그 모드**: `FastAPI(debug=True)` 상태에서는 상세한 에러 정보가 API 응답에 포함되어 시스템 내부 구조가 노출됩니다.

### ❌ 취약한 코드

**Python 백엔드 — FastAPI**

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# 디버그 모드 활성화
app = FastAPI(debug=True)

@app.post("/login")
async def login(username: str, password: str):
    # 디버그용 출력 — 비밀번호가 서버 로그에 기록됨
    print(f"[DEBUG] 로그인 시도: {username} / {password}")

    user = await authenticate(username=username, password=password)
    if user:
        return {"status": "ok"}
    return {"status": "fail"}

# 테스트용 엔드포인트 — 배포 시 제거 필요
@app.get("/debug/users")
async def debug_user_list():
    users = await get_all_users()
    return [{"username": u.username, "email": u.email, "is_staff": u.is_staff} for u in users]
```

**JavaScript 프론트엔드**

```javascript
// 인증 토큰이 브라우저 콘솔에 노출
async function fetchUserData() {
    const token = localStorage.getItem('auth_token');
    console.log('DEBUG: auth token =', token);
    console.log('DEBUG: API endpoint =', '/api/v2/internal/users');

    const response = await fetch('/api/v2/internal/users', {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.json();
}
```

### ✅ 안전한 코드

**Python 백엔드 — FastAPI**

```python
import os
import logging
from fastapi import FastAPI

logger = logging.getLogger(__name__)

# 프로덕션 환경에서는 debug=False
app = FastAPI(debug=False)

@app.post("/login")
async def login(username: str, password: str):
    # 로그에 비밀번호를 절대 포함하지 않음
    logger.info(f"로그인 시도: {username}")

    user = await authenticate(username=username, password=password)
    if user:
        logger.info(f"로그인 성공: {username}")
        return {"status": "ok"}

    logger.warning(f"로그인 실패: {username}")
    return {"status": "fail"}

# debug_user_list 엔드포인트 완전 제거
```

**FastAPI 미들웨어로 디버그 경로 차단**

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(debug=False)

# 프로덕션 환경에서 디버그 경로 접근 차단 미들웨어
@app.middleware("http")
async def block_debug_routes(request: Request, call_next):
    blocked_prefixes = ["/debug", "/test", "/admin-backdoor"]
    for prefix in blocked_prefixes:
        if request.url.path.startswith(prefix):
            return JSONResponse(
                status_code=404,
                content={"detail": "Not Found"}
            )
    response = await call_next(request)
    return response
```

**JavaScript 프론트엔드**

```javascript
async function fetchUserData() {
    const token = localStorage.getItem('auth_token');
    // console.log 제거 — 민감 정보를 클라이언트에 노출하지 않음

    const response = await fetch('/api/v2/internal/users', {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.json();
}
```

**FastAPI 프로덕션 배포 명령**

```bash
# 프로덕션 환경 — Gunicorn + Uvicorn Worker 조합 권장
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# --reload 옵션은 절대 프로덕션에서 사용하지 않음
# uvicorn main:app --reload  # 개발 전용
```

> **⚠️ 주의:** 배포 전 다음 키워드로 코드베이스를 반드시 검색하십시오: `print(`, `console.log(`, `debug=True`, `FastAPI(debug=True)`, `/debug`, `/test`, `TODO`, `FIXME`, `HACK`. CI/CD 파이프라인(Pipeline)에 이 검사를 자동화하면 실수로 디버그 코드가 배포되는 것을 방지할 수 있습니다.

### 바이브 코딩 시 체크포인트

| 점검 항목 | 확인 방법 |
|-----------|-----------|
| 모듈 수준 변수에 사용자 데이터 저장 여부 | `global` 키워드 사용 여부, 모듈 수준 변수에 요청별 데이터 저장 여부 확인 |
| 클래스 변수 사용 | 클래스 정의에서 사용자별 데이터가 클래스 변수로 선언되어 있는지 확인 |
| `Depends()` 활용 | 사용자별 서비스가 `Depends()`로 요청마다 새로 생성되는지 확인 |
| `print()` 문 잔존 여부 | 코드베이스 전체에서 `print(` 검색, 특히 비밀번호, 토큰, 키 관련 출력 |
| `console.log()` 잔존 여부 | JavaScript 파일에서 `console.log(` 검색 |
| `debug=True` 설정 | `FastAPI(debug=True)`, `uvicorn --reload` 인자 확인 |
| 디버그 엔드포인트 | URL 라우팅에서 `/debug`, `/test`, `/admin-backdoor` 등 테스트용 경로 확인 |
| 하드코딩된 테스트 계정 | 코드에서 `test@`, `admin/admin`, `password123` 등 검색 |
| CI/CD 자동 검사 | 배포 파이프라인에 디버그 코드 탐지 스크립트 포함 여부 |

---

> **📦 기타 캡슐화 이슈**
>
> 이 장에서 다루지 않은 캡슐화 관련 보안약점으로 **Public 메소드로부터 반환된 Private 배열**과 **Private 배열에 Public 데이터 할당** 문제가 있습니다. 파이썬에서는 이름 앞에 이중 밑줄(`__`)을 붙여 private 변수를 표시하는 관례를 사용합니다. private 배열을 public 메서드에서 직접 반환하면 외부에서 원본 배열을 수정할 수 있으므로, 슬라이싱(`return self.__data[:]`)이나 `copy.deepcopy()`를 사용하여 복사본을 반환해야 합니다. 마찬가지로, 외부 데이터를 private 배열에 대입할 때도 `self.__data = input_list[:]`처럼 복사본을 저장하여 외부 참조와의 연결을 끊어야 합니다. 바이브 코딩에서는 AI가 생성한 클래스 코드에서 mutable 객체(리스트, 딕셔너리)의 참조 공유 문제를 반드시 점검하십시오.
