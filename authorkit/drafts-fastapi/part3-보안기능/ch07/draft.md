# Chapter 07. 인증과 인가, 그리고 권한 설정

## 7-1. 적절한 인증 없이 중요 기능 허용

### 개요

인증(Authentication)이란 "당신이 누구인지 확인하는 과정"입니다. 여러분이 웹 애플리케이션에 로그인할 때 아이디와 패스워드를 입력하는 것이 가장 대표적인 인증 절차입니다. 문제는 AI 도구로 API를 빠르게 만들다 보면, 중요한 기능에 인증 절차를 빠뜨리는 경우가 빈번하게 발생한다는 것입니다.

예를 들어 "패스워드 변경 API를 만들어줘"라고 AI에게 요청하면, AI는 패스워드를 변경하는 로직은 잘 만들어주지만 **현재 로그인한 사용자인지 확인하는 과정**을 생략하는 경우가 많습니다. FastAPI에서는 `Depends()`를 활용한 의존성 주입으로 인증을 처리하는데, AI가 이 패턴을 누락하면 URL만 알면 누구의 패스워드든 변경할 수 있게 됩니다.

### 왜 위험한가

인증이 누락된 기능은 공격자에게 열린 문과 같습니다. 구체적으로 다음과 같은 위험이 존재합니다.

- **계정 탈취**: 패스워드 변경, 이메일 변경 등의 기능에 인증이 없으면 타인의 계정을 손쉽게 장악할 수 있습니다.
- **데이터 유출**: 관리자 전용 API에 인증이 없으면 전체 사용자 목록, 결제 정보 등이 노출될 수 있습니다.
- **권한 상승(Privilege Escalation)**: 일반 사용자가 관리자 기능에 접근하여 시스템 전체를 제어할 수 있습니다.

> **⚠️ 주의:** AI가 생성한 코드에서 `Depends(get_current_user)`나 `OAuth2PasswordBearer` 관련 의존성이 빠져 있는지 반드시 확인하십시오. AI는 "동작하는 코드"를 우선시하기 때문에 인증 의존성을 생략하는 경향이 있습니다.

### 취약 코드

다음은 패스워드 변경 시 현재 사용자의 인증을 수행하지 않는 ❌ 취약한 코드입니다.

```python
# ❌ 취약한 코드: 인증 없이 패스워드 변경 허용
from fastapi import FastAPI
from pydantic import BaseModel
import hashlib

app = FastAPI()

class PasswordChange(BaseModel):
    user_id: int
    new_password: str

@app.post("/change-password")
async def change_password(data: PasswordChange):
    # 현재 로그인한 사용자인지 확인하지 않음
    sha = hashlib.sha256(data.new_password.encode())
    update_password_in_db(data.user_id, sha.hexdigest())
    return {"message": "패스워드가 변경되었습니다."}
```

이 코드는 두 가지 심각한 문제를 가지고 있습니다. 첫째, JWT 토큰 검증이 없으므로 비로그인 상태에서도 접근 가능합니다. 둘째, 현재 패스워드와의 일치 여부를 확인하지 않으므로 URL만 알면 누구든 패스워드를 변경할 수 있습니다.

### 안전 코드

다음은 FastAPI의 `Depends()`와 `OAuth2PasswordBearer`를 활용하여 JWT 인증과 현재 패스워드 확인을 적용한 ✅ 안전한 코드입니다.

```python
# ✅ 안전한 코드: JWT 인증 + 재인증을 포함한 패스워드 변경
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, SecretStr
from sqlalchemy.orm import Session

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGORITHM = "HS256"

class PasswordChangeRequest(BaseModel):
    current_password: SecretStr      # Pydantic SecretStr로 민감정보 보호
    new_password: SecretStr
    confirm_password: SecretStr

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """JWT 토큰에서 현재 사용자를 추출합니다."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="인증 정보가 유효하지 않습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

@app.post("/change-password")
async def change_password(
    data: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),  # 인증 필수
    db: Session = Depends(get_db),
):
    # 현재 패스워드 일치 여부 확인 (재인증)
    if not pwd_context.verify(
        data.current_password.get_secret_value(),
        current_user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="현재 패스워드가 일치하지 않습니다.",
        )

    # 새 패스워드와 확인 패스워드 일치 확인
    if data.new_password.get_secret_value() != data.confirm_password.get_secret_value():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="새 패스워드가 일치하지 않습니다.",
        )

    current_user.hashed_password = pwd_context.hash(
        data.new_password.get_secret_value()
    )
    db.commit()
    return {"message": "패스워드가 변경되었습니다."}
```

핵심은 `Depends(get_current_user)`를 엔드포인트의 매개변수로 선언하는 것입니다. 이렇게 하면 유효한 JWT 토큰 없이는 해당 엔드포인트에 접근할 수 없습니다. 또한 Pydantic의 `SecretStr`을 사용하면 로그나 직렬화 시 패스워드 값이 `**********`로 마스킹됩니다.

### 바이브 코딩 시 체크포인트

- [ ] AI가 생성한 모든 엔드포인트에 `Depends(get_current_user)` 또는 인증 의존성이 적용되어 있는지 확인합니다.
- [ ] 패스워드 변경, 결제, 개인정보 수정 등 중요 기능에는 **재인증(Re-authentication)** 로직이 포함되어 있는지 확인합니다.
- [ ] AI에게 코드를 요청할 때 "로그인한 사용자만 접근 가능하도록 Depends를 사용해줘"라는 조건을 명시적으로 포함합니다.
- [ ] `OAuth2PasswordBearer`와 `python-jose`를 활용한 토큰 기반 인증이 적용되어 있는지 확인합니다.

> **💡 팁:** AI에게 코드를 요청할 때 "인증이 필요한 엔드포인트입니다. Depends(get_current_user)를 사용해주세요."라고 명시하면 인증 관련 코드를 포함할 확률이 크게 높아집니다. 예: "로그인한 사용자만 접근 가능한 패스워드 변경 API를 FastAPI로 만들어줘. 현재 패스워드 확인도 포함해줘."

---

## 7-2. 부적절한 인가

### 개요

인가(Authorization)란 "인증된 사용자가 특정 자원이나 기능에 접근할 권한이 있는지 확인하는 과정"입니다. 인증이 "누구인지 확인"이라면, 인가는 "무엇을 할 수 있는지 확인"하는 것입니다.

바이브 코딩에서 흔히 발생하는 실수는 JWT 토큰 검증만 하고 **역할(Role) 기반의 권한 확인을 생략**하는 것입니다. 예를 들어 일반 사용자가 관리자 전용 삭제 기능에 접근할 수 있다면 이는 인가가 부적절한 것입니다.

### 왜 위험한가

부적절한 인가는 다음과 같은 심각한 보안 사고로 이어질 수 있습니다.

- **수평적 권한 상승(Horizontal Privilege Escalation)**: 같은 역할의 다른 사용자 데이터에 접근할 수 있습니다. 예를 들어 A 사용자가 B 사용자의 주문 내역을 조회하는 경우입니다.
- **수직적 권한 상승(Vertical Privilege Escalation)**: 일반 사용자가 관리자 기능을 실행할 수 있습니다. 예를 들어 일반 사용자가 전체 게시글을 삭제하는 경우입니다.
- **데이터 변조**: 권한 없는 사용자가 중요 데이터를 수정하거나 삭제할 수 있습니다.

### 취약 코드

다음은 사용자의 권한 확인 없이 삭제 기능을 수행하는 ❌ 취약한 코드입니다.

```python
# ❌ 취약한 코드: 권한 확인 없이 콘텐츠 삭제
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

app = FastAPI()

@app.delete("/content/{content_id}")
async def delete_content(
    content_id: int,
    current_user: User = Depends(get_current_user),  # 인증만 확인
    db: Session = Depends(get_db),
):
    # 사용자의 역할이나 소유권 확인 없이 바로 삭제 수행
    content = db.query(Content).filter(Content.id == content_id).first()
    if content:
        db.delete(content)
        db.commit()
    return {"message": "삭제 완료"}
```

### 안전 코드

FastAPI의 `Depends()`를 중첩하여 역할 기반 접근 제어(RBAC, Role-Based Access Control)를 적용한 ✅ 안전한 코드입니다.

```python
# ✅ 안전한 코드: 역할 기반 권한 확인 후 삭제
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

app = FastAPI()

def require_role(*allowed_roles: str):
    """특정 역할을 가진 사용자만 접근을 허용하는 의존성 함수입니다."""
    async def role_checker(
        current_user: User = Depends(get_current_user),
    ):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="이 기능에 대한 접근 권한이 없습니다.",
            )
        return current_user
    return role_checker

@app.delete("/admin/content/{content_id}")
async def admin_delete_content(
    content_id: int,
    current_user: User = Depends(require_role("admin", "moderator")),
    db: Session = Depends(get_db),
):
    """관리자 또는 모더레이터만 접근 가능한 삭제 API입니다."""
    content = db.query(Content).filter(Content.id == content_id).first()
    if content is None:
        raise HTTPException(status_code=404, detail="콘텐츠를 찾을 수 없습니다.")
    db.delete(content)
    db.commit()
    return {"message": "삭제 완료"}

@app.delete("/content/{content_id}")
async def delete_own_content(
    content_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """일반 사용자는 본인의 콘텐츠만 삭제할 수 있습니다."""
    content = db.query(Content).filter(
        Content.id == content_id,
        Content.author_id == current_user.id,  # 소유권 확인
    ).first()
    if content is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="삭제 권한이 없거나 콘텐츠가 존재하지 않습니다.",
        )
    db.delete(content)
    db.commit()
    return {"message": "삭제 완료"}
```

`require_role()` 함수는 **고차 의존성(Higher-Order Dependency)** 패턴으로, 허용할 역할 목록을 매개변수로 받아 새로운 의존성 함수를 반환합니다. 이 패턴을 사용하면 엔드포인트마다 필요한 역할을 유연하게 지정할 수 있습니다.

### 바이브 코딩 시 체크포인트

- [ ] 모든 API 엔드포인트에 "누가 이 기능을 사용할 수 있는가?"를 정의했는지 확인합니다.
- [ ] 데이터 조회/수정/삭제 시 **소유권 확인**(현재 사용자의 데이터인지)을 수행하는지 확인합니다.
- [ ] AI에게 "관리자만 접근 가능" 또는 "본인 데이터만 접근 가능"이라는 조건을 명시합니다.
- [ ] URL에 포함된 ID 값을 변경하여 다른 사용자의 데이터에 접근할 수 없는지 테스트합니다.

> **💡 팁:** AI에게 코드를 요청할 때 "이 API는 admin 역할을 가진 사용자만 접근 가능합니다. `Depends(require_role('admin'))`을 사용해주세요. 일반 사용자는 본인의 데이터만 조회/수정 가능합니다."와 같이 역할별 접근 조건을 명확히 전달하십시오.

---

## 7-3. 중요한 자원에 대한 잘못된 권한 설정

### 개요

파일 권한(File Permission)이란 운영체제에서 파일이나 디렉터리에 대해 "누가 읽고, 쓰고, 실행할 수 있는지"를 제어하는 설정입니다. 파이썬에서는 `os.chmod()`, `os.fchmod()` 등의 함수를 통해 파일의 권한을 설정할 수 있습니다.

바이브 코딩으로 FastAPI 서버 배포 스크립트를 작성할 때, AI는 종종 파일 권한을 `0o777`(모든 사용자에게 모든 권한 허용)로 설정하는 코드를 생성합니다. 특히 업로드 디렉터리나 설정 파일의 권한 설정에서 이러한 문제가 빈번합니다.

### 왜 위험한가

잘못된 파일 권한 설정은 다음과 같은 위험을 초래합니다.

- **설정 파일 노출**: `.env` 파일에 저장된 데이터베이스 접속 정보, API 키 등을 누구나 읽을 수 있게 됩니다.
- **파일 변조**: 실행 파일이나 라이브러리를 악의적으로 수정할 수 있습니다.
- **악성 코드 실행**: 쓰기 권한이 열린 디렉터리에 악성 스크립트를 업로드하고 실행할 수 있습니다.

### 취약 코드

다음은 설정 파일에 모든 사용자의 접근을 허용하는 ❌ 취약한 코드입니다.

```python
# ❌ 취약한 코드: 모든 사용자에게 읽기/쓰기/실행 권한 부여
import os

def write_config():
    # 0o777 = 모든 사용자가 읽기, 쓰기, 실행 가능
    os.chmod('/app/config/.env', 0o777)
    with open('/app/config/.env', 'w') as f:
        f.write('DATABASE_URL=postgresql://admin:secret@localhost/mydb')
```

### 안전 코드

파일 소유자에게만 필요한 최소 권한을 부여하는 ✅ 안전한 코드입니다.

```python
# ✅ 안전한 코드: 소유자에게만 읽기/쓰기 권한 부여
import os
import stat

def write_env_file():
    env_path = '/app/config/.env'
    with open(env_path, 'w') as f:
        f.write('DATABASE_URL=postgresql://admin:secret@localhost/mydb\n')
    # 소유자만 읽기/쓰기 가능 (0o600)
    os.chmod(env_path, stat.S_IRUSR | stat.S_IWUSR)

def create_upload_directory():
    upload_dir = '/app/uploads'
    os.makedirs(upload_dir, exist_ok=True)
    # 소유자만 읽기/쓰기/실행 가능 (0o700)
    os.chmod(upload_dir, stat.S_IRWXU)
```

FastAPI 프로젝트에서 업로드 디렉터리를 안전하게 관리하는 예시입니다.

```python
# ✅ FastAPI 업로드 디렉터리 권한 설정
from fastapi import FastAPI, UploadFile, Depends
import os, stat

UPLOAD_DIR = "/app/uploads"

@app.on_event("startup")
async def startup_event():
    """서버 시작 시 업로드 디렉터리의 권한을 확인합니다."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.chmod(UPLOAD_DIR, stat.S_IRWXU)  # 소유자만 접근 가능

@app.post("/upload")
async def upload_file(
    file: UploadFile,
    current_user: User = Depends(get_current_user),
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    # 업로드된 파일도 소유자만 읽기/쓰기 가능
    os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)
    return {"filename": file.filename}
```

> **💡 팁:** 리눅스(Linux) 파일 권한을 외우기 어려우시다면, 최소한 이것만 기억하십시오. `0o600`은 소유자만 읽기/쓰기, `0o700`은 소유자만 읽기/쓰기/실행, `0o644`는 소유자 읽기/쓰기 + 나머지 읽기만, `0o777`은 **절대 사용 금지**입니다.

### 바이브 코딩 시 체크포인트

- [ ] AI가 생성한 코드에서 `os.chmod`나 `os.makedirs`를 사용하는 부분의 권한 값을 확인합니다.
- [ ] `0o777` 또는 `0o666`이 사용된 곳이 있다면 즉시 최소 권한으로 변경합니다.
- [ ] `.env` 파일의 권한이 소유자 전용(`0o600`)으로 설정되어 있는지 확인합니다.
- [ ] 배포 스크립트에서 파일 권한을 설정하는 부분이 있다면 최소 권한 원칙(Principle of Least Privilege)을 따르는지 검토합니다.
- [ ] Docker 환경에서 파일을 복사할 때 `--chown` 옵션을 사용하여 적절한 소유자와 권한을 설정합니다.

> **⚠️ 주의:** AI에게 "파일 권한 오류를 해결해줘"라고 요청하면, AI는 가장 쉬운 해결책인 `chmod 777`을 제안하는 경우가 많습니다. 이는 권한 문제를 해결하는 것이 아니라, 보안을 완전히 포기하는 것입니다. 반드시 필요한 최소 권한만 부여하십시오.
