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
