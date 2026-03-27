# Chapter 09. 난수, 패스워드, 그리고 인증 방어

## 9-1. 적절하지 않은 난수 값 사용

### 개요

난수(Random Number)는 세션 ID, 인증 토큰(Token), 암호화 키, 비밀번호 재설정 링크 등 보안에 민감한 다양한 곳에서 사용됩니다. 문제는 파이썬(Python)의 `random` 모듈이 생성하는 난수는 **의사 난수(Pseudo-Random Number)**로, 시드(Seed) 값을 알면 생성되는 모든 숫자를 예측할 수 있다는 것입니다.

바이브 코딩에서 AI에게 "랜덤 토큰을 생성해줘"라고 요청하면, AI는 종종 `random` 모듈을 사용하는 코드를 생성합니다. 이는 게임이나 시뮬레이션에서는 충분하지만, 보안 목적으로는 절대 사용해서는 안 됩니다.

### 왜 위험한가

예측 가능한 난수를 보안 목적으로 사용하면 다음과 같은 공격이 가능합니다.

- **세션 하이재킹(Session Hijacking)**: 세션 ID 생성에 `random`을 사용하면, 공격자가 다른 사용자의 세션 ID를 예측하여 로그인 상태를 탈취할 수 있습니다.
- **토큰 위조(Token Forgery)**: 패스워드 재설정 토큰이 예측 가능하면, 공격자가 다른 사용자의 패스워드를 재설정할 수 있습니다.
- **암호화 키 추측**: 암호화 키가 예측 가능한 난수로 생성되면 암호화 자체가 무력화됩니다.

### 취약한 코드

다음은 `random` 모듈로 보안 토큰을 생성하는 ❌ 취약한 코드입니다.

```python
# ❌ 취약한 코드: 보안 목적에 random 모듈 사용
import random
import string

def generate_session_id():
    # random 모듈은 예측 가능한 의사 난수를 생성
    random.seed(42)  # 고정 시드: 항상 같은 값이 생성됨
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

def generate_reset_token():
    # 시드를 설정하지 않아도 random은 보안용으로 부적합
    return str(random.randint(100000, 999999))
```

### 안전한 코드

보안 목적에 적합한 `secrets` 모듈을 사용하는 ✅ 안전한 코드입니다.

```python
# ✅ 안전한 코드: secrets 모듈로 안전한 난수 생성
import secrets
import string

def generate_session_id():
    # secrets 모듈은 암호학적으로 안전한 난수를 생성
    return secrets.token_hex(32)  # 64자의 16진수 문자열

def generate_reset_token():
    # URL에서 사용하기 안전한 토큰 생성
    return secrets.token_urlsafe(32)

def generate_otp():
    # 6자리 숫자 OTP 생성
    return ''.join([str(secrets.randbelow(10)) for _ in range(6)])

def generate_api_key():
    # API 키 생성
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(48))
```

> **💡 팁:** Python 3.6 미만의 환경에서는 `secrets` 모듈을 사용할 수 없습니다. 이 경우 `os.urandom()` 또는 `random.SystemRandom` 클래스를 사용하십시오.

```python
# Python 3.6 미만에서의 대안
import os
import binascii

def generate_token():
    return binascii.hexlify(os.urandom(32)).decode()
```

### 바이브 코딩 시 체크포인트

- [ ] AI가 생성한 코드에서 `import random`이 보안 관련 기능(토큰, 세션, 키 생성)에 사용되고 있지 않은지 확인합니다.
- [ ] 보안 관련 난수 생성에는 반드시 `secrets` 모듈을 사용합니다.
- [ ] `random.seed()`에 고정 값이 설정되어 있지 않은지 확인합니다.
- [ ] AI에게 "보안 토큰이니 secrets 모듈을 사용해줘"라고 명시합니다.

---

## 9-2. 취약한 패스워드 허용

### 개요

패스워드 정책(Password Policy)은 사용자가 설정하는 패스워드의 최소 요구 사항을 정의하는 규칙입니다. "1234", "password", "qwerty"와 같은 취약한 패스워드를 허용하면, 아무리 강력한 암호화를 적용하더라도 브루트포스 공격이나 사전 공격(Dictionary Attack)에 의해 쉽게 뚫릴 수 있습니다.

바이브 코딩에서 AI가 회원가입 기능을 생성할 때, 패스워드 유효성 검증(Validation) 로직을 포함하지 않는 경우가 많습니다. 사용자가 입력한 패스워드를 검증 없이 그대로 저장하는 것은 보안의 기본을 무시하는 것입니다.

### 왜 위험한가

- **사전 공격**: 흔히 사용되는 패스워드 목록을 대입하여 계정을 탈취합니다. "password123" 같은 패스워드는 수 초 만에 뚫립니다.
- **크리덴셜 스터핑(Credential Stuffing)**: 다른 사이트에서 유출된 패스워드를 그대로 시도합니다. 약한 패스워드일수록 여러 사이트에서 재사용될 확률이 높습니다.
- **레인보우 테이블 공격**: 짧고 단순한 패스워드는 이미 해시값이 계산되어 있는 테이블로 즉시 역추적 가능합니다.

### 취약한 코드

```python
# ❌ 취약한 코드: 패스워드 정책 없이 가입 허용
def register(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    # 패스워드 강도 확인 없이 바로 저장
    create_user(username, password)
    return redirect('/login')
```

### 안전한 코드

패스워드 정책을 적용하는 ✅ 안전한 코드입니다.

```python
# ✅ 안전한 코드: 패스워드 정책 적용
import re

def validate_password(password):
    """패스워드 정책 검증"""
    errors = []

    if len(password) < 8:
        errors.append("패스워드는 최소 8자 이상이어야 합니다.")
    if len(password) > 128:
        errors.append("패스워드는 128자를 초과할 수 없습니다.")
    if not re.search(r'[A-Z]', password):
        errors.append("대문자를 최소 1개 포함해야 합니다.")
    if not re.search(r'[a-z]', password):
        errors.append("소문자를 최소 1개 포함해야 합니다.")
    if not re.search(r'[0-9]', password):
        errors.append("숫자를 최소 1개 포함해야 합니다.")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("특수문자를 최소 1개 포함해야 합니다.")

    # 흔히 사용되는 취약한 패스워드 차단
    common_passwords = ['password', '123456', 'qwerty', 'abc123', 'password123']
    if password.lower() in common_passwords:
        errors.append("너무 흔한 패스워드입니다. 다른 패스워드를 사용해주세요.")

    return errors

def register(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    errors = validate_password(password)
    if errors:
        return render(request, 'register.html', {'errors': errors})

    create_user(username, password)
    return redirect('/login')
```

Django를 사용하는 경우 내장된 패스워드 검증기(Password Validator)를 활용할 수 있습니다.

```python
# ✅ Django settings.py에서 패스워드 검증기 설정
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
```

### 바이브 코딩 시 체크포인트

- [ ] 회원가입 및 패스워드 변경 기능에 패스워드 강도 검증 로직이 포함되어 있는지 확인합니다.
- [ ] 최소 8자 이상, 대소문자/숫자/특수문자 조합을 요구하는지 확인합니다.
- [ ] 흔히 사용되는 패스워드(Common Password)를 차단하는 로직이 있는지 확인합니다.
- [ ] Django의 경우 `AUTH_PASSWORD_VALIDATORS` 설정을 활용합니다.

---

## 9-3. 솔트 없는 일방향 해시 함수 사용

패스워드 해싱 흐름도는 `diagram.md`를 참고하십시오.

### 개요

일방향 해시 함수(One-way Hash Function)는 원본 데이터를 복원할 수 없는 고정 길이의 해시값으로 변환합니다. 패스워드 저장에 널리 사용되지만, 솔트(Salt) 없이 해시만 적용하면 **레인보우 테이블 공격**에 취약합니다.

솔트란 해시 계산 전에 원본 데이터에 추가하는 무작위 문자열입니다. 같은 패스워드라도 솔트가 다르면 완전히 다른 해시값이 생성되므로, 사전 계산된 해시 테이블을 무력화합니다.

### 왜 위험한가

- **레인보우 테이블 공격**: 솔트 없는 SHA-256 해시값은 이미 계산된 거대한 테이블에서 원문을 찾아낼 수 있습니다.
- **동일 해시값 문제**: 같은 패스워드를 사용하는 모든 사용자의 해시값이 동일하게 됩니다. 하나의 해시가 해독되면 같은 패스워드를 사용하는 모든 계정이 노출됩니다.
- **GPU 가속 공격**: 단순 해시 함수(SHA-256 등)는 GPU를 활용하면 초당 수십억 개의 해시를 계산할 수 있어, 브루트포스 공격에 취약합니다.

### 취약한 코드

```python
# ❌ 취약한 코드: 솔트 없이 단순 SHA-256 해시만 사용
import hashlib

def hash_password(password):
    # 솔트 없이 해시하면 레인보우 테이블 공격에 취약
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(password, stored_hash):
    return hash_password(password) == stored_hash
```

### 안전한 코드

bcrypt 또는 argon2를 사용하는 ✅ 안전한 코드입니다. 이 라이브러리들은 솔트를 자동으로 생성하고, **키 스트레칭(Key Stretching)** 기법으로 해시 계산 속도를 의도적으로 느리게 만들어 브루트포스 공격을 어렵게 합니다.

```python
# ✅ 안전한 코드: bcrypt 사용 (솔트 자동 생성 + 키 스트레칭)
import bcrypt

def hash_password(password):
    # bcrypt는 솔트를 자동으로 생성하고 해시에 포함시킴
    salt = bcrypt.gensalt(rounds=12)  # rounds가 높을수록 느리고 안전
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password, stored_hash):
    return bcrypt.checkpw(
        password.encode('utf-8'),
        stored_hash.encode('utf-8')
    )
```

```python
# ✅ 안전한 코드: argon2 사용 (현재 가장 권장되는 알고리즘)
from argon2 import PasswordHasher

ph = PasswordHasher(
    time_cost=3,        # 반복 횟수
    memory_cost=65536,  # 메모리 사용량 (KB)
    parallelism=4       # 병렬 처리 수
)

def hash_password(password):
    # argon2는 솔트 자동 생성 + 메모리 하드(Memory-hard) 함수
    return ph.hash(password)

def verify_password(password, stored_hash):
    try:
        return ph.verify(stored_hash, password)
    except Exception:
        return False
```

> **💡 팁:** 패스워드 해싱 알고리즘의 권장 순위는 **Argon2 > bcrypt > scrypt > PBKDF2** 순입니다. 가능하다면 Argon2를 사용하십시오. `pip install argon2-cffi`로 설치할 수 있습니다.

### 바이브 코딩 시 체크포인트

- [ ] `hashlib.sha256(password)`처럼 솔트 없이 단순 해시만 사용하는 코드가 없는지 확인합니다.
- [ ] 패스워드 저장에는 반드시 `bcrypt`, `argon2`, 또는 `scrypt`를 사용합니다.
- [ ] Django의 경우 기본 패스워드 해시가 PBKDF2를 사용하므로, 필요 시 Argon2로 업그레이드합니다.
- [ ] AI에게 "패스워드 해싱에 bcrypt를 사용해줘"라고 명시합니다.

---

## 9-4. 반복된 인증시도 제한 기능 부재

### 개요

레이트 리미팅(Rate Limiting)이란 특정 시간 내에 허용되는 요청 횟수를 제한하는 기법입니다. 로그인 시도에 횟수 제한이 없으면, 공격자는 수백만 개의 패스워드를 자동으로 시도하는 브루트포스 공격(Brute-Force Attack)을 수행할 수 있습니다.

바이브 코딩으로 로그인 기능을 만들 때, AI는 보통 아이디와 패스워드를 확인하는 로직만 생성하고, 반복 시도에 대한 제한을 포함하지 않습니다.

### 왜 위험한가

- **브루트포스 공격**: 초당 수천 건의 로그인 시도로 패스워드를 알아낼 수 있습니다.
- **크리덴셜 스터핑**: 유출된 대량의 계정 정보를 자동으로 시도합니다.
- **서비스 거부(DoS)**: 대량의 로그인 요청으로 서버 자원이 고갈될 수 있습니다.
- **계정 잠금 우회**: 제한이 없으면 공격자는 시간 제약 없이 무한히 시도할 수 있습니다.

### 취약한 코드

```python
# ❌ 취약한 코드: 로그인 시도 횟수 제한 없음
from django.shortcuts import render, redirect

def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    # 횟수 제한 없이 무한히 로그인 시도 가능
    user = authenticate(username=username, password=password)
    if user:
        auth_login(request, user)
        return redirect('/dashboard')
    return render(request, 'login.html', {'error': '로그인 실패'})
```

### 안전한 코드

로그인 시도 횟수를 제한하는 ✅ 안전한 코드입니다.

```python
# ✅ 안전한 코드: django-axes를 활용한 로그인 시도 제한
# pip install django-axes

# settings.py
INSTALLED_APPS = [
    # ...
    'axes',
]

MIDDLEWARE = [
    # AxesMiddleware는 가장 마지막에 위치
    # ...
    'axes.middleware.AxesMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# 5회 실패 시 계정 잠금
AXES_FAILURE_LIMIT = 5
# 30분 후 자동 잠금 해제
AXES_COOLOFF_TIME = 0.5  # 시간 단위 (0.5 = 30분)
# IP 기반 + 사용자명 기반 제한
AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = True
```

Django를 사용하지 않는 경우 직접 구현할 수 있습니다.

```python
# ✅ 안전한 코드: 직접 구현한 레이트 리미팅
import time
from collections import defaultdict

class LoginRateLimiter:
    def __init__(self, max_attempts=5, lockout_duration=1800):
        self.max_attempts = max_attempts
        self.lockout_duration = lockout_duration  # 초 단위 (1800 = 30분)
        self.attempts = defaultdict(list)

    def is_locked(self, identifier):
        """계정이 잠겨 있는지 확인"""
        now = time.time()
        # 잠금 기간이 지난 시도 기록 제거
        self.attempts[identifier] = [
            t for t in self.attempts[identifier]
            if now - t < self.lockout_duration
        ]
        return len(self.attempts[identifier]) >= self.max_attempts

    def record_failure(self, identifier):
        """실패한 시도 기록"""
        self.attempts[identifier].append(time.time())

    def reset(self, identifier):
        """로그인 성공 시 기록 초기화"""
        self.attempts[identifier] = []

limiter = LoginRateLimiter()

def login(request):
    username = request.POST.get('username')
    client_ip = request.META.get('REMOTE_ADDR')
    identifier = f"{username}:{client_ip}"

    if limiter.is_locked(identifier):
        return render(request, 'login.html', {
            'error': '로그인 시도 횟수를 초과했습니다. 30분 후 다시 시도해주세요.'
        })

    user = authenticate(username=username, password=request.POST.get('password'))
    if user:
        limiter.reset(identifier)
        auth_login(request, user)
        return redirect('/dashboard')

    limiter.record_failure(identifier)
    remaining = limiter.max_attempts - len(limiter.attempts[identifier])
    return render(request, 'login.html', {
        'error': f'로그인 실패. 남은 시도 횟수: {remaining}회'
    })
```

FastAPI에서는 `slowapi` 라이브러리를 사용하여 레이트 리미팅을 적용할 수 있습니다.

```python
# ✅ FastAPI에서의 레이트 리미팅
# pip install slowapi
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/login")
@limiter.limit("5/minute")  # 분당 5회로 제한
async def login(request: Request, credentials: LoginRequest):
    user = await authenticate(credentials.username, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="로그인 실패")
    return {"token": create_token(user)}
```

### 바이브 코딩 시 체크포인트

- [ ] 로그인 기능에 시도 횟수 제한이 적용되어 있는지 확인합니다.
- [ ] Django 프로젝트의 경우 `django-axes` 라이브러리를 설치하여 활용합니다.
- [ ] 일정 횟수 이상 실패 시 계정 잠금 또는 CAPTCHA 도입을 고려합니다.
- [ ] 로그인 실패 시 "아이디 또는 패스워드가 틀렸습니다"와 같이 어떤 정보가 틀렸는지 구분하지 않는 메시지를 사용합니다.
- [ ] AI에게 "로그인 시도 횟수 제한을 포함해줘"라고 명시합니다.

> **⚠️ 주의:** 로그인 실패 메시지에서 "아이디가 존재하지 않습니다" 또는 "패스워드가 틀렸습니다"처럼 구체적인 정보를 제공하면, 공격자가 유효한 아이디를 식별하는 데 악용할 수 있습니다. 항상 모호한 메시지를 사용하십시오.
