# Chapter 13. 에러 처리 — 오류가 보안 구멍이 되는 순간

프로그램에 오류가 발생하는 것은 자연스러운 일입니다. 문제는 그 오류를 어떻게 처리하느냐에 있습니다. 오류 메시지에 시스템 내부 정보가 담겨 외부에 노출되거나, 오류를 아예 무시해버리면 공격자에게 침투 경로를 열어주는 결과를 초래합니다. 이 장에서는 FastAPI 환경에서의 에러 처리(Error Handling) 관련 보안약점 세 가지를 다루겠습니다.

---

## 13-1. 오류 메시지 정보 노출

### 개요

응용 프로그램이 오류를 처리할 때, 예외 이름이나 추적 메시지(Traceback), 서버 환경 정보를 그대로 사용자에게 보여주면 공격자가 시스템 내부 구조를 파악하는 데 활용할 수 있습니다. 이를 오류 메시지 정보 노출(Information Exposure Through Error Message)이라고 합니다.

### 왜 위험한가

바이브 코딩으로 API를 만들 때, AI는 개발 편의를 위해 디버그 모드를 활성화한 상태로 코드를 생성하는 경우가 많습니다. FastAPI의 `debug=True` 설정은 개발 중에는 유용하지만, 이 상태로 배포하면 오류 발생 시 상세한 스택 트레이스(Stack Trace)가 API 응답에 포함됩니다. 공격자는 이 정보를 기반으로 SQL 인젝션(SQL Injection), 경로 조작(Path Traversal) 등 후속 공격을 설계합니다.

### ❌ 취약한 코드

**FastAPI 디버그 모드 활성화**

```python
import traceback
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# 디버그 모드 활성화 — 배포 시 반드시 변경 필요
app = FastAPI(debug=True)

@app.get("/fetch")
async def fetch_url(url: str):
    try:
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5)
            return {"content": response.text}
    except Exception as e:
        # 스택 트레이스를 그대로 응답에 포함 — 내부 경로와 코드 구조 노출
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )
```

`traceback.format_exc()`는 파일 경로, 함수명, 줄 번호 등 프로그램 내부 구조를 상세히 포함합니다. 이 정보가 API 응답으로 외부에 그대로 전달됩니다.

### ✅ 안전한 코드

**FastAPI 프로덕션 설정과 커스텀 예외 핸들러**

```python
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

# 프로덕션 환경에서는 debug=False
app = FastAPI(debug=False)

# 전역 예외 핸들러 — 모든 처리되지 않은 예외를 안전하게 처리
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # 내부 로그에만 상세 정보 기록
    logger.error(
        f"처리되지 않은 예외 발생: {request.method} {request.url}",
        exc_info=True
    )
    # 사용자에게는 최소 정보만 전달
    return JSONResponse(
        status_code=500,
        content={"detail": "일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요."}
    )

# HTTP 404 커스텀 핸들러
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": "요청을 처리할 수 없습니다."}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"요청 검증 실패: {request.url}")
    return JSONResponse(
        status_code=422,
        content={"detail": "입력 데이터 형식이 올바르지 않습니다."}
    )
```

**안전한 외부 통신 처리**

```python
import logging
import httpx
from fastapi import FastAPI

logger = logging.getLogger(__name__)
app = FastAPI(debug=False)

@app.get("/fetch")
async def fetch_url(url: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5)
            return {"content": response.text}
    except httpx.TimeoutException:
        logger.warning(f"외부 URL 타임아웃: {url}")
        return {"error": "요청 시간이 초과되었습니다."}
    except httpx.RequestError:
        logger.error("외부 URL 통신 에러 발생", exc_info=True)
        return {"error": "일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요."}
```

`logging` 모듈을 사용하면 상세한 에러 정보는 서버 로그 파일에만 기록되고, 사용자에게는 안전한 메시지만 보여줍니다.

> **💡 팁:** FastAPI에서도 배포 시 반드시 `FastAPI(debug=False)`로 설정하고, 프로덕션 환경에서는 Uvicorn을 `--no-access-log` 옵션과 함께 실행하거나 Gunicorn + Uvicorn Worker 조합을 사용해야 합니다. `uvicorn main:app --reload` 개발 서버는 절대 운영 환경에서 사용하지 마십시오.

---

## 13-2. 오류 상황 대응 부재

### 개요

오류가 발생할 수 있는 부분을 `try-except`로 감싸놓았지만, `except` 블록에서 아무런 조치도 취하지 않는 것을 오류 상황 대응 부재(Detection of Error Condition Without Action)라고 합니다. 이른바 "조용한 실패(Silent Failure)"입니다.

### 왜 위험한가

AI 코드 생성 도구는 에러를 피하기 위해 빈 `except` 블록이나 `pass` 문을 생성하는 경향이 있습니다. 코드가 에러 없이 실행되는 것처럼 보이지만, 실제로는 중요한 오류가 무시된 채 프로그램이 비정상적인 상태로 계속 실행됩니다. 예를 들어, 암호화 키 선택에서 오류가 발생했는데 이를 무시하면 기본값인 취약한 키로 암호화가 수행되어 데이터가 사실상 보호되지 않는 상황이 발생합니다.

### ❌ 취약한 코드

```python
from Crypto.Cipher import AES
from fastapi import FastAPI

app = FastAPI()

static_keys = [
    {'key': b'secure_key_00001', 'iv': b'secure_iv_000001'},
    {'key': b'secure_key_00002', 'iv': b'secure_iv_000002'},
]

@app.post("/encrypt")
async def encrypt_data(key_id: int, plain_text: str):
    # 기본값이 매우 취약한 키
    static_key = {'key': b'0000000000000000', 'iv': b'0000000000000000'}
    try:
        static_key = static_keys[key_id]
    except IndexError:
        # 오류를 무시하고 취약한 기본 키로 암호화 진행
        pass

    cipher = AES.new(static_key['key'], AES.MODE_CBC, static_key['iv'])
    # ... 암호화 수행
    return {"status": "encrypted"}
```

`key_id`가 유효하지 않은 경우 `IndexError`가 발생하지만 `pass`로 무시되어, `'0000000000000000'`이라는 예측 가능한 키로 암호화가 수행됩니다.

### ✅ 안전한 코드

```python
import secrets
import logging
from Crypto.Cipher import AES
from fastapi import FastAPI, HTTPException

logger = logging.getLogger(__name__)
app = FastAPI()

static_keys = [
    {'key': b'secure_key_00001', 'iv': b'secure_iv_000001'},
    {'key': b'secure_key_00002', 'iv': b'secure_iv_000002'},
]

@app.post("/encrypt")
async def encrypt_data(key_id: int, plain_text: str):
    try:
        static_key = static_keys[key_id]
    except IndexError:
        # 오류 발생 시 로깅 후 요청 거부
        logger.warning(f"유효하지 않은 key_id 요청: {key_id}")
        raise HTTPException(
            status_code=400,
            detail="유효하지 않은 암호화 키입니다."
        )

    cipher = AES.new(static_key['key'], AES.MODE_CBC, static_key['iv'])
    # ... 암호화 수행
    return {"status": "encrypted"}
```

오류 발생 시 `HTTPException`을 발생시켜 취약한 상태로 처리가 계속되는 것을 방지하고, 로그에 경고를 기록하여 운영자가 문제를 인지할 수 있도록 합니다.

---

## 13-3. 부적절한 예외 처리

### 개요

프로그램에서 발생할 수 있는 다양한 예외를 하나의 광범위한 `except` 절로 처리하는 것을 부적절한 예외 처리(Improper Check for Exceptional Conditions)라고 합니다. `except:` 또는 `except Exception:`으로 모든 예외를 한꺼번에 잡으면 어떤 종류의 오류가 발생했는지 구분할 수 없고, 각 상황에 맞는 적절한 대응이 불가능해집니다.

### 왜 위험한가

바이브 코딩에서 "이 코드에 에러 처리를 추가해줘"라고 요청하면 AI는 편의상 가장 넓은 범위의 예외를 잡는 코드를 생성하곤 합니다. 이렇게 하면 `FileNotFoundError`, `PermissionError`, `ValueError` 등 서로 전혀 다른 원인의 오류가 동일한 방식으로 처리됩니다. 파일이 없는 것과 권한이 없는 것은 원인도 대응 방법도 완전히 다르지만, 광범위한 예외 처리는 이를 구분할 수 없게 만듭니다.

더 위험한 것은 `except: pass` 패턴입니다. `KeyboardInterrupt`나 `SystemExit`같은 시스템 레벨 예외까지 삼켜버려 프로그램을 정상적으로 종료할 수조차 없게 만들 수 있습니다.

### ❌ 취약한 코드

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/config")
async def get_content():
    try:
        f = open('myfile.txt')
        s = f.readline()
        i = int(s.strip())
        return {"value": i}
    except:
        # 파일 없음, 권한 오류, 타입 변환 오류를 모두 동일하게 처리
        return {"error": "Unexpected error"}
```

`except:`는 `BaseException`을 포함한 모든 예외를 잡습니다. 파일이 없는 것인지, 파일 내용이 숫자가 아닌 것인지 구분이 불가능합니다.

### ✅ 안전한 코드

```python
import logging
from fastapi import FastAPI, HTTPException

logger = logging.getLogger(__name__)
app = FastAPI()

@app.get("/config")
async def get_content():
    try:
        # async with + aiofiles 사용으로 비동기 파일 처리
        import aiofiles
        async with aiofiles.open('myfile.txt', mode='r') as f:
            s = await f.readline()
            i = int(s.strip())
            return {"value": i}
    except FileNotFoundError:
        logger.error("설정 파일을 찾을 수 없습니다.")
        raise HTTPException(status_code=404, detail="설정 파일을 찾을 수 없습니다.")
    except PermissionError:
        logger.error("설정 파일에 대한 읽기 권한이 없습니다.")
        raise HTTPException(status_code=403, detail="파일 접근 권한이 없습니다.")
    except ValueError:
        logger.error("설정 파일의 데이터 형식이 올바르지 않습니다.")
        raise HTTPException(status_code=422, detail="설정 데이터 형식이 올바르지 않습니다.")
```

예외를 구체적으로 분류하여 각 상황에 맞는 HTTP 상태 코드와 메시지를 반환합니다. `async with`와 `aiofiles`를 사용하여 비동기 환경에서 자원 해제도 자동으로 보장합니다.

> **⚠️ 주의:** `except Exception as e: pass` 패턴을 AI가 생성하면 반드시 수정해야 합니다. 최소한 `logger.exception("예외 발생")`으로 로깅하고, 예외 종류별로 분기 처리하는 것이 올바른 방법입니다. FastAPI에서는 `@app.exception_handler()`를 활용하여 전역 수준의 예외 처리를 체계적으로 구성할 수 있습니다.

### 바이브 코딩 시 체크포인트

| 점검 항목 | 확인 방법 |
|-----------|-----------|
| `debug=True` 설정 여부 | `FastAPI(debug=True)`, `uvicorn --reload` 사용 여부 확인 |
| `traceback.format_exc()` 응답 포함 여부 | API 응답에 스택 트레이스가 포함되는지 확인 |
| 커스텀 예외 핸들러 설정 | `@app.exception_handler()` 로 전역 에러 처리 구성 여부 확인 |
| 빈 `except` 블록 | `except:` 뒤에 `pass`만 있는 코드 검색 |
| 광범위한 예외 처리 | `except Exception:` 사용 시 예외 종류를 세분화할 수 있는지 검토 |
| 로깅 설정 | `print()` 대신 `logging` 모듈을 사용하고 있는지 확인 |
| 에러 응답에 내부 정보 포함 여부 | API JSON 응답에 스택 트레이스, 파일 경로가 포함되지 않는지 확인 |
