# Chapter 10. 서명, 인증서, 무결성 검증

## 10-1. 부적절한 전자서명 확인

### 개요

전자서명(Digital Signature)은 데이터의 무결성(Integrity)과 인증(Authentication)을 보장하는 암호학적 기법입니다. FastAPI 애플리케이션에서 가장 흔히 접하는 전자서명은 JWT(JSON Web Token)입니다. JWT는 사용자 인증 정보를 담고 있으며, 서명을 통해 토큰이 변조되지 않았음을 보장합니다.

문제는 JWT의 서명을 제대로 검증하지 않거나, `alg: none` 공격을 허용하면 공격자가 토큰을 위조하여 다른 사용자로 로그인하거나 관리자 권한을 획득할 수 있다는 것입니다. FastAPI에서 `python-jose` 라이브러리를 사용할 때 특히 주의가 필요합니다.

### 왜 위험한가

부적절한 전자서명 확인은 다음과 같은 위험을 초래합니다.

- **토큰 위조**: 서명 검증을 생략하면, 공격자가 JWT의 페이로드(Payload)를 자유롭게 수정하여 관리자 권한을 획득할 수 있습니다.
- **알고리즘 혼동 공격(Algorithm Confusion)**: JWT 헤더의 `alg` 필드를 `none`으로 설정하여 서명 없이 토큰을 사용하는 공격입니다.
- **키 혼동 공격**: RS256(비대칭)으로 서명된 토큰을 HS256(대칭)으로 검증하도록 유도하여, 공개키를 비밀키로 사용하는 공격입니다.
- **데이터 변조**: API 요청의 전자서명을 검증하지 않으면, 요청 데이터가 중간에서 변조될 수 있습니다.

### 취약 코드

다음은 `python-jose`에서 JWT 서명을 제대로 검증하지 않는 ❌ 취약한 코드입니다.

```python
# ❌ 취약한 코드: JWT 서명 검증 미흡
from jose import jwt
from fastapi import FastAPI, Header

app = FastAPI()

async def get_user_from_token(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    # 서명을 검증하지 않고 디코딩
    payload = jwt.decode(token, None, options={"verify_signature": False})
    return payload.get("user_id")

async def verify_token_weak(token: str, secret: str):
    # algorithms에 허용 범위가 너무 넓음
    payload = jwt.decode(token, secret, algorithms=["HS256", "HS384", "HS512", "none"])
    return payload
```

### 안전 코드

`python-jose`를 사용하여 JWT 서명을 올바르게 검증하는 ✅ 안전한 코드입니다.

```python
# ✅ 안전한 코드: python-jose로 JWT 서명 검증 포함
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt, ExpiredSignatureError
from pydantic_settings import BaseSettings
from pydantic import SecretStr
from datetime import datetime, timedelta, timezone

class Settings(BaseSettings):
    jwt_secret_key: SecretStr
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    model_config = {"env_file": ".env"}

settings = Settings()
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def create_access_token(user_id: int, role: str) -> str:
    """JWT 액세스 토큰을 생성합니다."""
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(
        payload,
        settings.jwt_secret_key.get_secret_value(),
        algorithm=settings.jwt_algorithm,  # 명시적으로 단일 알고리즘 지정
    )

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """JWT 토큰을 검증하고 현재 사용자를 반환합니다."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="인증 정보가 유효하지 않습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key.get_secret_value(),
            algorithms=[settings.jwt_algorithm],  # 허용 알고리즘을 명시적으로 제한
            options={
                "verify_signature": True,    # 서명 검증 활성화
                "verify_exp": True,          # 만료 시간 검증
                "require_sub": True,         # sub 클레임 필수
                "require_exp": True,         # exp 클레임 필수
            },
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰이 만료되었습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user
```

비대칭 키(RSA)를 사용하는 경우에는 공개키와 개인키를 분리하여 사용합니다.

```python
# ✅ python-jose에서 RSA 기반 JWT (더 안전한 방식)
from jose import jwt
from cryptography.hazmat.primitives import serialization

def create_token_rsa(user_id: int) -> str:
    """RSA 개인키로 JWT를 서명합니다."""
    with open("private_key.pem", "rb") as f:
        private_key = f.read()

    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, private_key, algorithm="RS256")

async def get_current_user_rsa(token: str = Depends(oauth2_scheme)):
    """RSA 공개키로 JWT를 검증합니다."""
    with open("public_key.pem", "rb") as f:
        public_key = f.read()

    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],  # RS256만 허용 → 알고리즘 혼동 공격 차단
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")
    return payload
```

### 바이브 코딩 시 체크포인트

- [ ] `jwt.decode()`에 `verify_signature=False`가 설정되어 있지 않은지 확인합니다.
- [ ] `algorithms` 매개변수에 `"none"`이 포함되어 있지 않은지 확인합니다.
- [ ] `algorithms`에는 사용하는 단일 알고리즘만 명시합니다 (예: `["HS256"]`).
- [ ] JWT 만료 시간(`exp`)이 설정되어 있고 검증되는지 확인합니다.
- [ ] JWT 시크릿 키가 `BaseSettings`와 `SecretStr`로 환경 변수에서 관리되는지 확인합니다.
- [ ] AI에게 "python-jose로 JWT 서명 검증을 반드시 포함하고, algorithms에는 HS256만 허용해줘"라고 요청합니다.

> **💡 팁:** `python-jose`(`pip install python-jose[cryptography]`)를 사용하십시오. FastAPI 공식 문서에서도 이 라이브러리를 권장합니다. `jose`와 `jwt`(PyJWT)는 다른 패키지이므로 import 시 주의하십시오.

---

## 10-2. 부적절한 인증서 유효성 검증

### 개요

SSL/TLS 인증서(Certificate)는 HTTPS 통신에서 서버의 신원을 확인하고 데이터를 암호화하는 데 사용됩니다. FastAPI 애플리케이션에서 외부 API를 호출할 때 `httpx` 라이브러리를 주로 사용하는데, `verify=False`를 설정하면 인증서 검증을 건너뛰게 됩니다.

바이브 코딩에서 AI에게 API 호출 코드를 요청하면, 개발 편의를 위해 `verify=False`를 포함하는 코드를 생성하는 경우가 있습니다. 이는 중간자 공격(MITM, Man-In-The-Middle Attack)에 완전히 노출되는 심각한 보안 취약점입니다.

### 왜 위험한가

- **중간자 공격(MITM)**: 공격자가 클라이언트와 서버 사이에서 통신을 가로채고 변조할 수 있습니다. 인증서 검증을 하지 않으면, 공격자의 가짜 서버를 진짜 서버로 오인하게 됩니다.
- **데이터 도청**: 암호화된 것처럼 보이지만, 실제로는 공격자가 모든 통신 내용을 볼 수 있습니다.
- **API 키 유출**: MITM 공격을 통해 요청 헤더에 포함된 API 키, 인증 토큰 등이 유출될 수 있습니다.

### 취약 코드

```python
# ❌ 취약한 코드: httpx에서 SSL 인증서 검증 비활성화
import httpx

async def call_payment_api(payment_data: dict):
    async with httpx.AsyncClient(verify=False) as client:  # 인증서 검증 비활성화!
        response = await client.post(
            "https://api.payment.com/charge",
            json=payment_data,
        )
    return response.json()
```

```python
# ❌ 취약한 코드: SSL 컨텍스트에서 검증 비활성화
import ssl
import urllib.request

# 인증서 검증을 건너뛰는 SSL 컨텍스트
context = ssl._create_unverified_context()
response = urllib.request.urlopen("https://api.example.com", context=context)
```

### 안전 코드

```python
# ✅ 안전한 코드: httpx에서 SSL 인증서 검증 활성화
import httpx
from fastapi import FastAPI, Depends

app = FastAPI()

async def call_payment_api(payment_data: dict) -> dict:
    async with httpx.AsyncClient(verify=True) as client:  # 기본값 True, 명시적으로 설정
        response = await client.post(
            "https://api.payment.com/charge",
            json=payment_data,
            headers={"Authorization": f"Bearer {settings.payment_api_key.get_secret_value()}"},
        )
        response.raise_for_status()
    return response.json()

async def call_internal_api(data: dict) -> dict:
    # 내부 서버에 자체 서명 인증서를 사용하는 경우
    # 해당 CA 인증서 경로를 직접 지정
    async with httpx.AsyncClient(verify="/path/to/company-ca-bundle.crt") as client:
        response = await client.get("https://internal-api.company.com/data")
    return response.json()
```

```python
# ✅ 안전한 코드: FastAPI 엔드포인트에서 외부 API를 안전하게 호출
from fastapi import FastAPI, Depends, HTTPException
import httpx

app = FastAPI()

@app.post("/process-payment")
async def process_payment(
    payment: PaymentRequest,
    current_user: User = Depends(get_current_user),
):
    try:
        async with httpx.AsyncClient(
            verify=True,
            timeout=httpx.Timeout(10.0),  # 타임아웃 설정도 중요
        ) as client:
            response = await client.post(
                "https://api.payment.com/charge",
                json=payment.model_dump(),
            )
            response.raise_for_status()
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail="결제 서버 통신 오류")
    return response.json()
```

> **⚠️ 주의:** 개발 환경에서 자체 서명 인증서(Self-signed Certificate) 때문에 `verify=False`를 사용하는 경우가 있습니다. 이 코드가 운영 환경에 배포되지 않도록 환경 분리를 철저히 하십시오. `BaseSettings`를 활용하여 환경별로 인증서 경로를 분리하는 것을 권장합니다.

### 바이브 코딩 시 체크포인트

- [ ] 코드 전체에서 `verify=False`를 검색하여 제거합니다.
- [ ] `ssl._create_unverified_context()`가 사용되고 있지 않은지 확인합니다.
- [ ] `httpx.AsyncClient`에서 `verify` 매개변수의 기본값(True)이 유지되는지 확인합니다.
- [ ] 자체 서명 인증서가 필요한 경우 `verify="/path/to/cert.pem"`으로 CA 인증서를 직접 지정합니다.
- [ ] AI에게 "SSL 인증서 검증을 비활성화하지 마. verify=True를 유지해줘"라고 명시합니다.

> **💡 팁:** `httpx`에서 `verify` 매개변수의 기본값은 `True`입니다. 명시적으로 `verify=False`가 작성되어 있다면 누군가 의도적으로 검증을 비활성화한 것이므로 반드시 확인이 필요합니다.

---

## 10-3. 무결성 검사 없는 코드 다운로드

### 개요

무결성(Integrity)이란 데이터가 변조되지 않았음을 보장하는 것입니다. 외부에서 패키지, 라이브러리, 스크립트를 다운로드하여 사용할 때, 해당 코드가 원본과 동일한지 검증하지 않으면 악성 코드가 포함된 변조된 패키지를 실행할 수 있습니다.

바이브 코딩에서 AI가 추천하는 라이브러리를 무비판적으로 설치하거나, 검증되지 않은 소스에서 스크립트를 다운로드하여 실행하는 것은 공급망 공격(Supply Chain Attack)에 노출되는 위험한 행위입니다. FastAPI 프로젝트는 다양한 서드파티 라이브러리에 의존하므로 이 문제에 더욱 주의해야 합니다.

### 왜 위험한가

- **공급망 공격(Supply Chain Attack)**: 공격자가 널리 사용되는 패키지의 이름을 흉내 낸 악성 패키지를 배포합니다(타이포스쿼팅, Typosquatting). 예: `fastapi` 대신 `fastapl`, `python-jose` 대신 `python-j0se`.
- **의존성 혼동(Dependency Confusion)**: 내부 패키지와 같은 이름의 악성 패키지를 공개 저장소에 올려 설치를 유도합니다.
- **패키지 변조**: 인기 있는 패키지의 관리자 계정이 해킹되어 악성 코드가 주입되는 사례가 실제로 발생했습니다.

### 취약 코드

```python
# ❌ 취약한 코드: 검증 없이 외부 스크립트 다운로드 실행
import subprocess
import urllib.request

def install_tool():
    # 인터넷에서 다운로드한 스크립트를 검증 없이 바로 실행
    urllib.request.urlretrieve(
        "http://example.com/install.sh",  # HTTP 사용 (암호화 없음)
        "/tmp/install.sh",
    )
    subprocess.run(["bash", "/tmp/install.sh"])  # 검증 없이 실행
```

```bash
# ❌ 취약한 명령어: 검증 없이 curl로 스크립트 실행
curl http://example.com/setup.sh | bash
```

### 안전 코드

해시값을 통해 무결성을 검증하는 ✅ 안전한 코드입니다.

```python
# ✅ 안전한 코드: 다운로드 후 해시 검증
import hashlib
import os
import httpx

async def download_and_verify(
    url: str, expected_hash: str, save_path: str,
) -> str:
    """파일을 다운로드하고 SHA-256 해시로 무결성을 검증합니다."""
    async with httpx.AsyncClient(verify=True) as client:
        response = await client.get(url)
        response.raise_for_status()

    with open(save_path, "wb") as f:
        f.write(response.content)

    # SHA-256 해시로 무결성 검증
    sha256_hash = hashlib.sha256()
    with open(save_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)

    actual_hash = sha256_hash.hexdigest()
    if actual_hash != expected_hash:
        os.remove(save_path)  # 검증 실패 시 파일 삭제
        raise ValueError(
            f"무결성 검증 실패!\n"
            f"예상 해시: {expected_hash}\n"
            f"실제 해시: {actual_hash}"
        )
    return save_path
```

FastAPI 프로젝트의 패키지를 안전하게 관리하는 방법입니다.

```bash
# ✅ 안전한 방법: requirements.txt에 해시 포함
# pip install --require-hashes -r requirements.txt

# requirements.txt 예시
fastapi==0.115.0 \
    --hash=sha256:abc123...
python-jose[cryptography]==3.3.0 \
    --hash=sha256:def456...
passlib[bcrypt]==1.7.4 \
    --hash=sha256:ghi789...
```

```bash
# ✅ 안전한 방법: pip-audit으로 알려진 취약점 검사
pip install pip-audit
pip-audit
```

### 바이브 코딩 시 체크포인트

- [ ] AI가 추천하는 패키지 이름의 철자가 정확한지 PyPI에서 직접 확인합니다.
- [ ] `curl ... | bash`와 같은 검증 없는 스크립트 실행을 피합니다.
- [ ] 프로젝트에 `pip-audit`을 도입하여 정기적으로 취약점을 점검합니다.
- [ ] `requirements.txt`에 패키지 버전을 고정(`==`)하여 예기치 않은 업데이트를 방지합니다.
- [ ] `--require-hashes` 옵션으로 패키지 해시를 검증합니다.
- [ ] AI에게 "이 라이브러리가 안전한지 확인해줘"라고 요청하기보다는, 직접 PyPI 페이지와 GitHub 저장소를 확인하십시오.

> **⚠️ 주의:** AI가 존재하지 않는 패키지 이름을 제안하는 경우가 있습니다(할루시네이션, Hallucination). 공격자는 이 점을 악용하여, AI가 자주 추천하는 가상의 패키지 이름으로 악성 패키지를 등록할 수 있습니다. 반드시 패키지의 실존 여부와 다운로드 수를 확인하십시오.
