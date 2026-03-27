# PART 6: 바이브 코딩 보안 체크리스트

# Chapter 17

---

## 17-1. 배포 전 보안 체크리스트

### 개요

여러분이 바이브 코딩으로 만든 웹사이트를 세상에 공개하기 전, 반드시 점검해야 할 보안 항목을 정리하였습니다. 이 체크리스트는 PART 2~5에서 다룬 모든 핵심 보안 주제를 카테고리별로 요약한 것입니다. 하나라도 통과하지 못한 항목이 있다면 해당 챕터로 돌아가서 수정한 후 배포하십시오.

이 체크리스트는 특정 프레임워크에 종속되지 않습니다. Python, JavaScript, Java, Go, Ruby 등 어떤 기술 스택을 사용하든 동일하게 적용할 수 있습니다.

### 왜 위험한가

바이브 코딩의 가장 큰 위험은 "동작하면 완성"이라고 착각하는 것입니다. AI가 생성한 코드가 로컬 환경에서 정상적으로 동작하더라도, 인터넷에 공개되는 순간 전 세계의 자동화된 공격 도구(Bot)와 해커의 표적이 됩니다. 체크리스트 없이 배포하면 가장 기본적인 보안 허점마저 놓치게 됩니다.

### 인증/인가(Authentication/Authorization) 체크리스트

- [ ] 비밀번호는 bcrypt, scrypt, Argon2 등의 해시 알고리즘(Hash Algorithm)으로 저장하고 있습니까?
- [ ] 비밀번호를 평문(Plain Text)으로 저장하거나 MD5/SHA1으로만 해싱하고 있지 않습니까?
- [ ] 로그인 실패 시 구체적인 정보("아이디가 틀렸습니다")를 노출하지 않고, "아이디 또는 비밀번호가 일치하지 않습니다"처럼 일반적인 메시지를 사용하고 있습니까?
- [ ] 로그인 시도 횟수 제한(Rate Limiting)이 적용되어 있습니까?
- [ ] 세션 토큰(Session Token) 또는 JWT(JSON Web Token)의 만료 시간이 적절하게 설정되어 있습니까?
- [ ] 로그아웃 시 서버 측에서 세션이 완전히 무효화됩니까?
- [ ] 관리자 페이지에 별도의 인가(Authorization) 검증이 적용되어 있습니까?
- [ ] API 엔드포인트(Endpoint)마다 적절한 권한 검증이 이루어지고 있습니까?
- [ ] JWT 비밀키가 충분히 길고 복잡합니까? (최소 256비트 권장)
- [ ] 비밀번호 재설정 토큰에 만료 시간이 설정되어 있습니까?

> **⚠️ 주의:** AI 도구는 인증 기능 생성 시 비밀번호 해싱을 생략하는 경우가 매우 빈번합니다. 반드시 확인하십시오.

### 입력값 검증(Input Validation) 체크리스트

- [ ] 모든 사용자 입력에 대해 서버 측 검증(Server-side Validation)이 구현되어 있습니까?
- [ ] 클라이언트 측 검증(Client-side Validation)만으로 보안을 의존하고 있지 않습니까?
- [ ] SQL 쿼리에 매개변수화된 쿼리(Parameterized Query) 또는 ORM을 사용하고 있습니까?
- [ ] 사용자 입력이 HTML에 출력될 때 적절히 이스케이프(Escape) 처리되고 있습니까? (XSS 방지)
- [ ] 파일 업로드 시 파일 확장자, MIME 타입, 파일 크기를 검증하고 있습니까?
- [ ] 파일 업로드 경로에 경로 탐색(Path Traversal) 취약점이 없습니까?
- [ ] URL 리다이렉트 시 오픈 리다이렉트(Open Redirect) 취약점이 없습니까?
- [ ] 이메일, 전화번호 등의 입력 형식에 대한 검증이 적용되어 있습니까?
- [ ] POST 요청이 필요한 모든 폼에 CSRF(Cross-Site Request Forgery) 토큰이 포함되어 있습니까?
- [ ] Content-Type 헤더를 검증하여 예상치 못한 형식의 데이터를 거부하고 있습니까?

> **💡 팁:** 입력값 검증은 "허용 목록(Allowlist)" 방식이 "차단 목록(Blocklist)" 방식보다 안전합니다. 허용할 문자나 패턴을 명시적으로 정의하십시오.

### 민감정보 보호(Sensitive Data Protection) 체크리스트

- [ ] API 키, 데이터베이스 비밀번호, JWT 시크릿 등이 소스코드에 하드코딩되어 있지 않습니까?
- [ ] `.env` 파일이 `.gitignore`에 포함되어 있습니까?
- [ ] Git 히스토리에 과거에 커밋된 비밀키가 남아 있지 않습니까?
- [ ] 민감한 정보가 환경 변수(Environment Variable) 또는 시크릿 관리 서비스(Secret Manager)를 통해 관리됩니까?
- [ ] API 응답에 필요 이상의 사용자 정보(비밀번호 해시, 내부 ID 등)가 포함되지 않습니까?
- [ ] 에러 메시지에 스택 트레이스(Stack Trace), 데이터베이스 스키마, 파일 경로 등 내부 정보가 노출되지 않습니까?
- [ ] 로그(Log)에 비밀번호, 토큰, 개인정보 등 민감한 데이터가 기록되지 않습니까?
- [ ] 개인정보 수집 시 적절한 동의 절차가 구현되어 있습니까?
- [ ] 불필요한 개인정보를 수집하고 있지 않습니까? (최소 수집 원칙)
- [ ] 데이터베이스에 저장된 민감 데이터가 암호화(Encryption)되어 있습니까?

> **⚠️ 주의:** `git log`로 과거 커밋을 확인하십시오. `.env` 파일을 나중에 `.gitignore`에 추가하더라도 이미 커밋된 비밀키는 Git 히스토리에 영구적으로 남아 있습니다. 이 경우 반드시 해당 비밀키를 폐기하고 새로운 키를 발급받아야 합니다.

### 에러 처리(Error Handling) 체크리스트

- [ ] 프로덕션 환경에서 상세한 에러 메시지가 사용자에게 노출되지 않습니까?
- [ ] 커스텀 에러 페이지(404, 500 등)가 구성되어 있습니까?
- [ ] 예외 처리(Exception Handling)가 적절히 구현되어 처리되지 않은 예외가 발생하지 않습니까?
- [ ] 에러 로그가 안전한 위치에 저장되며, 외부에서 접근할 수 없습니까?
- [ ] 데이터베이스 연결 실패 등의 에러가 발생해도 서비스가 안전하게 종료되거나 복구됩니까?

### 배포 설정(Deployment Configuration) 체크리스트

- [ ] HTTPS가 적용되어 있습니까? (TLS/SSL 인증서 설정)
- [ ] HTTP 요청이 자동으로 HTTPS로 리다이렉트됩니까?
- [ ] 디버그 모드(Debug Mode)가 비활성화되어 있습니까?
- [ ] 보안 관련 HTTP 헤더가 설정되어 있습니까?
    - [ ] `X-Content-Type-Options: nosniff`
    - [ ] `X-Frame-Options: DENY` 또는 `SAMEORIGIN`
    - [ ] `X-XSS-Protection: 1; mode=block`
    - [ ] `Strict-Transport-Security` (HSTS)
    - [ ] `Content-Security-Policy` (CSP)
- [ ] 불필요한 포트가 외부에 개방되어 있지 않습니까?
- [ ] 데이터베이스가 외부 네트워크에서 직접 접근 불가능하도록 설정되어 있습니까?
- [ ] 서버의 운영체제와 소프트웨어가 최신 보안 패치가 적용된 상태입니까?
- [ ] `robots.txt`에 민감한 경로가 노출되어 있지 않습니까?
- [ ] 관리자 패널의 URL이 기본값(`/admin`)에서 변경되어 있습니까?
- [ ] CORS(Cross-Origin Resource Sharing) 설정이 필요한 도메인만 허용하고 있습니까?

> **💡 팁:** Vercel, Netlify, Railway, Render 같은 플랫폼을 사용하면 HTTPS 설정이 자동으로 적용됩니다. 그러나 보안 헤더와 CORS 설정은 여전히 여러분이 직접 구성해야 합니다.

### 바이브 코딩 시 체크포인트

- [ ] 위의 모든 카테고리를 검토하고, 미통과 항목에 대해 수정 작업을 완료하였습니까?
- [ ] 수정된 코드에 대해 AI 도구로 보안 재검토를 요청하였습니까?
- [ ] 팀원이 있다면 보안 체크리스트를 공유하고 교차 검증하였습니까?

---

## 17-2. AI에게 보안 검토 요청하는 프롬프트 예시

### 개요

AI 도구는 코드를 생성하는 것뿐만 아니라 코드를 검토하는 데도 활용할 수 있습니다. 이 절에서는 Claude, ChatGPT, Cursor, GitHub Copilot 등 모든 AI 도구에 붙여넣기하여 바로 사용할 수 있는 보안 검토 프롬프트 템플릿을 제공합니다.

이 프롬프트들은 특정 프레임워크에 종속되지 않으며, 어떤 언어/프레임워크를 사용하든 동일하게 적용할 수 있습니다.

### 왜 위험한가

AI에게 단순히 "이 코드 검토해줘"라고 요청하면 코드 스타일, 성능, 가독성 등에 대한 일반적인 피드백만 돌아오는 경우가 많습니다. 보안 취약점을 집중적으로 찾으려면 **구체적이고 보안에 특화된 프롬프트**가 필요합니다. 프롬프트가 모호하면 AI의 보안 검토도 모호해집니다.

### 프롬프트 템플릿

#### 프롬프트 1: 전체 보안 감사(Full Security Audit)

```text
다음 코드에 대해 보안 감사를 수행해 주십시오.

아래 카테고리별로 취약점을 분석하고, 각 취약점에 대해
(1) 위험 등급(상/중/하), (2) 설명, (3) 수정된 코드를 제시해 주십시오.

검토 카테고리:
- SQL 삽입(SQL Injection)
- 크로스사이트 스크립트(XSS)
- 크로스사이트 요청 위조(CSRF)
- 인증 및 인가 결함
- 민감정보 노출 (하드코딩된 비밀키, API 키 등)
- 안전하지 않은 설정 (디버그 모드, CORS 등)

사용 중인 언어/프레임워크: [여기에 기술 스택을 명시하십시오]

[여기에 코드를 붙여넣으십시오]
```

> **💡 팁:** 이 프롬프트는 프로젝트 전체 코드보다는 개별 파일이나 기능 단위로 사용하는 것이 효과적입니다. 코드가 너무 길면 AI가 핵심 취약점을 놓칠 수 있습니다.

#### 프롬프트 2: 인증 시스템 집중 검토

```text
아래 코드는 사용자 인증(로그인/회원가입) 시스템입니다.
다음 항목을 중점적으로 검토해 주십시오.

1. 비밀번호가 안전한 해시 알고리즘(bcrypt, scrypt, Argon2)으로 저장되는가?
2. 세션 또는 JWT 토큰 관리가 안전한가? (만료 시간, 서명 검증 등)
3. 브루트포스 공격(Brute Force Attack)에 대한 방어(Rate Limiting)가 있는가?
4. 비밀번호 재설정 흐름이 안전한가? (토큰 만료, 일회성 사용 등)
5. 인가(Authorization) 검증이 모든 보호된 엔드포인트에 적용되어 있는가?

취약한 부분이 있다면 수정된 코드와 함께 설명해 주십시오.

[여기에 인증 관련 코드를 붙여넣으십시오]
```

#### 프롬프트 3: API 엔드포인트 보안 검토

```text
아래 코드는 REST API 엔드포인트입니다.
OWASP API Security Top 10 기준으로 다음 항목을 검토해 주십시오.

1. 인증되지 않은 접근이 가능한 엔드포인트가 있는가?
2. 사용자가 다른 사용자의 데이터에 접근할 수 있는 IDOR(Insecure Direct Object Reference) 취약점이 있는가?
3. 입력값 검증이 누락된 곳이 있는가?
4. 응답에 불필요한 데이터(비밀번호 해시, 내부 ID 등)가 포함되어 있는가?
5. Rate Limiting이 적용되어 있는가?

각 문제에 대해 구체적인 공격 시나리오와 수정 방법을 제시해 주십시오.

[여기에 API 코드를 붙여넣으십시오]
```

#### 프롬프트 4: 환경 변수 및 비밀키 점검

```text
아래 프로젝트의 코드에서 보안상 민감한 정보를 찾아 주십시오.

다음 사항을 검토해 주십시오:
1. 하드코딩된 API 키, 비밀번호, 토큰, 시크릿이 있는가?
2. 데이터베이스 연결 문자열에 비밀번호가 포함되어 있는가?
3. .env 파일이 .gitignore에 포함되어 있는가?
4. 환경 변수가 누락되었을 때 안전하게 실패(Fail-Safe)하는가?

발견된 각 항목에 대해 환경 변수로 전환하는 수정된 코드를 제시해 주십시오.
필요한 .env.example 파일도 작성해 주십시오.

[여기에 코드를 붙여넣으십시오]
```

#### 프롬프트 5: 배포 전 최종 보안 점검

```text
아래 코드를 프로덕션 환경에 배포하려고 합니다.
배포 전 최종 보안 점검을 수행해 주십시오.

체크 항목:
1. 디버그 모드가 비활성화되어 있는가?
2. HTTPS가 강제 적용되는가?
3. 보안 헤더(HSTS, CSP, X-Frame-Options 등)가 설정되어 있는가?
4. CORS 설정이 적절한가? (와일드카드 * 사용 여부)
5. 에러 페이지가 내부 정보(스택 트레이스, DB 스키마)를 노출하지 않는가?
6. 로그에 민감한 정보(비밀번호, 토큰)가 기록되지 않는가?
7. 불필요한 파일(.env, .git, 디버그 엔드포인트)이 외부에 노출되지 않는가?

각 항목에 대해 통과/미통과를 판정하고, 미통과 항목은 수정 방법을 제시해 주십시오.

[여기에 코드를 붙여넣으십시오]
```

#### 프롬프트 6: AI 코딩 도구 전용 — 보안 강화 코드 생성 요청

```text
다음 기능을 구현해 주십시오.
반드시 아래의 보안 요구사항을 모두 충족해야 합니다.

기능: [구현할 기능을 설명하십시오]

보안 요구사항:
- 모든 비밀키와 민감정보는 환경 변수에서 로드할 것
- SQL 쿼리는 반드시 매개변수화된 쿼리 또는 ORM 쿼리 빌더를 사용할 것
- 사용자 입력은 서버 측에서 반드시 검증할 것
- 비밀번호는 bcrypt/scrypt/Argon2로 해싱할 것
- CSRF 토큰을 모든 POST 폼에 포함할 것
- 에러 메시지에 내부 정보(스택 트레이스, 파일 경로)를 노출하지 말 것
- 디버그 모드는 환경 변수로 제어할 것
- 사용자 입력이 HTML에 출력될 때 반드시 이스케이프 처리할 것

코드를 생성한 후, 본인이 생성한 코드에 대해 보안 자체 검토를 수행하고
잠재적 취약점이 있다면 함께 알려 주십시오.
```

> **💡 팁:** 프롬프트 6은 코드 생성과 보안 검토를 동시에 요청하는 방식입니다. AI에게 자체 검토를 요청하면 일반적인 코드 생성보다 보안 품질이 향상됩니다. 이 프롬프트를 프로젝트의 시스템 프롬프트, `.cursorrules` 파일, 또는 `CLAUDE.md` 파일에 포함시키면 매번 작성하지 않아도 됩니다.

### 바이브 코딩 시 체크포인트

- [ ] 코드 생성 후 위의 프롬프트 중 최소 하나를 사용하여 보안 검토를 수행하였습니까?
- [ ] AI의 보안 검토 결과에서 지적된 사항을 모두 수정하였습니까?
- [ ] 프롬프트 6을 프로젝트의 기본 설정에 포함시켰습니까?

---

## 17-3. 자주 발생하는 바이브 코딩 보안 실수 TOP 10

### 개요

이 절에서는 바이브 코딩 환경에서 가장 빈번하게 발생하는 보안 실수 10가지를 순위별로 정리하였습니다. 각 항목에 대해 실수의 내용, AI 도구에서 이 실수가 발생하는 이유, 그리고 수도 코드로 수정 방법을 설명합니다.

### 왜 위험한가

바이브 코딩의 보안 실수는 패턴이 있습니다. AI 도구들이 공통적으로 가지는 특성 때문에 동일한 유형의 취약점이 반복적으로 생성됩니다. 이 패턴을 미리 알고 있으면 AI가 코드를 생성할 때 즉시 문제를 발견할 수 있습니다.

---

### 1위: 비밀키 하드코딩(Hardcoded Secrets)

**무엇인가:** API 키, JWT 시크릿, 데이터베이스 비밀번호 등을 소스코드에 직접 작성하는 것입니다.

**왜 AI에서 발생하는가:** AI의 학습 데이터인 튜토리얼과 예제 코드 대부분이 설명의 편의를 위해 비밀키를 하드코딩합니다. AI는 여러분의 배포 환경을 알 수 없으므로 환경 변수 설정을 가정할 수 없습니다.

```pseudocode
// ❌ 취약한 수도 코드
SECRET_KEY = "my-secret-key-123"
DATABASE_URL = "postgresql://admin:password123@localhost/mydb"

// ✅ 안전한 수도 코드
SECRET_KEY = ENV.get("SECRET_KEY")
DATABASE_URL = ENV.get("DATABASE_URL")
IF SECRET_KEY is empty OR DATABASE_URL is empty:
    THROW ERROR "필수 환경 변수가 설정되지 않았습니다."
```

반드시 `.env` 파일을 `.gitignore`에 추가하고, `.env.example` 파일을 제공하여 필요한 환경 변수를 문서화하십시오.

---

### 2위: SQL 삽입(SQL Injection) 취약 쿼리

**무엇인가:** 사용자 입력을 문자열 결합으로 SQL 쿼리에 직접 삽입하는 것입니다.

**왜 AI에서 발생하는가:** 문자열 포매팅을 사용한 SQL 쿼리가 코드가 짧고 직관적이기 때문에 AI가 이 방식을 선호합니다.

```pseudocode
// ❌ 취약한 수도 코드
query = "SELECT * FROM users WHERE id = " + user_id
result = DATABASE.execute(query)

// ✅ 안전한 수도 코드
query = "SELECT * FROM users WHERE id = ?"
result = DATABASE.execute(query, [user_id])
```

---

### 3위: 비밀번호 평문 저장

**무엇인가:** 사용자의 비밀번호를 해싱 없이 데이터베이스에 그대로 저장하는 것입니다.

**왜 AI에서 발생하는가:** "회원가입 기능 만들어줘"라는 요청에 AI는 핵심 로직에 집중하고, 비밀번호 해싱을 부가적인 기능으로 취급하여 생략하는 경우가 많습니다.

```pseudocode
// ❌ 취약한 수도 코드
FUNCTION register(username, password):
    DATABASE.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                     [username, password])

// ✅ 안전한 수도 코드
FUNCTION register(username, password):
    password_hash = BCRYPT.hash(password)
    DATABASE.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                     [username, password_hash])
```

---

### 4위: CSRF 토큰 누락

**무엇인가:** 상태를 변경하는 POST 요청에 CSRF 토큰이 없는 것입니다.

**왜 AI에서 발생하는가:** AI는 HTML 폼의 기본 구조에 집중하며, CSRF 토큰은 명시적으로 요청하지 않으면 생략합니다.

**수정 방법:** 프레임워크의 CSRF 보호 기능을 반드시 활성화하고, 모든 POST 폼에 CSRF 토큰 필드를 추가하십시오.

```pseudocode
// ❌ 취약한 수도 코드
FORM action="/transfer" method="POST":
    INPUT name="amount"
    BUTTON "송금"

// ✅ 안전한 수도 코드
FORM action="/transfer" method="POST":
    HIDDEN_INPUT name="csrf_token" value=GENERATE_CSRF_TOKEN()
    INPUT name="amount"
    BUTTON "송금"
```

---

### 5위: 디버그 모드 활성화 상태로 배포

**무엇인가:** 개발용 디버그 설정이 프로덕션 환경에서도 활성화된 상태인 것입니다.

**왜 AI에서 발생하는가:** AI가 생성하는 서버 실행 코드는 거의 100% 디버그 모드가 활성화되어 있습니다. AI는 "이 코드가 프로덕션에 배포될 것"이라는 맥락을 고려하지 않습니다.

```pseudocode
// ❌ 취약한 수도 코드
APP.run(debug=TRUE)

// ✅ 안전한 수도 코드
debug_mode = ENV.get("APP_DEBUG", "false") == "true"
APP.run(debug=debug_mode)
```

---

### 6위: 입력값 서버 측 검증 누락

**무엇인가:** 사용자 입력에 대한 검증을 클라이언트(JavaScript)에서만 수행하고 서버 측 검증을 생략하는 것입니다.

**왜 AI에서 발생하는가:** AI에게 "폼 유효성 검사를 추가해줘"라고 요청하면 프론트엔드 검증을 먼저 구현합니다. 서버 측 검증은 별도로 요청하지 않으면 누락됩니다.

**수정 방법:** 모든 입력값은 반드시 서버 측에서 다시 검증해야 합니다. 클라이언트 검증은 사용자 편의를 위한 것이며, 보안을 위한 것이 아닙니다.

```pseudocode
// ✅ 안전한 수도 코드: 서버 측 검증
FUNCTION create_user(request):
    email = request.body["email"]
    age = request.body["age"]

    // 서버 측에서 반드시 재검증
    IF NOT is_valid_email(email):
        RETURN error("유효하지 않은 이메일 형식입니다.")
    IF NOT is_integer(age) OR age < 0 OR age > 150:
        RETURN error("유효하지 않은 나이입니다.")

    // 검증 후 처리
    save_user(email, age)
```

---

### 7위: 불충분한 에러 처리와 정보 노출

**무엇인가:** 에러 발생 시 스택 트레이스, 데이터베이스 쿼리, 파일 경로 등 내부 정보가 사용자에게 그대로 노출되는 것입니다.

**왜 AI에서 발생하는가:** AI는 개발 단계를 가정하고 코드를 생성하므로, 에러를 상세하게 출력하는 것을 "도움이 되는 기능"으로 취급합니다.

```pseudocode
// ❌ 취약한 수도 코드
FUNCTION handle_error(error):
    RETURN {"error": error.message, "trace": error.stack_trace}

// ✅ 안전한 수도 코드
FUNCTION handle_error(error):
    LOG.error("Unhandled exception: " + error.message, stack=error.stack_trace)
    RETURN {"error": "서버 내부 오류가 발생하였습니다."}
```

---

### 8위: CORS 전체 허용

**무엇인가:** CORS 설정에서 모든 출처(Origin)를 허용하는 `*` 와일드카드를 사용하는 것입니다.

**왜 AI에서 발생하는가:** 개발 중 CORS 에러는 매우 흔하며, AI는 이 에러를 가장 빠르게 해결하기 위해 `Access-Control-Allow-Origin: *`을 설정합니다.

```pseudocode
// ❌ 취약한 수도 코드
CORS.allow_origins("*")  // 모든 출처 허용

// ✅ 안전한 수도 코드
CORS.allow_origins(["https://yourdomain.com", "https://www.yourdomain.com"])
```

---

### 9위: 안전하지 않은 파일 업로드

**무엇인가:** 사용자가 업로드하는 파일에 대해 확장자, 크기, MIME 타입 등을 검증하지 않는 것입니다.

**왜 AI에서 발생하는가:** AI에게 "파일 업로드 기능 만들어줘"라고 요청하면 기본 기능만 구현합니다. 보안 로직은 명시적으로 요청하지 않으면 누락됩니다.

```pseudocode
// ❌ 취약한 수도 코드
FUNCTION upload(request):
    file = request.files["file"]
    SAVE_FILE(file, "uploads/" + file.name)
    RETURN "업로드 완료"

// ✅ 안전한 수도 코드
CONSTANT ALLOWED_EXT = [".png", ".jpg", ".jpeg", ".gif", ".pdf"]
CONSTANT MAX_SIZE = 5 * 1024 * 1024  // 5MB

FUNCTION upload(request):
    file = request.files["file"]

    // 확장자, 크기, MIME 타입 검증
    ext = GET_EXTENSION(file.name).lowercase()
    IF ext NOT IN ALLOWED_EXT:
        RETURN error("허용되지 않는 파일 형식입니다.")
    IF file.size > MAX_SIZE:
        RETURN error("파일 크기가 초과되었습니다.")

    // 안전한 파일명 생성
    safe_name = GENERATE_UUID() + ext
    SAVE_FILE(file, "uploads/" + safe_name)
    RETURN "업로드 완료"
```

---

### 10위: HTTPS 미적용 및 보안 헤더 누락

**무엇인가:** HTTP를 통해 데이터를 전송하거나, 보안 관련 HTTP 응답 헤더(Security Headers)를 설정하지 않는 것입니다.

**왜 AI에서 발생하는가:** AI는 로컬 개발 환경(`http://localhost`)을 기준으로 코드를 생성합니다. HTTPS 설정이나 보안 헤더는 인프라 계층의 설정이므로, 애플리케이션 코드를 생성하는 AI의 범위에서 벗어나는 경우가 많습니다.

```pseudocode
// ✅ 안전한 수도 코드: 보안 헤더 설정
FUNCTION configure_security(app):
    // HTTPS 강제 적용
    app.force_https = TRUE

    // 보안 헤더 설정
    app.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    app.headers["X-Content-Type-Options"] = "nosniff"
    app.headers["X-Frame-Options"] = "DENY"
    app.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'"
```

> **⚠️ 주의:** 위 TOP 10 실수 중 1위부터 5위까지는 거의 모든 바이브 코딩 프로젝트에서 발견됩니다. 배포 전 최소한 이 5가지만이라도 반드시 점검하십시오.

### 바이브 코딩 시 체크포인트

- [ ] 위 TOP 10 항목을 모두 확인하고, 자신의 프로젝트에 해당되는 실수가 없는지 점검하였습니까?
- [ ] 1위~5위 항목에 대해 특히 주의 깊게 코드를 검토하였습니까?
- [ ] AI에게 코드를 생성 요청할 때 위 실수들을 방지하는 조건을 프롬프트에 포함하였습니까?
- [ ] 17-2절의 프롬프트 템플릿을 사용하여 AI에게 자동 보안 검토를 요청하였습니까?

> **💡 팁:** 이 TOP 10 목록을 프로젝트 저장소의 보안 체크리스트 파일로 저장해 두면, 새로운 기능을 추가할 때마다 빠르게 참조할 수 있습니다. 또한 AI 코딩 도구의 프로젝트 설정 파일(`.cursorrules`, `CLAUDE.md`, `.github/copilot-instructions.md` 등)에 "위 10가지 보안 실수를 피하라"는 지침을 추가하면 AI가 처음부터 더 안전한 코드를 생성합니다.
