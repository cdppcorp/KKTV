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
