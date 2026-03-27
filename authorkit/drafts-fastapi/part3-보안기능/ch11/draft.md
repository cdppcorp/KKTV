# Chapter 11. 정보 노출을 차단하세요

## 11-1. 쿠키를 통한 정보 노출

### 개요

쿠키(Cookie)는 웹 브라우저에 저장되는 작은 데이터로, 로그인 상태 유지, 사용자 설정 저장 등에 사용됩니다. 그러나 쿠키의 보안 속성(Security Flag)을 적절히 설정하지 않으면, 세션 ID나 인증 토큰과 같은 중요 정보가 공격자에게 노출될 수 있습니다.

바이브 코딩에서 AI가 FastAPI의 쿠키 기반 인증 코드를 생성할 때, 쿠키의 보안 속성을 제대로 설정하지 않는 경우가 매우 빈번합니다. AI는 기능적으로 동작하는 코드를 우선시하기 때문에, `httponly`, `secure`, `samesite`와 같은 보안 속성을 생략하는 경향이 있습니다.

### 왜 위험한가

쿠키 보안 속성이 미설정된 경우 다음과 같은 공격이 가능합니다.

- **XSS(Cross-Site Scripting)를 통한 세션 탈취**: `HttpOnly` 속성이 없으면, 자바스크립트(JavaScript)에서 `document.cookie`로 쿠키에 접근할 수 있습니다. 공격자가 XSS 취약점을 이용하여 사용자의 JWT 토큰을 탈취할 수 있습니다.
- **네트워크 도청을 통한 쿠키 유출**: `Secure` 속성이 없으면, HTTP(평문) 연결에서도 쿠키가 전송됩니다. 공용 WiFi 등에서 패킷 스니핑으로 토큰이 노출될 수 있습니다.
- **CSRF(Cross-Site Request Forgery) 공격**: `SameSite` 속성이 없으면, 악의적인 외부 사이트에서 사용자의 쿠키를 포함한 요청을 보낼 수 있습니다. 사용자 모르게 결제, 회원 탈퇴 등의 요청이 실행될 수 있습니다.

### 취약 코드

다음은 FastAPI에서 쿠키 보안 속성을 설정하지 않은 ❌ 취약한 코드입니다.

```python
# ❌ 취약한 코드: 쿠키 보안 속성 미설정
from fastapi import FastAPI, Response
from jose import jwt

app = FastAPI()

@app.post("/login")
async def login(response: Response):
    user = authenticate(username, password)
    token = jwt.encode(
        {"sub": str(user.id)},
        SECRET_KEY,
        algorithm="HS256",
    )
    # 보안 속성 없이 토큰을 쿠키에 저장
    response.set_cookie("access_token", token)
    return {"message": "로그인 성공"}
```

### 안전 코드

FastAPI의 `Response` 객체에서 모든 보안 속성을 적용한 ✅ 안전한 코드입니다.

```python
# ✅ 안전한 코드: FastAPI에서 쿠키 보안 속성 설정
from fastapi import FastAPI, Response, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/login")
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 또는 패스워드가 올바르지 않습니다.",
        )

    token = jwt.encode(
        {
            "sub": str(user.id),
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        },
        settings.jwt_secret_key.get_secret_value(),
        algorithm="HS256",
    )

    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,     # JavaScript에서 접근 불가
        secure=True,       # HTTPS에서만 전송
        samesite="lax",    # 외부 사이트에서의 요청 시 쿠키 미전송
        max_age=3600,      # 1시간 후 만료
        path="/",
    )
    return {"message": "로그인 성공"}
```

쿠키 기반 인증에서 JWT를 추출하는 의존성 함수도 함께 구현합니다.

```python
# ✅ 쿠키에서 JWT를 추출하여 인증하는 의존성 함수
from fastapi import Cookie

async def get_current_user_from_cookie(
    access_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
):
    """쿠키에서 JWT를 추출하여 현재 사용자를 인증합니다."""
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증이 필요합니다.",
        )

    # "Bearer " 접두사 제거
    token = access_token.replace("Bearer ", "")
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key.get_secret_value(),
            algorithms=["HS256"],
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 인증 정보입니다.",
        )

    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if user is None:
        raise HTTPException(status_code=401, detail="사용자를 찾을 수 없습니다.")
    return user

@app.post("/logout")
async def logout(response: Response):
    """로그아웃 시 쿠키를 안전하게 삭제합니다."""
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
    )
    return {"message": "로그아웃 성공"}
```

각 보안 속성의 역할을 정리하면 다음과 같습니다.

| 속성 | 역할 | 미설정 시 위험 |
|---|---|---|
| `httponly` | JavaScript에서 쿠키 접근 차단 | XSS를 통한 토큰 탈취 |
| `secure` | HTTPS 연결에서만 쿠키 전송 | 네트워크 도청으로 쿠키 유출 |
| `samesite` | 외부 사이트 요청 시 쿠키 전송 제한 | CSRF 공격 |

> **💡 팁:** `samesite` 속성에는 세 가지 값이 있습니다. `strict`는 외부 사이트에서의 모든 요청에 쿠키를 보내지 않습니다(가장 안전하지만 사용자 경험이 불편할 수 있음). `lax`는 GET 요청에 한해 외부 사이트에서도 쿠키를 전송합니다(권장 설정). `none`은 모든 요청에 쿠키를 전송하며, 반드시 `secure=True`와 함께 사용해야 합니다.

### 바이브 코딩 시 체크포인트

- [ ] `response.set_cookie()` 호출 시 `httponly=True`, `secure=True`, `samesite="lax"`가 모두 설정되어 있는지 확인합니다.
- [ ] `max_age`를 설정하여 영구 쿠키를 방지합니다.
- [ ] 로그아웃 시 `response.delete_cookie()`로 쿠키를 삭제하되, 동일한 보안 속성을 지정하는지 확인합니다.
- [ ] 쿠키에 패스워드, 개인정보 등 민감한 정보를 직접 저장하지 않습니다. JWT 토큰만 저장하고, 실제 데이터는 서버 측 데이터베이스에 저장합니다.
- [ ] AI에게 "쿠키 보안 속성(httponly, secure, samesite)을 모두 설정해줘"라고 명시합니다.

---

## 11-2. 주석문 안에 포함된 시스템 주요정보

### 개요

주석(Comment)은 코드의 동작을 설명하기 위해 작성하는 텍스트로, 프로그램 실행에는 영향을 주지 않습니다. 그러나 주석에 패스워드, API 키, 서버 주소, 데이터베이스 접속 정보 등의 중요정보가 포함되어 있으면, 소스코드에 접근한 누구나 이 정보를 확인할 수 있습니다.

**이 문제는 바이브 코딩에서 특히 심각합니다.** AI 코드 생성 도구는 코드를 설명하기 위해 자동으로 주석을 생성하는데, 이 과정에서 다음과 같은 중요정보가 주석에 포함될 수 있습니다.

- AI에게 전달한 프롬프트(Prompt)에 포함된 API 키나 서버 주소
- 코드 예시에서 사용한 실제 접속 정보
- 디버깅 과정에서 남긴 임시 패스워드
- 내부 시스템의 구조나 취약점에 대한 설명

### 왜 위험한가

주석에 포함된 중요정보는 다음과 같은 경로로 유출됩니다.

- **소스코드 저장소 노출**: GitHub 등에 코드를 Push하면, 주석에 포함된 정보도 함께 공개됩니다.
- **API 문서 노출**: FastAPI의 자동 생성 문서(`/docs`, `/redoc`)에 주석 기반 docstring 내용이 노출될 수 있습니다.
- **로그 파일 노출**: 에러 발생 시 traceback에 소스 코드 줄이 포함되어 주석 내용이 노출될 수 있습니다.
- **빌드 산출물 포함**: Docker 이미지에 소스 코드와 주석이 그대로 포함됩니다.

> **⚠️ 주의:** AI는 코드를 설명하기 위해 주석을 매우 적극적으로 생성합니다. 특히 "이 코드는 DATABASE_URL=postgresql://admin:secret@192.168.1.100/mydb에 접속합니다"와 같이 인프라 정보를 주석에 포함하는 경우가 있습니다. AI가 생성한 모든 주석을 반드시 검토하십시오.

### 취약 코드

다음은 AI가 생성할 수 있는 위험한 주석이 포함된 ❌ 취약한 코드입니다.

```python
# ❌ 취약한 코드: 주석에 중요정보 포함
from fastapi import FastAPI
from sqlalchemy import create_engine

app = FastAPI()

# DB 접속 정보: admin / P@ssw0rd123!
# 서버: 192.168.1.100:5432
# TODO: 나중에 환경 변수로 변경하기
# 현재 테스트용 OpenAI 키: sk-proj-abc123xyz456
engine = create_engine(settings.database_url.get_secret_value())

@app.get("/admin/users")
async def get_users():
    """관리자 전용 API (인증 우회: ?debug=true로 접근 가능)"""
    # 이전 JWT 시크릿: my-old-secret-key-2024
    pass
```

### 안전 코드

중요정보가 제거된 ✅ 안전한 코드입니다.

```python
# ✅ 안전한 코드: 주석에 중요정보를 포함하지 않음
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from pydantic_settings import BaseSettings
from pydantic import SecretStr

class Settings(BaseSettings):
    database_url: SecretStr
    jwt_secret_key: SecretStr

    model_config = {"env_file": ".env"}

settings = Settings()
app = FastAPI()
engine = create_engine(settings.database_url.get_secret_value())

@app.get("/admin/users")
async def get_users(
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    """관리자 전용 사용자 목록 조회 API입니다."""
    return db.query(User).all()
```

배포 전에 주석에 포함된 중요정보를 검사하는 스크립트를 활용할 수 있습니다.

```python
# ✅ 주석 내 중요정보 검사 스크립트
import re
import os
from pathlib import Path

SENSITIVE_PATTERNS = [
    r"(?i)password\s*[:=]\s*\S+",        # password: xxx 또는 password=xxx
    r"(?i)api[_-]?key\s*[:=]\s*\S+",     # api_key: xxx
    r"(?i)secret\s*[:=]\s*\S+",          # secret: xxx
    r"sk-[a-zA-Z0-9]{20,}",             # OpenAI API 키 패턴
    r"(?i)token\s*[:=]\s*\S+",           # token: xxx
    r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",  # IP 주소
    r"(?i)admin\s*/\s*\S+",              # admin / password 패턴
    r"postgresql://\S+",                  # DB URL 패턴
]

def scan_comments_in_file(filepath: str) -> list[dict]:
    """파일의 주석에서 민감한 정보를 검사합니다."""
    issues = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            comment_match = re.search(r"#(.+)$", line)
            if comment_match:
                comment = comment_match.group(1)
                for pattern in SENSITIVE_PATTERNS:
                    if re.search(pattern, comment):
                        issues.append({
                            "file": filepath,
                            "line": line_num,
                            "content": line.strip(),
                        })
    return issues

def scan_fastapi_project(project_dir: str) -> list[dict]:
    """FastAPI 프로젝트 전체의 주석을 검사합니다."""
    all_issues = []
    exclude_dirs = {".git", "node_modules", "__pycache__", ".venv", "venv"}

    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for filename in files:
            if filename.endswith((".py", ".js", ".html", ".env.example")):
                filepath = os.path.join(root, filename)
                issues = scan_comments_in_file(filepath)
                all_issues.extend(issues)

    if all_issues:
        print(f"[경고] {len(all_issues)}개의 주석에서 민감한 정보가 발견되었습니다:")
        for issue in all_issues:
            print(f"  - {issue['file']}:{issue['line']}")
            print(f"    {issue['content']}")
    else:
        print("[안전] 주석에서 민감한 정보가 발견되지 않았습니다.")

    return all_issues
```

Git 커밋 전에 자동으로 시크릿을 검사하는 Pre-commit Hook도 활용할 수 있습니다.

```yaml
# ✅ .pre-commit-config.yaml에 시크릿 검사 도구 추가
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```

```bash
# detect-secrets 설치 및 사용
pip install detect-secrets
detect-secrets scan > .secrets.baseline
detect-secrets audit .secrets.baseline
```

### 바이브 코딩 시 체크포인트

- [ ] AI가 생성한 코드의 모든 주석을 검토하여 패스워드, API 키, 서버 주소, 접속 정보가 포함되어 있지 않은지 확인합니다.
- [ ] FastAPI의 docstring(`"""..."""`)에 내부 시스템 정보가 포함되어 있지 않은지 확인합니다. docstring 내용은 `/docs` 페이지에 그대로 노출됩니다.
- [ ] `TODO: 나중에 변경`, `임시 패스워드` 등의 주석이 운영 코드에 남아 있지 않은지 확인합니다.
- [ ] `detect-secrets`를 Pre-commit Hook으로 설정하여 커밋 전에 자동으로 검사합니다.
- [ ] AI에게 프롬프트를 전달할 때, 실제 API 키나 패스워드 대신 `YOUR_API_KEY_HERE`와 같은 플레이스홀더(Placeholder)를 사용합니다.
- [ ] AI가 생성한 코드에서 `# 이전 키:`, `# 테스트 계정:`, `# 접속 정보:` 등의 주석을 즉시 삭제합니다.

> **⚠️ 주의:** AI에게 "이 API 키로 OpenAI를 호출하는 FastAPI 코드를 만들어줘"라고 실제 키를 프롬프트에 포함하면, AI가 그 키를 주석에 포함할 가능성이 높습니다. 또한 AI 서비스의 대화 기록에 여러분의 키가 저장될 수 있습니다. 프롬프트에는 절대로 실제 중요정보를 포함하지 마십시오.

> **💡 팁:** FastAPI의 자동 문서 생성 기능(`/docs`, `/redoc`)은 운영 환경에서는 비활성화하는 것을 권장합니다. `app = FastAPI(docs_url=None, redoc_url=None)`으로 설정하면 API 문서 엔드포인트가 비활성화됩니다. 엔드포인트의 docstring에 포함된 내부 정보가 외부에 노출되는 것을 방지할 수 있습니다.
