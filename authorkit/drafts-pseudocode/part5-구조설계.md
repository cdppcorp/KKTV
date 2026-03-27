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
