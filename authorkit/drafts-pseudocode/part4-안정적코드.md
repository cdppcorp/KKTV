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
