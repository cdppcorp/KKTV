# 시큐어코딩 가이드라인 Skills
## 수도 코드(Pseudocode) 버전

> 바이브 코딩을 하는 모든 사람을 위한 보안 가이드
> 언어와 프레임워크에 구애받지 않는 보편적 보안 원칙
> ❌ 취약한 수도 코드 → ✅ 안전한 수도 코드 → 💬 AI에게 요청할 프롬프트

---

# 목차

## PART 1: 시작하기
- **Chapter 1**
  - 1-1. AI가 만든 코드도 취약할 수 있습니다
  - 1-2. 이 가이드의 활용법

## PART 2: 입력값을 믿지 마세요
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
  - 5-1. 경로 조작 및 자원 삽입(Path Traversal)
  - 5-2. 위험한 형식 파일 업로드(Unrestricted File Upload)
  - 5-3. 신뢰되지 않는 URL 자동 연결(Open Redirect)
  - 5-4. 부적절한 XML 외부 개체 참조(XXE)
- **Chapter 6. 데이터 타입과 보안 결정을 노리는 공격**
  - 6-1. 정수형 오버플로우(Integer Overflow)
  - 6-2. 보안기능 결정에 사용되는 부적절한 입력값
  - 6-3. 메모리 버퍼 오버플로우(Buffer Overflow)

## PART 3: 보안 기능을 제대로 구현하세요
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

## PART 4: 안정적인 코드를 작성하세요
- **Chapter 12. 시간 및 상태 -- 타이밍이 만드는 버그**
  - 12-1. 경쟁 조건: 검사 시점과 사용 시점(TOCTOU)
  - 12-2. 종료되지 않는 반복문 또는 재귀 함수
- **Chapter 13. 에러 처리 -- 오류가 보안 구멍이 되는 순간**
  - 13-1. 오류 메시지 정보 노출
  - 13-2. 오류 상황 대응 부재
  - 13-3. 부적절한 예외 처리
- **Chapter 14. 코드 오류 -- 개발자가 놓치기 쉬운 함정들**
  - 14-1. Null 역참조
  - 14-2. 부적절한 자원 해제
  - 14-3. 신뢰할 수 없는 데이터의 역직렬화

## PART 5: 구조와 설계로 지키세요
- **Chapter 15. 캡슐화 -- 보여서는 안 되는 것들**
  - 15-1. 잘못된 세션에 의한 데이터 정보 노출
  - 15-2. 제거되지 않고 남은 디버그 코드
- **Chapter 16. API 오용 -- 편리함 뒤에 숨은 위험**
  - 16-1. 취약한 API 사용

## PART 6: 바이브 코딩 보안 체크리스트
- **Chapter 17**
  - 17-1. 배포 전 보안 체크리스트
  - 17-2. AI에게 보안 검토 요청하는 프롬프트 예시
  - 17-3. 자주 발생하는 바이브 코딩 보안 실수 TOP 10

---

# PART 1: 시작하기

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

```pseudocode
// ❌ 취약한 수도 코드: 비밀키가 소스코드에 하드코딩되어 있습니다
CONSTANT SECRET_KEY = "super-secret-key-12345"

FUNCTION login(request):
    username = request.body["username"]
    password = request.body["password"]

    // 비밀번호를 평문으로 비교합니다
    IF username == "admin" AND password == "admin123":
        token = JWT.encode({"user": username}, SECRET_KEY)
        RETURN {"token": token}

    RETURN ERROR "인증 실패", status=401
```

이 코드에는 최소 세 가지 심각한 보안 문제가 있습니다.

- `SECRET_KEY`가 소스코드에 직접 작성되어 있어 Git 저장소에 노출됩니다
- 비밀번호를 평문(Plain Text)으로 비교합니다
- 관리자 계정 정보가 코드에 하드코딩되어 있습니다

```pseudocode
// ✅ 안전한 수도 코드: 환경 변수와 해시 비교를 사용합니다
SECRET_KEY = ENV.get("JWT_SECRET_KEY")
IF SECRET_KEY is empty:
    THROW ERROR "JWT_SECRET_KEY 환경 변수가 설정되지 않았습니다."

FUNCTION login(request):
    username = request.body.get("username", "")
    password = request.body.get("password", "")

    // 데이터베이스에서 사용자 조회
    user = DATABASE.find_user(username)
    IF user is NULL:
        RETURN ERROR "인증 실패", status=401

    // bcrypt로 해시된 비밀번호 비교
    IF BCRYPT.verify(password, user.password_hash):
        token = JWT.encode(
            {"user": username, "exp": NOW() + 1 hour},
            SECRET_KEY
        )
        RETURN {"token": token}

    RETURN ERROR "인증 실패", status=401
```

> **⚠️ 주의:** AI 도구에게 인증 관련 코드를 요청할 때는 반드시 "환경 변수에서 비밀키를 로드하고, bcrypt로 비밀번호를 해싱하라"고 명시적으로 지시하십시오. 명시하지 않으면 AI는 거의 확실하게 하드코딩된 값을 사용합니다.

#### 사례 2: SQL 삽입(SQL Injection)

"사용자 검색 기능을 만들어줘"라는 프롬프트에 AI가 생성하는 전형적인 패턴입니다.

```pseudocode
// ❌ 취약한 수도 코드
FUNCTION search_user(request):
    username = request.params["username"]

    // 문자열 결합으로 직접 SQL 쿼리 구성 — SQL 삽입 취약점
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    result = DATABASE.execute(query)
    RETURN result
```

공격자가 `username` 파라미터에 `' OR '1'='1' --`을 입력하면 전체 사용자 데이터가 유출됩니다.

```pseudocode
// ✅ 안전한 수도 코드
FUNCTION search_user(request):
    username = request.params.get("username", "")

    // 매개변수화된 쿼리(Parameterized Query) 사용
    query = "SELECT id, username, email FROM users WHERE username = ?"
    result = DATABASE.execute(query, [username])
    RETURN result
```

> **💡 팁:** AI에게 데이터베이스 쿼리 코드를 요청할 때는 "반드시 매개변수화된 쿼리(Parameterized Query) 또는 ORM을 사용하라"고 지시하십시오.

#### 사례 3: CSRF 토큰 누락

AI에게 "회원 정보 수정 폼을 만들어줘"라고 요청하면 CSRF 토큰이 빠진 폼이 생성되기도 합니다.

```pseudocode
// ❌ 취약한 수도 코드: CSRF 토큰이 없습니다
FORM action="/update-profile" method="POST":
    INPUT type="text" name="email" value=user.email
    INPUT type="text" name="nickname" value=user.nickname
    BUTTON "수정하기"

// ✅ 안전한 수도 코드: CSRF 토큰을 포함합니다
FORM action="/update-profile" method="POST":
    HIDDEN_INPUT name="csrf_token" value=GENERATE_CSRF_TOKEN()
    INPUT type="text" name="email" value=user.email
    INPUT type="text" name="nickname" value=user.nickname
    BUTTON "수정하기"
```

#### 사례 4: 디버그 모드 배포

AI가 생성한 서버 실행 코드에는 거의 항상 디버그 모드가 활성화되어 있습니다.

```pseudocode
// ❌ 취약한 수도 코드
APP.run(debug=TRUE, host="0.0.0.0", port=5000)

// ✅ 안전한 수도 코드
debug_mode = ENV.get("APP_DEBUG", "false") == "true"
APP.run(debug=debug_mode, host="0.0.0.0", port=ENV.get("PORT", 5000))
```

디버그 모드(Debug Mode)가 활성화된 상태로 배포하면 상세한 에러 메시지, 스택 트레이스(Stack Trace), 심지어 대화형 디버거까지 외부에 노출됩니다.

### 바이브 코딩 시 체크포인트

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

**특히 이 가이드의 가장 큰 특징은 특정 프로그래밍 언어나 프레임워크에 종속되지 않는다는 점입니다.** Python, JavaScript, Java, Go, Ruby 등 어떤 언어를 사용하든, Django, Express, Spring, Rails 등 어떤 프레임워크를 사용하든 동일하게 적용할 수 있도록 **수도 코드(Pseudocode)**로 작성되었습니다.

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

### 각 장의 3단계 구조: 수도 코드 + AI 프롬프트

이 가이드의 모든 보안 주제는 다음과 같은 **3단계(Three-Tier) 형식**으로 작성되어 있습니다. 이 형식은 바이브 코더가 보안 취약점을 이해하고, 수정하고, AI에게 올바르게 요청하는 전 과정을 지원합니다.

#### 1단계: 취약한 수도 코드 (Vulnerable Pseudocode)

해당 취약점이 어떤 코드 패턴에서 발생하는지 수도 코드로 보여줍니다. 수도 코드는 특정 프로그래밍 언어가 아닌 **누구나 읽을 수 있는 평이한 구조**로 작성됩니다. Python을 쓰든, JavaScript를 쓰든, Go를 쓰든 동일한 패턴을 자신의 코드에서 찾아낼 수 있습니다.

```pseudocode
// ❌ 취약한 수도 코드 예시
FUNCTION search(user_input):
    query = "SELECT * FROM users WHERE name = '" + user_input + "'"
    RETURN DATABASE.execute(query)
```

#### 2단계: 안전한 수도 코드 (Secure Pseudocode)

같은 기능을 안전하게 구현하는 패턴을 수도 코드로 보여줍니다. 여러분이 사용하는 언어와 프레임워크에 맞게 이 패턴을 적용하면 됩니다.

```pseudocode
// ✅ 안전한 수도 코드 예시
FUNCTION search(user_input):
    query = "SELECT * FROM users WHERE name = ?"
    RETURN DATABASE.execute(query, [user_input])  // 매개변수화된 쿼리
```

#### 3단계: AI에게 요청할 프롬프트 (Copy-Paste Prompt)

안전한 패턴을 실제 코드로 구현하기 위해 AI 도구(Cursor, Claude Code, Copilot 등)에 그대로 복사-붙여넣기할 수 있는 프롬프트를 제공합니다. 이 프롬프트에는 보안 요구사항이 명시적으로 포함되어 있어, AI가 처음부터 안전한 코드를 생성하도록 유도합니다.

```text
다음 기능을 구현해주세요:
- 사용자 검색 API 엔드포인트
- 반드시 매개변수화된 쿼리(Parameterized Query) 사용
- 사용자 입력을 직접 SQL 문자열에 연결하지 말 것
- ORM을 사용할 경우 raw query 대신 쿼리 빌더 사용
```

이 3단계 형식의 핵심은 **여러분이 보안 전문가가 아니어도, 수도 코드로 위험 패턴을 식별하고, AI 프롬프트로 안전한 코드를 생성할 수 있다**는 것입니다.

### 이 가이드를 읽는 두 가지 방법

#### 방법 1: 처음부터 끝까지 순서대로 읽기

보안에 대한 기초 지식이 부족하다고 느끼는 분께 권장합니다. PART 1에서 기본 개념을 이해한 후 PART 2부터 순서대로 읽어나가면 웹 보안에 대한 체계적인 이해를 쌓을 수 있습니다.

#### 방법 2: 필요한 부분만 골라 읽기

이미 웹 개발 경험이 있거나, 특정 보안 이슈를 해결해야 하는 분께 권장합니다. 목차에서 해당 주제를 찾아 바로 이동하십시오. 각 장은 독립적으로 읽을 수 있도록 구성되어 있습니다.

| 상황 | 추천 챕터 |
|------|-----------|
| 로그인 기능을 AI로 만들었다 | 7장 (PART 3) |
| API 키를 코드에 넣었다 | 8장 8-3절 (PART 3) |
| 파일 업로드 기능을 추가했다 | 5장 5-2절 (PART 2) |
| 배포 직전이다 | 17장 (PART 6) |
| 에러가 나는데 그냥 배포했다 | 13장 (PART 4) |

> **💡 팁:** 바이브 코딩으로 만든 프로젝트를 배포하기 직전이라면, 먼저 PART 6의 체크리스트(Chapter 17)로 이동하여 빠르게 점검한 후, 체크리스트에서 "불합격"인 항목의 해당 챕터를 참고하는 것이 가장 효율적입니다.

### AI 도구와 함께 이 가이드 활용하기

이 가이드는 AI 도구와 함께 사용하도록 설계되었습니다. 다음과 같은 워크플로를 권장합니다.

**1단계: AI로 코드 생성**
Cursor, Claude Code, Copilot 등으로 원하는 기능의 코드를 생성합니다.

**2단계: 이 가이드로 보안 점검**
생성된 코드를 이 가이드의 해당 챕터와 대조하여, 수도 코드에 표시된 취약 패턴이 있는지 확인합니다.

**3단계: AI에게 보안 개선 요청**
발견된 취약점이 있다면, 이 가이드에 제공된 프롬프트 템플릿을 복사하여 AI에게 수정을 요청합니다.

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

- [ ] 이 가이드의 PART 구조와 3단계 형식(수도 코드 + AI 프롬프트)을 이해하였는지 확인하십시오
- [ ] AI로 코드를 생성한 후 반드시 보안 점검 단계를 거치는 습관을 만드십시오
- [ ] PART 6의 체크리스트를 북마크하여 배포 전 언제든 참조할 수 있도록 하십시오
- [ ] AI에게 코드를 요청할 때 보안 요구사항을 프롬프트에 포함하는 것을 기본 원칙으로 삼으십시오

> **⚠️ 주의:** 이 가이드를 읽는 것만으로는 보안이 보장되지 않습니다. 반드시 자신의 코드에 직접 적용하고, 체크리스트를 통해 확인하는 실천이 필요합니다. 보안은 한 번의 작업이 아니라 지속적인 과정입니다.


---

# PART 2: 입력값을 믿지 마세요

---

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

예를 들어, 로그인 폼에서 비밀번호 입력란에 `' OR '1'='1` 이라고 입력하면:

```sql
-- 원래 의도된 쿼리
SELECT * FROM users WHERE username='admin' AND password='입력값'

-- 공격자의 입력으로 변조된 쿼리
SELECT * FROM users WHERE username='admin' AND password='' OR '1'='1'
```

조건절 `'1'='1'`은 항상 참이므로 비밀번호 없이 로그인에 성공하게 됩니다.

### ❌ 취약한 수도 코드

```pseudocode
// ❌ 취약한 수도 코드: 문자열 결합으로 SQL 쿼리 생성
FUNCTION update_board(request):
    name = request.body["name"]
    content_id = request.body["content_id"]

    // 문자열 결합으로 쿼리를 생성하면 SQL 삽입에 취약합니다
    query = "UPDATE board SET name='" + name + "' WHERE content_id='" + content_id + "'"
    DATABASE.execute(query)
    RETURN success_page

// ❌ 취약한 수도 코드: ORM의 raw 쿼리 기능 오용
FUNCTION member_search(request):
    name = request.body["name"]

    // ORM의 raw 쿼리에 문자열 결합을 하면 ORM의 보호 기능이 무력화됩니다
    query = "SELECT * FROM member WHERE name='" + name + "'"
    data = ORM.raw_query(query)
    RETURN render_page("member_list", data)
```

> **⚠️ 주의:** AI 도구에 "게시판 수정 기능 만들어줘"라고 요청하면, 간혹 위와 같은 문자열 결합 방식의 코드가 생성될 수 있습니다. 특히 "간단한 예제"를 요청하면 보안이 생략되는 경우가 많습니다.

### ✅ 안전한 수도 코드

```pseudocode
// ✅ 안전한 수도 코드: 매개변수화된 쿼리(Parameterized Query) 사용
FUNCTION update_board(request):
    name = request.body["name"]
    content_id = request.body["content_id"]

    // 플레이스홀더(?)를 사용하고, 값을 별도 인자로 바인딩합니다
    query = "UPDATE board SET name = ? WHERE content_id = ?"
    DATABASE.execute(query, [name, content_id])
    RETURN success_page

// ✅ 안전한 수도 코드: ORM의 쿼리 빌더 활용
FUNCTION member_search(request):
    name = request.body["name"]

    // ORM의 쿼리 빌더는 자동으로 매개변수화된 쿼리를 생성합니다
    data = ORM.Member.filter(name=name)
    RETURN render_page("member_list", data)
```

> **💡 팁:** ORM의 `filter()`, `find()`, `where()` 등 쿼리 빌더 메서드를 사용하면 프레임워크가 자동으로 SQL 삽입을 방지합니다. 가능한 한 ORM의 기본 기능을 활용하는 것이 가장 안전합니다.

### 💬 AI에게 요청할 프롬프트

```text
다음 기능을 구현해주세요:
- 게시판 수정(UPDATE) API 엔드포인트
- 반드시 매개변수화된 쿼리(Parameterized Query) 또는 ORM 쿼리 빌더 사용
- 사용자 입력을 직접 SQL 문자열에 연결(String Concatenation)하지 말 것
- f-string, 문자열 포매팅, + 연산자로 SQL을 조합하지 말 것
- raw SQL 사용이 불가피한 경우 반드시 플레이스홀더(?, %s, :name)와 바인딩 사용
```

### 체크포인트

- [ ] 문자열 결합이나 포매팅으로 SQL 쿼리를 만들고 있지 않은가?
- [ ] ORM의 기본 쿼리 빌더를 사용하고 있는가?
- [ ] raw SQL이 꼭 필요한 경우 매개변수화된 쿼리를 사용하고 있는가?

---



> **[참고 다이어그램] SQL 삽입 공격 흐름도**

# SQL 삽입 공격 흐름도

## ❌ 취약한 흐름 (문자열 결합 방식)

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

## ✅ 안전한 흐름 (파라미터화된 쿼리 방식)

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

## 핵심 차이점

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


---

## 2-2. LDAP 삽입(LDAP Injection)

> **기타 삽입 공격 — LDAP 삽입**
>
> **우선순위: 낮음** — 대부분의 바이브 코딩 프로젝트에서는 LDAP를 직접 다루는 경우가 드뭅니다. 하지만 기업용 사내 시스템이나 Active Directory 연동 기능을 구현할 때는 주의가 필요합니다.
>
> **LDAP(Lightweight Directory Access Protocol)**은 조직 내 사용자 정보를 관리하는 디렉터리 서비스 프로토콜입니다. SQL 삽입과 동일한 원리로, 사용자 입력값이 LDAP 쿼리문에 검증 없이 포함되면 공격자가 쿼리 구조를 변경하여 권한 상승이나 정보 유출을 시도할 수 있습니다.

```pseudocode
// ❌ 취약한 수도 코드
FUNCTION search_directory(keyword):
    filter = "(&(objectclass=" + keyword + "))"
    result = LDAP.search(filter)
    RETURN result

// ✅ 안전한 수도 코드
FUNCTION search_directory(keyword):
    escaped_keyword = LDAP.escape_filter_chars(keyword)
    filter = "(&(objectclass=" + escaped_keyword + "))"
    result = LDAP.search(filter)
    RETURN result
```

> **💡 팁:** LDAP 쿼리에 사용되는 입력값은 반드시 이스케이프(Escape) 처리하십시오. 화이트리스트(Whitelist) 방식으로 검색 가능한 값을 제한하는 것도 효과적입니다.

---

# Chapter 03. 코드와 명령어를 노리는 삽입 공격

## 3-1. 코드 삽입(Code Injection)

### 개요

코드 삽입(Code Injection)은 공격자가 애플리케이션에 임의의 프로그래밍 코드를 삽입하여 실행시키는 공격입니다. SQL 삽입이 데이터베이스를 대상으로 한다면, 코드 삽입은 **프로그래밍 언어 자체**를 대상으로 합니다.

대부분의 프로그래밍 언어에는 문자열을 코드로 해석하여 실행하는 함수가 존재합니다(Python의 `eval()`/`exec()`, JavaScript의 `eval()`, PHP의 `eval()` 등). 바이브 코딩 시 AI가 "동적으로 값을 계산해줘"라는 요청에 이 함수들을 사용하는 코드를 생성하는 경우가 있어 각별한 주의가 필요합니다.

### 왜 위험한가

코드 실행 함수에 사용자 입력값이 그대로 전달되면, 공격자는 서버에서 **어떤 코드든** 실행할 수 있습니다:

- **시스템 정보 탈취**: 서버 OS 정보, 환경 변수 노출
- **파일 시스템 접근**: 서버 파일 목록 조회, 파일 내용 읽기
- **원격 쉘 실행**: 서버에 원격으로 접속하여 완전한 제어권 획득
- **서비스 거부**: 무한 루프나 대기 명령으로 서버 마비

### ❌ 취약한 수도 코드

```pseudocode
// ❌ 취약한 수도 코드: eval()에 외부 입력값 직접 전달
FUNCTION calculate(request):
    expression = request.body["expression"]

    // eval()에 사용자 입력을 그대로 전달하면
    // 임의의 코드가 실행될 수 있습니다
    result = EVAL(expression)
    RETURN result

// ❌ 취약한 수도 코드: 사용자 입력으로 함수 동적 호출
FUNCTION call_api(request):
    function_name = request.body["function_name"]

    // 사용자가 전달한 함수명을 검증 없이 실행
    EXECUTE(function_name + "()")
    RETURN success_page
```

> **⚠️ 주의:** AI 도구에 "사용자가 입력한 수식을 계산해주는 기능 만들어줘"라고 요청하면 `eval()`을 사용하는 코드가 높은 확률로 생성됩니다. 이는 매우 위험합니다.

### ✅ 안전한 수도 코드

```pseudocode
// ✅ 안전한 수도 코드: 화이트리스트 기반 함수 실행 제한
ALLOWED_FUNCTIONS = ["get_friends_list", "get_address", "get_phone_number"]

FUNCTION call_api(request):
    function_name = request.body["function_name"]

    IF function_name NOT IN ALLOWED_FUNCTIONS:
        RETURN error_page("허용되지 않은 함수입니다.")

    EXECUTE(function_name + "()")
    RETURN success_page

// ✅ 가장 안전한 수도 코드: eval() 자체를 사용하지 않기
FUNCTION calculate(request):
    expression = request.body["expression"]

    TRY:
        // 안전한 수식 파서를 사용합니다 (리터럴 표현식만 허용)
        result = SAFE_LITERAL_EVAL(expression)
        RETURN result
    CATCH ParseError:
        RETURN error_page("올바른 값을 입력해주세요.")
```

> **💡 팁:** 수식 계산이 필요한 경우 안전한 수식 파서 라이브러리를 사용하십시오. `eval()` 계열 함수는 가능한 한 코드에서 완전히 제거하는 것이 최선입니다.

### 💬 AI에게 요청할 프롬프트

```text
다음 기능을 구현해주세요:
- 사용자가 입력한 수학 수식을 계산하는 API
- eval(), exec() 등 동적 코드 실행 함수를 절대 사용하지 말 것
- 안전한 수식 파서 라이브러리를 사용할 것 (예: Python의 ast.literal_eval, numexpr 또는 JavaScript의 math.js)
- 허용되지 않은 입력에 대해 명확한 에러 메시지를 반환할 것
```

---

## 3-2. 운영체제 명령어 삽입(OS Command Injection)

### 개요

운영체제 명령어 삽입(OS Command Injection)은 사용자 입력값이 시스템 명령어의 일부로 사용되어, 공격자가 의도하지 않은 운영체제 명령을 실행할 수 있는 취약점입니다.

시스템 명령어 실행 함수(`os.system()`, `subprocess`, `Runtime.exec()`, `child_process.exec()` 등)를 사용할 때, 파일 처리, 외부 프로그램 연동 등의 기능을 구현하면 이 취약점에 노출되기 쉽습니다.

### 왜 위험한가

공격자가 시스템 명령어를 주입하면 서버의 운영체제 수준에서 명령이 실행됩니다. 특수문자 `|`, `;`, `&`, `` ` `` 등을 사용하면 여러 명령어를 연결할 수 있습니다:

```text
# 원래 의도: 날짜를 인자로 백업 실행
backup.sh 2024-01-01

# 공격자 입력: 2024-01-01; cat /etc/passwd
# 실제 실행: backup.sh 2024-01-01; cat /etc/passwd
```

### ❌ 취약한 수도 코드

```pseudocode
// ❌ 취약한 수도 코드: 외부 입력값을 시스템 명령에 직접 사용
FUNCTION execute_command(request):
    app_name = request.body["app_name"]

    // 입력 파라미터를 제한하지 않아 모든 프로그램이 실행될 수 있습니다
    SYSTEM.execute(app_name)
    RETURN success_page

// ❌ 취약한 수도 코드: 쉘 모드로 명령 실행
FUNCTION run_backup(request):
    date = request.body["date"]

    // 쉘을 통해 명령을 실행하면 명령어 연결이 가능합니다
    command = "backup.sh " + date
    SYSTEM.shell_execute(command)
    RETURN success_page
```

### ✅ 안전한 수도 코드

```pseudocode
// ✅ 안전한 수도 코드: 화이트리스트로 실행 가능한 프로그램 제한
ALLOWED_PROGRAMS = ["notepad", "calc", "backup"]

FUNCTION execute_command(request):
    app_name = request.body["app_name"]

    IF app_name NOT IN ALLOWED_PROGRAMS:
        RETURN error_page("허용되지 않은 프로그램입니다.")

    SYSTEM.execute(app_name)
    RETURN success_page

// ✅ 안전한 수도 코드: 특수문자 필터링 + 배열 형태 인자 전달
FUNCTION run_backup(request):
    date = request.body["date"]

    // 명령어 연결에 사용되는 특수문자를 필터링합니다
    FOR EACH char IN ["|", ";", "&", ":", ">", "<", "`", "\\", "!"]:
        date = date.replace(char, "")

    // 쉘을 거치지 않고, 명령과 인자를 배열로 직접 전달합니다
    SYSTEM.execute_direct(["backup.sh", date])
    RETURN success_page
```

### 💬 AI에게 요청할 프롬프트

```text
다음 기능을 구현해주세요:
- 날짜를 입력받아 백업 스크립트를 실행하는 API
- 시스템 명령 실행 시 shell=True 또는 쉘 모드를 사용하지 말 것
- 명령어와 인자를 배열(리스트) 형태로 분리하여 전달할 것
- 입력값에서 |, ;, &, `, \\ 등 명령어 연결 특수문자를 필터링할 것
- 가능하다면 시스템 명령 대신 언어 내장 라이브러리로 대체할 것
```

### 체크포인트

- [ ] 시스템 명령 실행 시 쉘 모드(shell=True)를 사용하고 있지 않은가?
- [ ] 사용자 입력이 명령어의 일부로 사용된다면 특수문자 필터링이 적용되어 있는가?
- [ ] 시스템 명령어 호출 대신 언어 내장 라이브러리로 대체할 수 있는가?

---

## 3-3. XML 삽입(XML Injection)

### 개요

XML 삽입(XML Injection)은 XQuery 또는 XPath 쿼리문에 검증되지 않은 외부 입력값이 포함되어, 공격자가 쿼리 구조를 변경하고 허가되지 않은 데이터에 접근할 수 있는 보안약점입니다.

### 왜 위험한가

XML 기반 데이터 조회에서 XPath를 사용할 때, SQL 삽입과 동일한 원리로 쿼리가 변조될 수 있습니다:

```xpath
# 원래 의도된 쿼리
/collection/users/user[@name='kim']/home/text()

# 공격자가 name에 ' or '1'='1 입력 시
/collection/users/user[@name='' or '1'='1']/home/text()
```

### ❌ 취약한 수도 코드

```pseudocode
// ❌ 취약한 수도 코드: XPath 쿼리에 문자열 결합 사용
FUNCTION parse_xml(request):
    user_name = request.body["user_name"]
    tree = XML.parse("user.xml")

    // 검증되지 않은 입력값을 문자열 결합으로 쿼리에 포함합니다
    query = "/collection/users/user[@name='" + user_name + "']/home/text()"
    elements = tree.xpath(query)
    RETURN elements
```

### ✅ 안전한 수도 코드

```pseudocode
// ✅ 안전한 수도 코드: XPath 파라미터 바인딩 사용
FUNCTION parse_xml(request):
    user_name = request.body["user_name"]
    tree = XML.parse("user.xml")

    // 외부 입력값을 파라미터로 바인딩하여 사용합니다
    query = "/collection/users/user[@name = $paramname]/home/text()"
    elements = tree.xpath(query, paramname=user_name)
    RETURN elements
```

### 💬 AI에게 요청할 프롬프트

```text
다음 기능을 구현해주세요:
- XML 파일에서 사용자 정보를 검색하는 기능
- XPath 쿼리에 사용자 입력을 직접 문자열 결합하지 말 것
- 반드시 XPath 파라미터 바인딩($변수명) 사용
- 가능하다면 XML 대신 JSON 형식 사용을 검토할 것
```

---

## 3-4. 포맷 스트링 삽입(Format String Injection)

### 개요

포맷 스트링 삽입(Format String Injection)은 문자열 포매팅 기능을 사용할 때, 사용자 입력값이 포맷 문자열 자체에 포함되어 의도하지 않은 정보가 노출되는 취약점입니다.

### 왜 위험한가

포맷 문자열을 통해 객체의 속성에 접근하는 기능을 악용하면 서버의 내부 정보를 탈취할 수 있습니다. 사용자가 포맷 문자열 자체를 제어할 수 있으면 시스템 내부 변수, 비밀키 등이 노출될 수 있습니다.

### ❌ 취약한 수도 코드

```pseudocode
// ❌ 취약한 수도 코드: 사용자 입력을 포맷 문자열 자체로 사용
FUNCTION greeting(request):
    template = request.body["template"]

    // 사용자 입력이 포맷 문자열이 되면 내부 정보에 접근할 수 있습니다
    message = FORMAT_STRING(template, user=request.user)
    RETURN message

// ❌ 취약한 수도 코드: eval()과 포맷 문자열의 조합
FUNCTION render_message(request):
    user_input = request.body["input"]
    message = EVAL("FORMAT('" + user_input + "')")  // 매우 위험!
    RETURN message
```

### ✅ 안전한 수도 코드

```pseudocode
// ✅ 안전한 수도 코드: 포맷 문자열을 코드에 고정
FUNCTION greeting(request):
    name = request.body["name"]

    // 포맷 문자열은 코드에서 고정하고, 사용자 입력은 인자로만 전달합니다
    message = FORMAT_STRING("안녕하세요, {name}님!", name=name)
    RETURN message

// ✅ 안전한 수도 코드: 템플릿 엔진 활용
FUNCTION greeting(request):
    name = request.body["name"]

    // 템플릿 엔진에서 변수를 렌더링하면 자동으로 이스케이프됩니다
    RETURN render_template("greeting.html", name=name)
```

### 💬 AI에게 요청할 프롬프트

```text
다음 기능을 구현해주세요:
- 사용자 이름을 포함한 인사 메시지 생성 API
- 포맷 문자열(템플릿)은 코드에 고정할 것 (사용자가 제어 불가)
- 사용자 입력은 포맷 인자(argument)로만 전달할 것
- eval()과 포맷 문자열의 조합을 절대 사용하지 말 것
- 가능하면 프레임워크의 템플릿 엔진을 사용할 것
```

---

# Chapter 04. 웹 요청을 노리는 공격

## 4-1. 크로스사이트 스크립트(XSS)

### 개요

크로스사이트 스크립트(Cross-Site Scripting, XSS)는 웹 보안에서 가장 빈번하게 발생하는 취약점 중 하나입니다. 공격자가 웹 애플리케이션에 악성 스크립트(Script)를 삽입하여, 해당 페이지를 방문하는 다른 사용자의 브라우저에서 악성 코드가 실행되도록 만드는 공격입니다.

### 왜 위험한가

XSS 공격이 성공하면 공격자는 피해자의 브라우저에서 자바스크립트(JavaScript)를 실행할 수 있습니다:

- **세션 탈취**: 로그인 세션 쿠키를 훔쳐 계정을 장악합니다
- **키로깅(Keylogging)**: 사용자의 키보드 입력을 기록하여 비밀번호를 탈취합니다
- **피싱**: 가짜 로그인 폼을 삽입하여 인증 정보를 수집합니다
- **웹사이트 변조**: 페이지 내용을 임의로 수정하여 가짜 정보를 표시합니다

XSS 공격은 세 가지 유형으로 분류됩니다:

- **반사형 XSS(Reflected XSS)**: 악성 스크립트가 URL에 포함되어 서버 응답에 반사되는 방식
- **저장형 XSS(Stored XSS)**: 악성 스크립트가 데이터베이스에 저장되어 모든 방문자에게 영향
- **DOM 기반 XSS(DOM XSS)**: 클라이언트 측 JavaScript에서 DOM 조작으로 발생

### ❌ 취약한 수도 코드

```pseudocode
// ❌ 취약한 수도 코드: 출력 이스케이프 비활성화
FUNCTION profile_link(request):
    profile_url = request.body["profile_url"]
    profile_name = request.body["profile_name"]
    link_html = '<a href="' + profile_url + '">' + profile_name + '</a>'

    // 이스케이프를 비활성화하면 XSS 공격에 노출됩니다
    MARK_AS_SAFE(link_html)  // 프레임워크의 자동 이스케이프를 해제
    RETURN render_page("profile", link=link_html)

// ❌ 취약한 수도 코드: 템플릿에서 자동 이스케이프 해제
TEMPLATE profile.html:
    DISABLE_AUTO_ESCAPE:
        OUTPUT content          // 이스케이프 없이 출력 — XSS 취약!
    OUTPUT content | SAFE       // safe 필터도 이스케이프 해제

// ❌ 취약한 수도 코드: JavaScript DOM에서 innerHTML 사용
SCRIPT:
    keyword = URL.get_param("q")
    // innerHTML은 HTML을 파싱하므로 스크립트가 실행될 수 있습니다
    ELEMENT("search-result").innerHTML = "검색어: " + keyword
```

> **⚠️ 주의:** AI 도구에 "HTML 태그가 그대로 보여야 해"라고 요청하면 이스케이프를 비활성화하는 코드가 생성될 수 있습니다. 이는 XSS 보호를 완전히 해제하는 것이므로 매우 위험합니다.

### ✅ 안전한 수도 코드

```pseudocode
// ✅ 안전한 수도 코드: 프레임워크의 자동 이스케이프 유지
FUNCTION profile_link(request):
    profile_url = request.body["profile_url"]
    profile_name = request.body["profile_name"]

    // 이스케이프를 해제하지 않으면 프레임워크가 자동으로 처리합니다
    RETURN render_page("profile", url=profile_url, name=profile_name)

// ✅ 안전한 수도 코드: 서버 측에서 HTML 이스케이프 처리
FUNCTION search(request):
    keyword = request.body["keyword"]

    // HTML 특수문자를 엔티티 코드로 변환합니다
    // & → &amp;  < → &lt;  > → &gt;  " → &quot;  ' → &#x27;
    safe_keyword = HTML.escape(keyword)
    RETURN render_page("search", keyword=safe_keyword)

// ✅ 안전한 수도 코드: JavaScript에서 textContent 사용
SCRIPT:
    keyword = URL.get_param("q")
    // textContent는 HTML을 파싱하지 않으므로 XSS에 안전합니다
    ELEMENT("search-result").textContent = "검색어: " + keyword
```

### 💬 AI에게 요청할 프롬프트

```text
다음 기능을 구현해주세요:
- 사용자가 입력한 검색어를 결과 페이지에 표시하는 기능
- 모든 사용자 입력은 HTML 출력 전 반드시 이스케이프(Escape) 처리할 것
- mark_safe(), | safe, autoescape off 등 이스케이프 비활성화를 사용하지 말 것
- JavaScript에서 innerHTML 대신 textContent 또는 createElement()를 사용할 것
- 리치 텍스트가 필요한 경우 서버 측 HTML 정화(Sanitization) 라이브러리 적용
```

---



> **[참고 다이어그램] XSS 3가지 유형 비교도**

# XSS 3가지 유형 비교도

## ① 저장형 XSS (Stored XSS)

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

## ② 반사형 XSS (Reflected XSS)

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

## ③ DOM 기반 XSS (DOM-based XSS)

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

## 세 유형 비교 요약

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


---

## 4-2. 크로스사이트 요청 위조(CSRF)

### 개요

크로스사이트 요청 위조(Cross-Site Request Forgery, CSRF)는 사용자가 인지하지 못한 상황에서, 공격자가 의도한 행위(데이터 수정, 삭제, 등록 등)를 사용자 명의로 수행하게 만드는 공격입니다.

### 왜 위험한가

사용자가 웹사이트에 로그인한 상태에서 공격자가 만든 악성 페이지를 방문하면, 해당 페이지에서 사용자의 인증 정보(쿠키)를 이용하여 원래 사이트에 요청을 보냅니다. 서버는 이 요청이 사용자 본인의 의도인지 구분할 수 없습니다.

### ❌ 취약한 수도 코드

```pseudocode
// ❌ 취약한 수도 코드: CSRF 보호 미들웨어 비활성화
CONFIG middleware_list:
    SessionMiddleware           // 세션 관리
    // CsrfMiddleware           // CSRF 미들웨어가 주석 처리됨!
    AuthenticationMiddleware    // 인증 관리

// ❌ 취약한 수도 코드: 특정 뷰에서 CSRF 보호 해제
@CSRF_EXEMPT    // 이 뷰만 CSRF 보호를 해제합니다
FUNCTION pay_to_point(request):
    user_id = request.body["user_id"]
    pay = request.body["pay"]
    RETURN process_payment(user_id, pay)

// ❌ 취약한 수도 코드: 폼에 CSRF 토큰 누락
FORM action="/update" method="POST":
    // CSRF 토큰이 없습니다!
    INPUT type="text" name="email"
    BUTTON "수정하기"
```

> **⚠️ 주의:** AI 도구가 "403 Forbidden 에러가 나요"라는 질문에 대해 CSRF 보호를 비활성화하라고 답변하는 경우가 있습니다. 이는 문제를 해결하는 것이 아니라 보안 기능을 무력화하는 것입니다.

### ✅ 안전한 수도 코드

```pseudocode
// ✅ 안전한 수도 코드: CSRF 미들웨어 활성화
CONFIG middleware_list:
    SessionMiddleware
    CsrfMiddleware             // CSRF 미들웨어 반드시 활성화
    AuthenticationMiddleware

// ✅ 안전한 수도 코드: CSRF 토큰을 폼에 포함
FORM action="/update" method="POST":
    HIDDEN_INPUT name="csrf_token" value=GENERATE_CSRF_TOKEN()
    INPUT type="text" name="email"
    BUTTON "수정하기"

// ✅ 안전한 수도 코드: AJAX 요청 시 CSRF 토큰 포함
FUNCTION ajax_request(url, data):
    csrf_token = GET_CSRF_TOKEN_FROM_COOKIE()
    headers = {"X-CSRF-Token": csrf_token}
    RETURN HTTP.post(url, data, headers)
```

### 💬 AI에게 요청할 프롬프트

```text
다음 기능을 구현해주세요:
- 회원 정보 수정 폼과 처리 API
- 프레임워크의 CSRF 보호 미들웨어를 반드시 활성화할 것
- 모든 POST 폼에 CSRF 토큰을 포함할 것
- @csrf_exempt 또는 CSRF 비활성화를 사용하지 말 것
- AJAX 요청 시에도 CSRF 토큰을 헤더에 포함할 것
```

---



> **[참고 다이어그램] CSRF 공격 시퀀스**

# CSRF 공격 시퀀스

## 공격 흐름 전체도

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

## 단계별 상세 설명

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

## ✅ 방어: CSRF 토큰 적용 시

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


---

## 4-3. 서버사이드 요청 위조(SSRF)

### 개요

서버사이드 요청 위조(Server-Side Request Forgery, SSRF)는 공격자가 서버 측에서 다른 서버로 보내는 요청을 조작하여, 내부 네트워크의 자원에 접근하는 공격입니다.

### 왜 위험한가

SSRF는 공격자가 서버의 신뢰된 네트워크 위치를 악용하는 공격입니다:

- **내부 시스템 접근**: 외부에서 접근할 수 없는 관리자 페이지에 접근
- **클라우드 메타데이터 탈취**: AWS/GCP/Azure 인스턴스의 인증 키 획득
- **내부 파일 열람**: `file:///etc/passwd`로 서버 파일 시스템에 접근

### ❌ 취약한 수도 코드

```pseudocode
// ❌ 취약한 수도 코드: 사용자 입력 URL로 HTTP 요청
FUNCTION call_api(request):
    url = request.body["address"]

    // 사용자가 입력한 주소를 검증 없이 HTTP 요청을 보냅니다
    result = HTTP.get(url)
    RETURN result
```

### ✅ 안전한 수도 코드

```pseudocode
// ✅ 안전한 수도 코드: 허용 URL 화이트리스트 적용
ALLOWED_URLS = [
    "https://api.example.com/v1/public",
    "https://data.example.com/feed",
]

FUNCTION call_api(request):
    url = request.body["address"]

    IF url NOT IN ALLOWED_URLS:
        RETURN error_page("허용되지 않은 서버입니다.")

    result = HTTP.get(url, timeout=5)
    RETURN result

// ✅ 안전한 수도 코드: URL 파싱 후 내부 네트워크 차단
BLOCKED_NETWORKS = ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16",
                    "169.254.0.0/16", "127.0.0.0/8"]

FUNCTION safe_request(url):
    parsed = URL.parse(url)

    // 위험한 프로토콜 차단
    IF parsed.scheme NOT IN ["http", "https"]:
        THROW ERROR "허용되지 않은 프로토콜입니다."

    // 내부 네트워크 IP 차단
    ip = DNS.resolve(parsed.hostname)
    FOR EACH network IN BLOCKED_NETWORKS:
        IF ip IN network:
            THROW ERROR "내부 네트워크 접근은 허용되지 않습니다."

    RETURN HTTP.get(url, timeout=5)
```

### 💬 AI에게 요청할 프롬프트

```text
다음 기능을 구현해주세요:
- 외부 URL의 콘텐츠를 가져오는 API 엔드포인트
- 허용된 URL 목록(화이트리스트)으로 요청 대상을 제한할 것
- file://, gopher:// 등 위험한 프로토콜을 차단할 것
- 내부 네트워크 IP 대역(10.x, 172.16.x, 192.168.x, 127.x)을 차단할 것
- 클라우드 메타데이터 IP(169.254.169.254)를 반드시 차단할 것
- 요청 타임아웃을 설정할 것
```

---



> **[참고 다이어그램] SSRF 공격 흐름도**

# SSRF 공격 흐름도

## ❌ 취약한 흐름 (URL 검증 없음)

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

## 공격 대상별 위험도

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

## ✅ 안전한 흐름 (URL 화이트리스트 적용)

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

## 방어 체크리스트

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


---

## 4-4. HTTP 응답 분할(HTTP Response Splitting)

### 개요

HTTP 응답 분할(HTTP Response Splitting)은 HTTP 응답 헤더에 사용자 입력값이 포함될 때, 해당 입력에 개행문자(CR: `\r`, LF: `\n`)가 존재하면 HTTP 응답이 분리되는 취약점입니다.

### ❌ 취약한 수도 코드

```pseudocode
// ❌ 취약한 수도 코드: 외부 입력을 응답 헤더에 직접 사용
FUNCTION route(request):
    content_type = request.body["content-type"]

    response = NEW HttpResponse()
    response.headers["Content-Type"] = content_type  // 개행문자 삽입 가능!
    RETURN response
```

### ✅ 안전한 수도 코드

```pseudocode
// ✅ 안전한 수도 코드: 개행문자 제거
FUNCTION route(request):
    content_type = request.body["content-type"]

    // 응답 헤더에 포함될 수 있는 개행문자를 제거합니다
    content_type = content_type.replace("\r", "")
    content_type = content_type.replace("\n", "")

    response = NEW HttpResponse()
    response.headers["Content-Type"] = content_type
    RETURN response
```

### 💬 AI에게 요청할 프롬프트

```text
다음 기능을 구현해주세요:
- HTTP 응답 헤더에 사용자 입력을 포함하는 기능
- 헤더에 포함되는 모든 값에서 \r, \n 개행문자를 제거할 것
- 가능하면 사용자 입력을 헤더에 직접 사용하지 않도록 설계할 것
- 프레임워크/라이브러리를 최신 버전으로 유지할 것
```

---

# Chapter 05. 파일과 URL을 노리는 공격

## 5-1. 경로 조작 및 자원 삽입(Path Traversal)

### 개요

경로 조작(Path Traversal)은 검증되지 않은 외부 입력값을 사용하여 파일 시스템의 경로를 조작함으로써, 공격자가 허가되지 않은 파일이나 디렉터리에 접근할 수 있는 보안약점입니다.

### 왜 위험한가

공격자가 파일명에 `../`(상위 디렉터리 이동) 문자열을 삽입하면, 서버의 의도된 디렉터리를 벗어나 시스템 파일에 접근할 수 있습니다:

```text
# 정상적인 요청
GET /download?file=report.txt
→ 서버에서 열리는 파일: /var/www/uploads/report.txt

# 공격자의 요청
GET /download?file=../../../../etc/passwd
→ 서버에서 열리는 파일: /etc/passwd
```

### ❌ 취약한 수도 코드

```pseudocode
// ❌ 취약한 수도 코드: 외부 입력값을 파일 경로에 직접 사용
FUNCTION get_file(request):
    filename = request.body["request_file"]
    extension = GET_EXTENSION(filename).lowercase()

    IF extension NOT IN [".txt", ".csv"]:
        RETURN error_page("파일을 열 수 없습니다.")

    // 확장자만 검증하고 경로 조작 문자열은 검증하지 않습니다
    // ../../../../etc/passwd.txt 같은 입력이 가능합니다
    data = FILE.read(filename)
    RETURN data
```

### ✅ 안전한 수도 코드

```pseudocode
// ✅ 안전한 수도 코드: 기본 디렉터리(Base Directory) 제한
CONSTANT BASE_DIR = "/var/www/uploads"

FUNCTION get_file(request):
    filename = request.body["request_file"]
    extension = GET_EXTENSION(filename).lowercase()

    IF extension NOT IN [".txt", ".csv"]:
        RETURN error_page("파일을 열 수 없습니다.")

    // 절대 경로를 생성하고, 기본 디렉터리 내에 있는지 확인합니다
    safe_path = RESOLVE_REAL_PATH(JOIN_PATH(BASE_DIR, filename))

    IF NOT safe_path.starts_with(RESOLVE_REAL_PATH(BASE_DIR)):
        RETURN error_page("접근이 허용되지 않은 경로입니다.")

    TRY:
        data = FILE.read(safe_path)
        RETURN data
    CATCH FileNotFound:
        RETURN error_page("파일을 찾을 수 없습니다.")
```

> **💡 팁:** `RESOLVE_REAL_PATH()`는 심볼릭 링크와 `../` 등의 경로 조작을 모두 해석하여 실제 절대 경로를 반환합니다. 이 결과가 허용된 기본 디렉터리로 시작하는지 확인하면 경로 조작 공격을 효과적으로 방어할 수 있습니다.

### 💬 AI에게 요청할 프롬프트

```text
다음 기능을 구현해주세요:
- 파일 다운로드 API 엔드포인트
- 기본 디렉터리(Base Directory)를 설정하고, 해당 디렉터리 외부 접근을 차단할 것
- 파일 경로에서 ../, ..\\ 등 경로 조작 문자를 방어할 것
- realpath/resolve 등으로 실제 경로를 해석한 후 범위를 검증할 것
- 허용할 파일 확장자를 화이트리스트로 관리할 것
```

---

## 5-2. 위험한 형식 파일 업로드(Unrestricted File Upload)

### 개요

파일 업로드 기능에서 서버 측 실행 가능한 스크립트 파일의 업로드를 허용하면, 공격자가 웹 쉘(Web Shell)을 업로드하여 서버를 완전히 장악할 수 있습니다.

### 왜 위험한가

확장자만 검사하는 것으로는 부족합니다. 공격자는 이중 확장자(`malware.py.jpg`)를 사용하거나, 실제 내용은 스크립트이면서 확장자만 `.jpg`로 변경하는 방법을 사용합니다.

### ❌ 취약한 수도 코드

```pseudocode
// ❌ 취약한 수도 코드: 파일 검증 없이 업로드 허용
FUNCTION file_upload(request):
    file = request.files["upload_file"]

    // 파일의 크기, 개수, 확장자, 내용을 전혀 검증하지 않습니다
    SAVE_FILE(file, path="uploads/" + file.name)
    RETURN success_page
```

### ✅ 안전한 수도 코드

```pseudocode
// ✅ 안전한 수도 코드: 다중 검증 적용
CONSTANT MAX_FILE_COUNT = 5
CONSTANT MAX_FILE_SIZE = 5 * 1024 * 1024  // 5MB
CONSTANT ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif"]
CONSTANT ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "image/gif"]

FUNCTION file_upload(request):
    files = request.files

    // 1단계: 파일 개수 제한
    IF files.count == 0 OR files.count > MAX_FILE_COUNT:
        RETURN error_page("파일 개수 초과")

    saved_files = []
    FOR EACH file IN files:
        // 2단계: MIME 타입 검사
        IF file.content_type NOT IN ALLOWED_MIME_TYPES:
            RETURN error_page("허용되지 않은 파일 형식입니다.")

        // 3단계: 파일 크기 제한
        IF file.size > MAX_FILE_SIZE:
            RETURN error_page("파일 크기가 초과되었습니다.")

        // 4단계: 파일 확장자 검사
        extension = GET_EXTENSION(file.name).lowercase()
        IF extension NOT IN ALLOWED_EXTENSIONS:
            RETURN error_page("허용되지 않은 확장자입니다.")

        // 5단계: 파일명을 랜덤으로 변경하여 저장합니다
        safe_name = GENERATE_UUID() + extension
        SAVE_FILE(file, path="uploads/" + safe_name)
        saved_files.append(safe_name)

    RETURN success_page(saved_files)
```

> **💡 팁:** 확장자와 Content-Type은 공격자가 쉽게 변조할 수 있습니다. 파일의 첫 몇 바이트에 위치한 매직 바이트(Magic Bytes, 파일 시그니처)를 확인하면 실제 파일 형식을 보다 정확하게 판별할 수 있습니다.

### 💬 AI에게 요청할 프롬프트

```text
다음 기능을 구현해주세요:
- 이미지 파일 업로드 API
- 허용할 확장자를 화이트리스트로 관리 (jpg, png, gif만 허용)
- MIME 타입 검증을 추가할 것
- 파일 크기 제한(5MB)과 업로드 개수 제한(5개)을 설정할 것
- 업로드된 파일명을 UUID로 변경하여 저장할 것
- 업로드 디렉터리를 웹 루트 외부에 배치할 것
- 가능하면 매직 바이트(파일 시그니처) 검증도 추가할 것
```

---

## 5-3. 신뢰되지 않는 URL 자동 연결(Open Redirect)

### 개요

오픈 리다이렉트(Open Redirect)는 사용자 입력값을 외부 사이트 주소로 사용하여 리다이렉트하는 경우, 공격자가 피해자를 피싱(Phishing) 사이트로 유도할 수 있는 취약점입니다.

### ❌ 취약한 수도 코드

```pseudocode
// ❌ 취약한 수도 코드: 사용자 입력 URL로 직접 리다이렉트
FUNCTION redirect_url(request):
    url = request.body["url"]

    // 사용자 입력값을 검증 없이 리다이렉트에 사용합니다
    RETURN REDIRECT(url)
```

### ✅ 안전한 수도 코드

```pseudocode
// ✅ 안전한 수도 코드: 화이트리스트 또는 상대 URL만 허용
ALLOWED_URLS = ["/notice", "/dashboard", "/profile"]

FUNCTION redirect_url(request):
    url = request.body["url"]

    // 방법 1: 화이트리스트에 포함된 URL만 허용
    IF url NOT IN ALLOWED_URLS:
        RETURN error_page("허용되지 않는 주소입니다.")

    RETURN REDIRECT(url)

// ✅ 안전한 수도 코드: 외부 URL 차단
FUNCTION safe_redirect(request):
    url = request.body["url"]
    parsed = URL.parse(url)

    // scheme(http, https)이나 netloc(도메인)이 포함되면 외부 URL입니다
    IF parsed.scheme OR parsed.netloc:
        RETURN error_page("외부 URL로는 이동할 수 없습니다.")

    RETURN REDIRECT(url)
```

### 💬 AI에게 요청할 프롬프트

```text
다음 기능을 구현해주세요:
- 로그인 후 원래 페이지로 리다이렉트하는 기능
- 리다이렉트 대상을 상대 경로(Relative URL)로 제한할 것
- 외부 도메인으로의 리다이렉트를 차단할 것
- URL 파싱 후 scheme, netloc이 있으면 거부할 것
- 또는 허용 URL 화이트리스트를 사용할 것
```

---

## 5-4. 부적절한 XML 외부 개체 참조(XXE)

### 개요

XML 외부 엔티티(XML External Entity, XXE) 공격은 XML 문서에 포함된 DTD의 외부 엔티티 참조 기능을 악용하여, 서버의 파일을 읽거나 내부 네트워크에 접근하는 공격입니다.

### 왜 위험한가

공격자는 악성 XML을 전송하여 서버 파일을 읽을 수 있습니다:

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<foo>&xxe;</foo>
```

### ❌ 취약한 수도 코드

```pseudocode
// ❌ 취약한 수도 코드: 외부 엔티티 처리가 활성화됨
FUNCTION parse_xml(request):
    parser = XML.create_parser()
    parser.set_feature("external_entities", TRUE)  // 외부 엔티티 처리 활성화!
    document = parser.parse(request.body)
    RETURN process(document)
```

### ✅ 안전한 수도 코드

```pseudocode
// ✅ 안전한 수도 코드: 외부 엔티티 처리 비활성화
FUNCTION parse_xml(request):
    parser = XML.create_parser()
    parser.set_feature("external_entities", FALSE)   // 외부 엔티티 비활성화
    parser.set_feature("network_access", FALSE)       // 네트워크 접근 차단
    parser.set_feature("dtd_validation", FALSE)       // DTD 검증 비활성화
    parser.set_feature("load_dtd", FALSE)             // DTD 로드 비활성화
    document = parser.parse(request.body)
    RETURN process(document)
```

> **💡 팁:** 가능하다면 XML 대신 JSON 형식을 사용하는 것을 권장합니다. JSON은 외부 엔티티 참조 기능이 없으므로 XXE 공격 자체가 불가능합니다.

### 💬 AI에게 요청할 프롬프트

```text
다음 기능을 구현해주세요:
- XML 데이터를 파싱하는 API 엔드포인트
- XML 파서의 외부 엔티티(External Entity) 처리를 반드시 비활성화할 것
- DTD 로드 및 검증을 비활성화할 것
- 네트워크를 통한 외부 문서 조회를 차단할 것
- 가능하다면 XML 대신 JSON 형식을 사용할 것
```

---

# Chapter 06. 데이터 타입과 보안 결정을 노리는 공격

## 6-1. 정수형 오버플로우(Integer Overflow)

### 개요

정수형 오버플로우(Integer Overflow)는 변수가 저장할 수 있는 범위를 넘어선 값이 할당될 때, 실제 저장되는 값이 의도치 않게 아주 작은 수나 음수가 되어 프로그램이 예기치 않게 동작하는 취약점입니다.

일부 언어(Python 등)는 기본 정수형에서 오버플로우가 발생하지 않지만, C/C++ 기반 라이브러리(numpy, 데이터 처리 라이브러리 등)를 사용하거나, 고정 크기 정수형을 사용하는 언어(Java, C#, Go 등)에서는 오버플로우에 주의해야 합니다.

### 왜 위험한가

오버플로우가 발생하면:

- **금액 계산 오류**: 큰 금액의 연산에서 음수가 되어 결제 로직에 이상 발생
- **반복문 무한루프**: 카운터 변수의 오버플로우로 종료 조건을 만족하지 못하는 경우
- **메모리 할당 오류**: 할당할 크기가 0이나 음수가 되어 보안 문제 유발

### ❌ 취약한 수도 코드

```pseudocode
// ❌ 취약한 수도 코드: 범위 검증 없이 수치 연산
FUNCTION calculate_price(request):
    quantity = TO_INTEGER(request.body["quantity"])
    unit_price = TO_INTEGER(request.body["unit_price"])

    // 매우 큰 수를 입력하면 오버플로우 발생 가능
    // 고정 크기 정수형에서 total이 음수가 될 수 있습니다
    total = FIXED_INT64(quantity) * FIXED_INT64(unit_price)
    RETURN render_page("price", total=total)
```

### ✅ 안전한 수도 코드

```pseudocode
// ✅ 안전한 수도 코드: 입력값 범위 제한
CONSTANT MAX_QUANTITY = 10000
CONSTANT MAX_PRICE = 100000000  // 1억

FUNCTION calculate_price(request):
    TRY:
        quantity = TO_INTEGER(request.body["quantity"])
        unit_price = TO_INTEGER(request.body["unit_price"])
    CATCH ValueError:
        RETURN error_page("올바른 숫자를 입력해주세요.")

    // 입력값의 범위를 사전에 제한합니다
    IF quantity < 0 OR quantity > MAX_QUANTITY:
        RETURN error_page("수량 범위를 초과했습니다.")

    IF unit_price < 0 OR unit_price > MAX_PRICE:
        RETURN error_page("가격 범위를 초과했습니다.")

    // 안전한 범위 내에서 계산합니다
    total = quantity * unit_price
    RETURN render_page("price", total=total)
```

### 💬 AI에게 요청할 프롬프트

```text
다음 기능을 구현해주세요:
- 수량과 단가를 입력받아 총액을 계산하는 API
- 모든 수치 입력에 최소/최대 범위 검증을 적용할 것
- 금액 계산은 오버플로우가 발생하지 않는 자료형 사용할 것
- 음수 입력을 거부할 것
- 입력값 파싱 실패 시 명확한 에러 메시지를 반환할 것
```

---

## 6-2. 보안기능 결정에 사용되는 부적절한 입력값

### 개요

보안기능 결정에 사용되는 부적절한 입력값(Reliance on Untrusted Inputs in a Security Decision)은 쿠키(Cookie), 히든 필드(Hidden Field), URL 파라미터 등 클라이언트 측에서 조작 가능한 값을 기반으로 인증이나 인가 같은 보안 결정을 내리는 취약점입니다.

핵심 원칙: **클라이언트에서 오는 모든 데이터는 조작될 수 있습니다.**

### 왜 위험한가

- **쿠키**: 브라우저 개발자 도구나 프록시 도구로 언제든 수정 가능합니다
- **히든 필드**: HTML 소스에서 그대로 노출되며, 요청 시 값을 변경할 수 있습니다
- **URL 파라미터**: 주소창에서 직접 수정 가능합니다

### ❌ 취약한 수도 코드

```pseudocode
// ❌ 취약한 수도 코드: 쿠키로 관리자 여부 판단
FUNCTION reset_password(request):
    // 쿠키는 클라이언트에서 언제든 조작할 수 있습니다!
    user_role = request.cookies["user_role"]

    IF user_role == "admin":
        target_user = request.body["target_user"]
        new_password = generate_temp_password()
        reset_user_password(target_user, new_password)
        RETURN success_page
    RETURN error_page("권한이 없습니다.")

// ❌ 취약한 수도 코드: 히든 필드의 가격으로 결제
FUNCTION checkout(request):
    // 클라이언트에서 가격을 1원으로 변조할 수 있습니다!
    price = TO_INTEGER(request.body["price"])
    product_id = request.body["product_id"]
    process_payment(product_id, price)
    RETURN success_page

// ❌ 취약한 수도 코드: URL 파라미터로 다른 사용자 정보 접근
FUNCTION view_profile(request):
    // /profile?user_id=456 으로 변경하면 다른 사용자 정보를 볼 수 있습니다
    user_id = request.params["user_id"]
    user_data = get_user_info(user_id)
    RETURN render_page("profile", user=user_data)
```

### ✅ 안전한 수도 코드

```pseudocode
// ✅ 안전한 수도 코드: 서버 세션으로 권한 관리
@REQUIRE_LOGIN
@REQUIRE_ROLE("admin")  // 서버 측에서 권한 검증
FUNCTION reset_password(request):
    target_user = request.body["target_user"]
    new_password = generate_temp_password()
    reset_user_password(target_user, new_password)
    RETURN success_page

// ✅ 안전한 수도 코드: 서버에서 가격 조회 후 결제
FUNCTION checkout(request):
    product_id = request.body["product_id"]

    // 가격을 클라이언트에서 받지 않고, 서버 데이터베이스에서 조회합니다
    product = DATABASE.find_product(product_id)
    IF product is NULL:
        RETURN error_page("상품을 찾을 수 없습니다.")

    process_payment(product.id, product.price)
    RETURN success_page

// ✅ 안전한 수도 코드: 인증된 사용자 정보로 접근
@REQUIRE_LOGIN
FUNCTION view_profile(request):
    // URL 파라미터가 아닌, 서버 세션의 인증된 사용자 정보를 사용합니다
    user_data = get_user_info(request.authenticated_user.id)
    RETURN render_page("profile", user=user_data)
```

### 💬 AI에게 요청할 프롬프트

```text
다음 기능을 구현해주세요:
- 관리자 전용 비밀번호 초기화 기능
- 사용자 권한은 반드시 서버 세션/데이터베이스에서 확인할 것
- 쿠키, 히든 필드, URL 파라미터로 권한을 판단하지 말 것
- 프레임워크의 인증/인가 데코레이터 또는 미들웨어를 사용할 것
- 결제 기능에서 가격은 반드시 서버 DB에서 조회할 것
```

---

## 6-3. 메모리 버퍼 오버플로우(Buffer Overflow)

### 개요

메모리 버퍼 오버플로우(Buffer Overflow)는 프로그램이 할당된 메모리 영역을 넘어서 데이터를 쓰는 취약점입니다. C/C++ 같은 저수준 언어에서 주로 발생합니다.

> **💡 팁:** Python, JavaScript, Java, Go 등 메모리를 자동 관리하는 언어에서는 전통적인 버퍼 오버플로우가 발생하지 않습니다. 하지만 C 확장 모듈이나 네이티브 바인딩을 사용할 때는 주의가 필요합니다.

### 체크포인트

- [ ] C 확장 모듈이나 네이티브 바인딩을 직접 작성하지 않았는가?
- [ ] 외부 라이브러리를 호출할 때 입력 크기를 검증하는가?
- [ ] 사용하는 라이브러리를 최신 버전으로 유지하는가?

> **⚠️ 주의:** 바이브 코딩에서 이 취약점을 직접 마주칠 일은 거의 없지만, 의존 라이브러리의 보안 업데이트는 반드시 적용하십시오. 패키지 감사 도구(예: `pip audit`, `npm audit`, `cargo audit`)로 취약한 패키지를 확인할 수 있습니다.


---

# Part 3. 보안 기능 — 수도 코드 편

---

## 7장. 인증과 인가, 그리고 권한 설정

### 7-1. 적절한 인증 없이 중요 기능 허용

#### 개요

인증(Authentication)이란 "당신이 누구인지 확인하는 과정"입니다. 여러분이 웹사이트에 로그인할 때 아이디와 패스워드를 입력하는 것이 가장 대표적인 인증 절차입니다. AI 도구로 웹사이트를 빠르게 만들다 보면, 중요한 기능에 인증 절차를 빠뜨리는 경우가 빈번하게 발생합니다.

"패스워드 변경 페이지를 만들어줘"라고 AI에게 요청하면, AI는 변경 로직은 잘 만들어주지만 **현재 로그인한 사용자인지 확인하는 과정**을 생략하는 경우가 많습니다. 인증 없이 중요 기능이 노출되면, 공격자는 URL만 알면 누구의 패스워드든 변경할 수 있게 됩니다.

#### 왜 위험한가

- **계정 탈취**: 패스워드 변경, 이메일 변경 등의 기능에 인증이 없으면 타인의 계정을 손쉽게 장악할 수 있습니다.
- **데이터 유출**: 관리자 전용 API에 인증이 없으면 전체 사용자 목록, 결제 정보 등이 노출될 수 있습니다.
- **권한 상승**: 일반 사용자가 관리자 기능에 접근하여 시스템 전체를 제어할 수 있습니다.

> **⚠️ 주의:** AI가 생성한 코드에서 인증 데코레이터나 인증 미들웨어가 빠져 있는지 반드시 확인하십시오. AI는 "동작하는 코드"를 우선시하기 때문에 보안 장치를 생략하는 경향이 있습니다.

#### ❌ 취약한 수도 코드

```pseudocode
FUNCTION change_password(request):
    new_password = GET request.body["new_password"]
    user_id = GET request.body["user_id"]

    // 로그인 여부를 확인하지 않음
    // 현재 패스워드 일치 여부도 확인하지 않음
    hashed = HASH_SHA256(new_password)
    UPDATE_DB("users", user_id, password = hashed)

    RETURN SUCCESS("패스워드가 변경되었습니다")
```

이 코드는 두 가지 심각한 문제를 가지고 있습니다. 첫째, 로그인 여부를 확인하지 않으므로 비로그인 상태에서도 접근 가능합니다. 둘째, 현재 패스워드와의 일치 여부를 확인하지 않으므로 URL만 알면 누구든 패스워드를 변경할 수 있습니다.

#### ✅ 안전한 수도 코드

```pseudocode
FUNCTION change_password(request):
    // 1단계: 인증 확인 — 로그인하지 않은 사용자는 즉시 차단
    user = AUTHENTICATE(request.token)
    IF user IS NULL:
        RETURN ERROR(401, "로그인이 필요합니다")

    current_password = GET request.body["current_password"]
    new_password = GET request.body["new_password"]
    confirm_password = GET request.body["confirm_password"]

    // 2단계: 재인증 — 현재 패스워드 확인
    IF NOT VERIFY_PASSWORD(current_password, user.hashed_password):
        RETURN ERROR(403, "현재 패스워드가 일치하지 않습니다")

    // 3단계: 새 패스워드 확인
    IF new_password != confirm_password:
        RETURN ERROR(400, "새 패스워드가 일치하지 않습니다")

    // 4단계: 안전하게 패스워드 변경
    new_hash = HASH_WITH_SALT(new_password)  // bcrypt 또는 argon2
    UPDATE_DB("users", user.id, password = new_hash)

    RETURN SUCCESS("패스워드가 변경되었습니다")
```

#### 💬 AI에게 요청할 프롬프트

```text
로그인한 사용자만 접근 가능한 패스워드 변경 API를 만들어주세요:
- 인증 미들웨어 또는 데코레이터를 반드시 적용할 것
- 현재 패스워드를 확인하는 재인증(Re-authentication) 로직을 포함할 것
- 새 패스워드와 확인 패스워드의 일치 여부를 검증할 것
- user_id는 요청 본문이 아닌 세션/토큰에서 가져올 것
```

#### 체크포인트

- [ ] 모든 API 핸들러에 인증 미들웨어가 적용되어 있는지 확인합니다.
- [ ] 패스워드 변경, 결제, 개인정보 수정 등 중요 기능에는 재인증 로직이 포함되어 있는지 확인합니다.
- [ ] API 엔드포인트의 경우 토큰 기반 인증이 적용되어 있는지 확인합니다.

---



> **[참고 다이어그램] 인증 vs 인가 비교도**

# 다이어그램 5: 인증 vs 인가 비교도

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


---

### 7-2. 부적절한 인가

#### 개요

인가(Authorization)란 "인증된 사용자가 특정 자원이나 기능에 접근할 권한이 있는지 확인하는 과정"입니다. 인증이 "누구인지 확인"이라면, 인가는 "무엇을 할 수 있는지 확인"하는 것입니다.

바이브 코딩에서 흔히 발생하는 실수는 로그인 확인만 하고 **역할(Role) 기반의 권한 확인을 생략**하는 것입니다.

#### 왜 위험한가

- **수평적 권한 상승**: 같은 역할의 다른 사용자 데이터에 접근할 수 있습니다. 예를 들어 A 사용자가 B 사용자의 주문 내역을 조회하는 경우입니다.
- **수직적 권한 상승**: 일반 사용자가 관리자 기능을 실행할 수 있습니다.
- **데이터 변조**: 권한 없는 사용자가 중요 데이터를 수정하거나 삭제할 수 있습니다.

#### ❌ 취약한 수도 코드

```pseudocode
FUNCTION delete_content(request):
    action = GET request.body["action"]
    content_id = GET request.body["content_id"]

    // 사용자의 역할이나 소유권을 확인하지 않음
    IF action == "delete":
        DELETE_FROM_DB("contents", id = content_id)
        RETURN SUCCESS("삭제되었습니다")

    RETURN ERROR(400, "잘못된 요청입니다")
```

#### ✅ 안전한 수도 코드

```pseudocode
FUNCTION delete_content(request):
    // 1단계: 인증 확인
    user = AUTHENTICATE(request.token)
    IF user IS NULL:
        RETURN ERROR(401, "인증이 필요합니다")

    // 2단계: 권한 확인 (역할 기반 접근 제어)
    IF NOT user.has_permission("delete_content"):
        RETURN ERROR(403, "삭제 권한이 없습니다")

    content_id = GET request.body["content_id"]

    // 3단계: 소유권 확인 (관리자가 아닌 경우 본인 콘텐츠만)
    content = FIND_IN_DB("contents", id = content_id)
    IF content IS NULL:
        RETURN ERROR(404, "콘텐츠를 찾을 수 없습니다")

    IF user.role != "admin" AND content.author_id != user.id:
        RETURN ERROR(403, "본인의 콘텐츠만 삭제할 수 있습니다")

    // 4단계: 삭제 수행
    DELETE_FROM_DB("contents", id = content_id)
    RETURN SUCCESS("삭제되었습니다")
```

#### 💬 AI에게 요청할 프롬프트

```text
콘텐츠 삭제 API를 만들어주세요. 다음 권한 규칙을 적용해주세요:
- admin 역할: 모든 콘텐츠 삭제 가능
- 일반 사용자: 본인이 작성한 콘텐츠만 삭제 가능
- 비로그인 사용자: 접근 차단 (401)
- 권한 없는 요청: 403 에러 반환
- URL의 ID 값을 변경해도 다른 사용자의 데이터에 접근할 수 없도록 소유권 검증을 포함할 것
```

#### 체크포인트

- [ ] 모든 API에 "누가 이 기능을 사용할 수 있는가?"가 정의되어 있는지 확인합니다.
- [ ] 데이터 조회/수정/삭제 시 소유권 확인을 수행하는지 확인합니다.
- [ ] URL의 ID 값을 변경하여 다른 사용자의 데이터에 접근할 수 없는지 테스트합니다.

---

### 7-3. 중요한 자원에 대한 잘못된 권한 설정

#### 개요

파일 권한(File Permission)이란 운영체제에서 파일이나 디렉터리에 대해 "누가 읽고, 쓰고, 실행할 수 있는지"를 제어하는 설정입니다. AI는 종종 파일 권한을 `777`(모든 사용자에게 모든 권한 허용)로 설정하는 코드를 생성합니다. 편의성을 위한 것이지만, 보안 관점에서는 매우 위험합니다.

#### 왜 위험한가

- **설정 파일 노출**: 데이터베이스 접속 정보, API 키 등이 포함된 설정 파일을 누구나 읽을 수 있게 됩니다.
- **파일 변조**: 실행 파일이나 라이브러리를 악의적으로 수정할 수 있습니다.
- **악성 코드 실행**: 쓰기 권한이 열린 디렉터리에 악성 스크립트를 업로드하고 실행할 수 있습니다.

#### ❌ 취약한 수도 코드

```pseudocode
FUNCTION write_config():
    // 모든 사용자에게 읽기/쓰기/실행 권한 부여 — 절대 금지!
    SET_FILE_PERMISSION("/app/config/settings.json", "777")

    WRITE_FILE("/app/config/settings.json",
        '{"db_host": "localhost", "db_password": "secret123"}')
```

#### ✅ 안전한 수도 코드

```pseudocode
FUNCTION write_config():
    config_path = "/app/config/settings.json"

    WRITE_FILE(config_path, '{"db_host": "localhost"}')

    // 소유자만 읽기/쓰기 가능 (600)
    SET_FILE_PERMISSION(config_path, "600")

FUNCTION write_executable():
    script_path = "/app/scripts/deploy.sh"

    WRITE_FILE(script_path, '#!/bin/bash\necho "deploying..."')

    // 소유자만 읽기/실행 가능 (500)
    SET_FILE_PERMISSION(script_path, "500")
```

> **💡 팁:** 최소한 이것만 기억하십시오. `600`은 소유자만 읽기/쓰기, `700`은 소유자만 읽기/쓰기/실행, `644`는 소유자 읽기/쓰기 + 나머지 읽기만, `777`은 **절대 사용 금지**입니다.

#### 💬 AI에게 요청할 프롬프트

```text
설정 파일을 생성하는 코드를 만들어주세요:
- 파일 권한은 소유자 전용(600)으로 설정할 것
- 777이나 666 같은 과도한 권한은 절대 사용하지 말 것
- 실행 스크립트는 소유자만 실행 가능하도록(500 또는 700) 설정할 것
- 최소 권한 원칙(Principle of Least Privilege)을 따를 것
```

#### 체크포인트

- [ ] 파일 권한을 설정하는 코드에서 `777` 또는 `666`이 사용된 곳이 없는지 확인합니다.
- [ ] 설정 파일(`.env`, `config.json` 등)의 권한이 소유자 전용(`600`)으로 설정되어 있는지 확인합니다.

> **⚠️ 주의:** AI에게 "파일 권한 오류를 해결해줘"라고 요청하면, AI는 가장 쉬운 해결책인 `chmod 777`을 제안하는 경우가 많습니다. 이는 보안을 완전히 포기하는 것입니다.

---

## 8장. 암호화, 제대로 하고 계십니까

### 8-1. 취약한 암호화 알고리즘 사용

#### 개요

암호화 알고리즘은 중요한 정보를 보호하기 위한 핵심 수단입니다. 그러나 MD5, SHA-1, DES, RC4와 같은 알고리즘은 이미 취약한 것으로 판명되었습니다. AI가 학습한 데이터에 오래된 코드 예제가 다수 포함되어 있으므로, AI는 여전히 이러한 취약한 알고리즘을 사용하는 코드를 생성할 수 있습니다.

#### 왜 위험한가

- **해시 충돌**: MD5와 SHA-1은 서로 다른 입력에서 같은 해시값이 생성되는 충돌이 실제로 발견되었습니다.
- **브루트포스 공격**: DES는 56비트 키를 사용하므로, 현대 컴퓨터로 수 시간 내에 해독 가능합니다.
- **레인보우 테이블 공격**: MD5 해시값은 이미 방대한 테이블이 존재하여 원문을 역추적할 수 있습니다.

#### ❌ 취약한 수도 코드

```pseudocode
FUNCTION encrypt_data(plain_text, key):
    // DES는 56비트 키로 현대 컴퓨터에서 쉽게 해독 가능
    cipher = DES_ENCRYPT(key, mode = "ECB")
    encrypted = cipher.encrypt(plain_text)
    RETURN BASE64_ENCODE(encrypted)

FUNCTION hash_password(password):
    // MD5는 충돌이 발견되어 더 이상 안전하지 않음
    RETURN MD5_HASH(password)
```

#### ✅ 안전한 수도 코드

```pseudocode
FUNCTION encrypt_data(plain_text, key):
    // AES-256 CBC 모드 사용 (키 길이 32바이트 = 256비트)
    iv = GENERATE_RANDOM_BYTES(16)  // 초기화 벡터
    cipher = AES_ENCRYPT(key, mode = "CBC", iv = iv)
    encrypted = cipher.encrypt(PAD(plain_text))
    // IV를 암호문 앞에 결합하여 저장
    RETURN BASE64_ENCODE(iv + encrypted)

FUNCTION decrypt_data(encrypted_text, key):
    raw = BASE64_DECODE(encrypted_text)
    iv = raw[0:16]
    cipher = AES_DECRYPT(key, mode = "CBC", iv = iv)
    decrypted = UNPAD(cipher.decrypt(raw[16:]))
    RETURN decrypted

FUNCTION hash_data(data):
    // SHA-256은 현재 안전한 해시 알고리즘
    RETURN SHA256_HASH(data)
```

> **⚠️ 주의:** ECB 모드는 같은 평문 블록이 항상 같은 암호문을 생성하므로 패턴이 노출됩니다. 반드시 CBC, CTR, GCM 등의 운영 모드를 사용하십시오.

#### 💬 AI에게 요청할 프롬프트

```text
데이터 암호화 함수를 만들어주세요:
- AES-256 알고리즘을 사용할 것 (DES, MD5, SHA-1 사용 금지)
- ECB 모드가 아닌 CBC 또는 GCM 모드를 사용할 것
- 초기화 벡터(IV)는 매번 랜덤으로 생성할 것
- IV는 암호문과 함께 저장할 것
```

#### 체크포인트

- [ ] `DES`, `MD5`, `SHA1`, `RC4` 등 취약한 알고리즘을 사용하는 부분이 없는지 확인합니다.
- [ ] 대칭키 암호화는 AES-128 이상(권장 AES-256)을 사용합니다.
- [ ] ECB 모드 대신 CBC, GCM 등의 안전한 운영 모드를 사용하는지 확인합니다.

---



> **[참고 다이어그램] 암호화 알고리즘 안전/위험 분류표**

# 다이어그램 6: 암호화 알고리즘 안전/위험 분류표

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


---

### 8-2. 암호화되지 않은 중요정보

#### 개요

패스워드, 주민등록번호, 신용카드 번호 등의 중요정보가 평문(Plaintext)으로 저장되거나 전송되면, 데이터베이스 유출이나 네트워크 도청 시 모든 정보가 그대로 노출됩니다. "일단 동작하게 만들고 나중에 암호화를 추가하자"라는 생각은 매우 위험합니다.

#### 왜 위험한가

- **데이터베이스 유출**: 평문으로 저장된 패스워드는 DB 유출 시 즉시 악용됩니다.
- **네트워크 도청**: 평문으로 전송된 정보는 패킷 스니핑으로 가로챌 수 있습니다.
- **법적 책임**: 개인정보보호법에 따라 법적 제재를 받을 수 있습니다.

#### ❌ 취약한 수도 코드

```pseudocode
FUNCTION register_user(db, username, password):
    // 패스워드가 암호화 없이 그대로 저장됨
    DB_INSERT(db, "users",
        username = username,
        password = password   // 평문 저장!
    )

FUNCTION send_user_data(user_data):
    // HTTP(평문)로 개인정보 전송 — 도청 가능
    connection = OPEN_SOCKET("api.example.com", port = 80)
    connection.send(user_data)
```

#### ✅ 안전한 수도 코드

```pseudocode
FUNCTION register_user(db, username, password):
    // 솔트 생성 후 패스워드와 결합하여 해시
    salt = GENERATE_RANDOM_BYTES(32)
    hashed_password = SHA256_HASH(password + salt)

    DB_INSERT(db, "users",
        username = username,
        password = hashed_password,
        salt = salt
    )

FUNCTION send_user_data(user_data):
    // HTTPS를 사용하여 암호화된 채널로 전송
    response = HTTPS_POST(
        url = "https://api.example.com/users",   // HTTP가 아닌 HTTPS
        body = user_data,
        verify_ssl = TRUE   // SSL 인증서 검증 활성화
    )
    RETURN response
```

#### 💬 AI에게 요청할 프롬프트

```text
회원가입 기능을 만들어주세요:
- 패스워드는 반드시 해시화(bcrypt 또는 argon2)하여 저장할 것
- 평문 패스워드를 DB에 직접 저장하지 말 것
- 외부 API 통신은 반드시 HTTPS를 사용할 것
- 개인정보(이름, 전화번호 등)는 DB에 암호화하여 저장할 것
```

#### 체크포인트

- [ ] 패스워드를 평문으로 저장하는 코드가 없는지 확인합니다.
- [ ] 외부 API 통신에 `http://`가 아닌 `https://`를 사용하는지 확인합니다.
- [ ] 개인정보를 데이터베이스에 저장할 때 암호화를 적용하는지 확인합니다.

---

### 8-3. 하드코딩된 중요정보

#### 개요

하드코딩이란 소스 코드 내부에 패스워드, API 키, 데이터베이스 접속 정보 등을 직접 문자열로 작성하는 것입니다. **이것은 바이브 코딩에서 가장 빈번하게 발생하는 보안 실수입니다.**

AI에게 "데이터베이스에 연결하는 코드를 만들어줘"라고 요청하면, AI는 높은 확률로 코드 안에 예시 패스워드를 직접 작성합니다. 이 코드를 그대로 GitHub에 Push하면, 전 세계 누구나 여러분의 접속 정보를 볼 수 있습니다.

> **⚠️ 주의:** GitHub에는 API 키와 패스워드를 자동으로 수집하는 봇이 활동하고 있습니다. 한번 Push된 정보는 커밋 기록에 남아 삭제해도 복구할 수 있습니다.

#### ❌ 취약한 수도 코드

```pseudocode
// API 키가 소스코드에 그대로 노출
SET api_key = "sk-proj-abc123xyz456..."

FUNCTION get_db_connection():
    // 데이터베이스 접속 정보가 하드코딩됨
    RETURN DB_CONNECT(
        host = "db.example.com",
        port = 3306,
        user = "admin",
        password = "SuperSecret123!",
        database = "production_db"
    )
```

#### ✅ 안전한 수도 코드

```pseudocode
// .env 파일에서 환경 변수를 로드 (.env 파일은 .gitignore에 반드시 추가)
LOAD_ENV_FILE(".env")

SET api_key = ENV_GET("OPENAI_API_KEY")

FUNCTION get_db_connection():
    // 환경 변수에서 접속 정보를 가져옴
    RETURN DB_CONNECT(
        host = ENV_GET("DB_HOST"),
        port = ENV_GET("DB_PORT", default = 3306),
        user = ENV_GET("DB_USER"),
        password = ENV_GET("DB_PASSWORD"),
        database = ENV_GET("DB_NAME")
    )

FUNCTION validate_env_on_startup():
    // 애플리케이션 시작 시 필수 환경 변수 존재 여부 검증
    required = ["OPENAI_API_KEY", "DB_HOST", "DB_PASSWORD"]
    missing = FILTER(required, WHERE ENV_GET(var) IS NULL)
    IF missing IS NOT EMPTY:
        RAISE ERROR("필수 환경 변수가 설정되지 않았습니다: " + JOIN(missing, ", "))
```

#### 💬 AI에게 요청할 프롬프트

```text
데이터베이스 연결 코드를 만들어주세요:
- API 키, 패스워드 등 중요정보는 절대 소스코드에 하드코딩하지 말 것
- 모든 접속 정보는 환경 변수(.env 파일)에서 가져올 것
- .gitignore에 .env 파일을 추가하는 설정도 포함할 것
- 애플리케이션 시작 시 필수 환경 변수의 존재 여부를 검증하는 로직을 포함할 것
```

#### 체크포인트

- [ ] 소스코드에 API 키, 패스워드, 시크릿 키가 문자열로 하드코딩되어 있지 않은지 확인합니다.
- [ ] `.env` 파일이 `.gitignore`에 추가되어 있는지 확인합니다.
- [ ] Git 커밋 전, `git diff`로 중요 정보가 포함되어 있지 않은지 확인합니다.

---

### 8-4. 충분하지 않은 키 길이

#### 개요

암호화 키의 길이는 암호화의 강도를 결정하는 핵심 요소입니다. 아무리 안전한 알고리즘을 사용하더라도 키 길이가 충분하지 않으면, 브루트포스 공격으로 해독될 수 있습니다.

#### 권장 키 길이 표

| 알고리즘 유형 | 알고리즘 | ❌ 취약한 키 길이 | ✅ 권장 키 길이 |
|---|---|---|---|
| 대칭키 암호 | AES | 64비트 이하 | **128비트 이상** (권장 256비트) |
| 비대칭키 암호 | RSA | 1024비트 이하 | **2048비트 이상** (권장 3072비트) |
| 타원곡선 암호 | ECDSA | 160비트 이하 | **224비트 이상** (권장 256비트) |
| 해시 함수 | SHA | SHA-1 (160비트) | **SHA-256 이상** |

#### ❌ 취약한 수도 코드

```pseudocode
FUNCTION generate_key_pair():
    // 1024비트는 현대 컴퓨터로 해독 가능
    private_key = RSA_GENERATE(key_size = 1024)
    public_key = private_key.get_public_key()
    RETURN (private_key, public_key)
```

#### ✅ 안전한 수도 코드

```pseudocode
FUNCTION generate_key_pair():
    // 2048비트 이상으로 설정 (권장: 3072비트)
    private_key = RSA_GENERATE(key_size = 2048)
    public_key = private_key.get_public_key()
    RETURN (private_key, public_key)

FUNCTION generate_ecc_key():
    // P-256 곡선 사용 (224비트 이상)
    key = ECC_GENERATE(curve = "P-256")
    RETURN key
```

> **💡 팁:** 2030년 이후까지의 안전성을 고려한다면 RSA 3072비트, AES 256비트를 사용하는 것이 바람직합니다.

#### 💬 AI에게 요청할 프롬프트

```text
RSA 키 쌍을 생성하는 코드를 만들어주세요:
- RSA 키 길이는 최소 2048비트 이상으로 설정할 것
- 가능하면 3072비트 또는 4096비트를 사용할 것
- 대안으로 ECC P-256 곡선 사용도 고려할 것
- 1024비트 이하의 키는 절대 사용하지 말 것
```

#### 체크포인트

- [ ] RSA는 최소 2048비트, AES는 최소 128비트, ECC는 최소 224비트인지 확인합니다.
- [ ] 키 생성 함수의 키 길이 인자값을 반드시 확인합니다.

---

## 9장. 난수, 패스워드, 그리고 인증 방어

### 9-1. 적절하지 않은 난수 값 사용

#### 개요

난수(Random Number)는 세션 ID, 인증 토큰, 암호화 키 등 보안에 민감한 곳에서 사용됩니다. 문제는 일반적인 `random` 함수가 생성하는 난수는 **의사 난수**로, 시드 값을 알면 생성되는 모든 숫자를 예측할 수 있다는 것입니다.

AI에게 "랜덤 토큰을 생성해줘"라고 요청하면, AI는 종종 보안에 부적합한 일반 `random` 함수를 사용합니다.

#### 왜 위험한가

- **세션 하이재킹**: 세션 ID 생성에 예측 가능한 난수를 사용하면, 공격자가 다른 사용자의 세션 ID를 예측하여 탈취할 수 있습니다.
- **토큰 위조**: 패스워드 재설정 토큰이 예측 가능하면, 공격자가 다른 사용자의 패스워드를 재설정할 수 있습니다.
- **암호화 키 추측**: 암호화 키가 예측 가능한 난수로 생성되면 암호화 자체가 무력화됩니다.

#### ❌ 취약한 수도 코드

```pseudocode
FUNCTION generate_session_id():
    // 의사 난수: 시드를 알면 예측 가능
    RANDOM_SEED(42)  // 고정 시드: 항상 같은 값이 생성됨!
    RETURN RANDOM_STRING(length = 32, charset = "alphanumeric")

FUNCTION generate_reset_token():
    // 일반 random은 보안용으로 부적합
    RETURN TO_STRING(RANDOM_INT(100000, 999999))
```

#### ✅ 안전한 수도 코드

```pseudocode
FUNCTION generate_session_id():
    // 암호학적으로 안전한 난수 생성기 사용
    RETURN CRYPTO_RANDOM_HEX(length = 32)   // 64자의 16진수 문자열

FUNCTION generate_reset_token():
    // URL에서 사용하기 안전한 토큰 생성
    RETURN CRYPTO_RANDOM_URL_SAFE(length = 32)

FUNCTION generate_otp():
    // 6자리 숫자 OTP 생성 — 각 자리를 암호학적 난수로
    result = ""
    FOR i = 1 TO 6:
        result = result + TO_STRING(CRYPTO_RANDOM_INT(0, 9))
    RETURN result

FUNCTION generate_api_key():
    // API 키 생성
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    result = ""
    FOR i = 1 TO 48:
        result = result + CRYPTO_RANDOM_CHOICE(charset)
    RETURN result
```

#### 💬 AI에게 요청할 프롬프트

```text
보안 토큰 생성 함수를 만들어주세요:
- 일반 random이 아닌 암호학적으로 안전한 난수 생성기를 사용할 것
  (예: Python의 secrets, Java의 SecureRandom, Node.js의 crypto.randomBytes)
- 세션 ID, 패스워드 재설정 토큰, OTP 각각에 대한 생성 함수를 포함할 것
- 고정 시드(seed)를 절대 사용하지 말 것
```

#### 체크포인트

- [ ] 보안 관련 기능(토큰, 세션, 키 생성)에 일반 `random`이 사용되고 있지 않은지 확인합니다.
- [ ] 고정 시드(`seed(42)` 등)가 설정되어 있지 않은지 확인합니다.
- [ ] 보안 난수 생성에는 반드시 암호학적 난수 생성기를 사용합니다.

---

### 9-2. 취약한 패스워드 허용

#### 개요

패스워드 정책은 사용자가 설정하는 패스워드의 최소 요구 사항을 정의하는 규칙입니다. "1234", "password" 같은 취약한 패스워드를 허용하면, 아무리 강력한 암호화를 적용하더라도 쉽게 뚫릴 수 있습니다.

AI가 회원가입 기능을 생성할 때, 패스워드 유효성 검증 로직을 포함하지 않는 경우가 많습니다.

#### ❌ 취약한 수도 코드

```pseudocode
FUNCTION register(request):
    username = GET request.body["username"]
    password = GET request.body["password"]

    // 패스워드 강도 확인 없이 바로 저장
    CREATE_USER(username, password)
    RETURN REDIRECT("/login")
```

#### ✅ 안전한 수도 코드

```pseudocode
FUNCTION validate_password(password):
    errors = EMPTY_LIST

    IF LENGTH(password) < 8:
        APPEND(errors, "패스워드는 최소 8자 이상이어야 합니다")
    IF LENGTH(password) > 128:
        APPEND(errors, "패스워드는 128자를 초과할 수 없습니다")
    IF NOT CONTAINS_UPPERCASE(password):
        APPEND(errors, "대문자를 최소 1개 포함해야 합니다")
    IF NOT CONTAINS_LOWERCASE(password):
        APPEND(errors, "소문자를 최소 1개 포함해야 합니다")
    IF NOT CONTAINS_DIGIT(password):
        APPEND(errors, "숫자를 최소 1개 포함해야 합니다")
    IF NOT CONTAINS_SPECIAL_CHAR(password):
        APPEND(errors, "특수문자를 최소 1개 포함해야 합니다")

    // 흔히 사용되는 취약한 패스워드 차단
    common = ["password", "123456", "qwerty", "abc123", "password123"]
    IF LOWERCASE(password) IN common:
        APPEND(errors, "너무 흔한 패스워드입니다")

    RETURN errors

FUNCTION register(request):
    username = GET request.body["username"]
    password = GET request.body["password"]

    errors = validate_password(password)
    IF errors IS NOT EMPTY:
        RETURN ERROR(400, errors)

    CREATE_USER(username, HASH_PASSWORD(password))
    RETURN REDIRECT("/login")
```

#### 💬 AI에게 요청할 프롬프트

```text
회원가입 기능에 패스워드 정책 검증을 추가해주세요:
- 최소 8자 이상, 최대 128자 이하
- 대문자, 소문자, 숫자, 특수문자를 각각 최소 1개 이상 포함
- 흔히 사용되는 패스워드(password, 123456, qwerty 등) 차단
- 검증 실패 시 구체적인 오류 메시지를 반환할 것
```

#### 체크포인트

- [ ] 회원가입 및 패스워드 변경에 패스워드 강도 검증 로직이 포함되어 있는지 확인합니다.
- [ ] 최소 8자 이상, 대소문자/숫자/특수문자 조합을 요구하는지 확인합니다.
- [ ] 흔히 사용되는 패스워드를 차단하는 로직이 있는지 확인합니다.

---

### 9-3. 솔트 없는 일방향 해시 함수 사용

#### 개요

일방향 해시 함수는 원본 데이터를 복원할 수 없는 해시값으로 변환합니다. 그러나 솔트(Salt) 없이 해시만 적용하면 **레인보우 테이블 공격**에 취약합니다.

솔트란 해시 계산 전에 원본 데이터에 추가하는 무작위 문자열입니다. 같은 패스워드라도 솔트가 다르면 완전히 다른 해시값이 생성됩니다.

#### 왜 위험한가

- **레인보우 테이블 공격**: 솔트 없는 해시값은 사전 계산된 테이블에서 원문을 찾아낼 수 있습니다.
- **동일 해시값 문제**: 같은 패스워드를 사용하는 모든 사용자의 해시값이 동일하게 됩니다.
- **GPU 가속 공격**: 단순 해시 함수는 GPU로 초당 수십억 개의 해시를 계산할 수 있어 브루트포스에 취약합니다.

#### ❌ 취약한 수도 코드

```pseudocode
FUNCTION hash_password(password):
    // 솔트 없이 해시하면 레인보우 테이블 공격에 취약
    RETURN SHA256_HASH(password)

FUNCTION verify_password(password, stored_hash):
    RETURN hash_password(password) == stored_hash
```

#### ✅ 안전한 수도 코드

```pseudocode
// 방법 1: bcrypt 사용 (솔트 자동 생성 + 키 스트레칭)
FUNCTION hash_password(password):
    salt = BCRYPT_GENERATE_SALT(rounds = 12)  // rounds가 높을수록 안전
    hashed = BCRYPT_HASH(password, salt)
    RETURN hashed   // 솔트가 해시값에 자동 포함됨

FUNCTION verify_password(password, stored_hash):
    RETURN BCRYPT_VERIFY(password, stored_hash)

// 방법 2: argon2 사용 (현재 가장 권장되는 알고리즘)
FUNCTION hash_password_argon2(password):
    hashed = ARGON2_HASH(
        password,
        time_cost = 3,         // 반복 횟수
        memory_cost = 65536,   // 메모리 사용량 (KB)
        parallelism = 4        // 병렬 처리 수
    )
    RETURN hashed   // 솔트 자동 생성 + 메모리 하드 함수

FUNCTION verify_password_argon2(password, stored_hash):
    TRY:
        RETURN ARGON2_VERIFY(stored_hash, password)
    CATCH Exception:
        RETURN FALSE
```

> **💡 팁:** 패스워드 해싱 알고리즘의 권장 순위는 **Argon2 > bcrypt > scrypt > PBKDF2** 순입니다. 가능하다면 Argon2를 사용하십시오.

#### 💬 AI에게 요청할 프롬프트

```text
패스워드 해싱 및 검증 함수를 만들어주세요:
- bcrypt 또는 argon2를 사용할 것 (단순 SHA-256 해시 사용 금지)
- 솔트는 자동 생성되도록 할 것
- 키 스트레칭(반복 해싱)을 적용하여 브루트포스 공격을 어렵게 할 것
- 해시 생성 함수와 검증 함수를 분리하여 제공할 것
```

#### 체크포인트

- [ ] `SHA256(password)`처럼 솔트 없이 단순 해시만 사용하는 코드가 없는지 확인합니다.
- [ ] 패스워드 저장에는 반드시 bcrypt, argon2, 또는 scrypt를 사용합니다.

---



> **[참고 다이어그램] 패스워드 해싱 흐름도**

# 다이어그램 7: 패스워드 해싱 흐름도

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


---

### 9-4. 반복된 인증시도 제한 기능 부재

#### 개요

레이트 리미팅이란 특정 시간 내에 허용되는 요청 횟수를 제한하는 기법입니다. 로그인 시도에 횟수 제한이 없으면, 공격자는 수백만 개의 패스워드를 자동으로 시도하는 브루트포스 공격을 수행할 수 있습니다.

AI가 로그인 기능을 생성할 때, 반복 시도에 대한 제한을 포함하지 않는 것이 일반적입니다.

#### 왜 위험한가

- **브루트포스 공격**: 초당 수천 건의 로그인 시도로 패스워드를 알아낼 수 있습니다.
- **크리덴셜 스터핑**: 유출된 대량의 계정 정보를 자동으로 시도합니다.
- **서비스 거부(DoS)**: 대량의 로그인 요청으로 서버 자원이 고갈될 수 있습니다.

#### ❌ 취약한 수도 코드

```pseudocode
FUNCTION login(request):
    username = GET request.body["username"]
    password = GET request.body["password"]

    // 횟수 제한 없이 무한히 로그인 시도 가능
    user = AUTHENTICATE(username, password)
    IF user IS NOT NULL:
        CREATE_SESSION(user)
        RETURN REDIRECT("/dashboard")

    RETURN ERROR(401, "로그인 실패")
```

#### ✅ 안전한 수도 코드

```pseudocode
// 로그인 시도 횟수를 추적하는 제한기
CLASS LoginRateLimiter:
    max_attempts = 5
    lockout_duration = 1800  // 초 단위 (30분)
    attempts = EMPTY_MAP     // { identifier: [timestamp, ...] }

    FUNCTION is_locked(identifier):
        now = CURRENT_TIMESTAMP()
        // 잠금 기간이 지난 시도 기록 제거
        attempts[identifier] = FILTER(attempts[identifier],
            WHERE now - timestamp < lockout_duration)
        RETURN LENGTH(attempts[identifier]) >= max_attempts

    FUNCTION record_failure(identifier):
        APPEND(attempts[identifier], CURRENT_TIMESTAMP())

    FUNCTION reset(identifier):
        attempts[identifier] = EMPTY_LIST

SET limiter = NEW LoginRateLimiter()

FUNCTION login(request):
    username = GET request.body["username"]
    client_ip = GET request.remote_ip
    identifier = username + ":" + client_ip

    // 1단계: 잠금 상태 확인
    IF limiter.is_locked(identifier):
        RETURN ERROR(429, "로그인 시도 횟수를 초과했습니다. 30분 후 다시 시도해주세요.")

    // 2단계: 인증 시도
    user = AUTHENTICATE(username, GET request.body["password"])
    IF user IS NOT NULL:
        limiter.reset(identifier)
        CREATE_SESSION(user)
        RETURN REDIRECT("/dashboard")

    // 3단계: 실패 기록 및 남은 횟수 안내
    limiter.record_failure(identifier)
    remaining = limiter.max_attempts - LENGTH(limiter.attempts[identifier])

    // 모호한 메시지 사용 — "아이디가 없습니다" 등 구체적 정보 노출 금지
    RETURN ERROR(401, "아이디 또는 패스워드가 틀렸습니다. 남은 시도: " + remaining + "회")
```

> **⚠️ 주의:** 로그인 실패 메시지에서 "아이디가 존재하지 않습니다" 또는 "패스워드가 틀렸습니다"처럼 구체적인 정보를 제공하면, 공격자가 유효한 아이디를 식별하는 데 악용할 수 있습니다. 항상 모호한 메시지를 사용하십시오.

#### 💬 AI에게 요청할 프롬프트

```text
다음 보안 요구사항으로 로그인 기능을 구현해주세요:
- 비밀번호는 bcrypt 또는 argon2로 해싱
- 로그인 실패 시 구체적 원인을 노출하지 말 것 ("아이디 또는 비밀번호가 틀렸습니다"만 표시)
- 5회 실패 시 계정 잠금 또는 30분 지연 적용
- IP + 사용자명 조합으로 시도 횟수를 추적할 것
- 잠금 해제까지 남은 시간을 안내할 것
```

#### 체크포인트

- [ ] 로그인 기능에 시도 횟수 제한이 적용되어 있는지 확인합니다.
- [ ] 일정 횟수 이상 실패 시 계정 잠금 또는 CAPTCHA가 적용되는지 확인합니다.
- [ ] 로그인 실패 메시지가 구체적 정보를 노출하지 않는지 확인합니다.

---

## 10장. 서명, 인증서, 무결성 검증

### 10-1. 부적절한 전자서명 확인

#### 개요

전자서명(Digital Signature)은 데이터의 무결성과 인증을 보장하는 암호학적 기법입니다. 웹 개발에서 가장 흔히 접하는 전자서명은 JWT(JSON Web Token)입니다. JWT의 서명을 제대로 검증하지 않거나, `alg: none` 공격을 허용하면 공격자가 토큰을 위조하여 다른 사용자로 로그인할 수 있습니다.

#### 왜 위험한가

- **토큰 위조**: 서명 검증을 생략하면, 공격자가 JWT 페이로드를 수정하여 관리자 권한을 획득할 수 있습니다.
- **알고리즘 혼동 공격**: JWT 헤더의 `alg` 필드를 `none`으로 설정하여 서명 없이 토큰을 사용하는 공격입니다.
- **키 혼동 공격**: RS256(비대칭)으로 서명된 토큰을 HS256(대칭)으로 검증하도록 유도하는 공격입니다.

#### ❌ 취약한 수도 코드

```pseudocode
FUNCTION get_user_from_token(token):
    // 서명을 검증하지 않고 디코딩 — 위조된 토큰도 통과!
    payload = JWT_DECODE(token, verify_signature = FALSE)
    RETURN payload["user_id"]

FUNCTION verify_token_weak(token, secret):
    // algorithms 목록에 "none"을 허용 — 서명 없는 토큰도 통과!
    payload = JWT_DECODE(token, secret, algorithms = ["HS256", "none"])
    RETURN payload
```

#### ✅ 안전한 수도 코드

```pseudocode
SET SECRET_KEY = ENV_GET("JWT_SECRET_KEY")

FUNCTION create_token(user_id, role):
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": CURRENT_TIME() + HOURS(1),   // 만료 시간
        "iat": CURRENT_TIME()                // 발급 시간
    }
    // 명시적으로 알고리즘 지정
    RETURN JWT_ENCODE(payload, SECRET_KEY, algorithm = "HS256")

FUNCTION verify_token(token):
    TRY:
        // 반드시 서명을 검증하고, 허용 알고리즘을 명시적으로 지정
        payload = JWT_DECODE(
            token,
            SECRET_KEY,
            algorithms = ["HS256"],         // "none"을 절대 포함하지 않음
            verify_signature = TRUE,
            verify_expiration = TRUE,        // 만료 시간 검증
            require_claims = ["exp", "iat", "user_id"]  // 필수 클레임 확인
        )
        RETURN payload

    CATCH ExpiredTokenError:
        RAISE ERROR("토큰이 만료되었습니다")

    CATCH InvalidTokenError:
        RAISE ERROR("유효하지 않은 토큰입니다")
```

#### 💬 AI에게 요청할 프롬프트

```text
JWT 기반 인증 시스템을 만들어주세요:
- 토큰 생성 시 알고리즘을 명시적으로 HS256(또는 RS256)으로 지정할 것
- 토큰 검증 시 verify_signature를 반드시 TRUE로 설정할 것
- algorithms 목록에 "none"을 절대 포함하지 말 것
- 만료 시간(exp)을 설정하고 검증할 것
- 시크릿 키는 환경 변수에서 가져올 것
```

#### 체크포인트

- [ ] JWT 디코딩에 `verify_signature = FALSE`가 설정되어 있지 않은지 확인합니다.
- [ ] `algorithms` 매개변수에 `"none"`이 포함되어 있지 않은지 확인합니다.
- [ ] JWT 만료 시간이 설정되어 있고 검증되는지 확인합니다.
- [ ] JWT 시크릿 키가 환경 변수로 관리되는지 확인합니다.

---

### 10-2. 부적절한 인증서 유효성 검증

#### 개요

SSL/TLS 인증서는 HTTPS 통신에서 서버의 신원을 확인하고 데이터를 암호화하는 데 사용됩니다. 외부 API를 호출할 때 인증서 검증을 비활성화(`verify = FALSE`)하면 중간자 공격(MITM)에 완전히 노출됩니다.

AI에게 API 호출 코드를 요청하면, 개발 편의를 위해 인증서 검증을 비활성화하는 코드를 생성하는 경우가 있습니다.

#### 왜 위험한가

- **중간자 공격(MITM)**: 공격자가 통신을 가로채고 변조할 수 있습니다.
- **데이터 도청**: 암호화된 것처럼 보이지만, 공격자가 모든 통신 내용을 볼 수 있습니다.
- **API 키 유출**: 요청 헤더에 포함된 API 키, 인증 토큰 등이 유출될 수 있습니다.

#### ❌ 취약한 수도 코드

```pseudocode
FUNCTION call_payment_api(payment_data):
    // SSL 인증서 검증을 완전히 건너뜀!
    DISABLE_SSL_WARNINGS()
    response = HTTPS_POST(
        url = "https://api.payment.com/charge",
        body = payment_data,
        verify_ssl = FALSE   // 중간자 공격에 무방비!
    )
    RETURN response

FUNCTION call_api_unsafe():
    // 검증되지 않은 SSL 컨텍스트 사용
    context = CREATE_UNVERIFIED_SSL_CONTEXT()
    response = URL_OPEN("https://api.example.com", ssl_context = context)
    RETURN response
```

#### ✅ 안전한 수도 코드

```pseudocode
FUNCTION call_payment_api(payment_data):
    // SSL 인증서 검증 활성화 (기본값)
    response = HTTPS_POST(
        url = "https://api.payment.com/charge",
        body = payment_data,
        verify_ssl = TRUE   // 인증서 검증 활성화
    )
    RETURN response

FUNCTION call_internal_api(data):
    // 자체 서명 인증서를 사용하는 내부 서버의 경우
    // CA 인증서 경로를 직접 지정
    response = HTTPS_GET(
        url = "https://internal-api.company.com/data",
        verify_ssl = "/path/to/company-ca-bundle.crt"
    )
    RETURN response
```

> **⚠️ 주의:** 개발 환경에서 자체 서명 인증서 때문에 `verify = FALSE`를 사용하는 경우가 있습니다. 이 코드가 운영 환경에 배포되지 않도록 환경 분리를 철저히 하십시오.

#### 💬 AI에게 요청할 프롬프트

```text
외부 API 호출 코드를 만들어주세요:
- SSL 인증서 검증을 절대 비활성화하지 말 것 (verify=False 사용 금지)
- SSL 경고를 숨기는 코드(disable_warnings)를 포함하지 말 것
- 자체 서명 인증서가 필요한 경우 CA 인증서 경로를 직접 지정하는 방식을 사용할 것
- 기본 SSL 컨텍스트를 사용할 것
```

#### 체크포인트

- [ ] 코드 전체에서 `verify = FALSE` 또는 `verify_ssl = FALSE`를 검색하여 제거합니다.
- [ ] SSL 경고를 숨기는 코드가 없는지 확인합니다.
- [ ] 자체 서명 인증서가 필요한 경우 CA 인증서를 직접 지정하는 방식을 사용합니다.

---

### 10-3. 무결성 검사 없는 코드 다운로드

#### 개요

무결성이란 데이터가 변조되지 않았음을 보장하는 것입니다. 외부에서 패키지나 스크립트를 다운로드하여 사용할 때, 원본과 동일한지 검증하지 않으면 악성 코드가 포함된 변조된 패키지를 실행할 수 있습니다.

AI가 추천하는 라이브러리를 무비판적으로 설치하는 것은 공급망 공격에 노출되는 위험한 행위입니다.

#### 왜 위험한가

- **공급망 공격**: 패키지 이름을 흉내 낸 악성 패키지를 배포합니다(타이포스쿼팅). 예: `requests` 대신 `reqeusts`.
- **의존성 혼동**: 내부 패키지와 같은 이름의 악성 패키지를 공개 저장소에 올려 설치를 유도합니다.
- **패키지 변조**: 인기 패키지의 관리자 계정이 해킹되어 악성 코드가 주입된 사례가 실제로 발생했습니다.

> **⚠️ 주의:** AI가 존재하지 않는 패키지 이름을 제안하는 경우가 있습니다(할루시네이션). 공격자는 이 점을 악용하여, AI가 자주 추천하는 가상의 패키지 이름으로 악성 패키지를 등록할 수 있습니다.

#### ❌ 취약한 수도 코드

```pseudocode
FUNCTION install_tool():
    // 인터넷에서 다운로드한 스크립트를 검증 없이 바로 실행
    DOWNLOAD_FILE(
        url = "http://example.com/install.sh",  // HTTP 사용 (암호화 없음!)
        save_to = "/tmp/install.sh"
    )
    EXECUTE_SHELL("bash /tmp/install.sh")   // 검증 없이 실행!
```

#### ✅ 안전한 수도 코드

```pseudocode
FUNCTION download_and_verify(url, expected_hash, save_path):
    // HTTPS를 사용하여 다운로드
    DOWNLOAD_FILE(url, save_to = save_path)

    // SHA-256 해시로 무결성 검증
    actual_hash = CALCULATE_SHA256(save_path)

    IF actual_hash != expected_hash:
        DELETE_FILE(save_path)   // 검증 실패 시 파일 삭제
        RAISE ERROR(
            "무결성 검증 실패!\n" +
            "예상 해시: " + expected_hash + "\n" +
            "실제 해시: " + actual_hash
        )

    RETURN save_path

// 패키지 설치 시에도 해시 검증 적용
// requirements.txt 예시:
//   requests==2.31.0 --hash=sha256:58cd2187c01e70e6...
//   flask==3.0.0 --hash=sha256:21128f47e4e3b9d2...
// 설치 명령: pip install --require-hashes -r requirements.txt
```

#### 💬 AI에게 요청할 프롬프트

```text
외부 파일을 다운로드하는 코드를 만들어주세요:
- 반드시 HTTPS를 사용하여 다운로드할 것
- 다운로드 후 SHA-256 해시로 무결성을 검증할 것
- 검증 실패 시 파일을 삭제하고 에러를 발생시킬 것
- curl | bash 같은 검증 없는 실행 패턴을 사용하지 말 것
```

#### 체크포인트

- [ ] AI가 추천하는 패키지 이름의 철자가 정확한지 공식 저장소에서 직접 확인합니다.
- [ ] `curl ... | bash`와 같은 검증 없는 스크립트 실행을 피합니다.
- [ ] `requirements.txt`에 패키지 버전을 고정(`==`)하여 예기치 않은 업데이트를 방지합니다.
- [ ] 취약점 스캐너(pip-audit, safety 등)를 도입하여 정기적으로 점검합니다.

---

## 11장. 정보 노출을 차단하세요

### 11-1. 쿠키를 통한 정보 노출

#### 개요

쿠키(Cookie)는 웹 브라우저에 저장되는 작은 데이터로, 로그인 상태 유지 등에 사용됩니다. 쿠키의 보안 속성을 적절히 설정하지 않으면, 세션 ID나 인증 토큰이 공격자에게 노출될 수 있습니다.

AI가 세션 관리 코드를 생성할 때, `HttpOnly`, `Secure`, `SameSite`와 같은 보안 속성을 생략하는 경향이 있습니다.

#### 왜 위험한가

- **XSS를 통한 세션 탈취**: `HttpOnly`가 없으면, JavaScript에서 `document.cookie`로 쿠키에 접근할 수 있습니다.
- **네트워크 도청**: `Secure`가 없으면, HTTP 평문 연결에서도 쿠키가 전송되어 도청 가능합니다.
- **CSRF 공격**: `SameSite`가 없으면, 외부 사이트에서 사용자의 쿠키를 포함한 요청을 보낼 수 있습니다.

| 속성 | 역할 | 미설정 시 위험 |
|---|---|---|
| `HttpOnly` | JavaScript에서 쿠키 접근 차단 | XSS를 통한 세션 탈취 |
| `Secure` | HTTPS 연결에서만 쿠키 전송 | 네트워크 도청으로 쿠키 유출 |
| `SameSite` | 외부 사이트 요청 시 쿠키 전송 제한 | CSRF 공격 |

#### ❌ 취약한 수도 코드

```pseudocode
FUNCTION login_view(request):
    user = AUTHENTICATE(request)
    IF user IS NOT NULL:
        session_id = GENERATE_SESSION_ID()
        response = CREATE_RESPONSE("로그인 성공")

        // 보안 속성 없이 세션 ID를 쿠키에 저장 — 위험!
        SET_COOKIE(response, "session_id", session_id)

        RETURN response
```

#### ✅ 안전한 수도 코드

```pseudocode
FUNCTION login_view(request):
    user = AUTHENTICATE(request)
    IF user IS NOT NULL:
        session_id = CRYPTO_RANDOM_HEX(32)
        response = CREATE_RESPONSE("로그인 성공")

        // 세 가지 핵심 보안 속성을 모두 적용
        SET_COOKIE(response,
            name = "session_id",
            value = session_id,
            httponly = TRUE,      // JavaScript에서 접근 불가
            secure = TRUE,        // HTTPS에서만 전송
            samesite = "Lax",     // 외부 사이트 요청 시 쿠키 미전송
            max_age = 3600,       // 1시간 후 만료
            path = "/"
        )

        RETURN response
```

> **💡 팁:** `SameSite` 속성에는 세 가지 값이 있습니다. `Strict`는 외부 사이트에서의 모든 요청에 쿠키를 보내지 않습니다(가장 안전). `Lax`는 GET 요청에 한해 외부 사이트에서도 쿠키를 전송합니다(권장). `None`은 모든 요청에 쿠키를 전송하며, 반드시 `Secure`와 함께 사용해야 합니다.

#### 💬 AI에게 요청할 프롬프트

```text
로그인 후 세션 쿠키를 설정하는 코드를 만들어주세요:
- HttpOnly=True (JavaScript에서 접근 차단)
- Secure=True (HTTPS에서만 전송)
- SameSite=Lax (CSRF 방어)
- max_age=3600 (1시간 후 만료)
- 세션 ID는 암호학적으로 안전한 난수로 생성할 것
- 쿠키에 패스워드나 개인정보를 직접 저장하지 말 것
```

#### 체크포인트

- [ ] 쿠키 설정 시 `httponly`, `secure`, `samesite`가 모두 설정되어 있는지 확인합니다.
- [ ] 쿠키에 만료 시간이 설정되어 영구 쿠키를 방지하는지 확인합니다.
- [ ] 쿠키에 패스워드, 개인정보 등 민감한 정보를 직접 저장하지 않는지 확인합니다.

---

### 11-2. 주석문 안에 포함된 시스템 주요정보

#### 개요

주석은 코드의 동작을 설명하기 위해 작성하지만, 주석에 패스워드, API 키, 서버 주소 등이 포함되면 소스코드에 접근한 누구나 이 정보를 확인할 수 있습니다.

**이 문제는 바이브 코딩에서 특히 심각합니다.** AI 코드 생성 도구는 코드를 설명하기 위해 자동으로 주석을 생성하는데, 이 과정에서 여러분이 프롬프트에 포함한 API 키나 서버 주소, 디버깅 과정의 임시 패스워드 등이 주석에 포함될 수 있습니다.

#### 왜 위험한가

- **소스코드 저장소 노출**: GitHub에 Push하면, 주석에 포함된 정보도 함께 공개됩니다.
- **클라이언트 사이드 노출**: HTML 주석이나 JavaScript 주석은 브라우저의 "소스 보기"로 누구나 확인할 수 있습니다.
- **빌드 산출물 포함**: 최소화되지 않은 JavaScript에는 주석이 그대로 포함됩니다.

> **⚠️ 주의:** AI는 코드를 설명하기 위해 주석을 매우 적극적으로 생성합니다. "이 코드는 DB_HOST=192.168.1.100에 접속합니다"와 같이 인프라 정보를 주석에 포함하는 경우가 있습니다. AI가 생성한 모든 주석을 반드시 검토하십시오.

#### ❌ 취약한 수도 코드

```pseudocode
// DB 접속 정보: admin / P@ssw0rd123!
// 서버: 192.168.1.100:3306
FUNCTION get_connection():
    // TODO: 나중에 환경 변수로 변경하기
    // 현재 테스트용 키: sk-proj-abc123xyz456
    RETURN DB_CONNECT(
        host = ENV_GET("DB_HOST"),
        user = ENV_GET("DB_USER"),
        password = ENV_GET("DB_PASSWORD")
    )
```

```pseudocode
// HTML 주석 예시 — 브라우저에서 누구나 볼 수 있음!
// <!-- 관리자 페이지: /admin/dashboard (인증 우회: ?debug=true) -->
// <!-- API 엔드포인트: https://api.internal.company.com/v2 -->
```

#### ✅ 안전한 수도 코드

```pseudocode
// 환경 변수에서 DB 접속 정보를 가져와 연결을 생성합니다.
FUNCTION get_connection():
    RETURN DB_CONNECT(
        host = ENV_GET("DB_HOST"),
        user = ENV_GET("DB_USER"),
        password = ENV_GET("DB_PASSWORD"),
        database = ENV_GET("DB_NAME")
    )
```

배포 전에 주석에 포함된 중요정보를 자동으로 검사하는 것을 권장합니다.

```pseudocode
// 주석 내 민감 정보 검사 로직
SET SENSITIVE_PATTERNS = [
    "password[:=]",       // password: xxx 또는 password=xxx
    "api[_-]?key[:=]",    // api_key: xxx
    "secret[:=]",         // secret: xxx
    "sk-[a-zA-Z0-9]{20}", // OpenAI API 키 패턴
    "IP 주소 패턴",        // 예: 192.168.x.x
    "admin / ",           // admin / password 패턴
]

FUNCTION scan_comments(file_path):
    issues = EMPTY_LIST
    FOR EACH (line_number, line) IN READ_LINES(file_path):
        comment = EXTRACT_COMMENT(line)
        IF comment IS NOT NULL:
            FOR EACH pattern IN SENSITIVE_PATTERNS:
                IF REGEX_MATCH(pattern, comment):
                    APPEND(issues, {file: file_path, line: line_number, content: line})
    RETURN issues
```

#### 💬 AI에게 요청할 프롬프트

```text
코드를 생성할 때 주석에 다음 정보를 절대 포함하지 마세요:
- 패스워드, API 키, 시크릿 키의 실제 값
- 서버 IP 주소, 포트 번호, 내부 URL
- 테스트 계정 정보
- "TODO: 나중에 변경" 같은 임시 메모에 실제 값을 포함하지 말 것
- 만료된 키라도 주석에 남기지 말 것
또한, 프로젝트에 detect-secrets 같은 시크릿 스캐너를 pre-commit hook으로 설정하는 방법도 알려주세요.
```

#### 체크포인트

- [ ] AI가 생성한 코드의 모든 주석에서 패스워드, API 키, 서버 주소가 포함되어 있지 않은지 확인합니다.
- [ ] HTML과 JavaScript 주석에 시스템 내부 정보가 노출되어 있지 않은지 확인합니다.
- [ ] `TODO: 나중에 변경`, `임시 패스워드` 등의 주석이 운영 코드에 남아 있지 않은지 확인합니다.
- [ ] 시크릿 스캐너를 Pre-commit Hook으로 설정하여 커밋 전 자동 검사를 수행합니다.
- [ ] AI에게 프롬프트를 전달할 때, 실제 API 키 대신 `YOUR_API_KEY_HERE` 같은 플레이스홀더를 사용합니다.

> **⚠️ 주의:** AI에게 실제 API 키를 프롬프트에 포함하면, AI가 그 키를 주석에 포함할 가능성이 높습니다. 또한 AI 서비스의 대화 기록에 여러분의 키가 저장될 수 있습니다. 프롬프트에는 절대 실제 중요정보를 포함하지 마십시오.


---

# Part 4. 안정적 코드 — 수도 코드로 배우는 시간/에러/코드오류 보안

여러분이 AI로 생성한 코드가 "잘 돌아간다"고 해서 "안전하다"는 뜻은 아닙니다. 타이밍 버그, 오류 처리 실수, 코드 품질 문제는 운영 환경에서 서비스 장애와 보안 사고를 일으킵니다. 이 파트에서는 언어에 관계없이 적용할 수 있는 수도 코드(Pseudocode)로 핵심 원리를 익히겠습니다.

---

## 12장. 시간 및 상태 — 타이밍이 만드는 버그

---

### 12-1. 경쟁 조건: 검사 시점과 사용 시점(TOCTOU)

#### 개요

TOCTOU(Time Of Check, Time Of Use)란 자원의 상태를 **검사하는 시점**과 **실제로 사용하는 시점** 사이의 틈을 악용하는 보안약점입니다. 파일이 존재하는지 확인한 뒤 열려는 그 찰나에 다른 프로세스가 파일을 삭제하거나 심볼릭 링크로 교체할 수 있습니다.

#### 왜 위험한가

바이브 코딩으로 "파일 업로드 후 처리" 기능을 만들면, AI는 보통 "파일 존재 확인 -> 파일 읽기/쓰기"의 두 단계 흐름을 생성합니다. 단일 사용자 테스트에서는 문제가 없지만, 운영 환경에서 수십 명이 동시에 요청하면 한 사용자의 파일이 다른 사용자의 요청에 의해 덮어씌워지거나, 공격자가 권한 상승 공격에 악용할 수 있습니다.

```pseudocode
// ❌ 취약한 수도 코드
FUNCTION write_shared_file(filename, content):
    // 1단계: 검사(Check)
    IF FILE_EXISTS(filename):
        // ⚠️ 이 사이에 다른 스레드가 파일을 삭제하거나 교체할 수 있음!
        // 2단계: 사용(Use)
        file = OPEN(filename, "write")
        file.WRITE(content)
        file.CLOSE()
```

```pseudocode
// ✅ 안전한 수도 코드
LOCK shared_lock  // 공유 자원 보호용 잠금 객체

FUNCTION write_shared_file(filename, content):
    ACQUIRE shared_lock           // 잠금 획득 — 다른 스레드 대기
        IF FILE_EXISTS(filename):
            file = OPEN(filename, "write")
            file.WRITE(content)
            file.CLOSE()
    RELEASE shared_lock           // 잠금 해제
```

> 💡 **팁:** 실무에서는 Lock보다 UUID 기반 고유 파일명을 생성하여 충돌 자체를 원천 차단하거나, 데이터베이스 트랜잭션으로 묶는 것이 더 실용적입니다.

```text
💬 AI에게 요청할 프롬프트

"이 파일 쓰기 함수가 여러 스레드에서 동시에 호출될 때
TOCTOU 경쟁 조건이 발생하지 않도록 Lock 또는 원자적 연산을 적용해줘.
가능하면 UUID 기반 고유 파일명 방식도 대안으로 제시해줘."
```

---

### 12-2. 종료되지 않는 반복문 또는 재귀 함수

#### 개요

재귀 함수에 종료 조건(Base Case)이 없거나, 반복문의 탈출 조건에 도달할 수 없으면 무한 실행에 빠집니다. 서버의 메모리와 CPU를 고갈시켜 서비스 거부(DoS) 상태를 유발합니다.

#### 왜 위험한가

AI에게 "재귀 깊이 에러를 해결해줘"라고 요청하면, 근본 원인을 고치지 않고 재귀 제한값을 올리는 코드를 제안하는 경우가 있습니다. 이는 시한폭탄의 타이머를 늘리는 것과 같습니다. 트리 탐색, 중첩 카테고리 조회, 대댓글 처리 등 복잡한 로직에서 특히 자주 발생합니다.

```pseudocode
// ❌ 취약한 수도 코드
SET_RECURSION_LIMIT(100000)      // 위험! 근본 해결이 아님

FUNCTION factorial(num):
    // 기본 케이스(Base Case)가 없음 — 무한 재귀 발생!
    RETURN num * factorial(num - 1)
```

```pseudocode
// ✅ 안전한 수도 코드
FUNCTION factorial(num):
    // 명확한 기본 케이스 정의
    IF num <= 0:
        RETURN 1
    RETURN num * factorial(num - 1)

// 더 안전한 방법: 재귀 대신 반복문 사용
FUNCTION factorial_loop(num):
    result = 1
    FOR i FROM 1 TO num:
        result = result * i
    RETURN result
```

> ⚠️ **주의:** AI가 `SET_RECURSION_LIMIT`을 제안하면 거절하십시오. 재귀 깊이 에러의 올바른 해결책은 알고리즘을 반복문으로 변경하거나 로직을 재설계하는 것입니다.

```text
💬 AI에게 요청할 프롬프트

"이 재귀 함수에 명확한 종료 조건(Base Case)을 추가해줘.
재귀 깊이가 깊어질 수 있다면 반복문 방식으로 변환한 버전도 함께 제시해줘.
setrecursionlimit은 사용하지 마."
```

#### 체크포인트

| 점검 항목 | 확인 방법 |
|-----------|-----------|
| 공유 자원에 Lock 사용 여부 | 파일, 전역 변수 접근 시 잠금 또는 트랜잭션 사용 확인 |
| 파일명 충돌 방지 | UUID 기반 고유 파일명 사용 여부 확인 |
| 재귀 함수의 기본 케이스 | 모든 재귀 함수에 명확한 종료 조건이 있는지 확인 |
| 반복문 탈출 조건 | `WHILE TRUE` 패턴 사용 시 `BREAK` 조건이 반드시 도달 가능한지 확인 |
| 재귀 대신 반복문 검토 | 깊은 재귀가 예상되면 반복문이나 내장 함수로 대체 가능한지 검토 |

---

## 13장. 에러 처리 — 오류가 보안 구멍이 되는 순간

---

### 13-1. 오류 메시지 정보 노출

#### 개요

오류 발생 시 스택 트레이스, 서버 환경 정보, 데이터베이스 구조 등을 사용자에게 그대로 보여주면 공격자가 시스템 내부 구조를 파악하는 데 악용합니다.

#### 왜 위험한가

AI는 개발 편의를 위해 디버그 모드를 활성화한 상태로 코드를 생성합니다. 이 상태로 배포하면 파일 경로, 패키지 버전, 환경 변수 등 민감한 정보가 브라우저에 출력됩니다. 공격자는 이를 기반으로 SQL 삽입, 경로 조작 등 후속 공격을 설계합니다.

```pseudocode
// ❌ 취약한 수도 코드
CONFIG:
    DEBUG_MODE = TRUE              // 운영 환경에서 디버그 모드!
    ALLOWED_HOSTS = ["*"]          // 모든 호스트 허용!

FUNCTION fetch_url(url):
    TRY:
        response = HTTP_GET(url, timeout=5)
        RETURN response.body
    CATCH error:
        PRINT_FULL_STACK_TRACE(error)       // 내부 경로·코드 구조 노출!
        RETURN "오류가 발생했습니다."
```

```pseudocode
// ✅ 안전한 수도 코드
CONFIG:
    DEBUG_MODE = FALSE
    ALLOWED_HOSTS = [ENV("ALLOWED_HOST", "localhost")]

FUNCTION fetch_url(url):
    TRY:
        response = HTTP_GET(url, timeout=5)
        RETURN response.body
    CATCH error:
        LOG.error("외부 URL 통신 에러 발생", error)    // 서버 로그에만 기록
        RETURN "일시적인 오류가 발생했습니다."           // 일반적 메시지만 반환

// 사용자 정의 에러 페이지 등록
REGISTER_ERROR_HANDLER(400, show_error_400)
REGISTER_ERROR_HANDLER(403, show_error_403)
REGISTER_ERROR_HANDLER(404, show_error_404)
REGISTER_ERROR_HANDLER(500, show_error_500)
```

```text
💬 AI에게 요청할 프롬프트

"이 코드의 에러 처리를 운영 환경에 맞게 수정해줘.
사용자에게는 일반적인 오류 메시지만 보여주고,
상세 에러 정보는 서버 로그에만 기록하도록 해줘.
DEBUG 모드를 끄고 커스텀 에러 페이지도 설정해줘."
```

---

### 13-2. 오류 상황 대응 부재

#### 개요

`TRY-CATCH`로 감싸놓았지만 `CATCH` 블록에서 아무런 조치도 취하지 않는 것을 "조용한 실패(Silent Failure)"라고 합니다. 중요한 오류가 무시된 채 프로그램이 비정상 상태로 계속 실행됩니다.

#### 왜 위험한가

AI는 에러를 피하기 위해 빈 CATCH 블록이나 PASS 문을 생성하는 경향이 있습니다. 예를 들어, 암호화 키 선택에서 오류가 발생했는데 이를 무시하면 예측 가능한 기본 키로 암호화가 수행되어 데이터가 사실상 보호되지 않습니다.

```pseudocode
// ❌ 취약한 수도 코드
KEYS = [
    {key: "secure_key_001", iv: "secure_iv_001"},
    {key: "secure_key_002", iv: "secure_iv_002"}
]

FUNCTION encrypt(key_id, plain_text):
    // 기본값이 매우 취약한 키!
    selected_key = {key: "0000000000000000", iv: "0000000000000000"}
    TRY:
        selected_key = KEYS[key_id]
    CATCH IndexError:
        PASS                        // ⚠️ 오류 무시! 취약한 기본 키로 진행됨

    RETURN AES_ENCRYPT(selected_key.key, selected_key.iv, plain_text)
```

```pseudocode
// ✅ 안전한 수도 코드
FUNCTION encrypt(key_id, plain_text):
    TRY:
        selected_key = KEYS[key_id]
    CATCH IndexError:
        LOG.warning("유효하지 않은 key_id: " + key_id)
        selected_key = {                         // 안전한 랜덤 키 생성
            key: GENERATE_RANDOM_BYTES(16),
            iv: GENERATE_RANDOM_BYTES(16)
        }

    RETURN AES_ENCRYPT(selected_key.key, selected_key.iv, plain_text)
```

```text
💬 AI에게 요청할 프롬프트

"이 코드에서 빈 except/catch 블록이나 pass만 있는 오류 처리를 모두 찾아줘.
각 오류 상황에 맞는 적절한 대응 로직(로깅, 안전한 기본값, 오류 반환)을 추가해줘."
```

---

### 13-3. 부적절한 예외 처리

#### 개요

모든 예외를 하나의 광범위한 CATCH 절로 처리하면 어떤 종류의 오류인지 구분할 수 없고, 각 상황에 맞는 적절한 대응이 불가능해집니다. 시스템 레벨 예외까지 삼켜버려 프로그램을 정상 종료할 수조차 없게 됩니다.

```pseudocode
// ❌ 취약한 수도 코드
FUNCTION get_content():
    TRY:
        file = OPEN("myfile.txt")
        line = file.READ_LINE()
        number = PARSE_INT(line)
    CATCH *ANY_ERROR*:               // 파일 없음? 권한 오류? 타입 오류? 전부 동일 처리!
        PRINT("Unexpected error")
```

```pseudocode
// ✅ 안전한 수도 코드
FUNCTION get_content():
    TRY:
        file = OPEN("myfile.txt")
        line = file.READ_LINE()
        number = PARSE_INT(line)
        RETURN number
    CATCH FileNotFound:
        LOG.error("설정 파일을 찾을 수 없습니다.")
        RETURN NONE
    CATCH PermissionDenied:
        LOG.error("설정 파일에 대한 읽기 권한이 없습니다.")
        RETURN NONE
    CATCH InvalidFormat:
        LOG.error("설정 파일의 데이터 형식이 올바르지 않습니다.")
        RETURN NONE
    FINALLY:
        IF file IS NOT NONE:
            file.CLOSE()             // 예외 여부와 무관하게 자원 해제
```

> ⚠️ **주의:** AI가 `CATCH *ANY_ERROR*: PASS` 패턴을 생성하면 반드시 수정하십시오. 최소한 로깅을 추가하고, 예외 종류별로 분기 처리하는 것이 올바른 방법입니다.

```text
💬 AI에게 요청할 프롬프트

"이 코드의 예외 처리를 개선해줘.
'except Exception'이나 'except:'처럼 광범위한 예외 처리를 찾아서
구체적인 예외 종류별로 분리해줘.
각 예외에 맞는 로그 메시지와 대응 로직도 추가해줘."
```

#### 체크포인트

| 점검 항목 | 확인 방법 |
|-----------|-----------|
| `DEBUG = TRUE` 설정 여부 | 설정 파일에서 디버그 모드 확인 |
| 스택 트레이스 외부 노출 | 에러 응답에 내부 경로, 코드 구조가 포함되지 않는지 확인 |
| 빈 CATCH 블록 | CATCH 뒤에 PASS만 있는 코드 검색 |
| 광범위한 예외 처리 | `CATCH *ANY_ERROR*` 사용 시 세분화 가능한지 검토 |
| 로깅 설정 | `PRINT` 대신 `LOG` 모듈을 사용하고 있는지 확인 |
| 사용자 정의 에러 페이지 | 400, 403, 404, 500 에러 핸들러 등록 여부 확인 |

---

## 14장. 코드 오류 — 개발자가 놓치기 쉬운 함정들

---

### 14-1. Null 역참조

#### 개요

객체가 존재하지 않는 상태(Null/None)에서 해당 객체의 속성이나 메서드에 접근하면 프로그램이 즉시 중단됩니다. 공격자는 의도적으로 필수 파라미터를 누락시켜 이 오류를 유발하고, 노출되는 에러 메시지에서 시스템 정보를 수집합니다.

```pseudocode
// ❌ 취약한 수도 코드
FUNCTION parse_input(request):
    username = REQUEST.GET_PARAM("username")     // 키가 없으면 NONE 반환
    IF username.TRIM() == "":                    // ⚠️ NONE.TRIM() → 프로그램 중단!
        RETURN ERROR_PAGE("이름을 입력하세요.")
    RETURN SUCCESS_PAGE(username)
```

```pseudocode
// ✅ 안전한 수도 코드
FUNCTION parse_input(request):
    username = REQUEST.GET_PARAM("username")

    // NONE 체크를 먼저 수행 (단축 평가 활용)
    IF username IS NONE OR username.TRIM() == "":
        RETURN ERROR_PAGE("이름을 입력하세요.")

    username = username.TRIM()
    RETURN SUCCESS_PAGE(username)
```

> 💡 **팁:** `GET_PARAM("key", "")`처럼 기본값을 빈 문자열로 지정하면 NONE 반환을 원천적으로 방지할 수 있습니다.

```text
💬 AI에게 요청할 프롬프트

"이 코드에서 사용자 입력을 받는 부분을 점검해줘.
GET_PARAM이나 GET 메서드의 반환값이 None일 수 있는 경우를 모두 찾아서
None 체크를 추가하거나 기본값을 설정해줘."
```

---

### 14-2. 부적절한 자원 해제

#### 개요

파일, 데이터베이스 연결, 네트워크 소켓 등은 유한한 시스템 자원입니다. 사용 후 반환하지 않으면 자원이 고갈되어 새로운 요청을 처리할 수 없습니다. 중간에 예외가 발생하면 `CLOSE()` 호출에 도달하지 못하는 것이 핵심 문제입니다.

```pseudocode
// ❌ 취약한 수도 코드
FUNCTION get_config():
    TRY:
        file = OPEN("config.cfg")
        lines = file.READ_ALL_LINES()
        process_data(lines)          // ⚠️ 여기서 예외 발생 시 CLOSE()에 도달 불가!
        file.CLOSE()
        RETURN lines
    CATCH error:
        RETURN ""
```

```pseudocode
// ✅ 안전한 수도 코드

// 방법 1: WITH 문 (권장) — 블록 종료 시 자동으로 자원 해제
FUNCTION get_config():
    TRY:
        WITH file = OPEN("config.cfg"):
            lines = file.READ_ALL_LINES()
            process_data(lines)
            RETURN lines
    CATCH FileNotFound:
        LOG.error("설정 파일을 찾을 수 없습니다.")
        RETURN ""

// 방법 2: FINALLY 블록 — 예외 발생 여부와 무관하게 항상 실행
FUNCTION get_config():
    file = NONE
    TRY:
        file = OPEN("config.cfg")
        lines = file.READ_ALL_LINES()
        RETURN lines
    CATCH error:
        LOG.error("오류 발생: " + error)
        RETURN ""
    FINALLY:
        IF file IS NOT NONE:
            file.CLOSE()             // 항상 실행됨
```

> 💡 **팁:** 파일, DB 연결, 소켓 등 `CLOSE()`가 필요한 모든 자원에 `WITH` 문(컨텍스트 매니저)을 사용하는 것을 습관으로 만드십시오.

```text
💬 AI에게 요청할 프롬프트

"이 코드에서 파일, DB 연결, 소켓 등 자원을 열고 닫는 부분을 모두 찾아줘.
WITH 문(컨텍스트 매니저)으로 변환하여 예외 발생 시에도 자원이 반드시 해제되도록 수정해줘."
```

---

### 14-3. 신뢰할 수 없는 데이터의 역직렬화

#### 개요

역직렬화(Deserialization)는 바이트 스트림을 객체로 복원하는 과정입니다. 일부 직렬화 라이브러리는 복원 과정에서 임의 코드를 실행할 수 있으므로, 외부에서 전달된 데이터를 검증 없이 역직렬화하면 서버가 공격자에게 장악될 수 있습니다.

#### 왜 위험한가

AI에게 "객체를 저장하고 불러오는 코드를 만들어줘"라고 요청하면, 바이너리 직렬화 라이브러리(예: pickle)를 먼저 제안하는 경향이 있습니다. 사용자 업로드 파일, 쿠키, API 요청에 조작된 데이터가 포함되면 서버에서 공격자의 코드가 실행됩니다.

```pseudocode
// ❌ 취약한 수도 코드
FUNCTION load_user_object(request):
    user_data = REQUEST.GET_PARAM("userinfo")
    // 사용자 입력을 직접 바이너리 역직렬화 — 원격 코드 실행 위험!
    user_obj = BINARY_DESERIALIZE(user_data)
    RETURN RENDER("profile.html", user_obj)
```

```pseudocode
// ✅ 안전한 수도 코드

// 방법 1: JSON 사용 (권장) — 데이터만 파싱, 코드 실행 불가
FUNCTION load_user_object(request):
    TRY:
        user_data = REQUEST.GET_PARAM("userinfo", "{}")
        user_obj = JSON_PARSE(user_data)
        RETURN RENDER("profile.html", user_obj)
    CATCH JsonParseError:
        RETURN ERROR_PAGE("잘못된 데이터 형식입니다.")

// 방법 2: 바이너리 역직렬화가 반드시 필요한 경우 — HMAC 서명 검증
FUNCTION load_user_object(request):
    signature = REQUEST.GET_PARAM("signature")
    raw_data = REQUEST.GET_PARAM("userinfo")

    expected_sig = HMAC_SHA256(SECRET_KEY, raw_data)

    IF SECURE_COMPARE(expected_sig, signature):
        user_obj = BINARY_DESERIALIZE(raw_data)
        RETURN RENDER("profile.html", user_obj)
    ELSE:
        RETURN ERROR_PAGE("데이터 검증에 실패했습니다.")
```

> ⚠️ **주의:** 바이너리 직렬화(pickle 등)는 **신뢰할 수 없는 데이터에 대해 안전하지 않습니다**. 외부 입력에는 반드시 JSON을 사용하고, 내부 시스템 간 통신에서만 HMAC 서명 검증과 함께 사용하십시오.

```text
💬 AI에게 요청할 프롬프트

"이 코드에서 pickle, marshal 등 바이너리 역직렬화를 사용하는 부분을 모두 찾아줘.
외부 입력 데이터를 처리하는 부분은 JSON으로 대체하고,
내부용으로 꼭 필요한 부분은 HMAC 서명 검증을 추가해줘."
```

#### 체크포인트

| 점검 항목 | 확인 방법 |
|-----------|-----------|
| NONE 체크 누락 | 사용자 입력 반환값 사용 전 `IS NONE` 검사 여부 |
| 기본값 미설정 | `GET_PARAM("key")` 대신 `GET_PARAM("key", "")` 사용 여부 |
| WITH 문 사용 | 파일, DB 연결, 소켓 등에 WITH 문 사용 여부 |
| CLOSE() 누락 | FINALLY 블록 없이 OPEN 후 CLOSE를 호출하는 패턴 검색 |
| 바이너리 역직렬화 사용 | 코드베이스에서 pickle/marshal 사용 검색, 외부 데이터 처리 여부 확인 |
| JSON 대체 가능성 | 바이너리 직렬화 대신 JSON으로 대체할 수 있는지 검토 |


---

# Part 5. 구조 설계 — 수도 코드로 배우는 캡슐화와 API 보안

여러분이 AI로 빠르게 기능을 만들어도, 설계 수준의 보안을 놓치면 시스템 전체가 무너질 수 있습니다. 캡슐화 원칙을 지키지 않으면 사용자 간 데이터가 섞이고, API를 잘못 사용하면 원격 코드 실행이라는 최악의 결과를 초래합니다. 이 파트에서는 언어에 관계없이 적용할 수 있는 수도 코드(Pseudocode)로 구조 설계의 핵심 보안 원칙을 익히겠습니다.

---

## 15장. 캡슐화 — 보여서는 안 되는 것들

---

### 15-1. 잘못된 세션에 의한 데이터 정보 노출

#### 개요

다중 스레드 환경에서 클래스 변수나 전역 변수에 사용자별 데이터를 저장하면, 서로 다른 세션 간에 데이터가 공유되는 문제가 발생합니다. 사용자 A의 개인정보가 사용자 B에게 노출되는 심각한 사고로 이어질 수 있습니다.

#### 왜 위험한가

AI가 간단한 클래스 구조를 생성할 때, 데이터를 클래스 수준에 선언하는 것이 편리하다고 판단하지만 다중 스레드 환경에서의 부작용까지 고려하지 못합니다. 웹 프레임워크는 여러 요청을 동시에 처리하므로, 클래스 변수에 사용자 정보를 저장하면 한 사용자의 요청이 다른 사용자의 데이터를 덮어씁니다.

```pseudocode
// ❌ 취약한 수도 코드
CLASS UserDescription:
    // 클래스 변수 — 모든 인스턴스와 스레드가 공유!
    SHARED user_name = ""

    FUNCTION show_user_profile(request):
        // ⚠️ 스레드 A가 이름을 저장한 직후, 스레드 B가 덮어쓸 수 있음
        UserDescription.user_name = REQUEST.GET_PARAM("name", "")
        profile = GET_USER_DESCRIPTION(UserDescription.user_name)
        RETURN RENDER("profile.html", profile)
```

```pseudocode
// ✅ 안전한 수도 코드

// 방법 1: 지역 변수 사용 — 각 요청이 독립된 변수를 가짐
CLASS UserDescription:
    FUNCTION show_user_profile(request):
        LOCAL user_name = REQUEST.GET_PARAM("name", "")    // 지역 변수!
        LOCAL profile = GET_USER_DESCRIPTION(user_name)
        RETURN RENDER("profile.html", profile)

// 방법 2: 함수 기반 설계 — 클래스 변수 문제를 원천 차단
FUNCTION show_user_profile(request):
    user_name = REQUEST.GET_PARAM("name", "")
    profile = GET_USER_DESCRIPTION(user_name)
    RETURN RENDER("profile.html", profile)
```

> 💡 **팁:** 클래스 기반 설계보다 함수 기반 설계가 스레드 안전성 측면에서 더 직관적입니다. 클래스를 사용하더라도 사용자별 데이터는 반드시 지역 변수나 인스턴스 변수로 관리하십시오.

```text
💬 AI에게 요청할 프롬프트

"이 클래스에서 사용자별 데이터가 클래스 변수(static/shared)에 저장되어 있는지 점검해줘.
다중 스레드 환경에서 세션 간 데이터 오염이 발생하지 않도록
지역 변수 또는 인스턴스 변수로 변경해줘."
```

---

### 15-2. 제거되지 않고 남은 디버그 코드

#### 개요

개발 과정에서 삽입한 디버그 코드가 운영 환경에 그대로 배포되는 것은 가장 흔하면서도 가장 위험한 보안약점입니다. 디버그 출력문, 테스트 엔드포인트, 하드코딩된 테스트 계정이 여기에 해당합니다.

#### 왜 위험한가

**바이브 코딩에서 특히 높은 우선순위로 점검해야 합니다.** AI는 코드 동작을 보여주기 위해 `PRINT` 문을 자주 포함하고, "테스트 계정을 추가해줘", "디버그 모드를 켜줘" 같은 개발 중 요청에 응답한 코드가 배포본에 남는 경우가 많습니다.

디버그 코드가 남아 있으면:
- 서버 로그에 비밀번호, API 키가 평문으로 기록됩니다
- 브라우저 개발자 도구에서 인증 토큰, 내부 API 경로가 노출됩니다
- 테스트용 URL(`/debug`, `/test`)로 인증 없이 시스템에 접근할 수 있습니다
- 디버그 모드의 인터랙티브 콘솔이 서버의 완전한 제어권을 넘겨줍니다

```pseudocode
// ❌ 취약한 수도 코드

// 서버 설정
CONFIG:
    DEBUG_MODE = TRUE                              // 운영 환경에서 디버그!

// 백엔드 — 비밀번호가 로그에 기록됨
FUNCTION login(request):
    username = REQUEST.GET_PARAM("username")
    password = REQUEST.GET_PARAM("password")
    PRINT("[DEBUG] 로그인 시도: " + username + " / " + password)   // ⚠️ 비밀번호 노출!

    user = AUTHENTICATE(username, password)
    IF user EXISTS:
        RETURN JSON({status: "ok"})
    RETURN JSON({status: "fail"})

// 테스트용 엔드포인트 — 전체 사용자 목록 노출
FUNCTION debug_user_list(request):                  // ⚠️ 인증 없이 접근 가능!
    users = DATABASE.FIND_ALL("users", fields=["username", "email", "is_staff"])
    RETURN JSON(users)

// 프론트엔드 — 인증 토큰이 브라우저 콘솔에 노출
FUNCTION fetch_user_data():
    token = LOCAL_STORAGE.GET("auth_token")
    CONSOLE.LOG("DEBUG: auth token = " + token)     // ⚠️ 누구나 확인 가능!
    CONSOLE.LOG("DEBUG: API endpoint = /api/v2/internal/users")
    response = HTTP_GET("/api/v2/internal/users", headers={Authorization: token})
    RETURN response.json
```

```pseudocode
// ✅ 안전한 수도 코드

// 서버 설정
CONFIG:
    DEBUG_MODE = FALSE
    ALLOWED_HOSTS = [ENV("ALLOWED_HOST", "localhost")]

// 백엔드 — 로그에 비밀번호를 절대 포함하지 않음
FUNCTION login(request):
    username = REQUEST.GET_PARAM("username")
    password = REQUEST.GET_PARAM("password")

    LOG.info("로그인 시도: " + username)             // 비밀번호 제외!

    user = AUTHENTICATE(username, password)
    IF user EXISTS:
        LOG.info("로그인 성공: " + username)
        RETURN JSON({status: "ok"})

    LOG.warning("로그인 실패: " + username)
    RETURN JSON({status: "fail"})

// debug_user_list 엔드포인트 완전 제거!

// 프론트엔드 — CONSOLE.LOG 완전 제거
FUNCTION fetch_user_data():
    token = LOCAL_STORAGE.GET("auth_token")
    response = HTTP_GET("/api/v2/internal/users", headers={Authorization: token})
    RETURN response.json
```

> ⚠️ **주의:** 배포 전 다음 키워드로 코드베이스를 반드시 검색하십시오: `PRINT(`, `CONSOLE.LOG(`, `DEBUG = TRUE`, `/debug`, `/test`, `TODO`, `FIXME`, `HACK`. CI/CD 파이프라인에 이 검사를 자동화하면 디버그 코드가 실수로 배포되는 것을 방지할 수 있습니다.

```text
💬 AI에게 요청할 프롬프트

"이 프로젝트의 코드베이스 전체에서 디버그 코드를 점검해줘.
1) print/console.log 문에서 민감 정보(비밀번호, 토큰, 키)가 출력되는 부분
2) /debug, /test 같은 테스트 엔드포인트
3) DEBUG = True 설정
4) 하드코딩된 테스트 계정
을 모두 찾아서 제거하거나 안전한 로깅으로 교체해줘."
```

---

> **기타 캡슐화 이슈: Private 배열의 참조 공유 문제**
>
> private 배열을 public 메서드에서 직접 반환하면 외부에서 원본 배열을 수정할 수 있습니다. 마찬가지로 외부 데이터를 private 배열에 직접 대입하면 외부 참조를 통해 내부 상태가 변경됩니다.
>
> ```pseudocode
> // ❌ 취약: 원본 참조를 그대로 반환
> CLASS SecureList:
>     PRIVATE data = []
>
>     FUNCTION get_data():
>         RETURN this.data              // 외부에서 원본 수정 가능!
>
>     FUNCTION set_data(input_list):
>         this.data = input_list        // 외부 참조와 연결됨!
>
> // ✅ 안전: 복사본을 반환·저장
> CLASS SecureList:
>     PRIVATE data = []
>
>     FUNCTION get_data():
>         RETURN COPY(this.data)        // 복사본 반환
>
>     FUNCTION set_data(input_list):
>         this.data = COPY(input_list)  // 복사본 저장
> ```
>
> 바이브 코딩에서는 AI가 생성한 클래스 코드에서 mutable 객체(리스트, 딕셔너리, 맵)의 참조 공유 문제를 반드시 점검하십시오.

#### 체크포인트

| 점검 항목 | 확인 방법 |
|-----------|-----------|
| 클래스 변수에 사용자 데이터 저장 | 클래스 정의에서 사용자별 데이터가 SHARED/static으로 선언되었는지 확인 |
| 전역 변수 사용 | GLOBAL 키워드 또는 모듈 수준 변수에 요청별 데이터 저장 여부 |
| PRINT 문 잔존 | 코드 전체에서 PRINT 검색, 특히 비밀번호/토큰/키 관련 출력 |
| CONSOLE.LOG 잔존 | 프론트엔드 파일에서 CONSOLE.LOG 검색 |
| DEBUG = TRUE 설정 | 설정 파일 확인 |
| 디버그 엔드포인트 | URL 라우팅에서 /debug, /test 등 테스트용 경로 확인 |
| Private 배열 참조 공유 | mutable 객체를 반환/대입할 때 복사본 사용 여부 확인 |
| CI/CD 자동 검사 | 배포 파이프라인에 디버그 코드 탐지 스크립트 포함 여부 |

---

## 16장. API 오용 — 편리함 뒤에 숨은 위험

---

### 16-1. 취약한 API 사용

#### 개요

취약한 API란 보안상 사용이 금지되었거나 유지보수가 중단된 함수 및 패키지, 또는 부주의하게 사용될 가능성이 높은 API를 의미합니다. AI의 학습 데이터에는 오래된 코드가 포함되어 있어 이미 취약점이 발견된 구 버전의 API를 사용하거나, 더 안전한 대안이 있는데도 레거시 방식의 코드를 생성할 수 있습니다.

#### 왜 위험한가

대표적인 위험 사례:
- `YAML_LOAD()`: 임의 코드 실행이 가능 -> `YAML_SAFE_LOAD()`로 대체 필수
- `MD5`, `SHA1` 해시: 충돌 공격에 취약 -> 비밀번호에는 `BCRYPT`/`ARGON2` 사용
- `EVAL()`, `EXEC()`: 문자열을 코드로 실행 -> 외부 입력과 결합 시 원격 코드 실행
- 오래된 패키지 버전: 알려진 CVE 취약점이 포함된 채 사용

```pseudocode
// ❌ 취약한 수도 코드

// 1. 위험한 설정 파일 파싱
FUNCTION load_config(path):
    WITH file = OPEN(path):
        config = YAML_LOAD(file)       // ⚠️ 임의 코드 실행 가능!
    RETURN config

// 2. 취약한 해시 함수
FUNCTION hash_password(password):
    RETURN MD5_HASH(password)          // ⚠️ 충돌 공격에 취약!

// 3. 위험한 동적 실행
FUNCTION calculate(expression):
    result = EVAL(expression)          // ⚠️ 원격 코드 실행 가능!
    RETURN result

// 4. 오래된 패키지 의존
DEPENDENCIES:
    WebFramework == 2.2.0             // 알려진 보안 취약점 다수
    HTTPClient == 2.20.0              // CVE 취약점 포함
    ImageLibrary == 6.0.0             // 버퍼 오버플로우 취약점
```

```pseudocode
// ✅ 안전한 수도 코드

// 1. 안전한 설정 파일 파싱
FUNCTION load_config(path):
    WITH file = OPEN(path):
        config = YAML_SAFE_LOAD(file)  // 기본 데이터 타입만 허용
    RETURN config

// 2. 안전한 비밀번호 해싱
FUNCTION hash_password(password):
    salt = GENERATE_RANDOM_SALT()
    RETURN BCRYPT_HASH(password, salt)  // 충돌 공격에 안전

FUNCTION verify_password(password, stored_hash):
    RETURN BCRYPT_VERIFY(password, stored_hash)

// 3. 안전한 수식 평가
FUNCTION calculate(expression):
    TRY:
        result = SAFE_LITERAL_EVAL(expression)   // 리터럴만 평가, 코드 실행 불가
        RETURN result
    CATCH InvalidSyntax:
        RETURN NONE

// 4. 최신 안정 버전 사용
DEPENDENCIES:
    WebFramework >= 4.2, < 5.0        // 보안 패치가 적용된 최신 버전
    HTTPClient >= 2.31.0
    ImageLibrary >= 10.0.0
```

#### 안전한 패키지 선택 기준

AI가 제안한 패키지를 사용하기 전에 다음 항목을 확인하십시오:

1. **사용 통계**: 다운로드 수, GitHub 스타 수 확인
2. **이슈 관리**: 버그와 보안 이슈가 적시에 처리되고 있는지 확인
3. **마지막 업데이트**: 최근 6개월 이내 업데이트 여부 확인
4. **알려진 취약점**: NVD, CVEdetails에서 패키지명으로 검색

> 💡 **팁:** CI/CD 파이프라인에 패키지 취약점 검사 도구(`pip-audit`, `safety check`, `npm audit` 등)를 포함시키면, 취약한 패키지가 배포되기 전에 자동으로 차단할 수 있습니다. GitHub Dependabot이나 Snyk 같은 서비스도 활용하십시오.

```text
💬 AI에게 요청할 프롬프트

"이 프로젝트의 코드와 의존성 파일을 점검해줘.
1) yaml.load, eval, exec, pickle.loads 등 위험한 API 사용을 찾아 안전한 대안으로 교체해줘.
2) md5, sha1 해시를 비밀번호에 사용하고 있으면 bcrypt/argon2로 변경해줘.
3) requirements.txt / package.json의 패키지 버전이 오래되었으면 최신 안정 버전으로 업데이트해줘.
4) pip-audit 또는 safety check를 실행하여 알려진 취약점을 보고해줘."
```

---

> **기타 API 주의사항: DNS lookup에 의존한 보안 결정**
>
> 도메인명을 기반으로 접근 제어나 인증을 수행하면 DNS 스푸핑 공격에 취약합니다. 공격자가 DNS 캐시를 오염시키면 신뢰할 수 없는 서버가 정상 서버로 위장할 수 있습니다.
>
> ```pseudocode
> // ❌ 취약: 도메인명으로 보안 결정
> FUNCTION check_access(hostname):
>     resolved_ip = DNS_LOOKUP(hostname)          // DNS 스푸핑 가능!
>     IF hostname == "trusted-server.com":
>         ALLOW_ACCESS()
>
> // ✅ 안전: IP 주소 직접 비교 + TLS 인증서 검증
> FUNCTION check_access(client_ip):
>     IF client_ip IN TRUSTED_IP_LIST:
>         VERIFY_TLS_CERTIFICATE(client_ip)       // 인증서로 신원 확인
>         ALLOW_ACCESS()
> ```
>
> 바이브 코딩에서 AI가 `DNS_LOOKUP()`의 결과를 보안 판단에 사용하는 코드를 생성하면 주의 깊게 검토하십시오. 보안 결정에는 IP 주소 직접 비교 또는 TLS 인증서 검증을 사용해야 합니다.

#### 체크포인트

| 점검 항목 | 확인 방법 |
|-----------|-----------|
| YAML_LOAD 사용 여부 | YAML_SAFE_LOAD로 대체 |
| EVAL, EXEC 사용 여부 | SAFE_LITERAL_EVAL 또는 안전한 대안으로 대체 |
| MD5, SHA1 해시 사용 | 비밀번호에는 BCRYPT/ARGON2, 무결성에는 SHA256 이상 |
| 바이너리 역직렬화 사용 | JSON으로 대체하거나 HMAC 검증 추가 |
| 패키지 버전 고정 | 의존성 파일에 최소 버전 명시, 주기적 업데이트 |
| 패키지 취약점 검사 | pip-audit, safety check, npm audit 실행 |
| Deprecated API 사용 | 공식 문서에서 대체 API 확인 |
| DNS 기반 보안 결정 | 도메인명 대신 IP 주소 비교 또는 TLS 인증서 검증 사용 |
| SBOM 관리 | 프로젝트에 사용된 모든 외부 의존성 목록 관리 |


---

# PART 6: 바이브 코딩 보안 체크리스트

# Chapter 17

---

## 17-1. 배포 전 보안 체크리스트

> **[참고 다이어그램] 바이브 코딩 배포 전 보안 체크 플로우차트**

# 다이어그램 8: 바이브 코딩 보안 체크 플로우차트

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
│  │ ② .env 파일에 시크릿 분리했는가?   │─ No ─▶│ [수정 필요]│ │
│  │    (API키, DB비번, 토큰 등)        │       │ 하드코딩된 시크릿│ │
│  └──────────────┬──────────────────────┘       │ .env로 분리      │ │
│            Yes  │                              └──────────────────┘ │
│                 ▼                                                    │
│  ┌─────────────────────────────────────┐       ┌──────────────────┐ │
│  │ ③ 입력값 검증이 있는가?            │─ No ─▶│ [수정 필요]│ │
│  │    (SQL, XSS, 경로 조작 방어)      │       │ 모든 사용자 입력 │ │
│  └──────────────┬──────────────────────┘       │ 검증 로직 추가   │ │
│            Yes  │                              └──────────────────┘ │
│                 ▼                                                    │
│  ┌─────────────────────────────────────┐       ┌──────────────────┐ │
│  │ ④ 인증/인가가 적용되었는가?        │─ No ─▶│ [수정 필요]│ │
│  │    (로그인 + 권한 확인)            │       │ 인증/인가 미들웨 │ │
│  └──────────────┬──────────────────────┘       │ 어 적용          │ │
│            Yes  │                              └──────────────────┘ │
│                 ▼                                                    │
│  ┌─────────────────────────────────────┐       ┌──────────────────┐ │
│  │ ⑤ DEBUG=False 설정했는가?          │─ No ─▶│ [수정 필요]│ │
│  │    (프로덕션 환경 설정)            │       │ DEBUG=False 설정 │ │
│  └──────────────┬──────────────────────┘       │ 환경변수 분리    │ │
│            Yes  │                              └──────────────────┘ │
│                 ▼                                                    │
│  ┌─────────────────────────────────────┐       ┌──────────────────┐ │
│  │ ⑥ 에러 메시지에 민감정보 없는가?   │─ No ─▶│ [수정 필요]│ │
│  │    (스택트레이스, DB정보 노출)      │       │ 사용자에게 일반  │ │
│  └──────────────┬──────────────────────┘       │ 에러 메시지 반환 │ │
│            Yes  │                              └──────────────────┘ │
│                 ▼                                                    │
│  ┌─────────────────────────────────────┐       ┌──────────────────┐ │
│  │ ⑦ 보안 헤더 설정했는가?            │─ No ─▶│ [수정 필요]│ │
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
