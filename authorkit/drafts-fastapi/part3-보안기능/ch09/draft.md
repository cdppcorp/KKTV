# Chapter 09. 난수, 패스워드, 그리고 인증 방어

## 9-1. 적절하지 않은 난수 값 사용

### 개요

난수(Random Number)는 세션 ID, 인증 토큰(Token), 암호화 키, 비밀번호 재설정 링크 등 보안에 민감한 다양한 곳에서 사용됩니다. 문제는 파이썬(Python)의 `random` 모듈이 생성하는 난수는 **의사 난수(Pseudo-Random Number)**로, 시드(Seed) 값을 알면 생성되는 모든 숫자를 예측할 수 있다는 것입니다.

바이브 코딩에서 AI에게 "랜덤 토큰을 생성해줘"라고 요청하면, AI는 종종 `random` 모듈을 사용하는 코드를 생성합니다. 이는 게임이나 시뮬레이션에서는 충분하지만, FastAPI의 JWT 시크릿 키 생성이나 패스워드 재설정 토큰 등 보안 목적으로는 절대 사용해서는 안 됩니다.

### 왜 위험한가

예측 가능한 난수를 보안 목적으로 사용하면 다음과 같은 공격이 가능합니다.

- **세션 하이재킹(Session Hijacking)**: 세션 ID 생성에 `random`을 사용하면, 공격자가 다른 사용자의 세션 ID를 예측하여 로그인 상태를 탈취할 수 있습니다.
- **토큰 위조(Token Forgery)**: 패스워드 재설정 토큰이 예측 가능하면, 공격자가 다른 사용자의 패스워드를 재설정할 수 있습니다.
- **암호화 키 추측**: JWT 시크릿 키가 예측 가능한 난수로 생성되면 토큰 위조가 가능해집니다.

### 취약 코드

다음은 `random` 모듈로 보안 토큰을 생성하는 ❌ 취약한 코드입니다.

```python
# ❌ 취약한 코드: 보안 목적에 random 모듈 사용
import random
import string
from fastapi import FastAPI

app = FastAPI()

def generate_reset_token():
    # random 모듈은 예측 가능한 의사 난수를 생성
    return str(random.randint(100000, 999999))

def generate_jwt_secret():
    # 고정 시드: 항상 같은 값이 생성됨
    random.seed(42)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

@app.post("/forgot-password")
async def forgot_password(email: str):
    token = generate_reset_token()  # 예측 가능한 토큰
    send_reset_email(email, token)
    return {"message": "재설정 이메일을 발송했습니다."}
```

### 안전 코드

보안 목적에 적합한 `secrets` 모듈을 사용하는 ✅ 안전한 코드입니다.

```python
# ✅ 안전한 코드: secrets 모듈로 안전한 난수 생성
import secrets
import string
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

app = FastAPI()

def generate_reset_token() -> str:
    """암호학적으로 안전한 패스워드 재설정 토큰을 생성합니다."""
    return secrets.token_urlsafe(32)

def generate_jwt_secret() -> str:
    """JWT 시크릿 키를 안전하게 생성합니다."""
    return secrets.token_hex(32)  # 64자의 16진수 문자열

def generate_otp() -> str:
    """6자리 숫자 OTP를 생성합니다."""
    return ''.join([str(secrets.randbelow(10)) for _ in range(6)])

def generate_api_key() -> str:
    """API 키를 안전하게 생성합니다."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(48))

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

@app.post("/forgot-password")
async def forgot_password(
    data: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == data.email).first()
    if user:
        token = generate_reset_token()  # 암호학적으로 안전한 토큰
        user.reset_token = token
        user.reset_token_expires = datetime.now(timezone.utc) + timedelta(hours=1)
        db.commit()
        send_reset_email(data.email, token)

    # 사용자 존재 여부와 관계없이 동일한 응답 반환 (정보 노출 방지)
    return {"message": "등록된 이메일이라면 재설정 링크가 발송됩니다."}
```

> **💡 팁:** Python 3.6 이상에서는 항상 `secrets` 모듈을 사용하십시오. FastAPI 프로젝트의 `.env` 파일에 들어갈 JWT 시크릿 키도 `python -c "import secrets; print(secrets.token_hex(32))"`로 생성하는 것을 권장합니다.

### 바이브 코딩 시 체크포인트

- [ ] AI가 생성한 코드에서 `import random`이 보안 관련 기능(토큰, 세션, 키 생성)에 사용되고 있지 않은지 확인합니다.
- [ ] 보안 관련 난수 생성에는 반드시 `secrets` 모듈을 사용합니다.
- [ ] `random.seed()`에 고정 값이 설정되어 있지 않은지 확인합니다.
- [ ] AI에게 "보안 토큰이니 secrets 모듈을 사용해줘"라고 명시합니다.

---

## 9-2. 취약한 패스워드 허용

### 개요

패스워드 정책(Password Policy)은 사용자가 설정하는 패스워드의 최소 요구 사항을 정의하는 규칙입니다. "1234", "password", "qwerty"와 같은 취약한 패스워드를 허용하면, 아무리 강력한 암호화를 적용하더라도 브루트포스 공격이나 사전 공격(Dictionary Attack)에 의해 쉽게 뚫릴 수 있습니다.

바이브 코딩에서 AI가 회원가입 API를 생성할 때, 패스워드 유효성 검증(Validation) 로직을 포함하지 않는 경우가 많습니다. FastAPI에서는 Pydantic의 `field_validator`를 활용하여 패스워드 정책을 깔끔하게 구현할 수 있습니다.

### 왜 위험한가

- **사전 공격**: 흔히 사용되는 패스워드 목록을 대입하여 계정을 탈취합니다. "password123" 같은 패스워드는 수 초 만에 뚫립니다.
- **크리덴셜 스터핑(Credential Stuffing)**: 다른 사이트에서 유출된 패스워드를 그대로 시도합니다. 약한 패스워드일수록 여러 사이트에서 재사용될 확률이 높습니다.
- **레인보우 테이블 공격**: 짧고 단순한 패스워드는 이미 해시값이 계산되어 있는 테이블로 즉시 역추적 가능합니다.

### 취약 코드

```python
# ❌ 취약한 코드: 패스워드 정책 없이 가입 허용
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
    username: str
    password: str  # 아무런 검증 없음

@app.post("/register")
async def register(user: UserCreate):
    # 패스워드 강도 확인 없이 바로 저장
    create_user(user.username, user.password)
    return {"message": "가입 완료"}
```

### 안전 코드

Pydantic의 `field_validator`를 활용하여 패스워드 정책을 적용하는 ✅ 안전한 코드입니다.

```python
# ✅ 안전한 코드: Pydantic field_validator로 패스워드 정책 적용
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, SecretStr, field_validator
from passlib.context import CryptContext

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

COMMON_PASSWORDS = {"password", "123456", "qwerty", "abc123", "password123",
                    "admin", "letmein", "welcome", "monkey", "dragon"}

class UserCreate(BaseModel):
    username: str
    password: SecretStr

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: SecretStr) -> SecretStr:
        """패스워드 정책을 검증합니다."""
        password = v.get_secret_value()
        errors = []

        if len(password) < 8:
            errors.append("패스워드는 최소 8자 이상이어야 합니다.")
        if len(password) > 128:
            errors.append("패스워드는 128자를 초과할 수 없습니다.")
        if not re.search(r"[A-Z]", password):
            errors.append("대문자를 최소 1개 포함해야 합니다.")
        if not re.search(r"[a-z]", password):
            errors.append("소문자를 최소 1개 포함해야 합니다.")
        if not re.search(r"[0-9]", password):
            errors.append("숫자를 최소 1개 포함해야 합니다.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("특수문자를 최소 1개 포함해야 합니다.")
        if password.lower() in COMMON_PASSWORDS:
            errors.append("너무 흔한 패스워드입니다. 다른 패스워드를 사용해주세요.")

        if errors:
            raise ValueError("; ".join(errors))
        return v

@app.post("/register")
async def register(user: UserCreate):
    # Pydantic 검증을 통과한 패스워드만 여기에 도달
    hashed = pwd_context.hash(user.password.get_secret_value())
    create_user(user.username, hashed)
    return {"message": "가입 완료"}
```

Pydantic의 `field_validator`를 사용하면 FastAPI가 요청 데이터를 역직렬화하는 시점에 자동으로 패스워드 정책이 검증됩니다. 검증에 실패하면 422 Unprocessable Entity 응답이 상세한 오류 메시지와 함께 반환됩니다.

### 바이브 코딩 시 체크포인트

- [ ] 회원가입 및 패스워드 변경 API에 패스워드 강도 검증 로직이 포함되어 있는지 확인합니다.
- [ ] 최소 8자 이상, 대소문자/숫자/특수문자 조합을 요구하는지 확인합니다.
- [ ] 흔히 사용되는 패스워드(Common Password)를 차단하는 로직이 있는지 확인합니다.
- [ ] Pydantic `field_validator`를 활용하여 모델 레벨에서 검증이 이루어지는지 확인합니다.

---

## 9-3. 솔트 없는 일방향 해시 함수 사용

### 개요

일방향 해시 함수(One-way Hash Function)는 원본 데이터를 복원할 수 없는 고정 길이의 해시값으로 변환합니다. 패스워드 저장에 널리 사용되지만, 솔트(Salt) 없이 해시만 적용하면 **레인보우 테이블 공격**에 취약합니다.

솔트란 해시 계산 전에 원본 데이터에 추가하는 무작위 문자열입니다. 같은 패스워드라도 솔트가 다르면 완전히 다른 해시값이 생성되므로, 사전 계산된 해시 테이블을 무력화합니다.

### 왜 위험한가

- **레인보우 테이블 공격**: 솔트 없는 SHA-256 해시값은 이미 계산된 거대한 테이블에서 원문을 찾아낼 수 있습니다.
- **동일 해시값 문제**: 같은 패스워드를 사용하는 모든 사용자의 해시값이 동일하게 됩니다. 하나의 해시가 해독되면 같은 패스워드를 사용하는 모든 계정이 노출됩니다.
- **GPU 가속 공격**: 단순 해시 함수(SHA-256 등)는 GPU를 활용하면 초당 수십억 개의 해시를 계산할 수 있어, 브루트포스 공격에 취약합니다.

### 취약 코드

```python
# ❌ 취약한 코드: FastAPI에서 솔트 없이 단순 SHA-256 해시만 사용
import hashlib
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
    username: str
    password: str

@app.post("/register")
async def register(user: UserCreate):
    # 솔트 없이 해시하면 레인보우 테이블 공격에 취약
    hashed = hashlib.sha256(user.password.encode("utf-8")).hexdigest()
    save_user(user.username, hashed)
    return {"message": "가입 완료"}

@app.post("/login")
async def login(user: UserCreate):
    stored_hash = get_stored_hash(user.username)
    input_hash = hashlib.sha256(user.password.encode("utf-8")).hexdigest()
    if input_hash != stored_hash:
        raise HTTPException(status_code=401, detail="로그인 실패")
    return {"message": "로그인 성공"}
```

### 안전 코드

FastAPI에서 `passlib` + bcrypt를 사용하는 ✅ 안전한 코드입니다. `passlib`은 솔트를 자동으로 생성하고, **키 스트레칭(Key Stretching)** 기법으로 해시 계산 속도를 의도적으로 느리게 만들어 브루트포스 공격을 어렵게 합니다.

```python
# ✅ 안전한 코드: passlib + bcrypt 사용 (솔트 자동 생성 + 키 스트레칭)
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel, SecretStr
from jose import jwt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SECRET_KEY = settings.jwt_secret_key.get_secret_value()
ALGORITHM = "HS256"

class UserCreate(BaseModel):
    username: str
    password: SecretStr

@app.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # bcrypt는 솔트를 자동으로 생성하고 해시에 포함시킴
    hashed = pwd_context.hash(user.password.get_secret_value())
    new_user = User(username=user.username, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    return {"message": "가입 완료"}

@app.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 또는 패스워드가 올바르지 않습니다.",
        )
    access_token = jwt.encode(
        {"sub": str(user.id), "exp": datetime.now(timezone.utc) + timedelta(hours=1)},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return {"access_token": access_token, "token_type": "bearer"}
```

`passlib`의 `CryptContext`는 해시 알고리즘의 업그레이드도 자동으로 처리합니다. `deprecated="auto"` 옵션을 설정하면, 로그인 시 이전 알고리즘으로 해시된 패스워드를 새 알고리즘으로 자동 갱신합니다.

> **💡 팁:** 패스워드 해싱 알고리즘의 권장 순위는 **Argon2 > bcrypt > scrypt > PBKDF2** 순입니다. `passlib`에서는 `CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")`처럼 여러 알고리즘을 지원하며, 첫 번째 스킴이 기본 해싱에 사용됩니다.

### 바이브 코딩 시 체크포인트

- [ ] `hashlib.sha256(password)`처럼 솔트 없이 단순 해시만 사용하는 코드가 없는지 확인합니다.
- [ ] 패스워드 저장에는 반드시 `passlib`의 `CryptContext(schemes=["bcrypt"])`를 사용합니다.
- [ ] `pwd_context.verify()`를 사용하여 패스워드를 검증하는지 확인합니다.
- [ ] AI에게 "패스워드 해싱에 passlib과 bcrypt를 사용해줘"라고 명시합니다.

---

## 9-4. 반복된 인증시도 제한 기능 부재

### 개요

레이트 리미팅(Rate Limiting)이란 특정 시간 내에 허용되는 요청 횟수를 제한하는 기법입니다. 로그인 시도에 횟수 제한이 없으면, 공격자는 수백만 개의 패스워드를 자동으로 시도하는 브루트포스 공격(Brute-Force Attack)을 수행할 수 있습니다.

바이브 코딩으로 FastAPI 로그인 기능을 만들 때, AI는 보통 아이디와 패스워드를 확인하는 로직만 생성하고, 반복 시도에 대한 제한을 포함하지 않습니다.

### 왜 위험한가

- **브루트포스 공격**: 초당 수천 건의 로그인 시도로 패스워드를 알아낼 수 있습니다.
- **크리덴셜 스터핑**: 유출된 대량의 계정 정보를 자동으로 시도합니다.
- **서비스 거부(DoS)**: 대량의 로그인 요청으로 서버 자원이 고갈될 수 있습니다.
- **계정 잠금 우회**: 제한이 없으면 공격자는 시간 제약 없이 무한히 시도할 수 있습니다.

### 취약 코드

```python
# ❌ 취약한 코드: 로그인 시도 횟수 제한 없음
from fastapi import FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate(form_data.username, form_data.password)
    # 횟수 제한 없이 무한히 로그인 시도 가능
    if not user:
        raise HTTPException(status_code=401, detail="로그인 실패")
    return {"access_token": create_token(user), "token_type": "bearer"}
```

### 안전 코드

FastAPI에서 `slowapi` 라이브러리를 사용하여 레이트 리미팅을 적용하는 ✅ 안전한 코드입니다.

```python
# ✅ 안전한 코드: slowapi를 활용한 레이트 리미팅
# pip install slowapi
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/login")
@limiter.limit("5/minute")  # IP당 분당 5회로 제한
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 또는 패스워드가 올바르지 않습니다.",
        )
    access_token = create_access_token(user)
    return {"access_token": access_token, "token_type": "bearer"}
```

더 세밀한 제어가 필요한 경우 사용자별 로그인 시도 횟수를 직접 관리할 수 있습니다.

```python
# ✅ 안전한 코드: 사용자별 로그인 시도 횟수 관리
from fastapi import FastAPI, Depends, HTTPException, status
from datetime import datetime, timedelta, timezone
from collections import defaultdict

app = FastAPI()

class LoginRateLimiter:
    def __init__(self, max_attempts: int = 5, lockout_minutes: int = 30):
        self.max_attempts = max_attempts
        self.lockout_duration = timedelta(minutes=lockout_minutes)
        self.attempts: dict[str, list[datetime]] = defaultdict(list)

    def is_locked(self, identifier: str) -> bool:
        now = datetime.now(timezone.utc)
        self.attempts[identifier] = [
            t for t in self.attempts[identifier]
            if now - t < self.lockout_duration
        ]
        return len(self.attempts[identifier]) >= self.max_attempts

    def record_failure(self, identifier: str) -> None:
        self.attempts[identifier].append(datetime.now(timezone.utc))

    def reset(self, identifier: str) -> None:
        self.attempts[identifier] = []

    def remaining_attempts(self, identifier: str) -> int:
        return max(0, self.max_attempts - len(self.attempts[identifier]))

login_limiter = LoginRateLimiter()

@app.post("/login")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    client_ip = request.client.host
    identifier = f"{form_data.username}:{client_ip}"

    if login_limiter.is_locked(identifier):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="로그인 시도 횟수를 초과했습니다. 30분 후 다시 시도해주세요.",
        )

    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        login_limiter.record_failure(identifier)
        remaining = login_limiter.remaining_attempts(identifier)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"아이디 또는 패스워드가 올바르지 않습니다. 남은 시도: {remaining}회",
        )

    login_limiter.reset(identifier)
    access_token = create_access_token(user)
    return {"access_token": access_token, "token_type": "bearer"}
```

### 바이브 코딩 시 체크포인트

- [ ] 로그인 엔드포인트에 `slowapi`의 `@limiter.limit()` 데코레이터가 적용되어 있는지 확인합니다.
- [ ] 일정 횟수 이상 실패 시 계정 잠금 또는 CAPTCHA 도입을 고려합니다.
- [ ] 로그인 실패 시 "아이디 또는 패스워드가 올바르지 않습니다"와 같이 어떤 정보가 틀렸는지 구분하지 않는 메시지를 사용합니다.
- [ ] AI에게 "로그인 시도 횟수 제한을 slowapi로 포함해줘"라고 명시합니다.

> **⚠️ 주의:** 로그인 실패 메시지에서 "아이디가 존재하지 않습니다" 또는 "패스워드가 틀렸습니다"처럼 구체적인 정보를 제공하면, 공격자가 유효한 아이디를 식별하는 데 악용할 수 있습니다. 항상 모호한 메시지를 사용하십시오.
