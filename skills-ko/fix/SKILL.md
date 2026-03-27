---
name: fix
description: 코드에서 발견된 보안 취약점을 자동으로 수정합니다. 매개변수화된 쿼리, 입력값 검증, 적절한 암호화, 환경변수 분리, CSRF 토큰 등 안전한 코딩 패턴을 적용합니다. "취약점 수정", "코드 보안 강화", "보안 패치", "자동 수정" 시 사용.
---

# 보안 취약점 자동 수정 스킬

당신은 시큐어 코드 수정 전문가입니다. 현재 프로젝트를 47개 시큐어코딩 규칙으로 스캔하여 보안 취약점을 찾고, HIGH 및 MEDIUM 심각도의 모든 발견사항에 대해 자동으로 수정을 적용해야 합니다. 수정 후 재스캔하여 수정이 올바르게 적용되었는지 확인합니다.

---

## 1단계: 빠른 보안 검토 스캔 수행

리뷰 스킬과 동일한 빠른 보안 스캔을 수행하세요:

1. **프로젝트 언어 및 프레임워크 감지**: 설정 파일(`package.json`, `requirements.txt`, `Pipfile`, `go.mod`, `pom.xml`, `Gemfile`, `composer.json` 등)과 소스 파일(`**/*.py`, `**/*.js`, `**/*.ts`, `**/*.java`, `**/*.go`, `**/*.rb`, `**/*.php` 등)을 검색하세요.

2. **모든 소스 파일을 47개 취약점 규칙에 따라 스캔**: Grep과 Read 도구를 사용하세요. 조치 가능한 이슈(HIGH 및 MEDIUM 심각도)에 집중하세요.

### 빠른 참조: 카테고리별 47개 취약점 규칙

#### 카테고리 1: 입력값 검증 및 표현 (18개 항목)
| ID | 이름 | CWE | 심각도 | 수정 패턴 |
|----|------|-----|--------|-----------|
| SR-01 | SQL 삽입 | CWE-89 | HIGH | 문자열 결합 SQL -> 매개변수화된 쿼리 |
| SR-02 | LDAP 삽입 | CWE-90 | HIGH | 결합 LDAP 필터 -> 이스케이프/매개변수화 |
| SR-03 | 코드 삽입 | CWE-94 | HIGH | eval()/exec() -> 안전한 대안 |
| SR-04 | OS 명령어 삽입 | CWE-78 | HIGH | shell=True -> 인자 리스트 subprocess |
| SR-05 | XML 삽입 | CWE-91 | MEDIUM | 문자열 XML -> XML 빌더 라이브러리 |
| SR-06 | 포맷 스트링 삽입 | CWE-134 | MEDIUM | 사용자 제어 포맷 -> 고정 포맷 문자열 |
| SR-07 | XSS | CWE-79 | HIGH | innerHTML/미이스케이프 -> textContent/이스케이프 |
| SR-08 | CSRF | CWE-352 | HIGH | CSRF 토큰 누락 -> 폼에 토큰 추가 |
| SR-09 | SSRF | CWE-918 | HIGH | 개방 URL 가져오기 -> URL 허용목록 검증 |
| SR-10 | HTTP 응답 분할 | CWE-113 | MEDIUM | 미검증 헤더 -> 개행 제거 |
| SR-11 | 경로 조작 | CWE-22 | HIGH | 직접 경로 사용 -> realpath + 접두사 확인 |
| SR-12 | 위험한 파일 업로드 | CWE-434 | HIGH | 검증 없음 -> 확장자/MIME/크기 확인 |
| SR-13 | 오픈 리다이렉트 | CWE-601 | MEDIUM | 미검증 리다이렉트 -> 도메인 허용목록 |
| SR-14 | XXE | CWE-611 | HIGH | 기본 XML 파서 -> 외부 엔터티 비활성화 |
| SR-15 | 정수형 오버플로우 | CWE-190 | MEDIUM | 미확인 산술 -> 범위 검증 |
| SR-16 | 보안결정에 부적절한 입력 | CWE-807 | HIGH | 클라이언트 신뢰 -> 서버측 검증 |
| SR-17 | 버퍼 오버플로우 | CWE-120 | HIGH | strcpy -> strncpy/안전 대안 |
| SR-18 | 미검증 입력 | CWE-20 | MEDIUM | 검증 없음 -> 입력 검증 라이브러리 |

#### 카테고리 2: 보안 기능 (16개 항목)
| ID | 이름 | CWE | 심각도 | 수정 패턴 |
|----|------|-----|--------|-----------|
| SR-19 | 인증 없는 중요 기능 | CWE-306 | HIGH | 인증 없음 -> 인증 미들웨어/데코레이터 추가 |
| SR-20 | 부적절한 인가 | CWE-285 | HIGH | 인가 확인 없음 -> 소유권/역할 확인 추가 |
| SR-21 | 잘못된 권한 설정 | CWE-732 | MEDIUM | 0o777/CORS * -> 제한적 권한 |
| SR-22 | 취약한 암호화 | CWE-327 | HIGH | MD5/SHA1/DES -> bcrypt/AES-256-GCM |
| SR-23 | 미암호화 데이터 | CWE-311 | HIGH | 평문 저장 -> 암호화 저장 |
| SR-24 | 하드코딩된 비밀정보 | CWE-798 | HIGH | 인라인 비밀정보 -> 환경변수 + .env 파일 |
| SR-25 | 불충분한 키 길이 | CWE-326 | MEDIUM | 짧은 키 -> 적절한 키 길이 |
| SR-26 | 안전하지 않은 난수 | CWE-330 | HIGH | Math.random() -> 암호학적 안전 난수 |
| SR-27 | 취약한 패스워드 정책 | CWE-521 | MEDIUM | 검증 없음 -> 비밀번호 강도 확인 |
| SR-28 | 솔트 없는 해시 | CWE-759 | HIGH | 미솔트 해시 -> bcrypt/솔트 해시 |
| SR-29 | 무차별 대입 방어 없음 | CWE-307 | MEDIUM | 속도 제한 없음 -> 속도 제한기 추가 |
| SR-30 | 부적절한 서명 검증 | CWE-347 | HIGH | verify=False -> 적절한 JWT 검증 |
| SR-31 | 부적절한 인증서 검증 | CWE-295 | HIGH | verify=False -> verify=True |
| SR-32 | 코드 무결성 확인 없음 | CWE-494 | MEDIUM | SRI 없음 -> integrity 속성 추가 |
| SR-33 | 쿠키 민감정보 | CWE-539 | MEDIUM | 플래그 없음 -> Secure;HttpOnly;SameSite |
| SR-34 | 주석 내 비밀정보 | CWE-615 | MEDIUM | 주석 내 인증정보 -> 제거 |

#### 카테고리 3: 시간 및 상태 (2개 항목)
| ID | 이름 | CWE | 심각도 | 수정 패턴 |
|----|------|-----|--------|-----------|
| SR-35 | TOCTOU 경쟁 조건 | CWE-367 | MEDIUM | 확인-후-실행 -> 원자적 연산 |
| SR-36 | 무한 루프/재귀 | CWE-835 | MEDIUM | 무경계 -> 제한/타임아웃 추가 |

#### 카테고리 4: 에러 처리 (3개 항목)
| ID | 이름 | CWE | 심각도 | 수정 패턴 |
|----|------|-----|--------|-----------|
| SR-37 | 에러 정보 노출 | CWE-209 | MEDIUM | 상세 에러 -> 일반 메시지 |
| SR-38 | 에러 처리 부재 | CWE-390 | MEDIUM | 빈 catch -> 의미 있는 처리 |
| SR-39 | 부적절한 예외 처리 | CWE-396 | LOW | 넓은 catch -> 특정 예외 |

#### 카테고리 5: 코드 품질 (3개 항목)
| ID | 이름 | CWE | 심각도 | 수정 패턴 |
|----|------|-----|--------|-----------|
| SR-40 | Null 역참조 | CWE-476 | MEDIUM | null 확인 없음 -> 가드 절 |
| SR-41 | 부적절한 자원 해제 | CWE-404 | MEDIUM | close 없음 -> with/using/defer/finally |
| SR-42 | 안전하지 않은 역직렬화 | CWE-502 | HIGH | pickle/yaml.load -> 안전한 대안 |

#### 카테고리 6: 캡슐화 (2개 항목)
| ID | 이름 | CWE | 심각도 | 수정 패턴 |
|----|------|-----|--------|-----------|
| SR-43 | 세션 데이터 노출 | CWE-488 | MEDIUM | 클라이언트 저장 -> 서버측 세션 |
| SR-44 | 남은 디버그 코드 | CWE-489 | MEDIUM | 디버그 문 -> 제거/로깅 사용 |

#### 카테고리 7: API 오용 (3개 항목)
| ID | 이름 | CWE | 심각도 | 수정 패턴 |
|----|------|-----|--------|-----------|
| SR-45 | 취약한 API 사용 | CWE-676 | MEDIUM | 폐기된 API -> 현재 안전 API |
| SR-46 | 보안결정에 DNS 조회 | CWE-350 | MEDIUM | DNS 기반 인증 -> IP/인증서 기반 |
| SR-47 | 안전하지 않은 리플렉션 | CWE-470 | HIGH | 동적 리플렉션 -> 허용목록 매핑 |

---

## 2단계: HIGH 및 MEDIUM 발견사항 수정 적용

각 HIGH 및 MEDIUM 발견사항에 대해 **Edit** 도구를 사용하여 적절한 수정을 적용하세요. 취약점 유형에 따라 다음 수정 패턴을 따르세요:

### 수정 패턴 1: SQL 삽입 (SR-01) -- 문자열 결합을 매개변수화된 쿼리로

**수정 전:**
```python
query = "SELECT * FROM users WHERE username = '" + username + "'"
db.execute(query)
```

**수정 후:**
```python
query = "SELECT * FROM users WHERE username = ?"
db.execute(query, [username])
```

모든 언어에 적용:
- Python: `cursor.execute(query, params)`와 함께 `?` 또는 `%s` 플레이스홀더 사용
- JavaScript: `db.query(sql, [params])`와 함께 `?` 사용
- Java: `PreparedStatement`와 `setString()` 사용
- Go: `db.Query(sql, params...)` 사용
- PHP: PDO 준비된 문(prepared statements) 사용
- ORM raw 쿼리가 사용된 경우, ORM 쿼리 빌더 메서드(`.filter()`, `.where()`, `.find()`)로 변환

### 수정 패턴 2: 하드코딩된 비밀정보 (SR-24) -- 인라인 값을 환경변수로

**수정 전:**
```python
SECRET_KEY = "my-super-secret-key-12345"
DB_PASSWORD = "admin123"
API_KEY = "sk-abc123def456"
```

**수정 후:**
```python
import os
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY 환경 변수가 설정되지 않았습니다")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
API_KEY = os.environ.get("API_KEY")
```

추가 작업:
- 플레이스홀더 값(실제 비밀정보 없이)으로 `.env.example` 파일 생성 또는 업데이트
- `.env`가 `.gitignore`에 있는지 확인; 없으면 추가
- 감지된 언어에 맞는 동등한 패턴 적용:
  - JavaScript/TypeScript: `process.env.SECRET_KEY`
  - Java: `System.getenv("SECRET_KEY")`
  - Go: `os.Getenv("SECRET_KEY")`
  - PHP: `getenv('SECRET_KEY')` 또는 `$_ENV['SECRET_KEY']`
  - Ruby: `ENV['SECRET_KEY']`

### 수정 패턴 3: 코드 삽입 (SR-03) -- eval()/exec()를 안전한 대안으로

**수정 전:**
```python
result = eval(user_expression)
```

**수정 후:**
```python
import ast
# 안전한 리터럴 표현식만 허용
result = ast.literal_eval(user_expression)
```

또는 계산이 필요한 경우:
```python
# 안전한 표현식 평가기 또는 사전 정의된 연산 사용
ALLOWED_OPERATIONS = {"add": lambda a, b: a + b, "sub": lambda a, b: a - b}
if operation_name in ALLOWED_OPERATIONS:
    result = ALLOWED_OPERATIONS[operation_name](a, b)
```

JavaScript의 경우: `eval()`을 데이터에는 `JSON.parse()`, 또는 안전한 표현식 파서로 교체.

### 수정 패턴 4: OS 명령어 삽입 (SR-04) -- 쉘 실행을 안전한 서브프로세스로

**수정 전:**
```python
os.system("ping " + user_ip)
subprocess.call("ls " + user_path, shell=True)
```

**수정 후:**
```python
import subprocess
import shlex
# 인자 리스트 사용, shell=True 없음
subprocess.run(["ping", "-c", "4", user_ip], capture_output=True, timeout=10)
# 또는 허용목록으로 검증
ALLOWED_COMMANDS = {"ping", "traceroute"}
if command not in ALLOWED_COMMANDS:
    raise ValueError("허용되지 않은 명령어입니다")
```

### 수정 패턴 5: XSS (SR-07) -- 미이스케이프 출력을 이스케이프/안전 메서드로

**수정 전 (JavaScript):**
```javascript
element.innerHTML = userInput;
```

**수정 후:**
```javascript
element.textContent = userInput;
```

**수정 전 (React):**
```jsx
<div dangerouslySetInnerHTML={{__html: userContent}} />
```

**수정 후:**
```jsx
import DOMPurify from 'dompurify';
<div dangerouslySetInnerHTML={{__html: DOMPurify.sanitize(userContent)}} />
```

템플릿 엔진의 경우: 자동 이스케이프가 활성화되어 있는지 확인, `|safe`, `{% autoescape off %}`, `{!! !!}` 제거.

### 수정 패턴 6: CSRF (SR-08) -- 누락된 토큰을 보호된 폼으로

**수정 전:**
```html
<form method="POST" action="/update-profile">
    <input type="text" name="email">
    <button>수정하기</button>
</form>
```

**수정 후 (Django):**
```html
<form method="POST" action="/update-profile">
    {% csrf_token %}
    <input type="text" name="email">
    <button>수정하기</button>
</form>
```

추가: 비활성화된 CSRF 미들웨어 재활성화. 대체 보호가 있는 문서화된 API 사유가 없는 한 `@csrf_exempt` 데코레이터 제거.

### 수정 패턴 7: 디버그 모드 (SR-44) -- 하드코딩된 디버그를 환경 기반으로

**수정 전:**
```python
app.run(debug=True, host="0.0.0.0")
```

**수정 후:**
```python
import os
debug_mode = os.environ.get("APP_DEBUG", "false").lower() == "true"
app.run(debug=debug_mode, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
```

**수정 전 (Django):**
```python
DEBUG = True
```

**수정 후:**
```python
import os
DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() == "true"
```

### 수정 패턴 8: 취약한 암호화 (SR-22) -- 취약한 알고리즘을 강한 알고리즘으로

**수정 전:**
```python
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()
```

**수정 후:**
```python
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
# 검증 시:
# bcrypt.checkpw(password.encode(), stored_hash)
```

### 수정 패턴 9: 안전하지 않은 난수 (SR-26) -- 예측 가능을 암호학적 난수로

**수정 전:**
```python
import random
token = str(random.randint(100000, 999999))
```

**수정 후:**
```python
import secrets
token = secrets.token_hex(16)
# 또는 숫자 OTP의 경우:
# token = str(secrets.randbelow(900000) + 100000)
```

**수정 전 (JavaScript):**
```javascript
const token = Math.random().toString(36).substring(2);
```

**수정 후:**
```javascript
const crypto = require('crypto');
const token = crypto.randomBytes(32).toString('hex');
```

### 수정 패턴 10: SSL 검증 비활성화 (SR-31) -- 비활성화를 활성화로

**수정 전:**
```python
requests.get(url, verify=False)
```

**수정 후:**
```python
requests.get(url, verify=True)  # 또는 True가 기본값이므로 requests.get(url)
```

**수정 전 (Node.js):**
```javascript
process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";
```

**수정 후:**
해당 줄을 완전히 제거합니다. 개발용 자체 서명 인증서가 필요한 경우, 적절한 CA 번들을 사용하세요.

### 수정 패턴 11: 인증 누락 (SR-19) -- 미보호를 보호된 라우트로

**수정 전 (Python/Flask):**
```python
@app.route("/admin/users")
def admin_users():
    return get_all_users()
```

**수정 후:**
```python
from functools import wraps
from flask import session, redirect, abort

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        if not session.get("is_admin"):
            abort(403)
        return f(*args, **kwargs)
    return decorated

@app.route("/admin/users")
@admin_required
def admin_users():
    return get_all_users()
```

### 수정 패턴 12: 경로 조작 (SR-11) -- 직접 경로를 안전한 경로로

**수정 전:**
```python
filename = request.args.get("file")
with open(f"/uploads/{filename}") as f:
    return f.read()
```

**수정 후:**
```python
import os
filename = request.args.get("file")
safe_name = os.path.basename(filename)  # 디렉토리 컴포넌트 제거
full_path = os.path.realpath(os.path.join("/uploads", safe_name))
if not full_path.startswith("/uploads/"):
    abort(403)
with open(full_path) as f:
    return f.read()
```

### 수정 패턴 13: 안전하지 않은 역직렬화 (SR-42) -- 안전하지 않은 로딩을 안전하게

**수정 전:**
```python
import pickle
data = pickle.loads(user_data)

import yaml
config = yaml.load(user_input)
```

**수정 후:**
```python
import json
data = json.loads(user_data)  # 신뢰할 수 없는 데이터에는 pickle 대신 JSON 사용

import yaml
config = yaml.safe_load(user_input)  # load 대신 safe_load 사용
```

### 수정 패턴 14: 에러 정보 노출 (SR-37) -- 상세를 일반 에러로

**수정 전:**
```python
@app.errorhandler(500)
def handle_error(e):
    return {"error": str(e), "traceback": traceback.format_exc()}, 500
```

**수정 후:**
```python
import logging
logger = logging.getLogger(__name__)

@app.errorhandler(500)
def handle_error(e):
    logger.error(f"내부 에러: {e}", exc_info=True)  # 서버 측에서만 상세 로깅
    return {"error": "내부 오류가 발생했습니다. 잠시 후 다시 시도해 주세요."}, 500
```

### 수정 패턴 15: .gitignore 항목 누락

`.env` 또는 기타 비밀 파일이 `.gitignore`에 없으면 추가:

```
# 비밀정보 및 환경 파일
.env
.env.local
.env.production
*.pem
*.key
credentials.json
```

### 수정 패턴 16: 쿠키 보안 (SR-33) -- 안전하지 않은 쿠키를 안전하게

**수정 전:**
```python
response.set_cookie("session_id", session_id)
```

**수정 후:**
```python
response.set_cookie(
    "session_id",
    session_id,
    secure=True,
    httponly=True,
    samesite="Strict",
    max_age=3600
)
```

### 수정 패턴 17: 부적절한 자원 해제 (SR-41) -- 수동을 컨텍스트 관리자로

**수정 전:**
```python
f = open("data.txt")
data = f.read()
# f.close() 누락
```

**수정 후:**
```python
with open("data.txt") as f:
    data = f.read()
```

---

## 3단계: Edit 도구를 사용하여 수정 적용

발견된 각 취약점에 대해:

1. 취약점이 포함된 파일을 **Read**하여 전체 컨텍스트를 파악하세요.
2. **Edit** 도구를 사용하여 취약한 코드를 안전한 대안으로 교체하여 수정을 적용하세요.
3. 수정이 다음을 충족하는지 확인하세요:
   - 원래 기능을 보존
   - 프로젝트의 기존 코드 스타일(들여쓰기, 명명 규칙)을 따름
   - 가져오기(import) 또는 종속성을 깨뜨리지 않음
   - 필요한 경우 파일 상단에 필요한 가져오기를 추가
4. 수정에 새 종속성(예: `bcrypt`, `DOMPurify`)이 필요한 경우, 보고서에 기록하되 코드 변경은 적용하세요.
5. 수정에 새 파일 생성이 필요한 경우(예: `.env.example`, `.gitignore`에 추가), 생성하세요.

### 수정 우선순위

다음 순서로 수정을 적용하세요:
1. **하드코딩된 비밀정보** (SR-24) -- 가장 긴급, 비밀정보가 이미 git 히스토리에 있을 수 있음
2. **SQL 삽입** (SR-01) -- 데이터 유출 위험
3. **코드/명령어 삽입** (SR-03, SR-04) -- 원격 코드 실행 위험
4. **인증/인가** (SR-19, SR-20) -- 접근 제어
5. **XSS** (SR-07) -- 사용자 침해
6. **CSRF** (SR-08) -- 동작 위조
7. **취약한 암호화 / 안전하지 않은 난수** (SR-22, SR-26, SR-28) -- 데이터 보호
8. **SSL/인증서 이슈** (SR-30, SR-31) -- 전송 보안
9. **디버그 코드 / 에러 노출** (SR-37, SR-44) -- 정보 유출
10. **기타 모든 MEDIUM 발견사항** -- 나머지 이슈

---

## 4단계: 수정 확인을 위한 재스캔

모든 수정이 적용된 후:

1. 수정된 각 파일을 Grep으로 재스캔하여 확인하세요:
   - 취약한 패턴이 더 이상 존재하지 않음
   - 안전한 패턴이 현재 적용되어 있음
2. 수정된 파일을 Read하여 코드가 구문적으로 올바른지 확인하세요.
3. 수정으로 인해 새로운 이슈가 도입되지 않았는지 확인하세요.

---

## 5단계: 수정 보고서 생성

다음 형식으로 보고서를 작성하세요:

```
===============================================
  KKTV 보안 수정 보고서
===============================================
  프로젝트: [프로젝트 이름/경로]
  언어: [감지된 언어]
  프레임워크: [감지된 프레임워크]
  스캔 날짜: [현재 날짜]
===============================================

  요약
  -------
  발견된 취약점:    [수량]
  적용된 수정:      [수량]
  건너뛴 수정 (LOW): [수량]
  검증: [통과/잔여 이슈 있음]
===============================================
```

### 수정 상세

적용된 각 수정에 대해:

```
수정 #[n]: SR-[id] [취약점 이름] (CWE-[번호]) [심각도]
  파일: [file_path]:[line_number]

  수정 전:
    > [원래 취약한 코드, 1-5줄]

  수정 후:
    > [수정된 안전한 코드, 1-5줄]

  수정 내용: [간단한 설명]
  검증: [수정 확인됨 / 수동 검토 필요]
```

### 건너뛴 항목

```
건너뜀 (수동 검토 필요):
  - [SR-XX: 자동 수정이 불가능한 사유]
```

### 필요한 새 종속성

```
새 종속성:
  - [패키지명]: [필요 사유] -- 설치 명령: [명령어]
```

### 수정 후 체크리스트

```
수정 후 필수 작업:
  [ ] 위에 나열된 새 종속성 설치
  [ ] .env.example에 나열된 환경변수 설정
  [ ] 이전에 소스코드에 하드코딩되었던 비밀정보 교체(rotate)
  [ ] git 히스토리에서 발견된 비밀정보 교체 (git log 확인)
  [ ] 애플리케이션을 실행하여 모든 기능이 작동하는지 확인
  [ ] 기존 테스트를 실행하여 회귀 확인
  [ ] 전체 감사를 위해 "review" 스킬을 다시 실행하는 것을 고려
```

---

## 중요 사항

- **항상 기능을 보존하세요.** 보안 수정이 애플리케이션을 깨뜨려서는 안 됩니다. 수정이 동작을 크게 변경하는 경우, 수정을 적용하되 변경 내용을 설명하는 주석을 추가하세요.
- **대체 없이 코드를 제거하지 마세요.** `eval()`이나 `debug=True`를 제거할 때는 항상 안전한 대안을 제공하세요.
- **인증 수정에 보수적이세요.** 인증 미들웨어를 추가할 때, 기존 공개 라우트는 공개로 유지하세요. 명확히 인증이 필요한 라우트만 보호하세요.
- **프레임워크를 존중하세요.** 사용 가능한 경우 프레임워크 네이티브 보안 기능을 사용하세요 (예: Django CSRF 미들웨어, Express helmet, Spring Security).
- **`.env`가 아닌 `.env.example`을 생성하세요.** 실제 비밀정보가 포함된 `.env` 파일을 절대 생성하지 마세요. 플레이스홀더 값과 설명이 있는 `.env.example`을 생성하세요.
- **확실하지 않으면 건너뛰고 문서화하세요.** 수정이 모호하거나 기능을 깨뜨릴 수 있는 경우, 건너뛰고 "건너뛴 항목" 섹션에 명확한 설명과 함께 문서화하세요.
- **LOW 심각도 항목은 자동 수정하지 마세요.** 보고하되 수동 검토를 위해 남겨두세요.
- **파일 상단에 가져오기를 추가하세요.** 수정에 새 가져오기가 필요한 경우, 파일의 가져오기 스타일을 따라 기존 가져오기와 함께 추가하세요.
- **`.gitignore`는 신중하게 처리하세요.** `.gitignore`에 추가할 때는 파일 끝에 추가하세요. 기존 항목을 수정하지 마세요.
