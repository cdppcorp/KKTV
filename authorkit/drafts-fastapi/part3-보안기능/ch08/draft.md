# Chapter 08. 암호화, 제대로 하고 계십니까

## 8-1. 취약한 암호화 알고리즘 사용

### 개요

암호화 알고리즘(Encryption Algorithm)은 중요한 정보를 보호하기 위한 핵심 수단입니다. 그러나 과거에 안전하다고 여겨졌던 알고리즘 중 상당수가 컴퓨터 성능의 향상과 함께 취약해졌습니다. MD5, SHA-1, DES, RC4와 같은 알고리즘이 대표적입니다.

바이브 코딩에서 특히 주의해야 할 점은, AI가 학습한 데이터에 오래된 코드 예제가 다수 포함되어 있다는 것입니다. 따라서 AI는 여전히 MD5나 SHA-1을 사용하는 코드를 생성할 수 있습니다. 여러분이 직접 알고리즘의 안전성을 판단할 수 있어야 합니다.

### 왜 위험한가

취약한 암호화 알고리즘을 사용하면 다음과 같은 위험이 발생합니다.

- **해시 충돌(Hash Collision)**: MD5와 SHA-1은 서로 다른 입력에서 같은 해시값이 생성되는 충돌이 실제로 발견되었습니다. 이를 통해 위조된 인증서나 문서를 만들 수 있습니다.
- **브루트포스 공격(Brute-Force Attack)**: DES는 56비트 키를 사용하므로, 현대 컴퓨터로 수 시간 내에 모든 키를 시도할 수 있습니다.
- **레인보우 테이블(Rainbow Table) 공격**: MD5 해시값은 이미 방대한 레인보우 테이블이 존재하여, 해시값만으로 원문을 역추적할 수 있습니다.

### 취약 코드

다음은 FastAPI 애플리케이션에서 취약한 DES 알고리즘과 MD5 해시를 사용하는 ❌ 취약한 코드입니다.

```python
# ❌ 취약한 코드: DES 암호화 사용
from Crypto.Cipher import DES
import base64

def encrypt_data(plain_text: str, key: bytes) -> str:
    # DES는 56비트 키로 현대 컴퓨터에서 쉽게 해독 가능
    cipher = DES.new(key, DES.MODE_ECB)
    encrypted = base64.b64encode(cipher.encrypt(plain_text.ljust(8).encode()))
    return encrypted.decode("ASCII")
```

```python
# ❌ 취약한 코드: MD5 해시로 패스워드 저장
from fastapi import FastAPI
from pydantic import BaseModel
import hashlib

app = FastAPI()

class UserCreate(BaseModel):
    username: str
    password: str

@app.post("/register")
async def register(user: UserCreate):
    # MD5는 충돌이 발견되어 더 이상 안전하지 않음
    hashed = hashlib.md5(user.password.encode("utf-8")).hexdigest()
    save_user(user.username, hashed)
    return {"message": "가입 완료"}
```

### 안전 코드

AES-256과 `passlib` + bcrypt를 사용하는 ✅ 안전한 코드입니다.

```python
# ✅ 안전한 코드: AES-256 GCM 모드 암호화
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

def encrypt_data(plain_text: str, key: bytes) -> str:
    """AES-256 GCM 모드로 데이터를 암호화합니다.
    GCM 모드는 암호화와 무결성 검증을 동시에 제공합니다."""
    nonce = get_random_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plain_text.encode("utf-8"))
    # nonce + tag + ciphertext를 결합하여 저장
    return base64.b64encode(nonce + tag + ciphertext).decode("ASCII")

def decrypt_data(encrypted_text: str, key: bytes) -> str:
    raw = base64.b64decode(encrypted_text)
    nonce = raw[:12]
    tag = raw[12:28]
    ciphertext = raw[28:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    decrypted = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted.decode("utf-8")
```

```python
# ✅ 안전한 코드: passlib + bcrypt로 패스워드 해싱
from fastapi import FastAPI
from passlib.context import CryptContext
from pydantic import BaseModel, SecretStr

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    username: str
    password: SecretStr  # SecretStr로 로그 노출 방지

@app.post("/register")
async def register(user: UserCreate):
    # bcrypt는 솔트 자동 생성 + 키 스트레칭 적용
    hashed = pwd_context.hash(user.password.get_secret_value())
    save_user(user.username, hashed)
    return {"message": "가입 완료"}
```

> **⚠️ 주의:** ECB(Electronic Code Block) 모드는 같은 평문 블록이 항상 같은 암호문을 생성하므로 패턴이 노출됩니다. 반드시 GCM, CBC, CTR 등의 운영 모드를 사용하십시오. 특히 GCM 모드는 암호화와 무결성 검증을 동시에 제공하므로 가장 권장됩니다.

### 바이브 코딩 시 체크포인트

- [ ] AI가 생성한 코드에서 `DES`, `MD5`, `SHA1`, `RC4`, `Blowfish`를 사용하는 부분이 없는지 검색합니다.
- [ ] 대칭키 암호화는 AES-128 이상(권장 AES-256)을 사용합니다.
- [ ] 패스워드 해싱에는 `passlib`의 `CryptContext(schemes=["bcrypt"])`를 사용합니다.
- [ ] ECB 모드 대신 GCM, CBC 등의 안전한 운영 모드를 사용하는지 확인합니다.
- [ ] AI에게 "안전한 암호화 알고리즘을 사용해줘. bcrypt와 AES-256을 적용해줘"라고 명시합니다.

---

## 8-2. 암호화되지 않은 중요정보

### 개요

많은 웹 애플리케이션은 패스워드, 주민등록번호, 신용카드 번호 등의 중요정보(Sensitive Information)를 다루게 됩니다. 이러한 정보가 평문(Plaintext)으로 저장되거나 전송되면, 데이터베이스 유출이나 네트워크 도청 시 모든 정보가 그대로 노출됩니다.

바이브 코딩으로 빠르게 FastAPI 프로토타입을 만들 때, "일단 동작하게 만들고 나중에 암호화를 추가하자"라는 생각은 매우 위험합니다. 나중에 암호화를 추가하는 일은 처음부터 적용하는 것보다 훨씬 어렵고, 종종 잊혀지기도 합니다.

### 왜 위험한가

- **데이터베이스 유출**: 평문으로 저장된 패스워드는 DB 유출 사고 시 즉시 악용됩니다. 사용자들은 여러 사이트에서 같은 패스워드를 사용하는 경우가 많아 피해가 확대됩니다.
- **네트워크 도청**: 평문으로 전송된 정보는 패킷 스니핑(Packet Sniffing)을 통해 중간에서 가로챌 수 있습니다.
- **법적 책임**: 개인정보보호법에 따라 개인정보를 안전하게 관리하지 않을 경우 법적 제재를 받을 수 있습니다.

### 취약 코드

다음은 패스워드를 평문으로 데이터베이스에 저장하는 ❌ 취약한 코드입니다.

```python
# ❌ 취약한 코드: 패스워드 평문 저장
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

app = FastAPI()

class UserCreate(BaseModel):
    username: str
    password: str

@app.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # 패스워드가 암호화 없이 그대로 저장됨
    new_user = User(username=user.username, password=user.password)
    db.add(new_user)
    db.commit()
    return {"message": "가입 완료"}
```

```python
# ❌ 취약한 코드: HTTP로 외부 API 호출
import httpx

async def send_user_data(user_data: dict):
    async with httpx.AsyncClient() as client:
        # HTTP(평문)로 개인정보 전송
        response = await client.post(
            "http://api.example.com/users",
            json=user_data,
        )
    return response.json()
```

### 안전 코드

패스워드를 `passlib`으로 해시화하여 저장하고, `httpx`에서 HTTPS를 통해 전송하는 ✅ 안전한 코드입니다.

```python
# ✅ 안전한 코드: passlib + bcrypt로 패스워드 해시 저장
from fastapi import FastAPI, Depends
from passlib.context import CryptContext
from pydantic import BaseModel, SecretStr
from sqlalchemy.orm import Session

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    username: str
    password: SecretStr

@app.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password.get_secret_value())
    new_user = User(
        username=user.username,
        hashed_password=hashed_password,  # 해시화된 패스워드 저장
    )
    db.add(new_user)
    db.commit()
    return {"message": "가입 완료"}
```

```python
# ✅ 안전한 코드: httpx에서 HTTPS + 인증서 검증
import httpx

async def send_user_data(user_data: dict):
    async with httpx.AsyncClient(verify=True) as client:
        # HTTPS를 사용하여 암호화된 채널로 전송
        response = await client.post(
            "https://api.example.com/users",  # HTTP가 아닌 HTTPS 사용
            json=user_data,
        )
    return response.json()
```

> **💡 팁:** Pydantic의 `SecretStr` 타입을 사용하면 패스워드가 로그, `repr()`, JSON 직렬화 시 `**********`로 마스킹됩니다. 실제 값이 필요할 때는 `.get_secret_value()` 메서드를 호출합니다.

### 바이브 코딩 시 체크포인트

- [ ] 패스워드는 반드시 `passlib`의 `CryptContext`로 해시화하여 저장하고, 평문 저장 코드가 없는지 확인합니다.
- [ ] 외부 API 통신 시 `http://`가 아닌 `https://`를 사용하는지 확인합니다.
- [ ] `httpx.AsyncClient`에서 `verify=True`(기본값)를 유지하는지 확인합니다.
- [ ] Pydantic 모델에서 민감한 필드에 `SecretStr` 타입을 사용하는지 확인합니다.
- [ ] AI에게 "패스워드는 bcrypt로 해시 저장하고, 통신은 HTTPS를 사용해줘"라고 명시합니다.

---

## 8-3. 하드코딩된 중요정보

### 개요

하드코딩(Hardcoding)이란 소스 코드 내부에 패스워드, API 키(API Key), 데이터베이스 접속 정보 등의 중요정보를 직접 문자열로 작성하는 것을 말합니다. **이것은 바이브 코딩에서 가장 빈번하게 발생하는 보안 실수입니다.**

AI에게 "데이터베이스에 연결하는 FastAPI 코드를 만들어줘"라고 요청하면, AI는 높은 확률로 코드 안에 예시 패스워드와 호스트 정보를 직접 작성합니다. 여러분이 이 코드를 그대로 사용하여 GitHub에 Push하면, 전 세계 누구나 여러분의 데이터베이스 접속 정보를 볼 수 있게 됩니다.

> **⚠️ 주의:** GitHub에는 API 키와 패스워드를 자동으로 수집하는 봇(Bot)이 활동하고 있습니다. 한번 Push된 정보는 커밋 기록에 남아 삭제해도 복구할 수 있습니다. 실수를 발견하면 키를 즉시 폐기하고 새로 발급받아야 합니다.

### 왜 위험한가

하드코딩된 중요정보는 다음과 같은 경로로 유출됩니다.

- **소스코드 저장소(Repository) 노출**: GitHub, GitLab 등에 코드를 Push하면 공개 저장소의 경우 즉시 노출됩니다. 비공개 저장소라도 접근 권한이 있는 모든 개발자에게 노출됩니다.
- **로그(Log) 파일 노출**: 코드에 하드코딩된 값이 에러 메시지나 디버그 로그에 포함되어 출력될 수 있습니다.
- **빌드 산출물(Build Artifact) 노출**: 컴파일된 바이너리나 패키지에서 문자열을 추출하여 중요 정보를 획득할 수 있습니다.
- **AI 학습 데이터 오염**: 하드코딩된 키가 포함된 코드가 공개되면, AI 학습 데이터에 포함되어 다른 사람의 AI 응답에 여러분의 키가 노출될 수도 있습니다.

### 취약 코드

다음은 AI가 흔히 생성하는 형태의 ❌ 취약한 코드입니다.

```python
# ❌ 취약한 코드: API 키와 DB 정보가 소스코드에 하드코딩
from fastapi import FastAPI
from sqlalchemy import create_engine
import openai

app = FastAPI()

# OpenAI API 키가 소스코드에 그대로 노출
openai.api_key = "sk-proj-abc123xyz456..."

# 데이터베이스 접속 정보가 하드코딩됨
DATABASE_URL = "postgresql://admin:SuperSecret123!@db.example.com:5432/production_db"
engine = create_engine(DATABASE_URL)

# JWT 시크릿 키가 하드코딩됨
SECRET_KEY = "my-super-secret-jwt-key-12345"
```

### 안전 코드

Pydantic `BaseSettings`와 `python-dotenv`를 활용하는 ✅ 안전한 코드입니다.

**Step 1: `.env` 파일 생성 (절대 Git에 커밋하지 않습니다)**

```bash
# .env 파일 (이 파일은 .gitignore에 반드시 추가)
OPENAI_API_KEY=sk-proj-abc123xyz456...
DATABASE_URL=postgresql://admin:SuperSecret123!@db.example.com:5432/production_db
JWT_SECRET_KEY=your-very-long-random-secret-key
STRIPE_API_KEY=sk_live_51ABC...
```

**Step 2: `.gitignore`에 `.env` 추가**

```text
# .gitignore
.env
.env.local
.env.production
*.pem
*.key
```

**Step 3: Pydantic `BaseSettings`로 환경 변수 관리**

```python
# ✅ 안전한 코드: BaseSettings를 통한 중요정보 관리
from pydantic_settings import BaseSettings
from pydantic import SecretStr

class Settings(BaseSettings):
    """환경 변수에서 설정값을 자동으로 로드합니다."""
    openai_api_key: SecretStr
    database_url: SecretStr
    jwt_secret_key: SecretStr
    stripe_api_key: SecretStr

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

settings = Settings()
```

```python
# ✅ 안전한 코드: Settings 객체를 활용한 FastAPI 애플리케이션
from fastapi import FastAPI
from sqlalchemy import create_engine

app = FastAPI()

# 환경 변수에서 DB URL을 가져옴
engine = create_engine(settings.database_url.get_secret_value())

# JWT 시크릿 키도 환경 변수에서 가져옴
SECRET_KEY = settings.jwt_secret_key.get_secret_value()
```

`BaseSettings`는 `python-dotenv`를 내장 지원하며, 환경 변수가 누락되면 애플리케이션 시작 시 `ValidationError`를 발생시킵니다. `SecretStr` 타입을 사용하면 로그에 값이 노출되지 않습니다.

> **💡 팁:** `BaseSettings`에서 `SecretStr`을 사용하면 `settings.jwt_secret_key`를 `print()`하거나 로그에 출력해도 `SecretStr('**********')`로 마스킹됩니다. 실제 값이 필요할 때만 `.get_secret_value()`를 호출하십시오.

### 바이브 코딩 시 체크포인트

- [ ] AI가 생성한 코드에서 API 키, 패스워드, 시크릿 키(Secret Key)가 문자열로 하드코딩되어 있지 않은지 확인합니다.
- [ ] Pydantic `BaseSettings`를 사용하여 환경 변수를 타입 안전하게 관리합니다.
- [ ] `.env` 파일을 생성하고, 반드시 `.gitignore`에 추가합니다.
- [ ] Git 커밋 전, `git diff`로 중요 정보가 포함되어 있지 않은지 확인합니다.
- [ ] 이미 커밋된 키가 있다면 즉시 해당 키를 폐기하고 새로 발급받습니다.
- [ ] AI에게 코드를 요청할 때 "API 키는 BaseSettings와 환경 변수에서 가져와줘"라고 반드시 명시합니다.

> **⚠️ 주의:** `.env.example` 파일을 만들어 필요한 환경 변수의 목록을 공유하되, 실제 값은 절대 포함하지 마십시오.

```text
# .env.example (이 파일은 Git에 커밋해도 됩니다)
OPENAI_API_KEY=your_api_key_here
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
JWT_SECRET_KEY=your_secret_key_here
STRIPE_API_KEY=your_stripe_key_here
```

---

## 8-4. 충분하지 않은 키 길이

### 개요

암호화 키의 길이(Key Length)는 암호화의 강도를 결정하는 핵심 요소입니다. 아무리 안전한 알고리즘을 사용하더라도 키 길이가 충분하지 않으면, 공격자가 모든 가능한 키를 시도하는 브루트포스 공격으로 암호를 해독할 수 있습니다.

### 왜 위험한가

짧은 키 길이를 사용하면 공격자가 합리적인 시간 내에 모든 키 조합을 시도할 수 있습니다. 예를 들어 RSA 1024비트 키는 이미 안전하지 않은 것으로 분류되어 있으며, 2030년 이후에는 RSA 2048비트도 재검토가 필요할 수 있습니다.

### 권장 키 길이 표

다음은 알고리즘별 최소 권장 키 길이입니다.

| 알고리즘 유형 | 알고리즘 | ❌ 취약한 키 길이 | ✅ 권장 키 길이 |
|---|---|---|---|
| 대칭키 암호(Symmetric) | AES | 64비트 이하 | **128비트 이상** (권장 256비트) |
| 비대칭키 암호(Asymmetric) | RSA | 1024비트 이하 | **2048비트 이상** (권장 3072비트) |
| 비대칭키 암호 | DSA | 1024비트 이하 | **2048비트 이상** |
| 타원곡선 암호(ECC) | ECDSA | 160비트 이하 | **224비트 이상** (권장 256비트) |
| 해시 함수(Hash) | SHA | SHA-1 (160비트) | **SHA-256 이상** |

### 취약 코드

```python
# ❌ 취약한 코드: RSA 1024비트 키로 JWT 서명
from Crypto.PublicKey import RSA

def generate_jwt_keys():
    # 1024비트는 현대 컴퓨터로 해독 가능
    private_key = RSA.generate(1024)
    return private_key.export_key(), private_key.publickey().export_key()
```

### 안전 코드

```python
# ✅ 안전한 코드: RSA 2048비트 이상 키로 JWT 서명
from Crypto.PublicKey import RSA

def generate_jwt_keys():
    # 2048비트 이상으로 설정 (권장: 3072비트 이상)
    private_key = RSA.generate(2048)
    return private_key.export_key(), private_key.publickey().export_key()
```

```python
# ✅ 안전한 코드: python-jose에서 RS256 사용 시 충분한 키 길이 확보
from jose import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_rsa_keys():
    """FastAPI JWT 인증에 사용할 RSA 키 쌍을 생성합니다."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,  # 최소 2048비트
    )
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem
```

### 바이브 코딩 시 체크포인트

- [ ] AI가 생성한 암호화 코드에서 키 길이 설정값을 확인합니다.
- [ ] RSA는 최소 2048비트, AES는 최소 128비트, ECC는 최소 224비트인지 확인합니다.
- [ ] `RSA.generate()`, `rsa.generate_private_key()` 등의 함수 호출에서 키 크기 인자를 반드시 확인합니다.
- [ ] AI에게 "RSA 2048비트 이상으로 키를 생성해줘"라고 명시합니다.

> **💡 팁:** 2030년 이후까지의 안전성을 고려한다면 RSA 3072비트, AES 256비트를 사용하는 것이 바람직합니다.
