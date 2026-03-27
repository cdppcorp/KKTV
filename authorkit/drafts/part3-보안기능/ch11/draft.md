# Chapter 11. 정보 노출을 차단하세요

## 11-1. 쿠키를 통한 정보 노출

### 개요

쿠키(Cookie)는 웹 브라우저에 저장되는 작은 데이터로, 로그인 상태 유지, 사용자 설정 저장 등에 사용됩니다. 그러나 쿠키의 보안 속성(Security Flag)을 적절히 설정하지 않으면, 세션 ID나 인증 토큰과 같은 중요 정보가 공격자에게 노출될 수 있습니다.

바이브 코딩에서 AI가 세션 관리 코드를 생성할 때, 쿠키의 보안 속성을 제대로 설정하지 않는 경우가 매우 빈번합니다. AI는 기능적으로 동작하는 코드를 우선시하기 때문에, `HttpOnly`, `Secure`, `SameSite`와 같은 보안 속성을 생략하는 경향이 있습니다.

### 왜 위험한가

> **💡 팁:** XSS를 통한 쿠키 탈취 공격은 4장 4-1절을, CSRF 공격은 4장 4-2절을 참고하십시오.

쿠키 보안 속성이 미설정된 경우 다음과 같은 공격이 가능합니다.

- **XSS(Cross-Site Scripting)를 통한 세션 탈취**: `HttpOnly` 속성이 없으면, 자바스크립트(JavaScript)에서 `document.cookie`로 쿠키에 접근할 수 있습니다. 공격자가 XSS 취약점을 이용하여 사용자의 세션 ID를 탈취할 수 있습니다.
- **네트워크 도청을 통한 쿠키 유출**: `Secure` 속성이 없으면, HTTP(평문) 연결에서도 쿠키가 전송됩니다. 공용 WiFi 등에서 패킷 스니핑으로 세션 ID가 노출될 수 있습니다.
- **CSRF(Cross-Site Request Forgery) 공격**: `SameSite` 속성이 없으면, 악의적인 외부 사이트에서 사용자의 쿠키를 포함한 요청을 보낼 수 있습니다. 사용자 모르게 결제, 회원 탈퇴 등의 요청이 실행될 수 있습니다.

### 취약한 코드

다음은 쿠키 보안 속성을 설정하지 않은 ❌ 취약한 코드입니다.

```python
# ❌ 취약한 코드 (Django): 쿠키 보안 속성 미설정
from django.http import HttpResponse

def login_view(request):
    user = authenticate(request)
    if user:
        response = HttpResponse("로그인 성공")
        # 보안 속성 없이 세션 ID를 쿠키에 저장
        response.set_cookie('session_id', generate_session_id())
        return response
```

```python
# ❌ 취약한 코드 (Flask): 쿠키 보안 속성 미설정
from flask import Flask, make_response

@app.route('/login', methods=['POST'])
def login():
    response = make_response("로그인 성공")
    # 보안 속성 없이 쿠키 설정
    response.set_cookie('auth_token', token)
    return response
```

### 안전한 코드

세 가지 핵심 보안 속성을 모두 적용한 ✅ 안전한 코드입니다.

```python
# ✅ 안전한 코드 (Django): 쿠키 보안 속성 설정
from django.http import HttpResponse

def login_view(request):
    user = authenticate(request)
    if user:
        response = HttpResponse("로그인 성공")
        response.set_cookie(
            'session_id',
            generate_session_id(),
            httponly=True,    # JavaScript에서 접근 불가
            secure=True,      # HTTPS에서만 전송
            samesite='Lax',   # 외부 사이트에서의 요청 시 쿠키 미전송
            max_age=3600,     # 1시간 후 만료
            path='/',
        )
        return response
```

```python
# ✅ 안전한 코드 (Flask): 쿠키 보안 속성 설정
from flask import Flask, make_response

@app.route('/login', methods=['POST'])
def login():
    response = make_response("로그인 성공")
    response.set_cookie(
        'auth_token',
        token,
        httponly=True,
        secure=True,
        samesite='Lax',
        max_age=3600,
    )
    return response
```

Django 프로젝트에서는 `settings.py`에서 전역적으로 세션 쿠키의 보안 속성을 설정할 수 있습니다.

```python
# ✅ Django settings.py에서 세션 쿠키 보안 설정
# 세션 쿠키 보안 속성
SESSION_COOKIE_HTTPONLY = True    # JavaScript에서 세션 쿠키 접근 차단
SESSION_COOKIE_SECURE = True      # HTTPS에서만 세션 쿠키 전송
SESSION_COOKIE_SAMESITE = 'Lax'   # CSRF 방어

# CSRF 쿠키 보안 속성
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'Lax'

# 세션 만료 설정
SESSION_COOKIE_AGE = 3600          # 1시간 (초 단위)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # 브라우저 종료 시 세션 만료
```

FastAPI에서는 응답 객체에 직접 쿠키를 설정합니다.

```python
# ✅ FastAPI에서의 쿠키 보안 설정
from fastapi import Response

@app.post("/login")
async def login(response: Response):
    token = create_access_token(user)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=3600,
    )
    return {"message": "로그인 성공"}
```

각 보안 속성의 역할을 정리하면 다음과 같습니다.

| 속성 | 역할 | 미설정 시 위험 |
|---|---|---|
| `HttpOnly` | JavaScript에서 쿠키 접근 차단 | XSS를 통한 세션 탈취 |
| `Secure` | HTTPS 연결에서만 쿠키 전송 | 네트워크 도청으로 쿠키 유출 |
| `SameSite` | 외부 사이트 요청 시 쿠키 전송 제한 | CSRF 공격 |

> **💡 팁:** `SameSite` 속성에는 세 가지 값이 있습니다. `Strict`는 외부 사이트에서의 모든 요청에 쿠키를 보내지 않습니다(가장 안전하지만 사용자 경험이 불편할 수 있음). `Lax`는 GET 요청에 한해 외부 사이트에서도 쿠키를 전송합니다(권장 설정). `None`은 모든 요청에 쿠키를 전송하며, 반드시 `Secure` 속성과 함께 사용해야 합니다.

### 바이브 코딩 시 체크포인트

- [ ] `set_cookie()` 호출 시 `httponly=True`, `secure=True`, `samesite='Lax'`가 모두 설정되어 있는지 확인합니다.
- [ ] Django 프로젝트의 `settings.py`에서 `SESSION_COOKIE_HTTPONLY`, `SESSION_COOKIE_SECURE`, `SESSION_COOKIE_SAMESITE`를 설정합니다.
- [ ] 쿠키에 `max_age` 또는 만료 시간을 설정하여 영구 쿠키를 방지합니다.
- [ ] 쿠키에 패스워드, 개인정보 등 민감한 정보를 직접 저장하지 않습니다. 세션 ID만 저장하고, 실제 데이터는 서버 측에 저장합니다.
- [ ] AI에게 "쿠키 보안 속성(HttpOnly, Secure, SameSite)을 모두 설정해줘"라고 명시합니다.

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

> **💡 팁:** 하드코딩된 비밀번호와 API 키 문제는 8장 8-3절에서 자세히 다룹니다.

주석에 포함된 중요정보는 다음과 같은 경로로 유출됩니다.

- **소스코드 저장소 노출**: GitHub 등에 코드를 Push하면, 주석에 포함된 정보도 함께 공개됩니다. `.py` 파일뿐만 아니라 HTML, JavaScript 파일의 주석도 클라이언트에서 볼 수 있습니다.
- **클라이언트 사이드 노출**: HTML 주석(`<!-- -->`)이나 JavaScript 주석(`// `, `/* */`)은 브라우저의 "소스 보기" 기능으로 누구나 확인할 수 있습니다. 서버에서 실행되지 않는 프론트엔드(Front-end) 코드의 주석은 모든 방문자에게 그대로 노출됩니다.
- **빌드 산출물 포함**: 최소화(Minify)되지 않은 JavaScript 파일에는 주석이 그대로 포함됩니다.
- **디컴파일 가능**: 컴파일된 코드에서도 주석 정보를 추출할 수 있는 경우가 있습니다.

> **⚠️ 주의:** AI는 코드를 설명하기 위해 주석을 매우 적극적으로 생성합니다. 특히 "이 코드는 DB_HOST=192.168.1.100에 접속합니다"와 같이 인프라 정보를 주석에 포함하는 경우가 있습니다. AI가 생성한 모든 주석을 반드시 검토하십시오.

### 취약한 코드

다음은 AI가 생성할 수 있는 위험한 주석이 포함된 ❌ 취약한 코드입니다.

```python
# ❌ 취약한 코드: 주석에 중요정보 포함
import pymysql

# DB 접속 정보: admin / P@ssw0rd123!
# 서버: 192.168.1.100:3306
def get_connection():
    # TODO: 나중에 환경 변수로 변경하기
    # 현재 테스트용 키: sk-proj-abc123xyz456
    return pymysql.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        passwd=os.environ.get('DB_PASSWORD'),
    )
```

```html
<!-- ❌ 취약한 코드: HTML 주석에 시스템 정보 노출 -->
<!DOCTYPE html>
<html>
<head>
    <!-- 관리자 페이지: /admin/dashboard (인증 우회: ?debug=true) -->
    <!-- API 엔드포인트: https://api.internal.company.com/v2 -->
    <title>마이 페이지</title>
</head>
```

```javascript
// ❌ 취약한 코드: JavaScript 주석에 API 키 노출
// Firebase 설정 (키: AIzaSyB1234567890abcdef)
// 테스트 계정: test@example.com / test1234
const firebaseConfig = {
    apiKey: process.env.FIREBASE_API_KEY,
    // 이전 키 (만료됨): AIzaSyOLD_KEY_12345
};
```

### 안전한 코드

중요정보가 제거된 ✅ 안전한 코드입니다.

```python
# ✅ 안전한 코드: 주석에 중요정보를 포함하지 않음
import pymysql
import os

def get_connection():
    """환경 변수에서 DB 접속 정보를 가져와 연결을 생성합니다."""
    return pymysql.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        passwd=os.environ.get('DB_PASSWORD'),
        db=os.environ.get('DB_NAME'),
        charset='utf8',
    )
```

```html
<!-- ✅ 안전한 코드: HTML 주석에 시스템 정보를 포함하지 않음 -->
<!DOCTYPE html>
<html>
<head>
    <title>마이 페이지</title>
</head>
```

```javascript
// ✅ 안전한 코드: 주석에 키 값이나 접속 정보를 포함하지 않음
// Firebase 초기화 설정
const firebaseConfig = {
    apiKey: process.env.FIREBASE_API_KEY,
    authDomain: process.env.FIREBASE_AUTH_DOMAIN,
};
```

배포 전에 주석에 포함된 중요정보를 검사하는 스크립트를 활용할 수 있습니다.

```python
# ✅ 주석 내 중요정보 검사 스크립트
import re
import os

SENSITIVE_PATTERNS = [
    r'(?i)password\s*[:=]\s*\S+',       # password: xxx 또는 password=xxx
    r'(?i)api[_-]?key\s*[:=]\s*\S+',    # api_key: xxx
    r'(?i)secret\s*[:=]\s*\S+',         # secret: xxx
    r'sk-[a-zA-Z0-9]{20,}',            # OpenAI API 키 패턴
    r'(?i)token\s*[:=]\s*\S+',          # token: xxx
    r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',  # IP 주소
    r'(?i)admin\s*/\s*\S+',             # admin / password 패턴
]

def scan_comments_in_file(filepath):
    """파일의 주석에서 민감한 정보를 검사합니다."""
    issues = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            # Python 주석 검사
            comment_match = re.search(r'#(.+)$', line)
            if comment_match:
                comment = comment_match.group(1)
                for pattern in SENSITIVE_PATTERNS:
                    if re.search(pattern, comment):
                        issues.append({
                            'file': filepath,
                            'line': line_num,
                            'content': line.strip(),
                            'pattern': pattern,
                        })
    return issues

def scan_project(project_dir):
    """프로젝트 전체의 주석을 검사합니다."""
    all_issues = []
    for root, dirs, files in os.walk(project_dir):
        # .git, node_modules 등 제외
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', '__pycache__'}]
        for filename in files:
            if filename.endswith(('.py', '.js', '.html', '.jsx', '.tsx', '.ts')):
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

Git 커밋 전에 자동으로 주석을 검사하는 Pre-commit Hook도 활용할 수 있습니다.

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
- [ ] HTML과 JavaScript 파일의 주석에 시스템 내부 정보가 노출되어 있지 않은지 확인합니다. 이 주석은 브라우저에서 누구나 볼 수 있습니다.
- [ ] `TODO: 나중에 변경`, `임시 패스워드` 등의 주석이 운영 코드에 남아 있지 않은지 확인합니다.
- [ ] `detect-secrets` 또는 유사한 도구를 Pre-commit Hook으로 설정하여 커밋 전에 자동으로 검사합니다.
- [ ] AI에게 프롬프트를 전달할 때, 실제 API 키나 패스워드 대신 `YOUR_API_KEY_HERE`와 같은 플레이스홀더(Placeholder)를 사용합니다.
- [ ] AI가 생성한 코드에서 `# 이전 키:`, `# 테스트 계정:`, `# 접속 정보:` 등의 주석을 즉시 삭제합니다.

> **⚠️ 주의:** AI에게 "이 API 키로 OpenAI를 호출하는 코드를 만들어줘"라고 실제 키를 프롬프트에 포함하면, AI가 그 키를 주석에 포함할 가능성이 높습니다. 또한 AI 서비스의 대화 기록에 여러분의 키가 저장될 수 있습니다. 프롬프트에는 절대로 실제 중요정보를 포함하지 마십시오.

> **💡 팁:** JavaScript 코드를 배포할 때는 반드시 최소화(Minification) 도구를 사용하여 주석을 제거하십시오. Webpack, Vite 등의 빌드 도구는 프로덕션(Production) 빌드 시 자동으로 주석을 제거합니다. 그러나 이것은 최후의 방어선일 뿐, 애초에 주석에 중요정보를 포함하지 않는 것이 원칙입니다.
