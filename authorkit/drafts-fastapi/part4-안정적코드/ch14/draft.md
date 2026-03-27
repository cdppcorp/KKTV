# Chapter 14. 코드 오류 — 개발자가 놓치기 쉬운 함정들

완벽해 보이는 코드에도 미묘한 오류가 숨어 있을 수 있습니다. 변수가 `None`인지 확인하지 않거나, 파일이나 데이터베이스 연결을 제대로 닫지 않거나, 외부에서 전달된 데이터를 검증 없이 역직렬화하는 것은 모두 심각한 보안 사고로 이어질 수 있는 코드 오류(Code Quality)입니다. AI가 생성한 코드에서 특히 자주 발견되는 세 가지 패턴을 FastAPI 환경에서 살펴보겠습니다.

---

## 14-1. Null Pointer 역참조

### 개요

Null Pointer 역참조(Null Pointer Dereference)는 객체가 존재하지 않는 상태, 즉 `None` 상태에서 해당 객체의 속성이나 메서드에 접근하려 할 때 발생합니다. 파이썬에서는 C/C++과 같은 포인터 개념이 없지만, `None` 값을 참조하는 동일한 유형의 오류가 발생합니다. 이 오류는 `AttributeError`나 `TypeError`를 발생시키며, 프로그램이 예기치 않게 중단되거나 공격자가 오류 정보를 활용할 수 있습니다.

### 왜 위험한가

바이브 코딩으로 API 엔드포인트를 생성하면, AI는 쿼리 파라미터(Query Parameter)나 요청 본문(Request Body)에서 값을 가져온 뒤 바로 문자열 메서드를 호출하는 코드를 만들곤 합니다. 선택적 파라미터에 값이 전달되지 않으면 `None`이 되고, `None.strip()`이나 `None.split()` 같은 호출에서 프로그램이 중단됩니다. 공격자는 의도적으로 필수 파라미터를 누락시켜 이러한 예외를 유발하고, 노출되는 에러 메시지에서 시스템 정보를 수집합니다.

### ❌ 취약한 코드

```python
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/search")
async def parse_input(username: str = Query(default=None)):
    # username이 None일 경우 AttributeError 발생
    if username.strip() == "":
        return {"error": "이름을 입력하세요."}

    # 이후 처리 로직
    return {"name": username}
```

`username` 파라미터에 기본값이 `None`으로 설정되어 있으므로, 쿼리 파라미터 없이 요청하면 `None` 객체에 `.strip()`을 호출하여 `AttributeError: 'NoneType' object has no attribute 'strip'`이 발생합니다.

### ✅ 안전한 코드

**방법 1: `Optional[]` 타입 힌트와 명시적 None 체크**

```python
from typing import Optional
from fastapi import FastAPI, Query, HTTPException

app = FastAPI()

@app.get("/search")
async def parse_input(username: Optional[str] = Query(default=None)):
    # None 체크를 먼저 수행
    if username is None or username.strip() == "":
        raise HTTPException(status_code=400, detail="이름을 입력하세요.")

    # 안전하게 사용 가능
    username = username.strip()
    return {"name": username}
```

**방법 2: Pydantic 모델로 검증 자동화 (권장)**

```python
from pydantic import BaseModel, field_validator
from fastapi import FastAPI

app = FastAPI()

class UserInput(BaseModel):
    username: str  # 필수 필드 — None이면 자동으로 422 반환

    @field_validator("username")
    @classmethod
    def username_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("이름은 빈 문자열일 수 없습니다.")
        return v.strip()

@app.post("/search")
async def parse_input(user_input: UserInput):
    # Pydantic이 검증을 완료한 안전한 데이터
    return {"name": user_input.username}
```

Pydantic 모델을 사용하면 `None` 체크와 데이터 검증이 자동으로 이루어집니다. 필수 필드에 값이 없으면 FastAPI가 자동으로 422 응답을 반환하므로 `None` 역참조가 원천적으로 방지됩니다.

> **💡 팁:** FastAPI에서는 Pydantic 모델을 적극 활용하여 입력 검증을 선언적으로 처리하는 것이 가장 안전합니다. `Optional[str]`을 사용할 때는 반드시 `is None` 검사를 동반하고, 가능하면 필수 필드로 선언하여 `None` 자체를 방지하십시오.

---

## 14-2. 부적절한 자원 해제

### 개요

파일 핸들(File Handle), 데이터베이스 연결(Database Connection), HTTP 클라이언트 세션 등은 유한한 시스템 자원입니다. 사용이 끝난 자원을 적절히 반환하지 않으면 자원이 고갈되어 프로그램이 새로운 요청을 처리할 수 없게 됩니다. 이를 부적절한 자원 해제(Improper Resource Shutdown or Release)라고 합니다.

### 왜 위험한가

AI가 생성한 코드에서 파일을 열고 `close()`를 호출하는 패턴은 흔합니다. 하지만 `open()`과 `close()` 사이에서 예외가 발생하면 `close()`가 실행되지 않습니다. FastAPI의 비동기 환경에서는 HTTP 클라이언트(`httpx.AsyncClient`)와 데이터베이스 세션을 비동기적으로 관리해야 하므로, 자원 누수(Resource Leak) 문제가 더욱 빈번하게 발생합니다. 연결 풀(Connection Pool)이 고갈되면 전체 서비스가 마비됩니다.

### ❌ 취약한 코드

```python
import httpx
from fastapi import FastAPI

app = FastAPI()

@app.get("/proxy")
async def proxy_request(url: str):
    client = httpx.AsyncClient()
    try:
        response = await client.get(url, timeout=5)
        # 여기서 예외가 발생하면 client.aclose()가 실행되지 않음
        data = response.json()
        await client.aclose()  # 예외 발생 시 도달 불가
        return data
    except Exception:
        return {"error": "요청 실패"}
        # client가 닫히지 않은 채 남게 됨
```

`response.json()`에서 예외가 발생하면 `await client.aclose()`는 실행되지 않고, HTTP 연결이 반환되지 않은 채 남게 됩니다.

### ✅ 안전한 코드

**방법 1: `async with` 문 사용 (권장)**

```python
import httpx
import logging
from fastapi import FastAPI

logger = logging.getLogger(__name__)
app = FastAPI()

@app.get("/proxy")
async def proxy_request(url: str):
    try:
        # async with 문이 블록 종료 시 자동으로 클라이언트를 닫아줌
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5)
            return response.json()
    except httpx.TimeoutException:
        logger.warning(f"프록시 요청 타임아웃: {url}")
        return {"error": "요청 시간이 초과되었습니다."}
    except Exception as e:
        logger.error(f"프록시 요청 중 오류: {e}")
        return {"error": "일시적인 오류가 발생했습니다."}
```

**방법 2: FastAPI 의존성 주입으로 데이터베이스 세션 관리**

```python
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

app = FastAPI()

engine = create_async_engine("sqlite+aiosqlite:///app.db")
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Depends()로 세션 생명주기를 자동 관리
async def get_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    # db 세션은 요청 종료 시 자동으로 닫힘
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()
```

**방법 3: FastAPI Lifespan으로 전역 자원 관리**

```python
from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 애플리케이션 시작 시 전역 HTTP 클라이언트 생성
    app.state.http_client = httpx.AsyncClient()
    yield
    # 애플리케이션 종료 시 자동 정리
    await app.state.http_client.aclose()

app = FastAPI(lifespan=lifespan)

@app.get("/proxy")
async def proxy_request(url: str):
    response = await app.state.http_client.get(url, timeout=5)
    return response.json()
```

> **💡 팁:** FastAPI의 비동기 환경에서는 `async with` 문(비동기 컨텍스트 매니저)을 사용하여 자원 해제를 자동으로 보장하십시오. 데이터베이스 세션은 `Depends()`를 통해, 전역 자원은 `lifespan`을 통해 생명주기를 관리하는 것이 가장 안전합니다.

---

## 14-3. 신뢰할 수 없는 데이터의 역직렬화

### 개요

직렬화(Serialization)는 객체의 상태를 바이트 스트림(Byte Stream)으로 변환하는 과정이며, 역직렬화(Deserialization)는 그 반대 과정입니다. 파이썬의 `pickle` 모듈은 편리한 직렬화 도구이지만, 역직렬화 과정에서 임의 코드 실행(Arbitrary Code Execution)이 가능한 심각한 보안 위험을 내포하고 있습니다.

### 왜 위험한가

`pickle.loads()`는 바이트 스트림을 객체로 복원하면서 `__reduce__` 메서드를 호출합니다. 공격자는 이를 악용하여 `os.system("rm -rf /")` 같은 악성 명령을 포함한 pickle 데이터를 구성할 수 있습니다. AI가 "객체를 파일에 저장하고 불러오는 코드를 만들어줘"라고 요청받으면 가장 먼저 `pickle`을 사용하는 코드를 생성하는 경향이 있어 매우 주의가 필요합니다.

실제 공격 시나리오를 살펴보면, API 요청 본문(Body)에 악의적으로 조작된 pickle 데이터가 포함될 수 있습니다. 서버가 이를 `pickle.loads()`로 역직렬화하는 순간 공격자의 코드가 서버에서 실행됩니다.

### ❌ 취약한 코드

```python
import pickle
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/profile")
async def load_user_object(request: Request):
    # 사용자 입력을 직접 pickle로 역직렬화 — 원격 코드 실행 위험
    body = await request.body()
    user_obj = pickle.loads(body)
    return {"user": str(user_obj)}
```

사용자가 전송한 데이터를 검증 없이 `pickle.loads()`로 역직렬화하고 있습니다. 공격자는 서버에서 임의 명령을 실행할 수 있습니다.

### ✅ 안전한 코드

**방법 1: Pydantic 모델 사용 (권장)**

```python
from pydantic import BaseModel, EmailStr
from fastapi import FastAPI

app = FastAPI()

class UserProfile(BaseModel):
    username: str
    email: EmailStr
    age: int

@app.post("/profile")
async def load_user_object(user: UserProfile):
    # Pydantic이 자동으로 JSON 파싱 및 타입 검증 수행
    # 코드 실행 위험 없음
    return {"user": user.model_dump()}
```

**방법 2: HMAC 서명 검증 후 역직렬화 (pickle이 반드시 필요한 경우)**

```python
import hmac
import hashlib
import pickle
import os
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()
SECRET_KEY = os.environ.get('PICKLE_SECRET_KEY', '').encode()

@app.post("/internal/data")
async def load_internal_data(request: Request):
    signature = request.headers.get('X-Signature', '')
    body = await request.body()

    # HMAC으로 데이터 무결성 검증
    expected_signature = hmac.new(
        SECRET_KEY, body, hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected_signature, signature):
        raise HTTPException(status_code=403, detail="데이터 검증에 실패했습니다.")

    data = pickle.loads(body)
    return {"data": str(data)}
```

> **⚠️ 주의:** 파이썬 공식 문서에도 명시되어 있듯이, `pickle` 모듈은 **신뢰할 수 없는 데이터에 대해 안전하지 않습니다**. FastAPI에서는 Pydantic 모델을 활용하면 JSON 기반의 안전한 역직렬화가 자동으로 이루어집니다. 외부 입력 데이터에는 반드시 Pydantic 모델이나 `json.loads()`를 사용하고, 내부 시스템 간 통신에서 `pickle`이 꼭 필요한 경우에만 HMAC 서명 검증과 함께 사용해야 합니다.

### 바이브 코딩 시 체크포인트

| 점검 항목 | 확인 방법 |
|-----------|-----------|
| `None` 체크 누락 | `Optional[]` 타입 파라미터 사용 시 `is None` 검사 여부 |
| Pydantic 모델 활용 | 요청 본문을 `dict`가 아닌 Pydantic 모델로 받고 있는지 확인 |
| `async with` 문 사용 | httpx 클라이언트, DB 세션, 파일 등에 비동기 컨텍스트 매니저 사용 여부 확인 |
| `Depends()` 세션 관리 | 데이터베이스 세션이 `Depends()`로 주입되어 자동 정리되는지 확인 |
| `pickle.loads()` 사용 | 코드베이스에서 `pickle` 모듈 사용 검색, 외부 데이터 역직렬화 여부 확인 |
| Pydantic 대체 가능성 | `pickle` 또는 수동 JSON 파싱 대신 Pydantic 모델로 대체할 수 있는지 검토 |
| Lifespan 자원 관리 | 전역 HTTP 클라이언트나 DB 엔진이 `lifespan`으로 정리되는지 확인 |
