# 시큐어코딩 가이드라인 Skills
## FastAPI 버전

> 바이브 코딩을 하는 모든 사람을 위한 보안 가이드
> 특히 웹사이트를 바이브 코딩해서 퍼블리싱하는 사람들을 위하여
> FastAPI + SQLAlchemy + Pydantic 기반

---

# 목차

## PART 1. 시작하기
- Chapter 1. AI가 만든 코드도 취약할 수 있습니다
  - 1-1. AI가 만든 코드도 취약할 수 있습니다
  - 1-2. 이 가이드의 활용법

## PART 2. 입력값을 믿지 마세요 — 입력데이터 검증
- Chapter 2. 데이터베이스를 노리는 삽입 공격
  - 2-1. SQL 삽입(SQL Injection)
  - 2-2. LDAP 삽입(LDAP Injection)
- Chapter 3. 코드와 명령어를 노리는 삽입 공격
  - 3-1. 코드 삽입(Code Injection)
  - 3-2. 운영체제 명령어 삽입(OS Command Injection)
  - 3-3. XML 삽입(XML Injection)
  - 3-4. 포맷 스트링 삽입(Format String Injection)
- Chapter 4. 웹 요청을 노리는 공격
  - 4-1. 크로스사이트 스크립트(XSS)
  - 4-2. 크로스사이트 요청 위조(CSRF)
  - 4-3. 서버사이드 요청 위조(SSRF)
  - 4-4. HTTP 응답 분할(HTTP Response Splitting)
- Chapter 5. 파일과 URL을 노리는 공격
  - 5-1. 경로 조작 및 자원 삽입(Path Traversal & Resource Injection)
  - 5-2. 위험한 형식 파일 업로드(Unrestricted File Upload)
  - 5-3. 신뢰되지 않는 URL 자동 연결(Open Redirect)
  - 5-4. 부적절한 XML 외부 개체 참조(XXE)
- Chapter 6. 데이터 타입과 보안 결정을 노리는 공격
  - 6-1. 정수형 오버플로우(Integer Overflow)
  - 6-2. 보안기능 결정에 사용되는 부적절한 입력값

## PART 3. 보안 기능을 제대로 구현하세요
- Chapter 7. 인증과 인가, 그리고 권한 설정
  - 7-1. 적절한 인증 없이 중요 기능 허용
  - 7-2. 부적절한 인가
  - 7-3. 중요한 자원에 대한 잘못된 권한 설정
- Chapter 8. 암호화, 제대로 하고 계십니까
  - 8-1. 취약한 암호화 알고리즘 사용
  - 8-2. 암호화되지 않은 중요정보
  - 8-3. 하드코딩된 중요정보
  - 8-4. 충분하지 않은 키 길이
- Chapter 9. 난수, 패스워드, 그리고 인증 방어
  - 9-1. 적절하지 않은 난수 값 사용
  - 9-2. 취약한 패스워드 허용
  - 9-3. 솔트 없는 일방향 해시 함수 사용
  - 9-4. 반복된 인증시도 제한 기능 부재
- Chapter 10. 서명, 인증서, 무결성 검증
  - 10-1. 부적절한 전자서명 확인
  - 10-2. 부적절한 인증서 유효성 검증
  - 10-3. 무결성 검사 없는 코드 다운로드
- Chapter 11. 정보 노출을 차단하세요
  - 11-1. 쿠키를 통한 정보 노출
  - 11-2. 주석문 안에 포함된 시스템 주요정보

## PART 4. 안정적인 코드를 작성하세요
- Chapter 12. 시간 및 상태 — 타이밍이 만드는 버그
  - 12-1. 경쟁 조건: 검사 시점과 사용 시점(TOCTOU)
  - 12-2. 종료되지 않는 반복문 또는 재귀 함수
- Chapter 13. 에러 처리 — 오류가 보안 구멍이 되는 순간
  - 13-1. 오류 메시지 정보 노출
  - 13-2. 오류 상황 대응 부재
  - 13-3. 부적절한 예외 처리
- Chapter 14. 코드 오류 — 개발자가 놓치기 쉬운 함정들
  - 14-1. Null Pointer 역참조
  - 14-2. 부적절한 자원 해제
  - 14-3. 신뢰할 수 없는 데이터의 역직렬화

## PART 5. 구조와 설계로 지키세요
- Chapter 15. 캡슐화 — 보여서는 안 되는 것들
  - 15-1. 잘못된 세션에 의한 데이터 정보 노출
  - 15-2. 제거되지 않고 남은 디버그 코드
- Chapter 16. API 오용 — 편리함 뒤에 숨은 위험
  - 16-1. 취약한 API 사용

## PART 6. 바이브 코딩 보안 체크리스트
- Chapter 17. 배포 전 점검, AI 프롬프트, TOP 10 실수
  - 17-1. 배포 전 보안 체크리스트
  - 17-2. AI에게 보안 검토 요청하는 프롬프트 예시
  - 17-3. 자주 발생하는 바이브 코딩 보안 실수 TOP 10

---

# PART 1. 시작하기

# Chapter 1

---

## 1-1. AI가 만든 코드도 취약할 수 있습니다

### 개요

바이브 코딩(Vibe Coding)의 시대가 열렸습니다. Cursor, Claude Code, GitHub Copilot 같은 AI 도구를 활용하면 몇 시간 만에 웹사이트를 완성할 수 있습니다. 프롬프트 몇 줄로 로그인 시스템을 구축하고, 데이터베이스를 연결하며, 결제 기능까지 구현할 수 있는 시대입니다. 그러나 여기에는 심각한 함정이 숨어 있습니다. **AI가 생성한 코드가 정상적으로 동작한다고 해서 안전한 것은 아닙니다.**

이 장에서는 AI 도구가 왜 보안에 취약한 코드를 생성할 수 있는지, 그리고 바이브 코더(Vibe Coder)인 여러분이 왜 보안에 관심을 가져야 하는지 설명합니다.

### 왜 위험한가

AI 코드 생성 도구는 방대한 양의 오픈소스 코드와 온라인 튜토리얼을 학습하여 만들어졌습니다. 문제는 이 학습 데이터 자체에 보안 취약점이 포함된 코드가 상당수 존재한다는 것입니다. Stack Overflow의 답변, GitHub의 예제 코드, 블로그 튜토리얼 등 많은 자료가 **"동작하는 코드"**에 초점을 맞추고 있으며, 보안은 후순위로 밀려 있습니다.

2023년 스탠퍼드 대학교의 연구에 따르면, AI 코드 어시스턴트를 사용한 개발자가 작성한 코드는 그렇지 않은 개발자의 코드보다 보안 취약점이 더 많이 발견되었습니다. 더 우려스러운 점은, AI 도구를 사용한 개발자들이 자신의 코드가 더 안전하다고 **잘못 확신**하는 경향이 있었다는 것입니다.

바이브 코딩 환경에서 보안 취약점이 발생하는 주요 원인은 다음과 같습니다.

1. **학습 데이터의 편향**: AI는 보안이 취약한 코드 패턴도 학습합니다
2. **맥락의 부재**: AI는 여러분의 서비스가 어떤 위협에 노출되는지 모릅니다
3. **과신 효과**: "AI가 만들었으니 괜찮겠지"라는 심리가 코드 리뷰를 생략하게 합니다
4. **프롬프트의 한계**: "로그인 기능 만들어줘"라고 요청하면 AI는 동작하는 코드를 만들지, 안전한 코드를 만들지 않습니다

### 실제 사례: AI가 생성하는 취약한 코드 패턴

#### 사례 1: 하드코딩된 비밀키(Hardcoded Secrets)

AI에게 "JWT 인증 기능을 만들어줘"라고 요청하면 다음과 같은 코드를 생성하는 경우가 매우 빈번합니다.

❌ 취약한 코드

```python
import jwt
from flask import Flask, request, jsonify

app = Flask(__name__)

# AI가 생성한 코드 - 비밀키가 소스코드에 하드코딩되어 있습니다
SECRET_KEY = "super-secret-key-12345"

@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    # 비밀번호 평문 비교 - 또 다른 취약점
    if username == "admin" and password == "admin123":
        token = jwt.encode({"user": username}, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token})

    return jsonify({"error": "Invalid credentials"}), 401
```

이 코드에는 최소 세 가지 심각한 보안 문제가 있습니다.

- `SECRET_KEY`가 소스코드에 직접 작성되어 있어 Git 저장소에 노출됩니다
- 비밀번호를 평문(Plain Text)으로 비교합니다
- 관리자 계정 정보가 코드에 하드코딩되어 있습니다

✅ 안전한 코드

```python
import jwt
import os
import bcrypt
from flask import Flask, request, jsonify

app = Flask(__name__)

# 환경 변수에서 비밀키를 읽어옵니다 (자세한 내용은 8장 8-3절에서 다룹니다)
SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY 환경 변수가 설정되지 않았습니다.")

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', '')
    password = request.json.get('password', '')

    # 데이터베이스에서 사용자 조회
    user = db.users.find_one({"username": username})
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    # bcrypt로 해시된 비밀번호 비교 (자세한 내용은 9장 9-3절에서 다룹니다)
    if bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
        token = jwt.encode(
            {"user": username, "exp": datetime.utcnow() + timedelta(hours=1)},
            SECRET_KEY,
            algorithm="HS256"
        )
        return jsonify({"token": token})

    return jsonify({"error": "Invalid credentials"}), 401
```

> **⚠️ 주의:** AI 도구에게 인증 관련 코드를 요청할 때는 반드시 "환경 변수에서 비밀키를 로드하고, bcrypt로 비밀번호를 해싱하라"고 명시적으로 지시하십시오. 명시하지 않으면 AI는 거의 확실하게 하드코딩된 값을 사용합니다.

#### 사례 2: SQL 삽입(SQL Injection)

"사용자 검색 기능을 만들어줘"라는 프롬프트에 AI가 생성하는 전형적인 코드입니다.

❌ 취약한 코드

```python
@app.route('/search')
def search_user():
    username = request.args.get('username')

    # 문자열 포매팅으로 직접 SQL 쿼리 구성 - SQL 삽입 취약점
    query = f"SELECT * FROM users WHERE username = '{username}'"
    result = db.execute(query)

    return jsonify(result.fetchall())
```

공격자가 `username` 파라미터에 `' OR '1'='1' --`을 입력하면 전체 사용자 데이터가 유출됩니다. `'; DROP TABLE users; --`를 입력하면 사용자 테이블 전체가 삭제됩니다.

✅ 안전한 코드

```python
@app.route('/search')
def search_user():
    username = request.args.get('username', '')

    # 매개변수화된 쿼리(Parameterized Query) 사용
    query = "SELECT id, username, email FROM users WHERE username = ?"
    result = db.execute(query, (username,))

    return jsonify(result.fetchall())
```

> **💡 팁:** AI에게 데이터베이스 쿼리 코드를 요청할 때는 "반드시 매개변수화된 쿼리(Parameterized Query) 또는 ORM을 사용하라"고 지시하십시오.

#### 사례 3: 크로스사이트 요청 위조(CSRF) 토큰 누락

AI에게 "회원 정보 수정 폼을 만들어줘"라고 요청하면 다음과 같은 코드가 생성되기도 합니다.

❌ 취약한 코드

```html
<form action="/update-profile" method="POST">
    <input type="text" name="email" value="{{ user.email }}">
    <input type="text" name="nickname" value="{{ user.nickname }}">
    <button type="submit">수정하기</button>
</form>
```

이 폼에는 CSRF(Cross-Site Request Forgery) 토큰이 없습니다. 공격자가 악의적인 웹사이트에서 사용자 모르게 이 폼을 제출하도록 유도할 수 있습니다.

✅ 안전한 코드

```html
<form action="/update-profile" method="POST">
    <!-- CSRF 토큰 포함 -->
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
    <input type="text" name="email" value="{{ user.email }}">
    <input type="text" name="nickname" value="{{ user.nickname }}">
    <button type="submit">수정하기</button>
</form>
```

```python
# Flask 서버 측 CSRF 보호 설정
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)
```

#### 사례 4: 디버그 모드 배포

AI가 생성한 Flask 또는 Django 프로젝트의 실행 코드에는 거의 항상 디버그 모드가 활성화되어 있습니다.

❌ 취약한 코드

```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

디버그 모드(Debug Mode)가 활성화된 상태로 배포하면 상세한 에러 메시지, 스택 트레이스(Stack Trace), 심지어 대화형 디버거까지 외부에 노출됩니다.

✅ 안전한 코드

```python
import os

if __name__ == '__main__':
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
```

### 바이브 코딩 시 체크포인트

여러분이 AI 도구로 웹사이트를 만들 때 반드시 확인해야 할 핵심 사항을 정리합니다.

- [ ] AI가 생성한 코드에 비밀키, API 키, 비밀번호가 하드코딩되어 있지 않은지 확인하십시오
- [ ] 데이터베이스 쿼리가 문자열 결합이 아닌 매개변수화된 쿼리로 작성되어 있는지 확인하십시오
- [ ] 모든 POST 폼에 CSRF 토큰이 포함되어 있는지 확인하십시오
- [ ] 디버그 모드가 프로덕션 환경에서 비활성화되어 있는지 확인하십시오
- [ ] AI에게 코드를 요청할 때 보안 요구사항을 프롬프트에 명시하십시오

> **💡 팁:** AI 도구를 사용할 때 프롬프트 끝에 항상 "보안 모범 사례(Security Best Practices)를 따라줘"를 추가하는 습관을 기르십시오. 이것만으로도 AI가 생성하는 코드의 보안 품질이 크게 향상됩니다.

---

## 1-2. 이 가이드의 활용법

### 개요

이 가이드는 바이브 코딩으로 웹사이트를 만드는 여러분을 위해 설계되었습니다. 전문 보안 엔지니어가 아니더라도 이해할 수 있도록 모든 내용을 실용적이고 구체적으로 구성하였습니다. 이 절에서는 가이드의 전체 구조와 효과적인 활용 방법을 안내합니다.

### 가이드의 전체 구조

이 책은 6개의 PART로 구성되어 있습니다.

| PART | 제목 | 내용 |
|------|------|------|
| **PART 1** | 시작하기 | 왜 바이브 코딩에도 보안이 필요한가, 이 가이드의 활용법 |
| **PART 2** | 입력값을 믿지 마세요 | SQL 삽입, XSS, CSRF 등 입력데이터 검증 |
| **PART 3** | 보안 기능을 제대로 구현하세요 | 인증, 인가, 암호화, 패스워드, 민감정보 보호 |
| **PART 4** | 안정적인 코드를 작성하세요 | 경쟁조건, 에러처리, 코드오류 |
| **PART 5** | 구조와 설계로 지키세요 | 캡슐화, API 오용 |
| **PART 6** | 바이브 코딩 보안 체크리스트 | 배포 전 점검, AI 프롬프트, TOP 10 실수 |

PART 2부터 PART 5까지는 웹 애플리케이션의 주요 보안 취약점 카테고리를 다룹니다. 각 장은 하나의 취약점 유형을 깊이 있게 설명하며, 모두 동일한 구조를 따릅니다. PART 6은 실전에서 바로 활용할 수 있는 체크리스트와 도구를 제공합니다.

### 각 장의 구조

이 가이드의 모든 보안 주제는 다음과 같은 일관된 구조로 작성되어 있습니다.

#### 1단계: 개요

해당 보안 취약점이 무엇인지 간결하게 설명합니다. 전문 용어를 처음 사용할 때는 한글과 영어를 함께 표기합니다. 예를 들어, "크로스사이트 스크립트(Cross-Site Scripting, XSS)"과 같이 작성됩니다.

#### 2단계: 왜 위험한가

이 취약점이 실제로 어떤 피해를 초래할 수 있는지 설명합니다. 추상적인 위험이 아닌, 바이브 코딩 환경에서 실제로 발생할 수 있는 구체적인 시나리오를 다룹니다.

#### 3단계: 취약한 코드 vs. 안전한 코드

모든 주제에서 다음과 같은 코드 비교 형식을 사용합니다.

- **❌ 취약한 코드** — AI가 흔히 생성하는, 보안에 취약한 코드 예시입니다
- **✅ 안전한 코드** — 같은 기능을 안전하게 구현한 코드 예시입니다

코드 예시는 주로 Python(Flask/Django)과 JavaScript(Node.js/Express)로 작성되어 있으며, 바이브 코딩에서 가장 많이 사용되는 기술 스택을 반영하였습니다.

#### 4단계: 바이브 코딩 시 체크포인트

각 장의 마지막에는 해당 취약점에 대한 체크리스트가 제공됩니다. 이 체크리스트를 배포 전에 확인하면 해당 취약점을 효과적으로 예방할 수 있습니다.

### 이 가이드를 읽는 두 가지 방법

#### 방법 1: 처음부터 끝까지 순서대로 읽기

보안에 대한 기초 지식이 부족하다고 느끼는 분께 권장합니다. PART 1에서 기본 개념을 이해한 후 PART 2부터 순서대로 읽어나가면 웹 보안에 대한 체계적인 이해를 쌓을 수 있습니다. 이 방법은 약 1~2주 정도의 시간이 소요됩니다.

#### 방법 2: 필요한 부분만 골라 읽기

이미 웹 개발 경험이 있거나, 특정 보안 이슈를 해결해야 하는 분께 권장합니다. 목차에서 해당 주제를 찾아 바로 이동하십시오. 각 장은 독립적으로 읽을 수 있도록 구성되어 있습니다.

예를 들어, 다음과 같은 상황별 추천 경로가 있습니다.

| 상황 | 추천 챕터 |
|------|-----------|
| 로그인 기능을 AI로 만들었다 | 7장 (PART 3) |
| API 키를 코드에 넣었다 | 8장 8-3절 (PART 3) |
| 파일 업로드 기능을 추가했다 | 5장 5-2절 (PART 2) |
| 배포 직전이다 | 17장 (PART 6) |
| 에러가 나는데 그냥 배포했다 | 13장 (PART 4) |

> **💡 팁:** 바이브 코딩으로 만든 프로젝트를 배포하기 직전이라면, 먼저 PART 6의 체크리스트(Chapter 17)로 이동하여 빠르게 점검한 후, 체크리스트에서 "불합격"인 항목의 해당 챕터를 참고하는 것이 가장 효율적입니다.

### AI 도구와 함께 이 가이드 활용하기

이 가이드의 가장 큰 특징은 AI 도구와 함께 사용하도록 설계되었다는 점입니다. 다음과 같은 워크플로를 권장합니다.

**1단계: AI로 코드 생성**
Cursor, Claude Code, Copilot 등으로 원하는 기능의 코드를 생성합니다.

**2단계: 이 가이드로 보안 점검**
생성된 코드를 이 가이드의 해당 챕터와 대조하여 취약점이 있는지 확인합니다.

**3단계: AI에게 보안 개선 요청**
발견된 취약점을 AI에게 명시적으로 알려주고 수정을 요청합니다. PART 6에 준비된 프롬프트 템플릿을 활용하십시오.

**4단계: 체크리스트로 최종 확인**
배포 전 PART 6의 체크리스트를 통해 전체적인 보안 상태를 최종 점검합니다.

### 이 가이드에서 다루지 않는 것

이 가이드는 바이브 코딩으로 만든 웹 애플리케이션의 보안에 집중합니다. 다음 주제는 이 가이드의 범위에 포함되지 않습니다.

- 네트워크 보안(방화벽, VPN 등)의 심화 설정
- 모바일 네이티브 앱의 보안
- 대규모 엔터프라이즈 환경의 보안 아키텍처
- 침투 테스트(Penetration Testing) 방법론의 상세 내용

이러한 주제가 필요한 경우 OWASP(Open Web Application Security Project)의 공식 가이드라인을 참고하시기 바랍니다.

### 바이브 코딩 시 체크포인트

- [ ] 이 가이드의 PART 구조를 이해하고, 자신에게 맞는 읽기 방법을 선택하였는지 확인하십시오
- [ ] AI로 코드를 생성한 후 반드시 보안 점검 단계를 거치는 습관을 만드십시오
- [ ] PART 6의 체크리스트를 북마크하여 배포 전 언제든 참조할 수 있도록 하십시오
- [ ] AI에게 코드를 요청할 때 보안 요구사항을 프롬프트에 포함하는 것을 기본 원칙으로 삼으십시오

> **⚠️ 주의:** 이 가이드를 읽는 것만으로는 보안이 보장되지 않습니다. 반드시 자신의 코드에 직접 적용하고, 체크리스트를 통해 확인하는 실천이 필요합니다. 보안은 한 번의 작업이 아니라 지속적인 과정입니다.

---

# PART 2. 입력값을 믿지 마세요 — 입력데이터 검증

# Chapter 02. 데이터베이스를 노리는 삽입 공격

## 2-1. SQL 삽입(SQL Injection)

### 개요

SQL 삽입(SQL Injection)은 웹 보안 취약점 중 가장 오래되고 가장 치명적인 공격 중 하나입니다. 데이터베이스(Database)와 연동된 웹 애플리케이션에서 사용자 입력값에 대한 유효성 검증을 하지 않을 경우, 공격자가 입력 폼이나 URL 파라미터에 SQL 문을 삽입하여 데이터베이스의 정보를 열람하거나 조작할 수 있습니다.

바이브 코딩(Vibe Coding)으로 웹사이트를 만들 때, AI가 생성한 코드에서 데이터베이스 쿼리 부분을 특히 주의 깊게 살펴봐야 합니다. AI 도구가 때로는 편의를 위해 문자열 결합(String Concatenation) 방식으로 쿼리를 생성하는 경우가 있기 때문입니다.

### 왜 위험한가

SQL 삽입 공격이 성공하면 공격자는 다음과 같은 행위를 할 수 있습니다:

- **데이터 유출**: 회원 정보, 비밀번호, 개인정보 등 전체 데이터베이스 내용을 탈취할 수 있습니다
- **데이터 변조**: 게시글 수정, 회원 정보 변경, 관리자 권한 획득 등이 가능합니다
- **데이터 삭제**: `DROP TABLE` 등의 명령으로 전체 데이터를 삭제할 수 있습니다
- **서버 장악**: 일부 데이터베이스에서는 운영체제 명령어 실행까지 가능합니다

예를 들어, 로그인 폼에서 비밀번호 입력란에 `' OR '1'='1` 이라고 입력하면, 원래 의도된 쿼리가 완전히 다른 의미로 변환됩니다:

```sql
-- 원래 의도된 쿼리
SELECT * FROM users WHERE username='admin' AND password='입력값'

-- 공격자의 입력으로 변조된 쿼리
SELECT * FROM users WHERE username='admin' AND password='' OR '1'='1'
```

조건절 `'1'='1'`은 항상 참이므로 비밀번호 없이 로그인에 성공하게 됩니다.

### SQL 삽입 공격 흐름도

#### ❌ 취약한 흐름 (문자열 결합 방식)

```
 ┌─────────────┐         ┌─────────────────┐         ┌──────────────────┐         ┌─────────────┐
 │  공격자      │         │   웹 애플리케이션  │         │   조합된 SQL 쿼리  │         │  데이터베이스  │
 │             │         │  (검증 없음)      │         │                  │         │             │
 │ 입력값:      │         │                 │         │ SELECT * FROM    │         │ ⚠ 전체 데이터 │
 │ ' OR 1=1 -- │ ══════▶ │ 입력값을 그대로   │ ══════▶ │ users WHERE id=  │ ══════▶ │   유출됨!    │
 │             │         │ 쿼리에 삽입      │         │ '' OR 1=1 --'   │         │             │
 └─────────────┘         └─────────────────┘         └──────────────────┘         └─────────────┘
       ①                        ②                          ③                          ④
   악성 입력 전송           입력값 검증 없이              공격 구문이 SQL에            모든 사용자 정보
                          문자열 결합 수행              그대로 포함됨               무단 조회 성공
```

#### ✅ 안전한 흐름 (파라미터화된 쿼리 방식)

```
 ┌─────────────┐         ┌─────────────────┐         ┌──────────────────┐         ┌─────────────┐
 │  공격자      │         │   웹 애플리케이션  │         │  파라미터화된 쿼리  │         │  데이터베이스  │
 │             │         │ (Prepared Stmt)  │         │                  │         │             │
 │ 입력값:      │         │                 │         │ SELECT * FROM    │         │ ✅ 정상 동작  │
 │ ' OR 1=1 -- │ ──────▶ │ 입력값을 매개변수  │ ──────▶ │ users WHERE id=? │ ──────▶ │   결과 없음   │
 │             │         │ 로 바인딩        │         │ 값: "' OR 1=1 --"│         │  (공격 차단)  │
 └─────────────┘         └─────────────────┘         └──────────────────┘         └─────────────┘
       ①                        ②                          ③                          ④
   동일한 악성 입력          입력값을 데이터로만           SQL 구조와 데이터가          악성 입력이 단순
                          처리 (코드로 해석 안 함)       완전히 분리됨               문자열로 처리됨
```

#### 핵심 차이점

```
  ┌───────────────────────────────────────────────────────────────┐
  │                     문자열 결합 (위험)                         │
  │  "SELECT * FROM users WHERE id='" + 입력값 + "'"             │
  │  ══════▶  입력값이 SQL 코드로 실행됨                           │
  └───────────────────────────────────────────────────────────────┘

  ┌───────────────────────────────────────────────────────────────┐
  │                   파라미터 바인딩 (안전)                        │
  │  "SELECT * FROM users WHERE id=?"  +  매개변수: 입력값         │
  │  ──────▶  입력값이 항상 데이터로만 처리됨                        │
  └───────────────────────────────────────────────────────────────┘
```

### 취약한 코드

#### ❌ 취약한 코드: SQLAlchemy에서 text()와 문자열 결합 사용

```python
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/update-board")
async def update_board(
    request: Request,
    name: str = Form(...),
    content_id: str = Form(...),
    db: AsyncSession = Depends(get_async_session),
):
    # 문자열 결합으로 쿼리를 생성하면 SQL 삽입에 취약합니다
    sql_query = "UPDATE board SET name='" + name + "' WHERE content_id='" + content_id + "'"
    await db.execute(text(sql_query))
    await db.commit()

    return templates.TemplateResponse("success.html", {"request": request})
```

이 코드에서 `content_id` 값으로 `a' OR 'a'='a`를 입력하면, 조건절이 `content_id='a' OR 'a'='a'`로 바뀌어 board 테이블의 **모든 레코드**가 변경됩니다.

> **⚠️ 주의:** AI 도구에 "게시판 수정 기능 만들어줘"라고 요청하면, 간혹 위와 같은 문자열 결합 방식의 코드가 생성될 수 있습니다. 특히 "간단한 예제"를 요청하면 보안이 생략되는 경우가 많습니다.

#### ❌ 취약한 코드: SQLAlchemy에서 raw SQL 오용

```python
from fastapi import FastAPI, Form, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/member-search")
async def member_search(
    request: Request,
    name: str = Form(...),
    db: AsyncSession = Depends(get_async_session),
):
    # text()에 문자열 결합으로 쿼리를 전달하면 취약합니다
    query = "SELECT * FROM member WHERE name='" + name + "'"
    result = await db.execute(text(query))
    member_list = result.fetchall()

    return templates.TemplateResponse(
        "member_list.html", {"request": request, "member_list": member_list}
    )
```

SQLAlchemy의 ORM(Object-Relational Mapping)을 사용하면서도 `text()`에 문자열 결합을 하면 ORM의 보호 기능이 완전히 무력화됩니다.

### 안전한 코드

#### ✅ 안전한 코드: 바인드 파라미터(Bind Parameter) 사용

```python
from fastapi import FastAPI, Form, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/update-board")
async def update_board(
    request: Request,
    name: str = Form(...),
    content_id: str = Form(...),
    db: AsyncSession = Depends(get_async_session),
):
    # 바인드 파라미터(:name, :content_id)를 사용합니다
    sql_query = text("UPDATE board SET name=:name WHERE content_id=:content_id")
    # bindparams로 값을 안전하게 바인딩합니다
    await db.execute(sql_query, {"name": name, "content_id": content_id})
    await db.commit()

    return templates.TemplateResponse("success.html", {"request": request})
```

바인드 파라미터(Bind Parameter)를 사용하면 사용자 입력값이 SQL 구문이 아닌 **순수한 데이터**로만 처리됩니다. 공격자가 어떤 값을 넣더라도 쿼리 구조 자체는 변경할 수 없습니다.

#### ✅ 안전한 코드: SQLAlchemy text()의 올바른 사용

```python
from fastapi import FastAPI, Form, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/member-search")
async def member_search(
    request: Request,
    name: str = Form(...),
    db: AsyncSession = Depends(get_async_session),
):
    # 바인드 파라미터와 딕셔너리를 사용합니다
    query = text("SELECT * FROM member WHERE name=:name")
    result = await db.execute(query, {"name": name})
    member_list = result.fetchall()

    return templates.TemplateResponse(
        "member_list.html", {"request": request, "member_list": member_list}
    )
```

#### ✅ 가장 안전한 코드: SQLAlchemy ORM + Pydantic 모델 활용

```python
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Pydantic 모델로 입력값을 사전 검증합니다
class MemberSearchRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

@app.post("/member-search")
async def member_search(
    request: Request,
    search: MemberSearchRequest,
    db: AsyncSession = Depends(get_async_session),
):
    # SQLAlchemy ORM의 select()는 자동으로 바인드 파라미터를 생성합니다
    stmt = select(Member).where(Member.name == search.name)
    result = await db.execute(stmt)
    member_list = result.scalars().all()

    return templates.TemplateResponse(
        "member_list.html", {"request": request, "member_list": member_list}
    )
```

> **💡 팁:** SQLAlchemy ORM의 `select()`, `where()`, `filter()` 등의 메서드를 사용하면 프레임워크(Framework)가 자동으로 SQL 삽입을 방지합니다. 여기에 Pydantic 모델을 결합하면 입력값의 타입과 길이까지 사전 검증할 수 있어 가장 안전합니다.

#### ✅ 안전한 코드: SQLite에서의 바인드 파라미터

```python
import sqlite3

def get_user(username):
    conn = sqlite3.connect('mydb.sqlite3')
    cursor = conn.cursor()

    # ? 플레이스홀더 사용 (SQLite 방식)
    cursor.execute('SELECT * FROM users WHERE username=?', (username,))
    result = cursor.fetchone()

    conn.close()
    return result
```

SQLite에서는 `?`를 플레이스홀더(Placeholder)로 사용하거나, `:name` 형식의 Named Placeholder를 사용할 수 있습니다.

### 바이브 코딩 시 체크포인트

AI 도구로 데이터베이스 관련 코드를 생성할 때 다음 항목을 반드시 확인하십시오:

- [ ] **문자열 결합으로 SQL 쿼리를 만들고 있지 않은가?** `+` 연산자나 f-string으로 쿼리를 조합하는 코드는 모두 위험합니다
- [ ] **ORM의 기본 기능을 사용하고 있는가?** SQLAlchemy의 `select()`, `where()`, `filter()` 등 ORM 기본 메서드가 가장 안전합니다
- [ ] **raw SQL이 꼭 필요한가?** 복잡한 쿼리라도 대부분 ORM으로 표현할 수 있습니다. `text()` 사용은 최소화하십시오
- [ ] **바인드 파라미터를 사용하고 있는가?** raw SQL이 불가피한 경우 반드시 `:name` 등의 바인드 파라미터와 딕셔너리 바인딩을 사용하십시오
- [ ] **Pydantic 모델로 입력값을 검증하고 있는가?** FastAPI의 Pydantic 통합은 타입, 길이, 패턴 등 다양한 검증을 자동으로 수행합니다
- [ ] **AI에게 보안 요구사항을 명시했는가?** 프롬프트에 "SQL 인젝션 방지를 위해 파라미터 바인딩을 사용해줘"라고 명시하면 훨씬 안전한 코드가 생성됩니다

> **💡 팁:** AI 도구에 코드를 요청할 때 "SQLAlchemy ORM을 사용해서 안전하게 만들어줘"라고 추가하면, 대부분 ORM 기반의 안전한 코드를 생성합니다. "raw SQL 없이"라는 조건을 붙이는 것도 좋은 방법입니다.

---

## 2-2. LDAP 삽입(LDAP Injection)

> **📦 기타 삽입 공격 — LDAP 삽입**
>
> **우선순위: 낮음** — 대부분의 바이브 코딩 프로젝트에서는 LDAP를 직접 다루는 경우가 드뭅니다. 하지만 기업용 사내 시스템이나 Active Directory 연동 기능을 구현할 때는 주의가 필요합니다.
>
> **LDAP(Lightweight Directory Access Protocol)**은 조직 내 사용자 정보를 관리하는 디렉터리 서비스 프로토콜입니다. SQL 삽입과 동일한 원리로, 사용자 입력값이 LDAP 쿼리문에 검증 없이 포함되면 공격자가 쿼리 구조를 변경하여 권한 상승이나 정보 유출을 시도할 수 있습니다.
>
> **핵심 방어 방법:**
> - `ldap3` 라이브러리 사용 시 `escape_filter_chars()` 함수로 입력값을 이스케이프(Escape) 처리합니다
> - 화이트리스트(Whitelist) 방식으로 검색 가능한 값을 제한합니다
>
> ```python
> # ❌ 취약한 코드
> search_str = '(&(objectclass=%s))' % search_keyword
>
> # ✅ 안전한 코드
> from ldap3.utils.conv import escape_filter_chars
> escaped = escape_filter_chars(search_keyword)
> search_str = '(&(objectclass=%s))' % escaped
> ```
>
> AI 도구가 LDAP 관련 코드를 생성할 때는 반드시 입력값 이스케이프 처리가 포함되어 있는지 확인하십시오.

---

# Chapter 03. 코드와 명령어를 노리는 삽입 공격

## 3-1. 코드 삽입(Code Injection)

### 개요

코드 삽입(Code Injection)은 공격자가 애플리케이션에 임의의 프로그래밍 코드를 삽입하여 실행시키는 공격입니다. SQL 삽입이 데이터베이스를 대상으로 한다면, 코드 삽입은 **프로그래밍 언어 자체**를 대상으로 합니다.

파이썬(Python)에서 코드 삽입 공격을 유발하는 대표적인 함수는 `eval()`과 `exec()`입니다. 이 함수들은 문자열을 코드로 해석하여 실행하는 기능을 제공하며, 바이브 코딩(Vibe Coding) 시 AI가 "동적으로 값을 계산해줘"라는 요청에 이 함수들을 사용하는 코드를 생성하는 경우가 있어 각별한 주의가 필요합니다.

### 왜 위험한가

`eval()`이나 `exec()` 함수에 사용자 입력값이 그대로 전달되면, 공격자는 서버에서 **어떤 파이썬 코드든** 실행할 수 있습니다:

- **시스템 정보 탈취**: `__import__('platform').system()` 입력으로 서버 OS 정보 노출
- **파일 시스템 접근**: `__import__('os').listdir('/')` 입력으로 서버 파일 목록 조회
- **원격 쉘 실행**: 공격자가 서버에 원격으로 접속하여 완전한 제어권을 획득
- **서비스 거부**: `time.sleep(99999)` 등으로 서버를 마비시키는 것도 가능

예를 들어, 공격자가 다음과 같은 값을 입력하면 서버가 20초 동안 응답 불능 상태에 빠집니다:

```
compile('for x in range(1):\n import time\n time.sleep(20)','a','single')
```

### 취약한 코드

#### ❌ 취약한 코드: eval() 함수에 외부 입력값 직접 전달

```python
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/route")
async def route(request: Request, message: str = Form(...)):
    # eval() 함수에 사용자 입력을 그대로 전달하면
    # 임의의 파이썬 코드가 실행될 수 있습니다
    ret = eval(message)
    return templates.TemplateResponse(
        "success.html", {"request": request, "data": ret}
    )
```

#### ❌ 취약한 코드: exec() 함수로 동적 함수 호출

```python
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/request-rest-api")
async def request_rest_api(request: Request, function_name: str = Form(...)):
    # 사용자에게 전달받은 함수명을 검증하지 않고 실행
    # "__import__('platform').system()" 등을 입력하면
    # 시스템 정보가 노출됩니다
    exec('{}()'.format(function_name))
    return templates.TemplateResponse("success.html", {"request": request})
```

> **⚠️ 주의:** AI 도구에 "사용자가 입력한 수식을 계산해주는 기능 만들어줘"라고 요청하면 `eval()`을 사용하는 코드가 높은 확률로 생성됩니다. 이는 매우 위험합니다.

### 안전한 코드

#### ✅ 안전한 코드: Pydantic 검증 후 eval() 사용

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, field_validator

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class MessageRequest(BaseModel):
    message: str

    @field_validator("message")
    @classmethod
    def validate_message(cls, v: str) -> str:
        # 입력값이 영문과 숫자로만 구성되었는지 검증합니다
        if not v.isalnum():
            raise ValueError("영문과 숫자만 입력 가능합니다.")
        return v

@app.post("/route")
async def route(request: Request, body: MessageRequest):
    ret = eval(body.message)
    return templates.TemplateResponse(
        "success.html", {"request": request, "data": ret}
    )
```

#### ✅ 안전한 코드: 화이트리스트(Whitelist) 기반 함수 실행 제한

```python
from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 실행 가능한 함수를 사전에 정의합니다
WHITE_LIST = ['get_friends_list', 'get_address', 'get_phone_number']

@app.post("/request-rest-api")
async def request_rest_api(request: Request, function_name: str = Form(...)):
    # 허용된 함수 목록에 포함된 경우에만 실행합니다
    if function_name not in WHITE_LIST:
        raise HTTPException(status_code=400, detail="허용되지 않은 함수입니다.")

    exec('{}()'.format(function_name))
    return templates.TemplateResponse("success.html", {"request": request})
```

#### ✅ 가장 안전한 코드: eval()/exec() 자체를 사용하지 않기

```python
import ast
from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/calculate")
async def calculate(request: Request, expression: str = Form(...)):
    try:
        # ast.literal_eval()은 리터럴 표현식만 평가합니다
        # 함수 호출이나 import 등 위험한 코드는 실행되지 않습니다
        result = ast.literal_eval(expression)
        return templates.TemplateResponse(
            "success.html", {"request": request, "data": result}
        )
    except (ValueError, SyntaxError):
        raise HTTPException(status_code=400, detail="올바른 값을 입력해주세요.")
```

> **💡 팁:** 수식 계산이 필요한 경우 `ast.literal_eval()`을 사용하거나, 수학 전용 라이브러리인 `numexpr`, `sympy` 등을 활용하는 것이 `eval()`보다 훨씬 안전합니다.

### 바이브 코딩 시 체크포인트

- [ ] **코드에 `eval()` 또는 `exec()`가 포함되어 있지 않은가?** AI가 생성한 코드에서 이 함수들이 보이면 반드시 대안을 검토하십시오
- [ ] **동적 코드 실행이 정말 필요한가?** 대부분의 경우 `eval()` 없이도 동일한 기능을 구현할 수 있습니다
- [ ] **사용자 입력값이 코드 실행 함수에 직접 전달되지 않는가?** 불가피한 경우 화이트리스트로 실행 가능한 범위를 제한하십시오

---

## 3-2. 운영체제 명령어 삽입(OS Command Injection)

### 개요

운영체제 명령어 삽입(OS Command Injection)은 사용자 입력값이 시스템 명령어의 일부로 사용되어, 공격자가 의도하지 않은 운영체제 명령을 실행할 수 있는 취약점입니다.

파이썬에서는 `os.system()`, `subprocess.run()`, `subprocess.Popen()` 등의 함수가 운영체제 명령어를 실행합니다. 바이브 코딩으로 파일 처리, 시스템 유틸리티 호출, 외부 프로그램 연동 등의 기능을 구현할 때 이 취약점에 노출되기 쉽습니다.

### 왜 위험한가

공격자가 시스템 명령어를 주입하면 서버의 운영체제 수준에서 명령이 실행됩니다. 이는 코드 삽입보다 더 심각한 결과를 초래할 수 있습니다:

- **서버 파일 열람/삭제**: `cat /etc/passwd`, `rm -rf /` 등의 명령 실행 가능
- **악성 프로그램 설치**: `wget`이나 `curl`로 악성코드를 다운로드하여 실행
- **서버 장악**: 리버스 쉘(Reverse Shell)을 열어 서버를 완전히 제어

특수문자 `|`, `;`, `&`, `` ` `` 등을 사용하면 여러 명령어를 연결하여 실행할 수 있습니다:

```
# 원래 의도: 날짜를 인자로 백업 실행
backuplog.bat 2024-01-01

# 공격자 입력: 2024-01-01; cat /etc/passwd
# 실제 실행: backuplog.bat 2024-01-01; cat /etc/passwd
```

### 취약한 코드

#### ❌ 취약한 코드: os.system()에 외부 입력값 직접 사용

```python
import os
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/execute-command")
async def execute_command(request: Request, app_name: str = Form(...)):
    # 입력 파라미터를 제한하지 않아 외부 입력값으로
    # 전달된 모든 프로그램이 실행될 수 있습니다
    os.system(app_name)
    return templates.TemplateResponse("success.html", {"request": request})
```

#### ❌ 취약한 코드: subprocess에서 shell=True 사용

```python
import subprocess
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/execute-command")
async def execute_command(request: Request, date: str = Form(...)):
    # shell=True와 문자열 결합은 명령어 삽입의 원인이 됩니다
    cmd_str = "cmd /c backuplog.bat " + date
    subprocess.run(cmd_str, shell=True)
    return templates.TemplateResponse("success.html", {"request": request})
```

> **⚠️ 주의:** `subprocess.run()`의 `shell=True` 옵션은 중간 프로세스(쉘)를 통해 명령을 실행하므로, 와일드카드(Wildcard) 확장, 환경변수 참조, 명령어 연결 등이 모두 가능해져 매우 위험합니다.

### 안전한 코드

#### ✅ 안전한 코드: 화이트리스트로 실행 가능한 프로그램 제한

```python
import os
from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

ALLOW_PROGRAM = ['notepad', 'calc']

@app.post("/execute-command")
async def execute_command(request: Request, app_name: str = Form(...)):
    # 허용된 프로그램 목록에 포함되는지 검사합니다
    if app_name not in ALLOW_PROGRAM:
        raise HTTPException(status_code=400, detail="허용되지 않은 프로그램입니다.")

    os.system(app_name)
    return templates.TemplateResponse("success.html", {"request": request})
```

#### ✅ 안전한 코드: 특수문자 필터링 + 배열 형태 인자 전달

```python
import subprocess
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/execute-command")
async def execute_command(request: Request, date: str = Form(...)):
    # 명령어 연결에 사용되는 특수문자를 필터링합니다
    for word in ['|', ';', '&', ':', '>', '<', '`', '\\', '!']:
        date = date.replace(word, "")

    # shell=True를 사용하지 않고, 명령과 인자를 배열로 전달합니다
    subprocess.run(["cmd", "/c", "backuplog.bat", date])
    return templates.TemplateResponse("success.html", {"request": request})
```

> **💡 팁:** `subprocess` 사용 시 `shell=True`를 절대 사용하지 마십시오. 명령어와 인자를 리스트(List) 형태로 분리하여 전달하면 쉘 해석 과정 없이 직접 실행되므로 훨씬 안전합니다.

### 바이브 코딩 시 체크포인트

- [ ] **`os.system()` 대신 `subprocess.run()`을 리스트 인자로 사용하고 있는가?**
- [ ] **`shell=True` 옵션이 사용되고 있지 않은가?**
- [ ] **사용자 입력이 명령어의 일부로 사용된다면 특수문자 필터링이 적용되어 있는가?**
- [ ] **정말 시스템 명령어를 호출해야 하는가?** 파이썬 내장 라이브러리로 대체할 수 있는 경우가 많습니다 (예: `shutil` 모듈로 파일 복사)

---

## 3-3. XML 삽입(XML Injection)

### 개요

XML 삽입(XML Injection)은 XQuery 또는 XPath 쿼리문에 검증되지 않은 외부 입력값이 포함되어, 공격자가 쿼리 구조를 변경하고 허가되지 않은 데이터에 접근할 수 있는 보안약점입니다.

바이브 코딩 환경에서 XML 데이터를 직접 다루는 경우는 비교적 적지만, 레거시 시스템(Legacy System)과의 연동이나 SOAP API 호출 시 이 취약점을 마주할 수 있습니다.

### 왜 위험한가

XML 기반 데이터 조회에서 XPath를 사용할 때, SQL 삽입과 동일한 원리로 쿼리가 변조될 수 있습니다:

```xpath
# 원래 의도된 쿼리
/collection/users/user[@name='kim']/home/text()

# 공격자가 name에 ' or '1'='1 입력 시
/collection/users/user[@name='' or '1'='1']/home/text()
```

이렇게 되면 모든 사용자의 정보가 노출됩니다.

### 취약한 코드

#### ❌ 취약한 코드: XPath 쿼리에 문자열 결합 사용

```python
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from lxml import etree

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/parse-xml")
async def parse_xml(request: Request, user_name: str = Form(...)):
    parser = etree.XMLParser(resolve_entities=False)
    tree = etree.parse('user.xml', parser)
    root = tree.getroot()

    # 검증되지 않은 입력값을 문자열 결합으로 쿼리에 포함합니다
    query = "/collection/users/user[@name='" + user_name + "']/home/text()"
    elmts = root.xpath(query)

    return templates.TemplateResponse(
        "parse_xml.html", {"request": request, "xml_element": elmts}
    )
```

### 안전한 코드

#### ✅ 안전한 코드: XPath 파라미터 바인딩 사용

```python
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from lxml import etree

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/parse-xml")
async def parse_xml(request: Request, user_name: str = Form(...)):
    parser = etree.XMLParser(resolve_entities=False)
    tree = etree.parse('user.xml', parser)
    root = tree.getroot()

    # 외부 입력값을 $paramname으로 인자화하여 사용합니다
    query = '/collection/users/user[@name = $paramname]/home/text()'
    elmts = root.xpath(query, paramname=user_name)

    return templates.TemplateResponse(
        "parse_xml.html", {"request": request, "xml_element": elmts}
    )
```

> **💡 팁:** `lxml` 라이브러리의 XPath는 `$변수명` 형식의 파라미터 바인딩을 지원합니다. SQL의 바인드 파라미터와 동일한 원리이므로, 항상 파라미터 바인딩을 사용하십시오.

---

## 3-4. 포맷 스트링 삽입(Format String Injection)

### 개요

포맷 스트링 삽입(Format String Injection)은 파이썬의 f-string이나 `.format()` 메서드를 사용할 때, 사용자 입력값이 포맷 문자열 자체에 포함되어 의도하지 않은 정보가 노출되는 취약점입니다.

전통적인 C 언어의 포맷 스트링 공격과는 다소 다르지만, 파이썬에서도 `.format()` 메서드를 통해 객체의 속성(Attribute)에 접근하거나 내부 정보를 유출할 수 있습니다.

### 왜 위험한가

파이썬의 `.format()` 메서드는 객체의 속성에 접근하는 기능을 제공합니다. 공격자가 이를 악용하면 서버의 내부 정보를 탈취할 수 있습니다:

```python
# 의도된 사용
"Hello, {name}!".format(name="Kim")

# 공격자가 name에 다음과 같은 값을 전달하면?
# {user.__class__.__init__.__globals__}
# -> 글로벌 변수에 저장된 비밀키, 설정값 등이 노출됩니다
```

### 취약한 코드

#### ❌ 취약한 코드: 사용자 입력으로 포맷 문자열 구성

```python
from fastapi import FastAPI, Form, Request, Depends
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/greeting")
async def greeting(request: Request, template: str = Form(...)):
    # 사용자 입력을 포맷 문자열 자체로 사용하면 위험합니다
    # 예: template = "{user.__class__.__init__.__globals__}"
    message = template.format(user=request)
    return templates.TemplateResponse(
        "greeting.html", {"request": request, "message": message}
    )
```

#### ❌ 취약한 코드: f-string에서의 위험한 패턴

```python
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/render-message")
async def render_message(request: Request, user_input: str = Form(...)):
    # 사용자 입력을 eval()과 f-string으로 결합하면 코드 실행이 가능합니다
    # 이 패턴은 AI가 "동적 메시지 생성"을 구현할 때 생성할 수 있습니다
    message = eval(f"f'{user_input}'")
    return templates.TemplateResponse(
        "result.html", {"request": request, "message": message}
    )
```

> **⚠️ 주의:** `eval()`과 f-string의 조합은 코드 삽입과 포맷 스트링 삽입이 동시에 발생하는 매우 위험한 패턴입니다. AI가 이런 코드를 생성하면 즉시 수정하십시오.

### 안전한 코드

#### ✅ 안전한 코드: 고정된 포맷 문자열 사용

```python
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/greeting")
async def greeting(request: Request, name: str = Form(...)):
    # 포맷 문자열은 코드에서 고정하고, 사용자 입력은 인자로만 전달합니다
    message = "안녕하세요, {}님!".format(name)
    return templates.TemplateResponse(
        "greeting.html", {"request": request, "message": message}
    )
```

#### ✅ 안전한 코드: Jinja2 템플릿 활용

```python
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/greeting")
async def greeting(request: Request, name: str = Form(...)):
    # Jinja2 템플릿에서 변수를 렌더링하면 자동으로 이스케이프됩니다
    return templates.TemplateResponse(
        "greeting.html", {"request": request, "name": name}
    )
```

```html
<!-- templates/greeting.html -->
<p>안녕하세요, {{ name }}님!</p>
```

> **💡 팁:** 동적 메시지 생성이 필요한 경우, 포맷 문자열을 코드에 고정하고 사용자 입력은 **인자(Argument)**로만 전달하십시오. 사용자가 포맷 문자열 자체를 제어할 수 있게 하면 안 됩니다.

### 바이브 코딩 시 체크포인트

- [ ] **사용자 입력이 `.format()` 또는 f-string의 템플릿 부분에 사용되고 있지 않은가?**
- [ ] **`eval()`과 f-string이 조합되어 있지 않은가?**
- [ ] **동적 메시지는 Jinja2 템플릿으로 처리하고 있는가?**
- [ ] **포맷 문자열은 코드에 하드코딩(Hardcode)되어 있는가?**

---

# Chapter 04. 웹 요청을 노리는 공격

## 4-1. 크로스사이트 스크립트(XSS)

### 개요

크로스사이트 스크립트(Cross-Site Scripting, XSS)는 웹 보안에서 가장 빈번하게 발생하는 취약점 중 하나입니다. 공격자가 웹 애플리케이션에 악성 스크립트(Script)를 삽입하여, 해당 페이지를 방문하는 다른 사용자의 브라우저에서 악성 코드가 실행되도록 만드는 공격입니다.

바이브 코딩(Vibe Coding)으로 웹사이트를 만들 때, 사용자 입력을 화면에 출력하는 기능은 거의 모든 웹사이트에 존재합니다. 게시판, 댓글, 프로필, 검색 결과 등 어디서든 XSS 취약점이 발생할 수 있으므로, 여러분이 만드는 모든 웹페이지에서 이 취약점을 반드시 확인해야 합니다.

### 왜 위험한가

XSS 공격이 성공하면 공격자는 피해자의 브라우저에서 자바스크립트(JavaScript)를 실행할 수 있습니다:

- **세션 탈취**: `document.cookie`를 통해 로그인 세션을 훔쳐 계정을 장악합니다
- **키로깅(Keylogging)**: 사용자의 키보드 입력을 기록하여 비밀번호를 탈취합니다
- **피싱**: 가짜 로그인 폼을 삽입하여 사용자 인증 정보를 수집합니다
- **악성코드 배포**: 방문자의 브라우저를 통해 악성 프로그램을 다운로드시킵니다
- **웹사이트 변조**: 페이지 내용을 임의로 수정하여 가짜 정보를 표시합니다

### XSS 3가지 유형 비교도

#### ① 저장형 XSS (Stored XSS)

```
 ┌─────────────┐         ┌─────────────────┐         ┌─────────────┐         ┌─────────────┐
 │   공격자     │         │    웹 서버       │         │  데이터베이스  │         │  피해자 브라우저│
 │             │         │                 │         │             │         │             │
 │ <script>    │         │   게시글 저장     │         │ 악성 스크립트 │         │ ⚠ 스크립트   │
 │ 악성코드     │ ══════▶ │   처리           │ ══════▶ │ DB에 저장됨  │         │   자동 실행!  │
 │ </script>   │         │                 │         │             │         │             │
 └─────────────┘         └─────────────────┘         └─────────────┘         └─────────────┘
                                                           │                       ▲
                                                           │    피해자가 해당       │
                                                           │    페이지 접속 시      │
                                                           └───────────────────────┘
                                                              DB에서 읽어 응답에
                                                              포함하여 전달 ══════▶

  특징: 악성코드가 서버에 영구 저장 ──▶ 해당 페이지 방문하는 모든 사용자 피해
```

#### ② 반사형 XSS (Reflected XSS)

```
 ┌─────────────┐         ┌─────────────┐         ┌─────────────────┐         ┌─────────────┐
 │   공격자     │         │   피해자     │         │    웹 서버       │         │ 피해자 브라우저│
 │             │         │             │         │                 │         │             │
 │ 악성 URL    │         │ 링크 클릭    │         │  URL 파라미터를  │         │ ⚠ 스크립트   │
 │ 제작 및 전송 │ ══════▶ │             │ ══════▶ │  응답에 반사     │ ══════▶ │   실행됨!    │
 │             │         │             │         │                 │         │             │
 └─────────────┘         └─────────────┘         └─────────────────┘         └─────────────┘
       ①                       ②                        ③                        ④
  example.com/search       피해자가 악성            서버가 검색어를              반사된 스크립트가
  ?q=<script>...</script>  링크를 클릭             그대로 HTML에 포함           브라우저에서 실행

  특징: 악성코드가 서버에 저장되지 않음 ──▶ URL을 통해 1회성 공격
```

#### ③ DOM 기반 XSS (DOM-based XSS)

```
 ┌─────────────┐         ┌──────────────────────────────────────────────┐
 │   공격자     │         │            피해자 브라우저                     │
 │             │         │                                              │
 │ 악성 URL    │         │  ┌────────────────┐    ┌─────────────────┐   │
 │ 제작 및 전송 │ ══════▶ │  │ 자바스크립트가  │    │ ⚠ DOM 조작으로   │   │
 │             │         │  │ URL 해시값을    │══▶│   악성코드 실행!  │   │
 │             │         │  │ 직접 DOM에 삽입 │    │                 │   │
 └─────────────┘         │  └────────────────┘    └─────────────────┘   │
       ①                 │         ②                      ③             │
  example.com/#           │   클라이언트 JS가           DOM에 삽입된       │
  <script>...</script>   │   location.hash 읽어       스크립트 실행       │
                         │   innerHTML에 삽입                            │
                         └──────────────────────────────────────────────┘
                                서버를 거치지 않음!
                                ─ ─ ─ ─ ─▶ 서버 (관여하지 않음)

  특징: 서버 통신 없이 브라우저 내에서만 발생 ──▶ 서버 로그에 흔적 없음
```

#### 세 유형 비교 요약

```
  ┌────────────┬──────────────────┬──────────────────┬──────────────────┐
  │    구분     │   저장형 XSS     │   반사형 XSS     │  DOM 기반 XSS    │
  ├────────────┼──────────────────┼──────────────────┼──────────────────┤
  │ 악성코드    │ 서버 DB에 저장    │ URL에 포함       │ URL에 포함       │
  │ 위치       │                  │                  │                  │
  ├────────────┼──────────────────┼──────────────────┼──────────────────┤
  │ 서버 경유   │ ✅ 예            │ ✅ 예            │ ❌ 아니오        │
  ├────────────┼──────────────────┼──────────────────┼──────────────────┤
  │ 지속성      │ 영구적           │ 1회성            │ 1회성            │
  ├────────────┼──────────────────┼──────────────────┼──────────────────┤
  │ 위험도      │ ★★★ 높음        │ ★★ 중간          │ ★★ 중간          │
  └────────────┴──────────────────┴──────────────────┴──────────────────┘
```

### 취약한 코드

#### ❌ 취약한 코드: Jinja2 autoescape 비활성화

```python
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader

app = FastAPI()

# autoescape=False로 설정하면 XSS 공격에 노출됩니다
env = Environment(loader=FileSystemLoader("templates"), autoescape=False)
templates = Jinja2Templates(directory="templates")
templates.env = env

@app.post("/profile-link")
async def profile_link(request: Request, profile_url: str = Form(...), profile_name: str = Form(...)):
    # 외부 입력값을 검증 없이 HTML 태그 생성에 사용
    object_link = '<a href="{}">{}</a>'.format(profile_url, profile_name)

    return templates.TemplateResponse(
        "my_profile.html", {"request": request, "object_link": object_link}
    )
```

#### ❌ 취약한 코드: Jinja2 템플릿에서 safe 필터 오용

```html
<!doctype html>
<html>
<body>
    <div class="content">
        <!-- autoescape false 블록으로 XSS 보호를 해제합니다 -->
        {% autoescape false %}
        {{ content }}
        {% endautoescape %}
    </div>
    <div class="content2">
        <!-- safe 필터도 XSS 보호를 해제합니다 -->
        {{ content | safe }}
    </div>
</body>
</html>
```

> **⚠️ 주의:** AI 도구에 "HTML 태그가 그대로 보여야 해"라고 요청하면 `| safe` 필터나 `autoescape false`를 사용하는 코드가 생성될 수 있습니다. 이는 XSS 보호를 완전히 해제하는 것이므로 매우 위험합니다.

#### ❌ 취약한 코드: HTMLResponse로 직접 HTML 생성

```python
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/search", response_class=HTMLResponse)
async def search(search_keyword: str = Query(...)):
    # 사용자의 입력을 검증이나 치환 없이 HTML에 직접 삽입합니다
    return f"""
    <html>
    <body>
        <p>검색어: {search_keyword}</p>
    </body>
    </html>
    """
```

#### ❌ 취약한 코드: JavaScript에서의 DOM XSS

```html
<script>
// URL 파라미터를 그대로 DOM에 삽입하면 XSS가 발생합니다
const params = new URLSearchParams(window.location.search);
const keyword = params.get('q');

// innerHTML은 HTML을 파싱하므로 스크립트가 실행될 수 있습니다
document.getElementById('search-result').innerHTML =
    '검색어: ' + keyword;
</script>
```

### 안전한 코드

#### ✅ 안전한 코드: Jinja2 기본 autoescape 활성화

```python
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
# Jinja2Templates는 기본적으로 .html 파일에 대해 autoescape가 활성화됩니다
templates = Jinja2Templates(directory="templates")

@app.post("/profile-link")
async def profile_link(request: Request, profile_url: str = Form(...), profile_name: str = Form(...)):
    # 템플릿에서 자동 이스케이프가 적용되므로
    # HTML 태그는 문자열 그대로 표시됩니다
    return templates.TemplateResponse(
        "my_profile.html", {
            "request": request,
            "profile_url": profile_url,
            "profile_name": profile_name,
        }
    )
```

```html
<!-- templates/my_profile.html -->
<!-- Jinja2의 자동 이스케이프가 XSS를 방지합니다 -->
<a href="{{ profile_url }}">{{ profile_name }}</a>
```

#### ✅ 안전한 코드: Jinja2 템플릿에서 autoescape 유지

```html
<!doctype html>
<html>
<body>
    <div class="content">
        {% autoescape true %}
        <!-- autoescape true로 XSS 공격을 방지합니다 -->
        {{ content }}
        {% endautoescape %}
    </div>
    <div class="content2">
        <!-- safe 필터를 사용하지 않습니다 -->
        {{ content }}
    </div>
</body>
</html>
```

> **💡 팁:** FastAPI의 `Jinja2Templates`는 기본적으로 `.html`, `.htm`, `.xml` 확장자에 대해 `autoescape`가 활성화되어 있습니다. 특별한 이유가 없다면 이 설정을 변경하지 마십시오. `Jinja2` 환경을 커스텀 생성할 때 `autoescape=False`로 설정하면 보호가 해제되므로 주의하십시오.

#### ✅ 안전한 코드: html.escape() 사용

```python
import html
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/search")
async def search(request: Request, search_keyword: str = Form(...)):
    # HTML 엔티티 코드로 치환하여 스크립트 실행을 방지합니다
    escape_keyword = html.escape(search_keyword)
    return templates.TemplateResponse(
        "search.html", {"request": request, "search_keyword": escape_keyword}
    )
```

`html.escape()`는 `&`, `<`, `>`, `"`, `'` 등의 특수문자를 `&amp;`, `&lt;`, `&gt;`, `&quot;`, `&#x27;`로 변환합니다.

#### ✅ 안전한 코드: JavaScript에서 textContent 사용

```html
<script>
const params = new URLSearchParams(window.location.search);
const keyword = params.get('q');

// textContent는 HTML을 파싱하지 않으므로 XSS에 안전합니다
document.getElementById('search-result').textContent =
    '검색어: ' + keyword;
</script>
```

> **💡 팁:** JavaScript에서 DOM을 조작할 때 `innerHTML` 대신 `textContent`를 사용하면 HTML 태그가 파싱되지 않아 XSS를 방지할 수 있습니다. HTML 구조를 동적으로 생성해야 하는 경우에는 `createElement()`와 `textContent`를 조합하십시오.

### 바이브 코딩 시 체크포인트

- [ ] **Jinja2 환경에서 `autoescape=False`를 설정하고 있지 않은가?** 이 설정은 XSS 보호를 해제합니다
- [ ] **템플릿에서 `| safe` 필터나 `{% autoescape false %}`를 사용하고 있지 않은가?**
- [ ] **`HTMLResponse`로 사용자 입력을 직접 포함한 HTML을 반환하고 있지 않은가?** 반드시 `Jinja2Templates`를 사용하십시오
- [ ] **JavaScript에서 `innerHTML`을 사용하고 있지 않은가?** `textContent`나 `createElement()`를 사용하십시오
- [ ] **사용자 입력이 HTML 속성에 들어가는 경우 따옴표로 감싸져 있는가?**
- [ ] **리치 텍스트 에디터(Rich Text Editor)를 사용하는 경우 서버 측 HTML 정화(Sanitization) 라이브러리를 적용했는가?** `bleach` 라이브러리 등을 사용하십시오

---

## 4-2. 크로스사이트 요청 위조(CSRF)

### 개요

크로스사이트 요청 위조(Cross-Site Request Forgery, CSRF)는 사용자가 인지하지 못한 상황에서, 공격자가 의도한 행위(데이터 수정, 삭제, 등록 등)를 사용자 명의로 수행하게 만드는 공격입니다.

사용자가 웹사이트에 로그인한 상태에서 공격자가 만든 악성 페이지를 방문하면, 해당 페이지에서 사용자의 인증 정보(쿠키)를 이용하여 원래 사이트에 요청을 보냅니다. 서버는 이 요청이 사용자 본인의 의도인지 구분할 수 없습니다.

### CSRF 공격 시퀀스

#### 공격 흐름 전체도

```
  ┌─────────────┐                              ┌─────────────────┐
  │  정상 웹사이트 │                              │   공격자 서버    │
  │ (은행, 쇼핑몰) │                              │ (evil.com)     │
  └──────┬──────┘                              └────────┬────────┘
         │                                              │
         │  ① 정상 로그인                                │
         │◀══════════════════╗                          │
         │  세션 쿠키 발급     ║                          │
         │══════════════════▶║                          │
         │                   ║                          │
         │            ┌──────╨──────┐                   │
         │            │   피해자     │                   │
         │            │  (사용자)    │                   │
         │            └──────┬──────┘                   │
         │                   │                          │
         │                   │  ② 공격자 페이지 방문       │
         │                   │  (메일 링크, 게시글 등)     │
         │                   │════════════════════════▶ │
         │                   │                          │
         │                   │  ③ 숨겨진 요청 자동 전송    │
         │◀══════════════════╪══════════════════════════│
         │  공격자가 심어둔    │  <img src="bank.com/     │
         │  위조 요청 수신     │   transfer?to=공격자      │
         │  + 피해자 쿠키 포함 │   &amount=1000000">     │
         │                   │                          │
         │  ④ 정상 요청으로    │                          │
         │  판단하여 처리      │                          │
         │══════════════════▶│                          │
         │  송금 완료!        │                          │
         │                   │                          │
```

#### ✅ 방어: CSRF 토큰 적용 시

```
  ┌─────────────┐         ┌─────────────────┐         ┌─────────────────┐
  │  공격자 서버  │         │    웹 서버       │         │    결과          │
  │             │         │                 │         │                 │
  │ 위조 요청    │         │ CSRF 토큰 검증   │         │ ✅ 요청 거부     │
  │ (토큰 없음)  │ ══════▶ │ 토큰 불일치!     │ ──────▶ │   공격 차단됨    │
  │             │         │                 │         │                 │
  └─────────────┘         └─────────────────┘         └─────────────────┘

  공격자는 CSRF 토큰 값을 알 수 없음 ──▶ 유효한 요청 위조 불가능
```

### 왜 위험한가

CSRF 공격의 대표적인 시나리오를 살펴보겠습니다:

1. 여러분이 만든 쇼핑몰에 사용자가 로그인합니다
2. 사용자가 다른 탭에서 공격자의 웹페이지를 방문합니다
3. 공격자의 페이지에는 다음과 같은 숨겨진 폼이 있습니다:

```html
<!-- 공격자의 페이지에 숨겨진 폼 -->
<form action="https://your-shop.com/transfer" method="POST" id="evil-form">
    <input type="hidden" name="to" value="attacker_account" />
    <input type="hidden" name="amount" value="1000000" />
</form>
<script>document.getElementById('evil-form').submit();</script>
```

4. 사용자의 브라우저가 자동으로 로그인 쿠키를 포함하여 요청을 보냅니다
5. 서버는 정상 요청으로 판단하여 송금을 처리합니다

### 취약한 코드

#### ❌ 취약한 코드: CSRF 보호 미적용

```python
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# CSRF 보호 미들웨어가 전혀 적용되지 않은 상태입니다
@app.post("/pay-to-point")
async def pay_to_point(
    request: Request,
    user_id: str = Form(...),
    pay: str = Form(...),
    product_info: str = Form(...),
):
    ret = handle_pay(user_id, pay, product_info)
    return templates.TemplateResponse(
        "view_wallet.html", {"request": request, "wallet": ret}
    )
```

#### ❌ 취약한 코드: 템플릿에서 CSRF 토큰 누락

```html
<!--html page-->
<form action="/pay-to-point" method="POST">
    <!-- form 태그 내부에 CSRF 토큰이 없습니다 -->
    <input type="text" name="user_id" />
    <input type="text" name="pay" />
    <input type="hidden" name="product_info" value="item_001" />
    <input type="submit"/>
</form>
```

> **⚠️ 주의:** AI 도구가 "403 Forbidden 에러가 나요"라는 질문에 대해 CSRF 미들웨어를 제거하라고 답변하는 경우가 있습니다. 이는 문제를 해결하는 것이 아니라 보안 기능을 무력화하는 것입니다.

### 안전한 코드

#### ✅ 안전한 코드: Starlette CSRF 미들웨어 적용

```python
from fastapi import FastAPI, Form, Request, Depends
from fastapi.templating import Jinja2Templates
from starlette_csrf import CSRFMiddleware

app = FastAPI()

# CSRF 보호 미들웨어를 적용합니다
app.add_middleware(
    CSRFMiddleware,
    secret="여러분의-비밀키-환경변수에서-불러오세요",
    required_urls=["/pay-to-point", "/transfer", "/checkout"],
    exempt_urls=["/api/webhook"],  # 웹훅 등 예외 URL
)

templates = Jinja2Templates(directory="templates")

@app.post("/pay-to-point")
async def pay_to_point(
    request: Request,
    user_id: str = Form(...),
    pay: str = Form(...),
    product_info: str = Form(...),
):
    ret = handle_pay(user_id, pay, product_info)
    return templates.TemplateResponse(
        "view_wallet.html", {"request": request, "wallet": ret}
    )
```

#### ✅ 안전한 코드: 커스텀 CSRF 토큰 구현

```python
import secrets
from fastapi import FastAPI, Form, Request, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="여러분의-비밀키")
templates = Jinja2Templates(directory="templates")

def generate_csrf_token(request: Request) -> str:
    """CSRF 토큰을 생성하고 세션에 저장합니다."""
    if "csrf_token" not in request.session:
        request.session["csrf_token"] = secrets.token_hex(32)
    return request.session["csrf_token"]

def verify_csrf_token(request: Request, csrf_token: str = Form(...)):
    """폼에서 전달된 CSRF 토큰이 세션의 토큰과 일치하는지 검증합니다."""
    session_token = request.session.get("csrf_token")
    if not session_token or not secrets.compare_digest(session_token, csrf_token):
        raise HTTPException(status_code=403, detail="CSRF 토큰이 유효하지 않습니다.")

@app.get("/pay-form")
async def pay_form(request: Request):
    token = generate_csrf_token(request)
    return templates.TemplateResponse(
        "pay_form.html", {"request": request, "csrf_token": token}
    )

@app.post("/pay-to-point")
async def pay_to_point(
    request: Request,
    user_id: str = Form(...),
    pay: str = Form(...),
    product_info: str = Form(...),
    _: None = Depends(verify_csrf_token),
):
    ret = handle_pay(user_id, pay, product_info)
    return templates.TemplateResponse(
        "view_wallet.html", {"request": request, "wallet": ret}
    )
```

#### ✅ 안전한 코드: 템플릿에 CSRF 토큰 포함

```html
<!-- templates/pay_form.html -->
<form action="/pay-to-point" method="POST">
    <!-- CSRF 토큰을 hidden input으로 포함합니다 -->
    <input type="hidden" name="csrf_token" value="{{ csrf_token }}" />
    <input type="text" name="user_id" />
    <input type="text" name="pay" />
    <input type="hidden" name="product_info" value="item_001" />
    <input type="submit"/>
</form>
```

> **💡 팁:** FastAPI에서 POST 요청 시 "403 Forbidden" 에러가 발생하면, CSRF를 비활성화하는 대신 폼에 CSRF 토큰 hidden input을 추가하십시오. 이것이 올바른 해결 방법입니다. AJAX 요청의 경우 `X-CSRF-Token` 헤더에 토큰을 포함하십시오.

### 바이브 코딩 시 체크포인트

- [ ] **CSRF 보호 미들웨어(`CSRFMiddleware` 또는 커스텀 구현)가 적용되어 있는가?**
- [ ] **모든 POST 폼에 CSRF 토큰이 hidden input으로 포함되어 있는가?**
- [ ] **특정 엔드포인트에 대해 CSRF 보호를 불필요하게 예외 처리하고 있지 않은가?**
- [ ] **AJAX 요청 시 CSRF 토큰을 헤더에 포함하고 있는가?**
- [ ] **세션 미들웨어(`SessionMiddleware`)가 설정되어 있는가?**

---

## 4-3. 서버사이드 요청 위조(SSRF)

### 개요

서버사이드 요청 위조(Server-Side Request Forgery, SSRF)는 공격자가 서버 측에서 다른 서버로 보내는 요청을 조작하여, 내부 네트워크의 자원에 접근하는 공격입니다.

바이브 코딩으로 외부 API를 호출하는 기능, URL 프리뷰(Preview) 기능, 웹훅(Webhook) 처리 등을 구현할 때 이 취약점에 노출될 수 있습니다.

### SSRF 공격 흐름도

#### ❌ 취약한 흐름 (URL 검증 없음)

```
                         ┌─────────────────────────────────────────────────┐
                         │              내부 네트워크 (방화벽 내부)           │
                         │                                                 │
 ┌─────────────┐         │  ┌─────────────────┐         ┌───────────────┐  │
 │   공격자     │         │  │   웹 애플리케이션  │         │  내부 서버     │  │
 │  (외부)      │         │  │                 │         │ (DB, 관리자 등) │  │
 │             │         │  │  URL 파라미터:   │         │               │  │
 │ url=http:// │         │  │  검증 없이       │         │ ⚠ 내부 정보   │  │
 │ 192.168.1.1 │ ══════▶ │  │  서버가 직접 요청 │ ══════▶ │   유출됨!     │  │
 │ /admin      │         │  │                 │         │               │  │
 └─────────────┘         │  └─────────────────┘         └───────────────┘  │
                         │         │                                       │
       ①                 │         │ ══════▶  ┌───────────────────────┐    │
   공격자가 내부 주소를     │         │          │ 클라우드 메타데이터     │    │
   URL 파라미터로 전달     │         │          │ 169.254.169.254      │    │
                         │         │          │                       │    │
                         │         │          │ ⚠ AWS 자격증명,       │    │
                         │         │          │   IAM 역할 정보 유출!  │    │
                         │         │          └───────────────────────┘    │
                         │                                                 │
                         └─────────────────────────────────────────────────┘
```

#### ✅ 안전한 흐름 (URL 화이트리스트 적용)

```
                         ┌─────────────────────────────────────────────────┐
                         │              내부 네트워크 (방화벽 내부)           │
                         │                                                 │
 ┌─────────────┐         │  ┌─────────────────┐         ┌───────────────┐  │
 │   공격자     │         │  │   웹 애플리케이션  │         │  내부 서버     │  │
 │  (외부)      │         │  │                 │         │               │  │
 │             │         │  │ ┌─────────────┐ │         │ ✅ 접근 차단   │  │
 │ url=http:// │         │  │ │ URL 검증     │ │         │               │
 │ 192.168.1.1 │ ──────▶ │  │ │             │ │ ─ ─ ─▶ │ (요청 도달     │  │
 │ /admin      │         │  │ │ ❌ 차단!     │ │         │  하지 않음)    │  │
 │             │         │  │ └─────────────┘ │         │               │  │
 └─────────────┘         │  └─────────────────┘         └───────────────┘  │
                         │                                                 │
                         └─────────────────────────────────────────────────┘
```

### 왜 위험한가

SSRF는 공격자가 **서버의 신뢰된 네트워크 위치**를 악용하는 공격입니다:

- **내부 시스템 접근**: `http://192.168.0.45/admin`과 같이 외부에서 접근할 수 없는 관리자 페이지에 접근
- **클라우드 메타데이터 탈취**: `http://169.254.169.254/latest/meta-data/`로 AWS 인스턴스의 인증 키를 획득
- **내부 파일 열람**: `file:///etc/passwd`로 서버의 파일 시스템에 접근
- **포트 스캐닝**: 내부 네트워크의 서비스 구성을 파악

### 취약한 코드

#### ❌ 취약한 코드: 사용자 입력 URL로 HTTP 요청

```python
import httpx
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/call-third-party-api")
async def call_third_party_api(request: Request, address: str = Form(...)):
    # 사용자가 입력한 주소를 검증하지 않고 HTTP 요청을 보냅니다
    async with httpx.AsyncClient() as client:
        response = await client.get(address)

    return templates.TemplateResponse(
        "result.html", {"request": request, "result": response.text}
    )
```

### 안전한 코드

#### ✅ 안전한 코드: 허용 URL 화이트리스트 적용

```python
import httpx
from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 허용하는 서버 목록을 화이트리스트로 관리합니다
# DNS rebinding 공격 방지를 위해 도메인보다 IP 사용을 권장합니다
ALLOW_SERVER_LIST = [
    'https://127.0.0.1/latest/',
    'https://192.168.0.1/user_data',
    'https://192.168.0.100/v1/public',
]

@app.post("/call-third-party-api")
async def call_third_party_api(request: Request, address: str = Form(...)):
    # 화이트리스트에 포함된 URL만 허용합니다
    if address not in ALLOW_SERVER_LIST:
        raise HTTPException(status_code=400, detail="허용되지 않은 서버입니다.")

    async with httpx.AsyncClient() as client:
        response = await client.get(address, timeout=5.0)

    return templates.TemplateResponse(
        "result.html", {"request": request, "result": response.text}
    )
```

#### ✅ 안전한 코드: URL 파싱 후 검증

```python
import socket
import ipaddress
from urllib.parse import urlparse
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl

app = FastAPI()

BLOCKED_NETWORKS = [
    ipaddress.ip_network('10.0.0.0/8'),
    ipaddress.ip_network('172.16.0.0/12'),
    ipaddress.ip_network('192.168.0.0/16'),
    ipaddress.ip_network('169.254.0.0/16'),  # 클라우드 메타데이터
    ipaddress.ip_network('127.0.0.0/8'),     # 루프백
]

class URLRequest(BaseModel):
    # Pydantic의 HttpUrl 타입으로 URL 형식을 사전 검증합니다
    url: HttpUrl

async def safe_request(url: str) -> str:
    parsed = urlparse(url)

    # file:// 등의 위험한 프로토콜 차단
    if parsed.scheme not in ('http', 'https'):
        raise HTTPException(status_code=400, detail="허용되지 않은 프로토콜입니다.")

    # 내부 네트워크 IP 차단
    ip = socket.gethostbyname(parsed.hostname)
    for network in BLOCKED_NETWORKS:
        if ipaddress.ip_address(ip) in network:
            raise HTTPException(
                status_code=400, detail="내부 네트워크 접근은 허용되지 않습니다."
            )

    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=5.0)
    return response.text

@app.post("/call-api")
async def call_api(body: URLRequest):
    result = await safe_request(str(body.url))
    return {"result": result}
```

> **💡 팁:** 클라우드 환경(AWS, GCP, Azure)에서는 메타데이터 서비스(169.254.169.254)에 대한 접근을 반드시 차단하십시오. 메타데이터를 통해 인스턴스의 IAM 역할 자격 증명이 탈취될 수 있습니다. FastAPI에서는 Pydantic의 `HttpUrl` 타입을 활용하면 URL 형식 검증을 자동화할 수 있습니다.

### 바이브 코딩 시 체크포인트

- [ ] **사용자 입력 URL로 서버에서 HTTP 요청을 보내는 코드가 있는가?**
- [ ] **URL 화이트리스트 또는 내부 네트워크 차단이 적용되어 있는가?**
- [ ] **`file://`, `gopher://` 등 위험한 프로토콜이 차단되어 있는가?**
- [ ] **클라우드 메타데이터 IP(169.254.169.254)에 대한 접근이 차단되어 있는가?**
- [ ] **Pydantic의 `HttpUrl` 타입으로 URL 형식이 사전 검증되고 있는가?**

---

## 4-4. HTTP 응답 분할(HTTP Response Splitting)

### 개요

HTTP 응답 분할(HTTP Response Splitting)은 HTTP 응답 헤더에 사용자 입력값이 포함될 때, 해당 입력에 개행문자(CR: `\r`, LF: `\n`)가 존재하면 HTTP 응답이 두 개 이상으로 분리되는 취약점입니다. 공격자는 이를 이용하여 두 번째 응답에 악성 코드를 주입할 수 있습니다.

### 왜 위험한가

응답 헤더가 분할되면 공격자가 완전히 새로운 HTTP 응답을 만들어낼 수 있습니다. 이를 통해 XSS 공격이나 캐시 훼손(Cache Poisoning) 공격이 가능합니다.

### 취약한 코드

#### ❌ 취약한 코드: 외부 입력을 응답 헤더에 직접 사용

```python
from fastapi import FastAPI, Form
from fastapi.responses import Response

app = FastAPI()

@app.post("/route")
async def route(content_type: str = Form(...)):
    # 외부 입력값을 검증 없이 응답 헤더에 포함합니다
    return Response(
        content="OK",
        headers={"Content-Type": content_type}
    )
```

### 안전한 코드

#### ✅ 안전한 코드: 개행문자 제거

```python
from fastapi import FastAPI, Form
from fastapi.responses import Response

app = FastAPI()

@app.post("/route")
async def route(content_type: str = Form(...)):
    # 응답 헤더에 포함될 수 있는 개행문자를 제거합니다
    content_type = content_type.replace('\r', '').replace('\n', '')

    return Response(
        content="OK",
        headers={"Content-Type": content_type}
    )
```

#### ✅ 더 안전한 코드: Pydantic으로 헤더 값 검증

```python
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator

app = FastAPI()

class HeaderRequest(BaseModel):
    content_type: str

    @field_validator("content_type")
    @classmethod
    def validate_content_type(cls, v: str) -> str:
        # 개행문자가 포함되어 있으면 거부합니다
        if re.search(r'[\r\n]', v):
            raise ValueError("헤더 값에 개행문자를 포함할 수 없습니다.")
        # 허용된 Content-Type 패턴만 승인합니다
        allowed_types = ['text/html', 'text/plain', 'application/json', 'application/xml']
        if v not in allowed_types:
            raise ValueError("허용되지 않은 Content-Type입니다.")
        return v

@app.post("/route")
async def route(body: HeaderRequest):
    from fastapi.responses import Response
    return Response(
        content="OK",
        headers={"Content-Type": body.content_type}
    )
```

> **💡 팁:** 최신 버전의 FastAPI와 Starlette는 응답 헤더에서 개행문자를 자동으로 처리하는 보호 기능이 내장되어 있습니다. 하지만 프레임워크의 보호에만 의존하지 말고, 응답 헤더에 사용되는 외부 입력값은 항상 검증하는 습관을 가지십시오. 프레임워크와 라이브러리를 항상 최신 버전으로 유지하는 것도 중요합니다.

### 바이브 코딩 시 체크포인트

- [ ] **사용자 입력값이 HTTP 응답 헤더(Set-Cookie, Content-Type, Location 등)에 포함되고 있지 않은가?**
- [ ] **불가피하게 포함되는 경우 `\r`, `\n` 개행문자가 제거되고 있는가?**
- [ ] **Pydantic 모델로 헤더에 사용될 값을 사전 검증하고 있는가?**
- [ ] **FastAPI, Starlette 등 프레임워크가 최신 버전인가?**

---

# Chapter 05. 파일과 URL을 노리는 공격

## 5-1. 경로 조작 및 자원 삽입(Path Traversal & Resource Injection)

### 개요

경로 조작(Path Traversal)은 검증되지 않은 외부 입력값을 사용하여 파일 시스템의 경로를 조작함으로써, 공격자가 허가되지 않은 파일이나 디렉터리(Directory)에 접근할 수 있는 보안약점입니다. 자원 삽입(Resource Injection)은 이 원리를 파일뿐 아니라 소켓 포트, 네트워크 자원 등에까지 확장한 개념입니다.

바이브 코딩(Vibe Coding)으로 파일 업로드/다운로드 기능, 이미지 뷰어, 문서 관리 시스템 등을 만들 때 이 취약점이 자주 발생합니다. AI 도구가 생성하는 파일 처리 코드에서 경로 검증이 누락되는 경우가 많으므로 반드시 확인해야 합니다.

### 왜 위험한가

공격자가 파일명에 `../`(상위 디렉터리 이동) 문자열을 삽입하면, 서버의 의도된 디렉터리를 벗어나 시스템의 모든 파일에 접근할 수 있습니다:

```
# 정상적인 요청
GET /download?file=report.txt
# 서버에서 열리는 파일: /var/www/uploads/report.txt

# 공격자의 요청
GET /download?file=../../../../etc/passwd
# 서버에서 열리는 파일: /etc/passwd (운영체제 사용자 정보!)
```

### 취약한 코드

#### ❌ 취약한 코드: 외부 입력값을 파일 경로에 직접 사용

```python
import os
import aiofiles
from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/get-info")
async def get_info(request: Request, request_file: str = Form(...)):
    # 외부 입력값으로부터 파일명을 입력 받습니다
    filename, file_ext = os.path.splitext(request_file)
    file_ext = file_ext.lower()

    if file_ext not in ['.txt', '.csv']:
        raise HTTPException(status_code=400, detail="파일을 열 수 없습니다.")

    # 확장자만 검증하고 경로 조작 문자열은 검증하지 않습니다
    # ../../../../etc/passwd.txt 같은 입력이 가능합니다
    async with aiofiles.open(request_file, mode='r') as f:
        data = await f.read()

    return templates.TemplateResponse(
        "success.html", {"request": request, "data": data}
    )
```

### 안전한 코드

#### ✅ 더 안전한 코드: 기본 디렉터리(Base Directory) 제한 + Pydantic 검증

```python
import os
import aiofiles
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, field_validator

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 파일 접근이 허용된 기본 디렉터리를 지정합니다
BASE_DIR = '/var/www/uploads'

class FileRequest(BaseModel):
    request_file: str = Field(..., max_length=255)

    @field_validator("request_file")
    @classmethod
    def validate_filename(cls, v: str) -> str:
        # 경로 구분자 및 상위 디렉터리 이동 문자를 차단합니다
        if '..' in v or '/' in v or '\\' in v:
            raise ValueError("파일명에 경로 조작 문자를 포함할 수 없습니다.")
        return v

@app.post("/get-info")
async def get_info(request: Request, body: FileRequest):
    filename, file_ext = os.path.splitext(body.request_file)
    file_ext = file_ext.lower()

    if file_ext not in ['.txt', '.csv']:
        raise HTTPException(status_code=400, detail="파일을 열 수 없습니다.")

    # 절대 경로를 생성하고, 기본 디렉터리 내에 있는지 확인합니다
    safe_path = os.path.realpath(os.path.join(BASE_DIR, body.request_file))

    if not safe_path.startswith(os.path.realpath(BASE_DIR)):
        raise HTTPException(status_code=403, detail="접근이 허용되지 않은 경로입니다.")

    try:
        async with aiofiles.open(safe_path, mode='r') as f:
            data = await f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")

    return templates.TemplateResponse(
        "success.html", {"request": request, "data": data}
    )
```

> **💡 팁:** `os.path.realpath()`는 심볼릭 링크(Symbolic Link)와 `../` 등의 경로 조작을 모두 해석하여 실제 절대 경로를 반환합니다. 이 결과가 허용된 기본 디렉터리로 시작하는지 확인하면 경로 조작 공격을 효과적으로 방어할 수 있습니다.

### 바이브 코딩 시 체크포인트

- [ ] **파일 경로에 사용자 입력이 포함되는 경우 `../`, `/`, `\` 등의 경로 조작 문자가 필터링되고 있는가?**
- [ ] **`os.path.realpath()`로 실제 경로를 해석한 후 기본 디렉터리 범위 내인지 확인하고 있는가?**
- [ ] **Pydantic `field_validator`로 파일명을 사전 검증하고 있는가?**
- [ ] **파일 다운로드 기능에서 사용자가 임의의 시스템 파일에 접근할 수 없도록 제한되어 있는가?**
- [ ] **외부 입력값이 포트 번호, 소켓 주소 등 시스템 자원 식별자로 사용되는 경우 화이트리스트로 제한하고 있는가?**

---

## 5-2. 위험한 형식 파일 업로드(Unrestricted File Upload)

### 개요

파일 업로드 기능에서 서버 측 실행 가능한 스크립트 파일(`.py`, `.php`, `.jsp`, `.sh` 등)의 업로드를 허용하면, 공격자가 웹 쉘(Web Shell)을 업로드하여 서버를 완전히 장악할 수 있습니다.

### 취약한 코드

#### ❌ 취약한 코드: 파일 검증 없이 업로드 허용

```python
import aiofiles
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "media/screenshot"

@app.post("/file-upload")
async def file_upload(request: Request, upload_file: UploadFile = File(...)):
    # 파일의 크기, 개수, 확장자, 내용을 전혀 검증하지 않습니다
    file_path = f"{UPLOAD_DIR}/{upload_file.filename}"
    async with aiofiles.open(file_path, "wb") as f:
        content = await upload_file.read()
        await f.write(content)

    return templates.TemplateResponse(
        "success.html", {"request": request, "filename": upload_file.filename}
    )
```

### 안전한 코드

#### ✅ 안전한 코드: 다중 검증 적용

```python
import os
import uuid
import aiofiles
from fastapi import FastAPI, UploadFile, File, Request, HTTPException
from fastapi.templating import Jinja2Templates
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "media/screenshot"
FILE_COUNT_LIMIT = 5
FILE_SIZE_LIMIT = 5 * 1024 * 1024  # 5MB
WHITE_LIST_EXT = ['.jpg', '.jpeg', '.png', '.gif']
WHITE_LIST_MIME = ['image/jpeg', 'image/png', 'image/gif']

@app.post("/file-upload")
async def file_upload(
    request: Request,
    upload_files: List[UploadFile] = File(...),
):
    if len(upload_files) == 0 or len(upload_files) > FILE_COUNT_LIMIT:
        raise HTTPException(status_code=400, detail="파일 개수 초과")

    filename_list = []
    for upload_file in upload_files:
        if upload_file.content_type not in WHITE_LIST_MIME:
            raise HTTPException(status_code=400, detail="허용되지 않은 파일 형식입니다.")

        content = await upload_file.read()
        if len(content) > FILE_SIZE_LIMIT:
            raise HTTPException(status_code=400, detail="파일 크기가 초과되었습니다.")

        _, file_ext = os.path.splitext(upload_file.filename)
        if file_ext.lower() not in WHITE_LIST_EXT:
            raise HTTPException(status_code=400, detail="허용되지 않은 확장자입니다.")

        safe_filename = str(uuid.uuid4()) + file_ext.lower()
        file_path = os.path.join(UPLOAD_DIR, safe_filename)

        async with aiofiles.open(file_path, "wb") as f:
            await f.write(content)

        filename_list.append(safe_filename)

    return templates.TemplateResponse(
        "success.html", {"request": request, "filename_list": filename_list}
    )
```

### 바이브 코딩 시 체크포인트

- [ ] **파일 확장자를 화이트리스트 방식으로 검증하고 있는가?**
- [ ] **Content-Type(MIME 타입)을 검사하고 있는가?**
- [ ] **파일 크기와 업로드 개수에 제한이 있는가?**
- [ ] **업로드된 파일명을 UUID 등으로 변경하여 저장하고 있는가?**
- [ ] **업로드 디렉터리가 웹 루트 외부에 위치하는가?**

---

## 5-3. 신뢰되지 않는 URL 자동 연결(Open Redirect)

### 개요

오픈 리다이렉트(Open Redirect)는 사용자 입력값을 외부 사이트 주소로 사용하여 리다이렉트(Redirect)하는 경우, 공격자가 이를 악용하여 피해자를 피싱(Phishing) 사이트로 유도할 수 있는 취약점입니다.

### 안전한 코드

#### ✅ 더 안전한 코드: Pydantic 검증 + 상대 URL 제한

```python
from urllib.parse import urlparse
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, field_validator

app = FastAPI()

class RedirectRequest(BaseModel):
    url: str

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        parsed = urlparse(v)
        if parsed.scheme or parsed.netloc:
            raise ValueError("외부 URL로는 이동할 수 없습니다.")
        if not v.startswith('/'):
            raise ValueError("올바른 경로 형식이 아닙니다.")
        return v

@app.post("/redirect-url")
async def redirect_url(body: RedirectRequest):
    return RedirectResponse(url=body.url, status_code=303)
```

> **💡 팁:** 로그인 후 리다이렉트 기능을 구현할 때, 가능한 한 상대 경로(Relative URL)만 허용하십시오. `/dashboard`, `/profile`과 같은 내부 경로만 허용하면 외부 사이트로의 리다이렉트를 원천적으로 차단할 수 있습니다.

### 바이브 코딩 시 체크포인트

- [ ] **`RedirectResponse`에 사용자 입력값이 직접 전달되고 있지 않은가?**
- [ ] **리다이렉트 대상 URL을 화이트리스트로 관리하거나, 상대 URL만 허용하고 있는가?**
- [ ] **Pydantic `field_validator`로 URL을 사전 검증하고 있는가?**

---

## 5-4. 부적절한 XML 외부 개체 참조(XXE)

### 개요

XML 외부 엔티티(XML External Entity, XXE) 공격은 XML 문서에 포함된 DTD(Document Type Definition)의 외부 엔티티 참조 기능을 악용하여, 서버의 파일을 읽거나 내부 네트워크에 접근하는 공격입니다.

### 안전한 코드

#### ✅ FastAPI에서의 권장 패턴: XML 대신 JSON 사용

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class DataRequest(BaseModel):
    name: str
    value: int

@app.post("/data")
async def receive_data(body: DataRequest):
    return {"name": body.name, "value": body.value}
```

> **💡 팁:** FastAPI의 강점인 Pydantic + JSON 조합을 활용하면 XML 관련 보안 위험을 원천적으로 차단할 수 있습니다.

### 바이브 코딩 시 체크포인트

- [ ] **XML 파서의 외부 엔티티 처리 옵션이 비활성화되어 있는가?**
- [ ] **`lxml` 사용 시 `resolve_entities=False`, `no_network=True`가 설정되어 있는가?**
- [ ] **XML 대신 JSON을 사용할 수 있는지 검토했는가?**

---

# Chapter 06. 데이터 타입과 보안 결정을 노리는 공격

## 6-1. 정수형 오버플로우(Integer Overflow)

### 개요

정수형 오버플로우(Integer Overflow)는 변수가 저장할 수 있는 범위를 넘어선 값이 할당될 때, 실제 저장되는 값이 의도치 않게 아주 작은 수나 음수가 되어 프로그램이 예기치 않게 동작하는 취약점입니다.

파이썬(Python)은 다른 언어와 달리 기본 정수형에 대해 **임의 정밀도 연산(Arbitrary-Precision Arithmetic)**을 지원하므로, 순수 파이썬 코드에서는 정수형 오버플로우가 발생하지 않습니다. 하지만 `numpy`, `pandas` 등 C 기반 라이브러리를 사용할 때는 고정 크기 정수형이 사용되므로 오버플로우가 발생할 수 있습니다.

### 안전한 코드

#### ✅ 안전한 코드: Pydantic 모델로 입력값 범위 제한

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

app = FastAPI()
templates = Jinja2Templates(directory="templates")

MAX_QUANTITY = 10000
MAX_PRICE = 100_000_000  # 1억

class PriceRequest(BaseModel):
    quantity: int = Field(..., ge=0, le=MAX_QUANTITY)
    unit_price: int = Field(..., ge=0, le=MAX_PRICE)

@app.post("/calculate-price")
async def calculate_price(request: Request, body: PriceRequest):
    total = body.quantity * body.unit_price
    return templates.TemplateResponse(
        "price.html", {"request": request, "total": total}
    )
```

> **💡 팁:** FastAPI에서는 Pydantic의 `Field(ge=0, le=10000)`처럼 선언적으로 범위를 지정하면 자동 검증이 수행되어 매우 편리합니다.

### 바이브 코딩 시 체크포인트

- [ ] **`numpy`, `pandas` 등 C 기반 라이브러리에서 정수 연산을 수행할 때 입력값의 범위를 검증하고 있는가?**
- [ ] **금액, 수량 등 비즈니스 로직의 계산에 파이썬 기본 자료형을 사용하고 있는가?**
- [ ] **외부 입력값이 수치 연산에 사용될 때 Pydantic `Field`의 `ge`, `le`, `gt`, `lt` 옵션으로 최소/최대 범위가 설정되어 있는가?**

---

## 6-2. 보안기능 결정에 사용되는 부적절한 입력값

### 개요

보안기능 결정에 사용되는 부적절한 입력값(Reliance on Untrusted Inputs in a Security Decision)은 쿠키(Cookie), 히든 필드(Hidden Field), 환경변수 등 클라이언트 측에서 조작 가능한 값을 기반으로 인증이나 인가 같은 보안 결정을 내리는 취약점입니다.

여러분이 반드시 인지해야 할 중요한 원칙은 **클라이언트에서 오는 모든 데이터는 조작될 수 있다**는 것입니다.

### 안전한 코드

#### ✅ 안전한 코드: 서버에서 가격 조회 후 결제

```python
from fastapi import FastAPI, Form, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/checkout")
async def checkout(
    request: Request,
    product_id: str = Form(...),
    db: AsyncSession = Depends(get_async_session),
):
    # 가격을 클라이언트에서 받지 않고, 서버 데이터베이스에서 조회합니다
    stmt = select(Product).where(Product.id == product_id)
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")

    # 서버에 저장된 실제 가격으로 결제를 처리합니다
    process_payment(product.id, product.price)
    return templates.TemplateResponse(
        "checkout_success.html", {"request": request}
    )
```

### 바이브 코딩 시 체크포인트

- [ ] **쿠키, 히든 필드, URL 파라미터 값을 보안 결정(인증, 인가, 결제)에 사용하고 있지 않은가?**
- [ ] **사용자 권한 확인은 서버 측 JWT 토큰 검증 또는 데이터베이스 조회를 기반으로 수행하고 있는가?**
- [ ] **가격, 할인율 등 금전적 가치가 있는 데이터를 서버에서 조회하고 있는가?**
- [ ] **FastAPI의 `Depends()`를 활용하여 인증/인가 의존성을 체계적으로 관리하고 있는가?**

> **⚠️ 주의:** "클라이언트에서 보내는 데이터는 모두 거짓말일 수 있다"라는 원칙을 항상 기억하십시오.

---

# PART 3. 보안 기능을 제대로 구현하세요

# Chapter 07. 인증과 인가, 그리고 권한 설정

### 인증 vs 인가 비교도

```
┌─────────────────────────────────────────────────────────────────────┐
│                    인증(Authentication) vs 인가(Authorization)                    │
├─────────────────────────────────┬───────────────────────────────────┤
│         ① 인증 (Authentication)         │         ② 인가 (Authorization)          │
├─────────────────────────────────┼───────────────────────────────────┤
│                                 │                                   │
│  핵심 질문:                     │  핵심 질문:                       │
│  "당신은 누구입니까?"           │  "무엇을 할 수 있습니까?"        │
│                                 │                                   │
│  ┌───────────────────────┐      │  ┌─────────────────────────┐      │
│  │  검증 수단            │      │  │  검증 수단              │      │
│  │  ・로그인 (ID/PW)     │      │  │  ・권한 (Permission)    │      │
│  │  ・비밀번호           │      │  │  ・역할 (Role)          │      │
│  │  ・생체인식 (지문 등) │      │  │  ・접근제어 (ACL)       │      │
│  └───────────┬───────────┘      │  └───────────┬─────────────┘      │
│              │                  │              │                    │
│              ▼                  │              ▼                    │
│  ┌───────────────────────┐      │  ┌─────────────────────────┐      │
│  │    결과: 신원 확인    │      │  │    결과: 행위 허가      │      │
│  └───────────────────────┘      │  └─────────────────────────┘      │
│                                 │                                   │
├─────────────────────────────────┴───────────────────────────────────┤
│                                                                     │
│              전체 흐름: 인증 → 인가 → 자원 접근                     │
│                                                                     │
│  ┌────────┐      ┌────────────┐      ┌────────────┐      ┌───────┐ │
│  │ 사용자 │──▶│   ① 인증   │══▶│   ② 인가   │──▶│ 자원  │ │
│  │        │      │ (신원확인) │      │ (권한확인) │      │ 접근  │ │
│  └────────┘      └──────┬─────┘      └──────┬─────┘      └───────┘ │
│                         │                   │                       │
│                    실패 시               실패 시                    │
│                         │                   │                       │
│                         ▼                   ▼                       │
│                  ┌────────────┐      ┌────────────┐                 │
│                  │ 401        │      │ 403        │                 │
│                  │ Unauthorized│      │ Forbidden  │                 │
│                  │ (인증 실패)│      │ (인가 실패)│                 │
│                  └────────────┘      └────────────┘                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## 7-1. 적절한 인증 없이 중요 기능 허용

### 개요

인증(Authentication)이란 "당신이 누구인지 확인하는 과정"입니다. AI 도구로 API를 빠르게 만들다 보면, 중요한 기능에 인증 절차를 빠뜨리는 경우가 빈번하게 발생합니다.

### 안전 코드

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
    current_password: SecretStr
    new_password: SecretStr
    confirm_password: SecretStr

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
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
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not pwd_context.verify(
        data.current_password.get_secret_value(),
        current_user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="현재 패스워드가 일치하지 않습니다.",
        )

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

### 바이브 코딩 시 체크포인트

- [ ] AI가 생성한 모든 엔드포인트에 `Depends(get_current_user)` 또는 인증 의존성이 적용되어 있는지 확인합니다.
- [ ] 패스워드 변경, 결제, 개인정보 수정 등 중요 기능에는 **재인증(Re-authentication)** 로직이 포함되어 있는지 확인합니다.

---

## 7-2. 부적절한 인가

### 개요

인가(Authorization)란 "인증된 사용자가 특정 자원이나 기능에 접근할 권한이 있는지 확인하는 과정"입니다.

### 안전 코드

```python
# ✅ 안전한 코드: 역할 기반 권한 확인 후 삭제
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

app = FastAPI()

def require_role(*allowed_roles: str):
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
    content = db.query(Content).filter(Content.id == content_id).first()
    if content is None:
        raise HTTPException(status_code=404, detail="콘텐츠를 찾을 수 없습니다.")
    db.delete(content)
    db.commit()
    return {"message": "삭제 완료"}
```

### 바이브 코딩 시 체크포인트

- [ ] 모든 API 엔드포인트에 "누가 이 기능을 사용할 수 있는가?"를 정의했는지 확인합니다.
- [ ] 데이터 조회/수정/삭제 시 **소유권 확인**을 수행하는지 확인합니다.

---

## 7-3. 중요한 자원에 대한 잘못된 권한 설정

### 개요

파일 권한(File Permission)이란 운영체제에서 파일이나 디렉터리에 대해 "누가 읽고, 쓰고, 실행할 수 있는지"를 제어하는 설정입니다.

### 바이브 코딩 시 체크포인트

- [ ] AI가 생성한 코드에서 `os.chmod`나 `os.makedirs`를 사용하는 부분의 권한 값을 확인합니다.
- [ ] `0o777` 또는 `0o666`이 사용된 곳이 있다면 즉시 최소 권한으로 변경합니다.
- [ ] `.env` 파일의 권한이 소유자 전용(`0o600`)으로 설정되어 있는지 확인합니다.

> **💡 팁:** `0o600`은 소유자만 읽기/쓰기, `0o700`은 소유자만 읽기/쓰기/실행, `0o777`은 **절대 사용 금지**입니다.

---

# Chapter 08. 암호화, 제대로 하고 계십니까

### 암호화 알고리즘 안전/위험 분류표

```
┌─────────────────────────────────────────────────────────────────────┐
│               암호화 알고리즘 안전/위험 분류표                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ❌ 위험 (사용 금지) ══════════════════════════════════════════     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  알고리즘       │  유형          │  위험 사유               │    │
│  ├─────────────────┼────────────────┼──────────────────────────┤    │
│  │  DES            │  대칭 암호     │  56비트 키, 무차별 크랙  │    │
│  │  3DES           │  대칭 암호     │  느리고 취약, 폐기 예정  │    │
│  │  RC4            │  스트림 암호   │  편향 바이트, TLS 금지   │    │
│  │  MD5            │  해시          │  충돌 공격 가능          │    │
│  │  SHA-1          │  해시          │  충돌 공격 실증됨        │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                     │
│  ✅ 안전 (권장) ──────────────────────────────────────────────     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  알고리즘       │  유형          │  권장 용도               │    │
│  ├─────────────────┼────────────────┼──────────────────────────┤    │
│  │  AES-256        │  대칭 암호     │  데이터 암호화           │    │
│  │  ChaCha20       │  스트림 암호   │  모바일/경량 암호화      │    │
│  │  RSA-2048+      │  비대칭 암호   │  키 교환, 전자서명       │    │
│  │  SHA-256 (HMAC) │  메시지 인증   │  무결성 검증             │    │
│  │  bcrypt         │  패스워드 해시 │  패스워드 저장           │    │
│  │  argon2         │  패스워드 해시 │  패스워드 저장 (최신)    │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  💡 바이브 코더 빠른 판별법:                                │    │
│  │                                                             │    │
│  │  import hashlib                                             │    │
│  │  hashlib.md5(...)      ══▶  ❌ 즉시 교체                   │    │
│  │  hashlib.sha1(...)     ══▶  ❌ 즉시 교체                   │    │
│  │  bcrypt.hashpw(...)    ──▶  ✅ 안전                        │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## 8-1. 취약한 암호화 알고리즘 사용

### 바이브 코딩 시 체크포인트

- [ ] AI가 생성한 코드에서 `DES`, `MD5`, `SHA1`, `RC4`, `Blowfish`를 사용하는 부분이 없는지 검색합니다.
- [ ] 대칭키 암호화는 AES-128 이상(권장 AES-256)을 사용합니다.
- [ ] 패스워드 해싱에는 `passlib`의 `CryptContext(schemes=["bcrypt"])`를 사용합니다.

---

## 8-2. 암호화되지 않은 중요정보

### 바이브 코딩 시 체크포인트

- [ ] 패스워드는 반드시 `passlib`의 `CryptContext`로 해시화하여 저장하고, 평문 저장 코드가 없는지 확인합니다.
- [ ] 외부 API 통신 시 `http://`가 아닌 `https://`를 사용하는지 확인합니다.
- [ ] Pydantic 모델에서 민감한 필드에 `SecretStr` 타입을 사용하는지 확인합니다.

---

## 8-3. 하드코딩된 중요정보

### 안전 코드

```python
# ✅ 안전한 코드: BaseSettings를 통한 중요정보 관리
from pydantic_settings import BaseSettings
from pydantic import SecretStr

class Settings(BaseSettings):
    openai_api_key: SecretStr
    database_url: SecretStr
    jwt_secret_key: SecretStr

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

settings = Settings()
```

### 바이브 코딩 시 체크포인트

- [ ] AI가 생성한 코드에서 API 키, 패스워드, 시크릿 키가 문자열로 하드코딩되어 있지 않은지 확인합니다.
- [ ] Pydantic `BaseSettings`를 사용하여 환경 변수를 타입 안전하게 관리합니다.
- [ ] `.env` 파일을 생성하고, 반드시 `.gitignore`에 추가합니다.

---

## 8-4. 충분하지 않은 키 길이

### 권장 키 길이 표

| 알고리즘 유형 | 알고리즘 | ❌ 취약한 키 길이 | ✅ 권장 키 길이 |
|---|---|---|---|
| 대칭키 암호(Symmetric) | AES | 64비트 이하 | **128비트 이상** (권장 256비트) |
| 비대칭키 암호(Asymmetric) | RSA | 1024비트 이하 | **2048비트 이상** (권장 3072비트) |
| 타원곡선 암호(ECC) | ECDSA | 160비트 이하 | **224비트 이상** (권장 256비트) |
| 해시 함수(Hash) | SHA | SHA-1 (160비트) | **SHA-256 이상** |

---

# Chapter 09. 난수, 패스워드, 그리고 인증 방어

### 패스워드 해싱 흐름도

```
┌─────────────────────────────────────────────────────────────────────┐
│                     패스워드 해싱 흐름도                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ❌ 취약한 방식 (사용 금지)                                        │
│  ─────────────────────────                                          │
│                                                                     │
│  ┌──────────┐     ┌─────────────┐     ┌──────────────┐             │
│  │ 비밀번호 │══▶│  MD5/SHA-1  │══▶│ 해시값 저장  │             │
│  │ "1234"   │     │  (단순 해싱)│     │ e10adc3949...│             │
│  └──────────┘     └─────────────┘     └──────┬───────┘             │
│                                              │                      │
│                                              ▼                      │
│                                 ┌──────────────────────┐            │
│                                 │ ⚠️  레인보우 테이블로 │            │
│                                 │    수초 만에 크랙!    │            │
│                                 └──────────────────────┘            │
│                                                                     │
│  ✅ 안전한 방식 (권장)                                             │
│  ─────────────────────                                              │
│                                                                     │
│  ┌──────────┐     ┌────────────────┐     ┌─────────────────────┐   │
│  │ 비밀번호 │──▶│ ② 랜덤 솔트  │──▶│ ③ bcrypt / argon2  │   │
│  │ "1234"   │     │    생성        │     │ (비밀번호 + 솔트)  │   │
│  └──────────┘     │ "x7Kp2m..."   │     │  반복 해싱 수천 회  │   │
│                    └────────────────┘     └──────────┬──────────┘   │
│                                                      │              │
│                                                      ▼              │
│                                          ┌───────────────────────┐  │
│                                          │ ④ 해시값 + 솔트 저장 │  │
│                                          │ "$2b$12$x7Kp2m..."   │  │
│                                          └───────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## 9-1. 적절하지 않은 난수 값 사용

### 바이브 코딩 시 체크포인트

- [ ] AI가 생성한 코드에서 `import random`이 보안 관련 기능에 사용되고 있지 않은지 확인합니다.
- [ ] 보안 관련 난수 생성에는 반드시 `secrets` 모듈을 사용합니다.

---

## 9-2. 취약한 패스워드 허용

### 바이브 코딩 시 체크포인트

- [ ] 회원가입 및 패스워드 변경 API에 패스워드 강도 검증 로직이 포함되어 있는지 확인합니다.
- [ ] 최소 8자 이상, 대소문자/숫자/특수문자 조합을 요구하는지 확인합니다.

---

## 9-3. 솔트 없는 일방향 해시 함수 사용

### 바이브 코딩 시 체크포인트

- [ ] `hashlib.sha256(password)`처럼 솔트 없이 단순 해시만 사용하는 코드가 없는지 확인합니다.
- [ ] 패스워드 저장에는 반드시 `passlib`의 `CryptContext(schemes=["bcrypt"])`를 사용합니다.

---

## 9-4. 반복된 인증시도 제한 기능 부재

### 바이브 코딩 시 체크포인트

- [ ] 로그인 엔드포인트에 `slowapi`의 `@limiter.limit()` 데코레이터가 적용되어 있는지 확인합니다.
- [ ] 로그인 실패 시 어떤 정보가 틀렸는지 구분하지 않는 메시지를 사용합니다.

---

# Chapter 10. 서명, 인증서, 무결성 검증

## 10-1. 부적절한 전자서명 확인

### 바이브 코딩 시 체크포인트

- [ ] `jwt.decode()`에 `verify_signature=False`가 설정되어 있지 않은지 확인합니다.
- [ ] `algorithms` 매개변수에 `"none"`이 포함되어 있지 않은지 확인합니다.
- [ ] `algorithms`에는 사용하는 단일 알고리즘만 명시합니다 (예: `["HS256"]`).

---

## 10-2. 부적절한 인증서 유효성 검증

### 바이브 코딩 시 체크포인트

- [ ] 코드 전체에서 `verify=False`를 검색하여 제거합니다.
- [ ] `ssl._create_unverified_context()`가 사용되고 있지 않은지 확인합니다.

---

## 10-3. 무결성 검사 없는 코드 다운로드

### 바이브 코딩 시 체크포인트

- [ ] AI가 추천하는 패키지 이름의 철자가 정확한지 PyPI에서 직접 확인합니다.
- [ ] `curl ... | bash`와 같은 검증 없는 스크립트 실행을 피합니다.
- [ ] `requirements.txt`에 패키지 버전을 고정(`==`)하여 예기치 않은 업데이트를 방지합니다.

---

# Chapter 11. 정보 노출을 차단하세요

## 11-1. 쿠키를 통한 정보 노출

### 바이브 코딩 시 체크포인트

- [ ] `response.set_cookie()` 호출 시 `httponly=True`, `secure=True`, `samesite="lax"`가 모두 설정되어 있는지 확인합니다.
- [ ] `max_age`를 설정하여 영구 쿠키를 방지합니다.

---

## 11-2. 주석문 안에 포함된 시스템 주요정보

### 바이브 코딩 시 체크포인트

- [ ] AI가 생성한 코드의 모든 주석을 검토하여 패스워드, API 키, 서버 주소가 포함되어 있지 않은지 확인합니다.
- [ ] FastAPI의 docstring에 내부 시스템 정보가 포함되어 있지 않은지 확인합니다. docstring 내용은 `/docs` 페이지에 그대로 노출됩니다.
- [ ] `detect-secrets`를 Pre-commit Hook으로 설정하여 커밋 전에 자동으로 검사합니다.

---

# PART 4. 안정적인 코드를 작성하세요

# Chapter 12. 시간 및 상태 — 타이밍이 만드는 버그

여러 작업이 동시에 실행되는 환경에서는 "언제" 코드가 실행되는지가 "무엇을" 실행하는지만큼 중요합니다. FastAPI는 `async/await` 기반의 비동기 프레임워크이므로, 동시성 문제가 스레드가 아닌 코루틴(Coroutine) 수준에서 발생합니다.

---

## 12-1. 경쟁 조건: 검사 시점과 사용 시점(TOCTOU)

### ✅ 안전한 코드

```python
import os
import asyncio
from fastapi import FastAPI, UploadFile

app = FastAPI()
file_lock = asyncio.Lock()

@app.post("/upload")
async def write_shared_file(file: UploadFile):
    filepath = f"./uploads/{file.filename}"

    async with file_lock:
        if os.path.isfile(filepath):
            content = await file.read()
            with open(filepath, 'wb') as f:
                f.write(content)
            return {"status": "updated"}

    return {"status": "file not found"}
```

> **💡 팁:** `asyncio.Lock()`은 단일 프로세스 내에서만 유효하므로, 다중 워커(Worker) 환경에서는 Redis 분산 락(Distributed Lock)이나 데이터베이스 수준의 잠금을 사용하십시오.

---

## 12-2. 종료되지 않는 반복문 또는 재귀 함수

### ✅ 안전한 코드

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

MAX_DEPTH = 10

def get_nested_comments(comment_id: int, depth: int = 0):
    if depth >= MAX_DEPTH:
        return []

    replies = fetch_replies(comment_id)
    if not replies:
        return []

    for reply in replies:
        reply["children"] = get_nested_comments(reply["id"], depth + 1)
    return replies
```

> **⚠️ 주의:** AI가 `RecursionError`를 해결하기 위해 `sys.setrecursionlimit()`을 제안하면 주의해야 합니다. 이는 근본적인 해결이 아니라 시한폭탄의 타이머를 늘리는 것과 같습니다.

### 바이브 코딩 시 체크포인트

| 점검 항목 | 확인 방법 |
|-----------|-----------|
| 공유 자원에 Lock 사용 여부 | 파일, 전역 변수 접근 시 `asyncio.Lock()` 또는 데이터베이스 트랜잭션 사용 확인 |
| 재귀 함수의 기본 케이스 | 모든 재귀 함수에 명확한 종료 조건이 있는지 확인 |
| `setrecursionlimit` 사용 여부 | 코드베이스에서 해당 함수 호출을 검색하여 불필요한 사용 제거 |

---

# Chapter 13. 에러 처리 — 오류가 보안 구멍이 되는 순간

---

## 13-1. 오류 메시지 정보 노출

### ✅ 안전한 코드

```python
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)
app = FastAPI(debug=False)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        f"처리되지 않은 예외 발생: {request.method} {request.url}",
        exc_info=True
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요."}
    )
```

---

## 13-2. 오류 상황 대응 부재

오류가 발생할 수 있는 부분을 `try-except`로 감싸놓았지만, `except` 블록에서 아무런 조치도 취하지 않는 "조용한 실패(Silent Failure)"를 피하십시오.

---

## 13-3. 부적절한 예외 처리

### 바이브 코딩 시 체크포인트

| 점검 항목 | 확인 방법 |
|-----------|-----------|
| `debug=True` 설정 여부 | `FastAPI(debug=True)`, `uvicorn --reload` 사용 여부 확인 |
| 빈 `except` 블록 | `except:` 뒤에 `pass`만 있는 코드 검색 |
| 광범위한 예외 처리 | `except Exception:` 사용 시 예외 종류를 세분화할 수 있는지 검토 |
| 로깅 설정 | `print()` 대신 `logging` 모듈을 사용하고 있는지 확인 |

---

# Chapter 14. 코드 오류 — 개발자가 놓치기 쉬운 함정들

---

## 14-1. Null Pointer 역참조

### ✅ 안전한 코드: Pydantic 모델로 검증 자동화 (권장)

```python
from pydantic import BaseModel, field_validator
from fastapi import FastAPI

app = FastAPI()

class UserInput(BaseModel):
    username: str

    @field_validator("username")
    @classmethod
    def username_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("이름은 빈 문자열일 수 없습니다.")
        return v.strip()

@app.post("/search")
async def parse_input(user_input: UserInput):
    return {"name": user_input.username}
```

---

## 14-2. 부적절한 자원 해제

### ✅ 안전한 코드: FastAPI 의존성 주입으로 데이터베이스 세션 관리

```python
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

app = FastAPI()
engine = create_async_engine("sqlite+aiosqlite:///app.db")
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()
```

---

## 14-3. 신뢰할 수 없는 데이터의 역직렬화

> **⚠️ 주의:** `pickle` 모듈은 **신뢰할 수 없는 데이터에 대해 안전하지 않습니다**. FastAPI에서는 Pydantic 모델을 활용하면 JSON 기반의 안전한 역직렬화가 자동으로 이루어집니다.

### 바이브 코딩 시 체크포인트

| 점검 항목 | 확인 방법 |
|-----------|-----------|
| `None` 체크 누락 | `Optional[]` 타입 파라미터 사용 시 `is None` 검사 여부 |
| `async with` 문 사용 | httpx 클라이언트, DB 세션, 파일 등에 비동기 컨텍스트 매니저 사용 여부 확인 |
| `pickle.loads()` 사용 | 코드베이스에서 `pickle` 모듈 사용 검색, 외부 데이터 역직렬화 여부 확인 |
| Lifespan 자원 관리 | 전역 HTTP 클라이언트나 DB 엔진이 `lifespan`으로 정리되는지 확인 |

---

# PART 5. 구조와 설계로 지키세요

# Chapter 15. 캡슐화 — 보여서는 안 되는 것들

---

## 15-1. 잘못된 세션에 의한 데이터 정보 노출

### ✅ 안전한 코드: Depends()를 활용한 의존성 주입

```python
from fastapi import FastAPI, Depends, Form

app = FastAPI()

class UserService:
    def __init__(self, user_name: str):
        self.user_name = user_name

    async def get_profile(self):
        return await fetch_profile_from_db(self.user_name)

async def get_user_service(name: str = Form(...)) -> UserService:
    return UserService(user_name=name)

@app.post("/profile")
async def show_user_profile(service: UserService = Depends(get_user_service)):
    profile = await service.get_profile()
    return {"profile": profile}
```

> **💡 팁:** 사용자별 데이터는 반드시 함수의 지역 변수나 `Depends()`로 주입된 인스턴스에 보관하십시오. 모듈 수준 변수에는 설정값이나 상수만 저장해야 합니다.

---

## 15-2. 제거되지 않고 남은 디버그 코드

> **⚠️ 주의:** 배포 전 다음 키워드로 코드베이스를 반드시 검색하십시오: `print(`, `console.log(`, `debug=True`, `FastAPI(debug=True)`, `/debug`, `/test`, `TODO`, `FIXME`, `HACK`.

### 바이브 코딩 시 체크포인트

| 점검 항목 | 확인 방법 |
|-----------|-----------|
| 모듈 수준 변수에 사용자 데이터 저장 여부 | `global` 키워드 사용 여부 확인 |
| `print()` 문 잔존 여부 | 코드베이스 전체에서 `print(` 검색 |
| `debug=True` 설정 | `FastAPI(debug=True)`, `uvicorn --reload` 인자 확인 |
| 디버그 엔드포인트 | URL 라우팅에서 `/debug`, `/test` 등 테스트용 경로 확인 |
| 하드코딩된 테스트 계정 | 코드에서 `test@`, `admin/admin`, `password123` 등 검색 |

---

# Chapter 16. API 오용 — 편리함 뒤에 숨은 위험

---

## 16-1. 취약한 API 사용

### 안전한 패키지 선택 기준

1. **사용 통계**: PyPI 통계나 GitHub 스타(Star) 수를 참고
2. **이슈 관리**: 버그 리포트와 보안 이슈가 적시에 처리되는지 확인
3. **마지막 업데이트**: 최근 6개월 이내에 업데이트가 있었는지 확인
4. **알려진 취약점**: NIST NVD에서 패키지명으로 검색

### 바이브 코딩 시 체크포인트

| 점검 항목 | 확인 방법 |
|-----------|-----------|
| `yaml.load()` 사용 여부 | `yaml.safe_load()`로 대체 |
| `eval()`, `exec()` 사용 여부 | `ast.literal_eval()` 또는 안전한 대안으로 대체 |
| `md5`, `sha1` 해시 사용 | 비밀번호에는 `bcrypt`, 무결성 검증에는 `sha256` 이상 사용 |
| 패키지 버전 고정 | `requirements.txt`에 최소 버전 명시, 주기적 업데이트 |
| 패키지 취약점 검사 | `pip-audit` 또는 `safety check` 실행 |

---

# PART 6. 바이브 코딩 보안 체크리스트

# Chapter 17

### 바이브 코딩 배포 전 보안 체크 플로우차트

```
┌─────────────────────────────────────────────────────────────────────┐
│              바이브 코딩 배포 전 보안 체크 플로우차트               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────┐                                        │
│  │ ① AI로 코드 생성 완료  │                                        │
│  └────────────┬────────────┘                                        │
│               │                                                     │
│               ▼                                                     │
│  ┌─────────────────────────────────────┐       ┌──────────────────┐ │
│  │ ② .env 파일에 시크릿 분리했는가?   │─ No ─▶│ 🔧 수정 필요    │ │
│  │    (API키, DB비번, 토큰 등)        │       │ 하드코딩된 시크릿│ │
│  └──────────────┬──────────────────────┘       │ .env로 분리      │ │
│            Yes  │                              └──────────────────┘ │
│                 ▼                                                    │
│  ┌─────────────────────────────────────┐       ┌──────────────────┐ │
│  │ ③ 입력값 검증이 있는가?            │─ No ─▶│ 🔧 수정 필요    │ │
│  │    (SQL, XSS, 경로 조작 방어)      │       │ 모든 사용자 입력 │ │
│  └──────────────┬──────────────────────┘       │ 검증 로직 추가   │ │
│            Yes  │                              └──────────────────┘ │
│                 ▼                                                    │
│  ┌─────────────────────────────────────┐       ┌──────────────────┐ │
│  │ ④ 인증/인가가 적용되었는가?        │─ No ─▶│ 🔧 수정 필요    │ │
│  │    (로그인 + 권한 확인)            │       │ 인증/인가 미들웨 │ │
│  └──────────────┬──────────────────────┘       │ 어 적용          │ │
│            Yes  │                              └──────────────────┘ │
│                 ▼                                                    │
│  ┌─────────────────────────────────────┐       ┌──────────────────┐ │
│  │ ⑤ DEBUG=False 설정했는가?          │─ No ─▶│ 🔧 수정 필요    │ │
│  │    (프로덕션 환경 설정)            │       │ DEBUG=False 설정 │ │
│  └──────────────┬──────────────────────┘       │ 환경변수 분리    │ │
│            Yes  │                              └──────────────────┘ │
│                 ▼                                                    │
│  ┌─────────────────────────────────────┐       ┌──────────────────┐ │
│  │ ⑥ 에러 메시지에 민감정보 없는가?   │─ No ─▶│ 🔧 수정 필요    │ │
│  │    (스택트레이스, DB정보 노출)      │       │ 사용자에게 일반  │ │
│  └──────────────┬──────────────────────┘       │ 에러 메시지 반환 │ │
│            Yes  │                              └──────────────────┘ │
│                 ▼                                                    │
│  ┌─────────────────────────────────────┐       ┌──────────────────┐ │
│  │ ⑦ 보안 헤더 설정했는가?            │─ No ─▶│ 🔧 수정 필요    │ │
│  │    (CSP, HSTS, X-Frame 등)         │       │ 보안 헤더 미들웨 │ │
│  └──────────────┬──────────────────────┘       │ 어 추가 (helmet) │ │
│            Yes  │                              └──────────────────┘ │
│                 ▼                                                    │
│  ┌─────────────────────────────────────┐                            │
│  │  ✅ 배포 준비 완료!                │                            │
│  │     모든 보안 체크 통과            │                            │
│  └─────────────────────────────────────┘                            │
│                                                                     │
│  💡 팁: 각 단계에서 "No"가 나오면 수정 후 ①부터 다시 시작!        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 17-1. 배포 전 보안 체크리스트

### 개요

여러분이 바이브 코딩으로 만든 웹사이트를 세상에 공개하기 전, 반드시 점검해야 할 보안 항목을 정리하였습니다. 이 체크리스트는 PART 2~5에서 다룬 모든 핵심 보안 주제를 카테고리별로 요약한 것입니다.

### 인증/인가(Authentication/Authorization) 체크리스트

- [ ] 비밀번호는 bcrypt, scrypt, Argon2 등의 해시 알고리즘(Hash Algorithm)으로 저장하고 있습니까?
- [ ] 비밀번호를 평문(Plain Text)으로 저장하거나 MD5/SHA1으로만 해싱하고 있지 않습니까?
- [ ] 로그인 실패 시 구체적인 정보를 노출하지 않습니까?
- [ ] 로그인 시도 횟수 제한(Rate Limiting)이 적용되어 있습니까?
- [ ] 세션 토큰 또는 JWT의 만료 시간이 적절하게 설정되어 있습니까?
- [ ] 로그아웃 시 서버 측에서 세션이 완전히 무효화됩니까?
- [ ] 관리자 페이지에 별도의 인가(Authorization) 검증이 적용되어 있습니까?
- [ ] API 엔드포인트마다 적절한 권한 검증이 이루어지고 있습니까?
- [ ] JWT 비밀키가 충분히 길고 복잡합니까? (최소 256비트 권장)
- [ ] 비밀번호 재설정 토큰에 만료 시간이 설정되어 있습니까?

### 입력값 검증(Input Validation) 체크리스트

- [ ] 모든 사용자 입력에 대해 서버 측 검증이 구현되어 있습니까?
- [ ] 클라이언트 측 검증만으로 보안을 의존하고 있지 않습니까?
- [ ] SQL 쿼리에 매개변수화된 쿼리 또는 ORM을 사용하고 있습니까?
- [ ] 사용자 입력이 HTML에 출력될 때 적절히 이스케이프 처리되고 있습니까?
- [ ] 파일 업로드 시 파일 확장자, MIME 타입, 파일 크기를 검증하고 있습니까?
- [ ] URL 리다이렉트 시 오픈 리다이렉트 취약점이 없습니까?
- [ ] POST 요청이 필요한 모든 폼에 CSRF 토큰이 포함되어 있습니까?

### 민감정보 보호(Sensitive Data Protection) 체크리스트

- [ ] API 키, 데이터베이스 비밀번호, JWT 시크릿 등이 소스코드에 하드코딩되어 있지 않습니까?
- [ ] `.env` 파일이 `.gitignore`에 포함되어 있습니까?
- [ ] Git 히스토리에 과거에 커밋된 비밀키가 남아 있지 않습니까?
- [ ] API 응답에 필요 이상의 사용자 정보가 포함되지 않습니까?
- [ ] 에러 메시지에 내부 정보가 노출되지 않습니까?
- [ ] 로그에 비밀번호, 토큰, 개인정보 등 민감한 데이터가 기록되지 않습니까?

### 에러 처리(Error Handling) 체크리스트

- [ ] 프로덕션 환경에서 상세한 에러 메시지가 사용자에게 노출되지 않습니까?
- [ ] 커스텀 에러 페이지(404, 500 등)가 구성되어 있습니까?
- [ ] 예외 처리가 적절히 구현되어 있습니까?

### 배포 설정(Deployment Configuration) 체크리스트

- [ ] HTTPS가 적용되어 있습니까?
- [ ] 디버그 모드가 비활성화되어 있습니까?
- [ ] 보안 관련 HTTP 헤더가 설정되어 있습니까?
- [ ] CORS 설정이 필요한 도메인만 허용하고 있습니까?

---

## 17-2. AI에게 보안 검토 요청하는 프롬프트 예시

### 프롬프트 1: 전체 보안 감사(Full Security Audit)

```text
다음 코드에 대해 보안 감사를 수행해 주십시오.

아래 카테고리별로 취약점을 분석하고, 각 취약점에 대해
(1) 위험 등급(상/중/하), (2) 설명, (3) 수정된 코드를 제시해 주십시오.

검토 카테고리:
- SQL 삽입(SQL Injection)
- 크로스사이트 스크립트(XSS)
- 크로스사이트 요청 위조(CSRF)
- 인증 및 인가 결함
- 민감정보 노출
- 안전하지 않은 설정

[여기에 코드를 붙여넣으십시오]
```

### 프롬프트 6: Cursor/Claude Code 전용 — 보안 강화 코드 생성 요청

```text
다음 기능을 구현해 주십시오.
반드시 아래의 보안 요구사항을 모두 충족해야 합니다.

기능: [구현할 기능을 설명하십시오]

보안 요구사항:
- 모든 비밀키와 민감정보는 환경 변수에서 로드할 것
- SQL 쿼리는 반드시 매개변수화된 쿼리를 사용할 것
- 사용자 입력은 서버 측에서 반드시 검증할 것
- 비밀번호는 bcrypt로 해싱할 것
- CSRF 토큰을 모든 POST 폼에 포함할 것
- 에러 메시지에 내부 정보를 노출하지 말 것
- 디버그 모드는 환경 변수로 제어할 것

코드를 생성한 후, 본인이 생성한 코드에 대해 보안 자체 검토를 수행하고
잠재적 취약점이 있다면 함께 알려 주십시오.
```

---

## 17-3. 자주 발생하는 바이브 코딩 보안 실수 TOP 10

### 1위: 비밀키 하드코딩(Hardcoded Secrets)

```python
# ❌ 취약한 코드
SECRET_KEY = "my-secret-key-123"
DATABASE_URL = "postgresql://admin:password123@localhost/mydb"

# ✅ 안전한 코드
import os
SECRET_KEY = os.environ["SECRET_KEY"]
DATABASE_URL = os.environ["DATABASE_URL"]
```

---

### 2위: SQL 삽입(SQL Injection) 취약 쿼리

```python
# ❌ 취약한 코드
query = f"SELECT * FROM users WHERE id = {user_id}"

# ✅ 안전한 코드
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```

---

### 3위: 비밀번호 평문 저장

```python
# ❌ 취약한 코드
def register(username, password):
    db.execute("INSERT INTO users (username, password) VALUES (?, ?)",
               (username, password))

# ✅ 안전한 코드
import bcrypt

def register(username, password):
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
               (username, password_hash))
```

---

### 4위: CSRF 토큰 누락

프레임워크의 CSRF 보호 기능을 반드시 활성화하고, 모든 폼에 CSRF 토큰 필드를 추가하십시오.

---

### 5위: 디버그 모드 활성화 상태로 배포

```python
# ❌ 취약한 코드
app.run(debug=True)

# ✅ 안전한 코드
import os
app.run(debug=os.environ.get("FLASK_DEBUG", "false").lower() == "true")
```

---

### 6위: 입력값 서버 측 검증 누락

모든 입력값은 반드시 서버 측에서 다시 검증해야 합니다. 클라이언트 검증은 사용자 편의를 위한 것이며, 보안을 위한 것이 아닙니다.

---

### 7위: 불충분한 에러 처리와 정보 노출

```python
# ❌ 취약한 코드
@app.errorhandler(Exception)
def handle_error(e):
    return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

# ✅ 안전한 코드
@app.errorhandler(Exception)
def handle_error(e):
    app.logger.error(f"Unhandled exception: {e}", exc_info=True)
    return jsonify({"error": "서버 내부 오류가 발생하였습니다."}), 500
```

---

### 8위: CORS 전체 허용

```python
# ❌ 취약한 코드
from flask_cors import CORS
CORS(app)  # 모든 출처 허용

# ✅ 안전한 코드
from flask_cors import CORS
CORS(app, origins=["https://yourdomain.com", "https://www.yourdomain.com"])
```

---

### 9위: 안전하지 않은 파일 업로드

파일 유형 검증, 크기 제한, UUID 기반 안전한 파일명 생성을 반드시 적용하십시오.

---

### 10위: HTTPS 미적용 및 보안 헤더 누락

HTTPS를 적용하고, 보안 관련 HTTP 응답 헤더(HSTS, CSP, X-Frame-Options 등)를 설정하십시오.

---

> **⚠️ 주의:** 위 TOP 10 실수 중 1위부터 5위까지는 거의 모든 바이브 코딩 프로젝트에서 발견됩니다. 배포 전 최소한 이 5가지만이라도 반드시 점검하십시오.

### 바이브 코딩 시 체크포인트

- [ ] 위 TOP 10 항목을 모두 확인하고, 자신의 프로젝트에 해당되는 실수가 없는지 점검하였습니까?
- [ ] 1위~5위 항목에 대해 특히 주의 깊게 코드를 검토하였습니까?
- [ ] AI에게 코드를 생성 요청할 때 위 실수들을 방지하는 조건을 프롬프트에 포함하였습니까?
- [ ] 17-2절의 프롬프트 템플릿을 사용하여 AI에게 자동 보안 검토를 요청하였습니까?

> **💡 팁:** 이 TOP 10 목록을 프로젝트 저장소의 `SECURITY_CHECKLIST.md` 파일로 저장해 두면, 새로운 기능을 추가할 때마다 빠르게 참조할 수 있습니다. 또한 Cursor의 `.cursorrules` 파일이나 Claude Code의 `CLAUDE.md` 파일에 "위 10가지 보안 실수를 피하라"는 지침을 추가하면 AI가 처음부터 더 안전한 코드를 생성합니다.
