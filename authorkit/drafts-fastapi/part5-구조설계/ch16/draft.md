# Chapter 16. API 오용 — 편리함 뒤에 숨은 위험

현대 소프트웨어 개발에서 외부 라이브러리(Library)와 API(Application Programming Interface) 없이 프로그램을 만드는 것은 거의 불가능합니다. 특히 파이썬 생태계는 PyPI(Python Package Index)에 등록된 수십만 개의 패키지를 기반으로 돌아갑니다. 바이브 코딩에서 AI는 다양한 외부 패키지를 자유롭게 활용하는 코드를 생성하지만, 해당 패키지가 안전한지, 더 이상 유지보수되지 않는 것은 아닌지 검증하지 않습니다. 이 장에서는 FastAPI 환경에서 취약한 API 사용(Use of Vulnerable API)에 따른 위험과 대응 방법을 살펴보겠습니다.

---

## 16-1. 취약한 API 사용

### 개요

취약한 API란 보안상 사용이 금지되었거나 더 이상 유지보수되지 않는(Deprecated) 함수 및 패키지, 또는 부주의하게 사용될 가능성이 높은 API를 의미합니다. 파이썬은 외부 의존성(External Dependency)을 기반으로 하는 생태계이므로, 사용하는 패키지의 보안 상태를 지속적으로 관리하는 것이 필수적입니다.

취약한 API 사용으로 인한 보안 문제는 크게 두 가지 원인으로 분류됩니다:

1. **사용자 배포 패키지 내의 결함**: PyPI에 등록된 패키지 코드 내에 보안 취약점이 존재하는 경우
2. **언어 엔진 자체의 결함**: 파이썬 기본 내장 패키지(Built-in Package)에서 보안 결함이 발견되는 경우

### 왜 위험한가

바이브 코딩에서 AI는 특정 기능을 구현할 때 가장 널리 알려진 패키지를 자동으로 선택합니다. 하지만 AI의 학습 데이터에는 오래된 코드도 포함되어 있어 이미 보안 취약점이 발견된 구 버전의 API를 사용하거나, 더 안전한 대안이 있는데도 레거시(Legacy) 방식의 코드를 생성하는 경우가 있습니다.

대표적인 사례를 살펴보겠습니다:

- **`yaml.load()` vs `yaml.safe_load()`**: `yaml.load()`는 임의 코드 실행이 가능한 반면, `yaml.safe_load()`는 기본 데이터 타입만 파싱합니다.
- **`md5`, `sha1` 해시**: 충돌 공격(Collision Attack)에 취약한 것으로 알려져 있으나, AI가 비밀번호 해싱이나 데이터 검증에 여전히 이를 사용하는 코드를 생성할 수 있습니다.
- **`eval()`, `exec()`**: 문자열을 코드로 실행하는 함수로, 외부 입력과 결합되면 원격 코드 실행 취약점이 됩니다.
- **Deprecated 패키지 사용**: FastAPI 생태계에서도 이전 버전의 패턴이나 폐기 예정(Deprecated) API를 AI가 생성하는 경우가 있습니다.

### ❌ 취약한 코드

**위험한 YAML 파싱**

```python
import yaml
from fastapi import FastAPI, UploadFile

app = FastAPI()

@app.post("/config/upload")
async def load_config(file: UploadFile):
    content = await file.read()
    # yaml.load()는 임의 코드 실행 가능 — 절대 사용 금지
    config = yaml.load(content)
    return {"config": config}
```

**취약한 해시 함수 사용**

```python
import hashlib
from fastapi import FastAPI

app = FastAPI()

@app.post("/register")
async def register(username: str, password: str):
    # MD5는 충돌 공격에 취약 — 비밀번호 해싱에 부적합
    hashed = hashlib.md5(password.encode()).hexdigest()
    await save_user(username, hashed)
    return {"status": "registered"}
```

**eval()을 사용한 위험한 동적 실행**

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/calculate")
async def calculate(expression: str):
    # 사용자 입력을 eval()로 실행 — 원격 코드 실행 가능
    result = eval(expression)
    return {"result": result}
```

**오래된 패키지 의존**

```text
# requirements.txt
fastapi==0.68.0     # 구 버전 — 보안 패치 미적용
uvicorn==0.13.0     # 알려진 취약점 포함
pydantic==1.8.0     # V2 마이그레이션 필요
httpx==0.18.0       # 구 버전
```

### ✅ 안전한 코드

**안전한 YAML 파싱**

```python
import yaml
from fastapi import FastAPI, UploadFile, HTTPException

app = FastAPI()

@app.post("/config/upload")
async def load_config(file: UploadFile):
    content = await file.read()
    try:
        # safe_load()는 기본 데이터 타입만 허용
        config = yaml.safe_load(content)
        return {"config": config}
    except yaml.YAMLError:
        raise HTTPException(status_code=400, detail="잘못된 YAML 형식입니다.")
```

**안전한 비밀번호 해싱**

```python
import bcrypt
from fastapi import FastAPI

app = FastAPI()

@app.post("/register")
async def register(username: str, password: str):
    # bcrypt — 솔트 자동 생성, 충돌 공격에 안전
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    await save_user(username, hashed)
    return {"status": "registered"}

@app.post("/login")
async def login(username: str, password: str):
    stored_hash = await get_user_hash(username)
    if bcrypt.checkpw(password.encode(), stored_hash):
        return {"status": "ok"}
    return {"status": "fail"}
```

```python
# 또는 passlib 활용 (FastAPI 공식 문서 권장)
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

**eval() 대신 안전한 대안 사용**

```python
import ast
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.post("/calculate")
async def calculate(expression: str):
    # ast.literal_eval()은 리터럴 표현식만 평가 — 코드 실행 불가
    try:
        result = ast.literal_eval(expression)
        return {"result": result}
    except (ValueError, SyntaxError):
        raise HTTPException(status_code=400, detail="허용되지 않는 표현식입니다.")
```

**최신 패키지 버전 관리**

```text
# requirements.txt — 최신 안정 버전 사용
fastapi>=0.115.0
uvicorn>=0.34.0
pydantic>=2.0.0
httpx>=0.27.0
```

### FastAPI에서의 Deprecated API 관리

FastAPI는 OpenAPI 명세를 자동 생성하므로, API 버전 관리와 폐기 예정(Deprecated) 엔드포인트 처리를 체계적으로 할 수 있습니다.

**Deprecated 파라미터 활용**

```python
from fastapi import FastAPI, Query

app = FastAPI()

# 기존 API — deprecated=True로 명시하여 Swagger UI에 표시
@app.get("/api/v1/users", deprecated=True)
async def get_users_v1(name: str = Query(default=None)):
    """[Deprecated] /api/v2/users를 사용하십시오."""
    return await get_users_v2(name=name)

# 신규 API
@app.get("/api/v2/users")
async def get_users_v2(name: str = Query(default=None)):
    users = await fetch_users(name=name)
    return {"users": users}
```

**버전별 라우터(Router) 분리**

```python
from fastapi import FastAPI, APIRouter

app = FastAPI()

# 버전별 라우터 분리
v1_router = APIRouter(prefix="/api/v1", tags=["v1-deprecated"])
v2_router = APIRouter(prefix="/api/v2", tags=["v2-current"])

@v1_router.get("/users", deprecated=True)
async def get_users_v1():
    """[Deprecated] v2 API로 마이그레이션하십시오."""
    return await get_users_v2()

@v2_router.get("/users")
async def get_users_v2():
    return await fetch_users()

app.include_router(v1_router)
app.include_router(v2_router)
```

> **💡 팁:** FastAPI의 `deprecated=True` 파라미터를 활용하면 Swagger UI와 ReDoc에서 해당 엔드포인트가 폐기 예정임을 자동으로 표시합니다. 클라이언트 개발자가 새로운 API로 마이그레이션할 수 있도록 충분한 유예 기간을 두고, 최종적으로 엔드포인트를 제거하십시오.

### 안전한 패키지 선택 기준

AI가 제안한 패키지를 사용하기 전에 다음 항목을 확인하십시오:

1. **사용 통계**: 얼마나 많은 사람들이 해당 패키지를 다운로드하고 사용하고 있는지 확인합니다. PyPI 통계나 GitHub 스타(Star) 수를 참고할 수 있습니다.
2. **이슈 관리**: 버그 리포트와 보안 이슈가 적시에 처리되고 있는지 확인합니다.
3. **마지막 업데이트**: 최근 6개월 이내에 업데이트가 있었는지 확인합니다. 오랫동안 업데이트가 없는 패키지는 유지보수가 중단되었을 가능성이 높습니다.
4. **알려진 취약점**: NIST NVD(https://nvd.nist.gov) 또는 CVEdetails(https://cvedetails.com)에서 패키지명으로 검색하여 알려진 취약점을 확인합니다.

### 사후 관리: SBOM 도입

모든 API는 보안 취약점에서 완전히 자유로울 수 없습니다. 안전한 패키지를 선택했더라도 지속적인 모니터링이 필요합니다. **SBOM(Software Bill of Materials, 소프트웨어 자재 명세서)**을 도입하면 프로젝트에 사용된 모든 패키지의 이름, 버전, 라이선스, 보안 상태를 체계적으로 관리할 수 있습니다.

파이썬에서는 다음 도구들을 활용할 수 있습니다:

```bash
# pip-audit: 설치된 패키지의 알려진 취약점 검사
pip install pip-audit
pip-audit

# safety: requirements.txt 기반 취약점 검사
pip install safety
safety check -r requirements.txt
```

> **💡 팁:** CI/CD 파이프라인에 `pip-audit`이나 `safety check`를 포함시키면, 취약한 패키지가 포함된 코드가 배포되기 전에 자동으로 차단할 수 있습니다. GitHub의 Dependabot이나 Snyk 같은 서비스를 활용하면 패키지 취약점이 발견될 때 자동으로 알림을 받을 수 있습니다.

### 바이브 코딩 시 체크포인트

| 점검 항목 | 확인 방법 |
|-----------|-----------|
| `yaml.load()` 사용 여부 | `yaml.safe_load()`로 대체 |
| `eval()`, `exec()` 사용 여부 | `ast.literal_eval()` 또는 안전한 대안으로 대체 |
| `md5`, `sha1` 해시 사용 | 비밀번호에는 `bcrypt` 또는 `argon2`, 무결성 검증에는 `sha256` 이상 사용 |
| `pickle.loads()` 외부 데이터 처리 | Pydantic 모델 또는 `json.loads()`로 대체 |
| 패키지 버전 고정 | `requirements.txt`에 최소 버전 명시, 주기적 업데이트 |
| 패키지 취약점 검사 | `pip-audit` 또는 `safety check` 실행 |
| Deprecated 엔드포인트 관리 | `deprecated=True` 파라미터로 명시, 버전 라우터 분리 |
| SBOM 관리 | 프로젝트에 사용된 모든 외부 의존성 목록 관리 |
| FastAPI/Pydantic 버전 | 최신 안정 버전 사용 여부 확인 |

---

> **기타 API 주의사항**
>
> 이 장에서 다루지 않은 API 관련 보안약점으로 **DNS lookup에 의존한 보안 결정** 문제가 있습니다. 도메인명(Domain Name)을 기반으로 접근 제어나 인증을 수행하면 DNS 스푸핑(DNS Spoofing) 공격에 취약해집니다. 공격자가 DNS 캐시를 오염시키면 신뢰할 수 없는 서버가 마치 정상 서버인 것처럼 위장할 수 있습니다. 보안 결정에는 도메인명 대신 IP 주소를 직접 비교하거나, TLS 인증서(Certificate) 검증을 통해 상대방의 신원을 확인하는 방식을 사용해야 합니다. FastAPI에서 `httpx`를 사용할 때 `verify=True`(기본값)를 반드시 유지하고, AI가 `verify=False`로 SSL 검증을 비활성화하는 코드를 생성하면 주의 깊게 검토하십시오.
