---
name: start
description: 47개 CWE 매핑 시큐어코딩 규칙으로 프로젝트 전체 보안 감사를 수행합니다. 요약 보고서 + 카테고리별 상세 보고서를 별도 파일로 생성하여 읽기 편하게 제공합니다. "보안 검토 시작", "보안 스캔", "코드 감사", "취약점 확인" 시 사용.
---

# 보안 감사 스킬

당신은 시큐어 코드 감사관입니다. 현재 프로젝트를 7개 카테고리 47개 시큐어코딩 규칙에 따라 스캔하고, **요약 보고서** + **카테고리별 상세 보고서**를 별도 마크다운 파일로 생성하십시오.

## 보고서 출력 구조

프로젝트 루트의 `reports/security/` 에 저장합니다:

```
reports/security/
├── summary.md                      ← 한눈에 보는 요약 (합격률, 심각도별 건수, TOP 5)
├── cat1-입력검증.md                 ← 카테고리 1: 입력데이터 검증 및 표현 (18개 규칙)
├── cat2-보안기능.md                 ← 카테고리 2: 보안기능 (16개 규칙)
├── cat3-시간상태.md                 ← 카테고리 3: 시간 및 상태 (2개 규칙)
├── cat4-에러처리.md                 ← 카테고리 4: 에러처리 (3개 규칙)
├── cat5-코드품질.md                 ← 카테고리 5: 코드오류 (3개 규칙)
├── cat6-캡슐화.md                   ← 카테고리 6: 캡슐화 (2개 규칙)
└── cat7-API오용.md                  ← 카테고리 7: API 오용 (3개 규칙)
```

### summary.md 형식:
- 프로젝트명, 기술 스택, 스캔 일시
- 전체 합격률 (시각적 막대)
- 심각도별 분류: HIGH / MEDIUM / LOW 건수
- 가장 긴급한 5개 발견 항목 (파일:줄 포함 한 줄 요약)
- 카테고리별 합격률
- 각 카테고리 파일로의 링크

### 카테고리 파일 형식:
- 카테고리명 및 설명
- 각 규칙: ID, 이름, CWE, 심각도, 합격/불합격/해당없음 상태
- 불합격 항목: 파일:줄, 취약 코드 스니펫, 수정 권고
- 카테고리 하단에 소결

모든 파일 작성 후 summary.md 내용을 사용자에게 직접 보여주십시오.

---

## 1단계: 프로젝트 언어 및 프레임워크 감지

스캔 전에 프로젝트의 기술 스택을 식별하세요:

1. Glob 도구를 사용하여 설정 파일을 찾으세요: `package.json`, `requirements.txt`, `Pipfile`, `Cargo.toml`, `go.mod`, `pom.xml`, `build.gradle`, `Gemfile`, `composer.json`, `*.csproj`, `pubspec.yaml`
2. Glob으로 소스 파일을 찾으세요: `**/*.py`, `**/*.js`, `**/*.ts`, `**/*.java`, `**/*.go`, `**/*.rb`, `**/*.php`, `**/*.rs`, `**/*.cs`, `**/*.dart`
3. 프레임워크 지표를 확인하세요:
   - Python: `manage.py` (Django), `app.py`/`wsgi.py` (Flask), `main.py` (FastAPI)
   - JavaScript/TypeScript: `next.config.*` (Next.js), `nuxt.config.*` (Nuxt), `angular.json` (Angular), `vite.config.*`, package.json 내 `express`
   - Java: `@SpringBootApplication` (Spring Boot)
   - Go: `gin`, `echo`, `fiber` imports
   - Ruby: `config/routes.rb` (Rails)
   - PHP: `artisan` (Laravel)
4. 감지된 언어, 프레임워크, 스캔 대상 소스 파일 목록을 기록하세요.

---

## 2단계: 47개 취약점 규칙에 따라 스캔

모든 소스 파일을 아래 7개 카테고리 47개 규칙에 따라 스캔하세요. Grep과 Read 도구를 사용하여 취약한 패턴을 검색하세요.

### 카테고리 1: 입력값 검증 및 표현 (18개 항목)

**SR-01: SQL 삽입 (CWE-89)**
- 검색 대상: SQL 쿼리에서의 문자열 결합, f-string 쿼리, `+` 연산자로 SQL 구성, `.format()` 사용, 매개변수 바인딩 없는 raw SQL
- 취약 패턴: `"SELECT * FROM users WHERE id='" + user_input + "'"`, `f"SELECT * FROM users WHERE id={user_id}"`, `query = "... %s ..." % variable`
- 안전 패턴: `?` 또는 `%s` 플레이스홀더와 별도 바인딩을 사용하는 매개변수화된 쿼리, `.filter()`, `.where()`, `.find()` 등 ORM 쿼리 빌더
- 심각도: HIGH

**SR-02: LDAP 삽입 (CWE-90)**
- 검색 대상: 문자열 결합으로 구성된 LDAP 쿼리, LDAP 필터에서 이스케이프되지 않은 사용자 입력
- 취약 패턴: `"(uid=" + username + ")"`, 변수를 직접 삽입한 LDAP 필터 문자열
- 안전 패턴: 사용자 입력에 LDAP 이스케이프 함수 적용, 매개변수화된 LDAP 쿼리
- 심각도: HIGH

**SR-03: 코드 삽입 (CWE-94)**
- 검색 대상: `eval()`, `exec()`, `Function()` 생성자, `setTimeout(문자열)`, `setInterval(문자열)`, 사용자 입력을 이용한 동적 코드 실행
- 취약 패턴: `eval(user_input)`, `exec(user_code)`, `new Function(user_string)`
- 안전 패턴: `eval`/`exec` 완전 배제, AST 파싱 사용, 안전한 표현식 평가기 사용
- 심각도: HIGH

**SR-04: 운영체제 명령어 삽입 (CWE-78)**
- 검색 대상: `os.system()`, `subprocess.call(shell=True)`, `child_process.exec()`, `Runtime.exec()`, 사용자 입력을 포함한 백틱 실행
- 취약 패턴: `os.system("ping " + user_ip)`, `exec("ls " + user_path)`, 검증되지 않은 입력과 함께 shell=True
- 안전 패턴: 인자 리스트를 사용하는 `subprocess.run()` (shell=True 없이), 허용 목록 명령어 검증, `shlex.quote()` 이스케이프
- 심각도: HIGH

**SR-05: XML 삽입 (CWE-91)**
- 검색 대상: 결합으로 구성된 XML 문자열, XML 문서에 직접 삽입된 사용자 입력
- 취약 패턴: `"<user>" + username + "</user>"`, 이스케이프되지 않은 입력으로 구성된 XML
- 안전 패턴: XML 빌더 라이브러리, 특수 문자(`<`, `>`, `&`, `"`, `'`) 적절한 이스케이프
- 심각도: MEDIUM

**SR-06: 포맷 스트링 삽입 (CWE-134)**
- 검색 대상: 사용자 제어 포맷 문자열, 사용자 입력을 포맷 문자열로 사용하는 `printf` 스타일 포매팅
- 취약 패턴: `printf(user_input)`, `String.format(user_input)`, 포맷 지정자가 포함된 `logging.info(user_input)`
- 안전 패턴: 고정 포맷 문자열에 사용자 입력은 인자로만 전달
- 심각도: MEDIUM

**SR-07: 크로스사이트 스크립트 / XSS (CWE-79)**
- 검색 대상: HTML 출력에서 이스케이프되지 않은 사용자 입력, `innerHTML`, `dangerouslySetInnerHTML`, `v-html`, `|safe` 필터, `{% autoescape off %}`, Blade의 `{!! !!}`
- 취약 패턴: `document.innerHTML = user_input`, `<div dangerouslySetInnerHTML={{__html: userInput}}>`, 자동 이스케이프 없는 템플릿 렌더링
- 안전 패턴: 자동 이스케이프 템플릿 엔진, `innerHTML` 대신 `textContent`, 새니타이제이션 라이브러리 (DOMPurify), Content-Security-Policy 헤더
- 심각도: HIGH

**SR-08: 크로스사이트 요청 위조 / CSRF (CWE-352)**
- 검색 대상: CSRF 토큰 없는 POST/PUT/DELETE 폼, 상태 변경하는 GET 요청, 비활성화된 CSRF 미들웨어
- 취약 패턴: csrf_token 없는 `<form method="POST">`, `@csrf_exempt`, `csrf: false`, 주석 처리되거나 제거된 CSRF 미들웨어
- 안전 패턴: 모든 상태 변경 폼에 CSRF 토큰, SameSite 쿠키 속성, 프레임워크 CSRF 미들웨어 활성화
- 심각도: HIGH

**SR-09: 서버사이드 요청 위조 / SSRF (CWE-918)**
- 검색 대상: 검증 없이 사용자 제공 URL로 HTTP 요청, `requests.get(user_url)`, `fetch(user_url)`, `urllib.urlopen(user_url)`
- 취약 패턴: 사용자 입력에서 임의 URL 가져오기, 도메인 허용 목록 없음
- 안전 패턴: URL 허용 목록 검증, 사설 IP 범위 차단 (10.x, 172.16-31.x, 192.168.x, 127.x, 169.254.x), DNS 리바인딩 보호
- 심각도: HIGH

**SR-10: HTTP 응답 분할 (CWE-113)**
- 검색 대상: 새니타이제이션 없이 HTTP 헤더에 사용자 입력, 헤더 값의 개행 문자
- 취약 패턴: `\r\n` 제거 없이 `response.setHeader("Location", user_input)`
- 안전 패턴: 헤더 값에서 개행 문자 제거/거부, 프레임워크의 헤더 설정 함수 사용
- 심각도: MEDIUM

**SR-11: 경로 조작 (CWE-22)**
- 검색 대상: 사용자 입력을 경로에 사용하는 파일 작업, `../` 미차단, 검증 없이 사용자 입력과 함께 `os.path.join`
- 취약 패턴: `open("/uploads/" + filename)`, 정규화 없이 사용자 제어 컴포넌트로 경로 구성
- 안전 패턴: `os.path.realpath()` + 접두사 확인, basename 추출, 허용된 디렉토리 허용 목록
- 심각도: HIGH

**SR-12: 위험한 형식 파일 업로드 (CWE-434)**
- 검색 대상: 파일 업로드 엔드포인트, 파일 유형 검증 누락, 파일 크기 제한 누락, 실행 가능한 업로드 경로
- 취약 패턴: 모든 파일 확장자 허용, 원본 이름으로 웹 접근 가능 디렉토리에 업로드 저장, MIME 타입 확인 없음
- 안전 패턴: 확장자 허용 목록, MIME 타입 검증, 파일 크기 제한, 랜덤 파일명 생성, 웹 루트 외부 저장
- 심각도: HIGH

**SR-13: 오픈 리다이렉트 (CWE-601)**
- 검색 대상: 사용자 입력에서 리다이렉트 URL, `redirect(request.params["url"])`, 사용자 입력에서 `Location` 헤더
- 취약 패턴: 검증 없이 `return redirect(request.GET["next"])`
- 안전 패턴: 허용된 리다이렉트 도메인 허용 목록, 상대 경로만 허용, URL 파싱 및 도메인 확인
- 심각도: MEDIUM

**SR-14: XML 외부 개체 / XXE (CWE-611)**
- 검색 대상: 외부 엔터티 비활성화 없는 XML 파싱, `XMLParser`, `DocumentBuilder`, 보안 플래그 없는 `lxml.etree.parse`
- 취약 패턴: 기본 XML 파서 설정, DTD 처리 활성화
- 안전 패턴: `defusedxml` (Python), 파서 설정에서 DTD/외부 엔터티 비활성화, `FEATURE_SECURE_PROCESSING`
- 심각도: HIGH

**SR-15: 정수형 오버플로우 (CWE-190)**
- 검색 대상: 오버플로우 검사 없는 산술 연산, 큰 숫자의 검증 없는 타입 캐스팅, 크기 계산
- 취약 패턴: 오버플로우 검사 없는 곱셈, 큰 값을 작은 정수 타입으로 캐스팅
- 안전 패턴: 오버플로우 안전 산술 함수, 산술 전 범위 검증, 큰 정수 타입 사용
- 심각도: MEDIUM

**SR-16: 보안기능 결정에 부적절한 입력값 (CWE-807)**
- 검색 대상: 클라이언트 제어 값(쿠키, 히든 필드, HTTP 헤더, user-agent)에 기반한 보안 결정
- 취약 패턴: `if request.headers["X-Role"] == "admin"`, 클라이언트 측 역할/권한 주장 신뢰
- 안전 패턴: 서버 측 세션/토큰 검증, 서버 측 세션에 역할 저장, 서명 검증이 있는 JWT
- 심각도: HIGH

**SR-17: 메모리 버퍼 오버플로우 (CWE-120)**
- 검색 대상: C/C++/Rust unsafe 블록에서의 안전하지 않은 버퍼 연산, `strcpy`, `strcat`, `sprintf`, `gets`, 검증 없는 입력의 고정 크기 버퍼
- 취약 패턴: `strcpy(buffer, user_input)`, `gets(buffer)`, 길이 확인 없는 `sprintf(buf, "%s", input)`
- 안전 패턴: `strncpy`, `snprintf`, 경계가 있는 버퍼 연산, Rust 안전 문자열 타입
- 심각도: HIGH

**SR-18: 미검증 입력 (일반) (CWE-20)**
- 검색 대상: 검증 없이 요청 매개변수를 사용하는 엔드포인트, 타입 확인 누락, 길이 제한 누락, 형식 검증 누락
- 취약 패턴: 검증 없이 `request.body` / `request.params` 직접 사용
- 안전 패턴: 입력 검증 라이브러리 (Joi, Zod, Pydantic, marshmallow), 타입 확인, 길이 제한, 형식 정규식
- 심각도: MEDIUM

### 카테고리 2: 보안 기능 (16개 항목)

**SR-19: 적절한 인증 없이 중요 기능 허용 (CWE-306)**
- 검색 대상: 인증 미들웨어 없는 관리자/관리 엔드포인트, 민감한 작업을 위한 보호되지 않은 API 라우트
- 취약 패턴: `@login_required`, `@auth` 또는 인증 미들웨어 없는 관리자 라우트; 공개된 직접 데이터베이스 수정 엔드포인트
- 안전 패턴: 모든 민감한 라우트에 인증 미들웨어/데코레이터, 중앙화된 인증 확인
- 심각도: HIGH

**SR-20: 부적절한 인가 (CWE-285)**
- 검색 대상: 인증 후 역할/권한 확인 누락, 수평적 권한 상승 (사용자가 다른 사용자 데이터 접근)
- 취약 패턴: 요청자가 해당 리소스를 소유하는지 확인 없이 `get_user(request.params["user_id"])`
- 안전 패턴: `request.user.id == resource.owner_id` 확인, 역할 기반 접근 제어 (RBAC), 정책 기반 인가
- 심각도: HIGH

**SR-21: 중요한 자원에 대한 잘못된 권한 설정 (CWE-732)**
- 검색 대상: 모든 사용자가 읽을 수 있는 파일 권한, 과도하게 허용적인 CORS, `chmod 777`, `0o777`, 퍼블릭 S3 버킷, 허용적인 ACL
- 취약 패턴: `os.chmod(file, 0o777)`, `CORS(origins="*")`, 인증된 API에 대한 `Access-Control-Allow-Origin: *`
- 안전 패턴: 최소 권한 원칙, 제한적 파일 권한 (0o600, 0o644), 특정 CORS 출처
- 심각도: MEDIUM

**SR-22: 취약한 암호화 알고리즘 사용 (CWE-327)**
- 검색 대상: 비밀번호 해싱에 MD5, SHA1, DES, RC4, ECB 모드, 커스텀 암호화 알고리즘
- 취약 패턴: `hashlib.md5(password)`, `SHA1`, `DES`, `AES-ECB`, `RC4`
- 안전 패턴: 비밀번호에 bcrypt/scrypt/Argon2, 암호화에 AES-256-GCM, 무결성에 SHA-256+
- 심각도: HIGH

**SR-23: 암호화되지 않은 중요정보 (CWE-311)**
- 검색 대상: 데이터베이스에 평문 비밀번호, HTTP를 통해 전송되는 민감 데이터, 암호화되지 않은 PII 저장
- 취약 패턴: `user.password = plain_password`, 평문으로 저장된 신용카드 번호, 민감 데이터를 위한 HTTP 전용 API
- 안전 패턴: 저장 시 암호화 (AES-256), 전송 시 암호화 (TLS/HTTPS), PII에 대한 필드 수준 암호화
- 심각도: HIGH

**SR-24: 하드코딩된 중요정보 (CWE-798)**
- 검색 대상: 소스코드에 하드코딩된 API 키, 비밀번호, 토큰, 시크릿 키; `password = "..."`, `api_key = "..."`, `secret = "..."`, `token = "..."` 패턴과 일치하는 문자열
- 취약 패턴: `SECRET_KEY = "my-secret-key"`, `DB_PASSWORD = "admin123"`, `API_KEY = "sk-..."`, `token = "ghp_..."`, 코드 내 AWS 액세스 키
- 안전 패턴: 환경 변수 (`os.environ`, `process.env`), `.env` 파일 (`.gitignore`에 포함), 시크릿 관리자 (AWS Secrets Manager, HashiCorp Vault)
- 심각도: HIGH

**SR-25: 충분하지 않은 키 길이 (CWE-326)**
- 검색 대상: 2048비트 미만 RSA 키, 128비트 미만 AES 키, 256비트 미만 HMAC 키, 짧은 JWT 시크릿
- 취약 패턴: `RSA(1024)`, `AES-64`, 짧은 문자열 JWT 시크릿 (32자 미만)
- 안전 패턴: RSA >= 2048비트, AES >= 128비트 (256 권장), HMAC >= 256비트
- 심각도: MEDIUM

**SR-26: 적절하지 않은 난수 값 사용 (CWE-330)**
- 검색 대상: 보안 목적(토큰, 비밀번호, 세션 ID, OTP)에 `Math.random()`, `random.random()`, `rand()` 사용
- 취약 패턴: `token = Math.random().toString(36)`, OTP에 `random.randint()`, 세션 ID에 `rand()`
- 안전 패턴: `crypto.randomBytes()`, `secrets.token_hex()`, `SecureRandom`, `/dev/urandom`, `crypto.getRandomValues()`
- 심각도: HIGH

**SR-27: 취약한 패스워드 허용 (CWE-521)**
- 검색 대상: 길이/복잡성 요구사항 없는 비밀번호 필드, 비밀번호 검증 로직 없음
- 취약 패턴: 모든 문자열을 비밀번호로 허용, 최소 길이 < 8, 복잡성 요구사항 없음
- 안전 패턴: 최소 8자 이상, 대소문자 + 숫자 + 특수문자 혼합 요구, 유출된 비밀번호 목록 대조
- 심각도: MEDIUM

**SR-28: 솔트 없는 일방향 해시 함수 사용 (CWE-759)**
- 검색 대상: 솔트 없는 비밀번호 해싱, `SHA256(password)` 직접 사용, `hashlib.sha256(password.encode())`
- 취약 패턴: `hash = SHA256(password)`, 솔트 없는 `hashlib.sha256(password)`
- 안전 패턴: bcrypt (내장 솔트 포함), 랜덤 솔트가 있는 `hashlib.pbkdf2_hmac()`, Argon2
- 심각도: HIGH

**SR-29: 반복된 인증시도 제한 기능 부재 (CWE-307)**
- 검색 대상: 속도 제한 없는 로그인 엔드포인트, 계정 잠금 없음, 실패 후 CAPTCHA 없음
- 취약 패턴: 속도 제한 미들웨어 없는 로그인 엔드포인트, 무제한 재시도 허용
- 안전 패턴: 속도 제한 미들웨어 (express-rate-limit, django-ratelimit), N회 실패 후 계정 잠금, 반복 실패 시 CAPTCHA
- 심각도: MEDIUM

**SR-30: 부적절한 전자서명 확인 (CWE-347)**
- 검색 대상: 알고리즘 지정 없는 JWT 검증, 우회 가능한 서명 검증, `algorithms=["none"]`
- 취약 패턴: `jwt.decode(token, verify=False)`, `jwt.decode(token, algorithms=["none", "HS256"])`, 서명 확인 누락
- 안전 패턴: 명시적 알고리즘 지정, 항상 서명 검증, `none` 알고리즘 거부
- 심각도: HIGH

**SR-31: 부적절한 인증서 유효성 검증 (CWE-295)**
- 검색 대상: HTTP 요청에서 `verify=False`, SSL 검증 비활성화, `NODE_TLS_REJECT_UNAUTHORIZED=0`, `rejectUnauthorized: false`
- 취약 패턴: `requests.get(url, verify=False)`, `process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0"`, `ssl: { rejectUnauthorized: false }`
- 안전 패턴: 항상 SSL 인증서 검증, 시스템 CA 번들 사용, 중요 서비스에 인증서 피닝
- 심각도: HIGH

**SR-32: 무결성 검사 없는 코드 다운로드 (CWE-494)**
- 검색 대상: 해시 검증 없이 URL에서 스크립트/코드 다운로드, `curl | bash`, SRI 없는 CDN 리소스
- 취약 패턴: `integrity` 속성 없는 `<script src="https://cdn.example.com/lib.js">`, `curl https://... | sh`
- 안전 패턴: 서브리소스 무결성(SRI) 해시, 패키지 잠금 파일, 실행 전 해시 검증
- 심각도: MEDIUM

**SR-33: 쿠키를 통한 정보 노출 (CWE-539)**
- 검색 대상: `Secure`, `HttpOnly`, `SameSite` 플래그 없는 쿠키; 쿠키에 저장된 민감 데이터
- 취약 패턴: `Set-Cookie: session=abc123` (플래그 없음), 쿠키에 사용자 역할/PII 저장
- 안전 패턴: `Secure; HttpOnly; SameSite=Strict`, 쿠키에 세션 ID만 저장, 서버 측 세션 저장소
- 심각도: MEDIUM

**SR-34: 주석문 안에 포함된 시스템 주요정보 (CWE-615)**
- 검색 대상: 코드 주석에 비밀번호, API 키, 인증정보가 있는 TODO, 내부 URL, 데이터베이스 연결 문자열
- 취약 패턴: `// password: admin123`, `// TODO: 이 API 키 제거`, `/* DB: mysql://root:pass@... */`
- 안전 패턴: 주석에 비밀정보 없음, 시크릿 관리 도구 사용, 배포 전 TODO 주석 정리
- 심각도: MEDIUM

### 카테고리 3: 시간 및 상태 (2개 항목)

**SR-35: TOCTOU 경쟁 조건 (CWE-367)**
- 검색 대상: 파일 존재 확인 후 파일 작업, 권한 확인 후 접근, 잠금 없는 확인-후-실행 패턴
- 취약 패턴: `if file_exists(path): open(path)`, 원자적 연산 없이 `if user.has_permission(): do_action()`
- 안전 패턴: 원자적 파일 연산, 잠금이 있는 데이터베이스 트랜잭션, 낙관적 동시성 제어
- 심각도: MEDIUM

**SR-36: 종료되지 않는 반복문 또는 재귀 함수 (CWE-835)**
- 검색 대상: 명확한 종료 없는 while/for 루프, 기저 조건 제한 없는 재귀 함수, 루프에 타임아웃 없음
- 취약 패턴: break 조건 없는 `while True:`, 깊이 제한 없는 재귀, 루프 카운터 경계 누락
- 안전 패턴: 명시적 루프 경계, 재귀 깊이 제한, 타임아웃 메커니즘, 최대 반복 횟수
- 심각도: MEDIUM

### 카테고리 4: 에러 처리 (3개 항목)

**SR-37: 오류 메시지 정보 노출 (CWE-209)**
- 검색 대상: 사용자에게 반환되는 상세 에러 메시지, API 응답의 스택 트레이스, 클라이언트에 노출되는 데이터베이스 에러
- 취약 패턴: `return {"error": str(exception)}`, `res.status(500).send(err.stack)`, 프로덕션에서 `DEBUG = True`
- 안전 패턴: 사용자에게 일반적인 에러 메시지, 서버 측에서만 상세 로깅, 커스텀 에러 페이지, `DEBUG = False`
- 심각도: MEDIUM

**SR-38: 오류 상황 대응 부재 (CWE-390)**
- 검색 대상: 빈 catch 블록, 무시된 예외, I/O 연산 주변 에러 처리 없음, try/catch 없는 데이터베이스 호출
- 취약 패턴: `except: pass`, `catch(e) {}`, 파일/네트워크/DB 연산 주변에 try/catch 없음
- 안전 패턴: 모든 catch 블록에 의미 있는 에러 처리, 에러 로깅, 우아한 기능 저하
- 심각도: MEDIUM

**SR-39: 부적절한 예외 처리 (CWE-396)**
- 검색 대상: 과도하게 넓은 catch 블록 (`catch(Exception)`, `except Exception`), 모든 에러를 잡아서 무시
- 취약 패턴: `except Exception as e: pass`, `catch(Exception e) { return null; }`, 특정 에러를 숨기는 일반적 catch
- 안전 패턴: 특정 예외 잡기, 각 예외 유형에 맞게 처리, 알 수 없는 예외 다시 발생
- 심각도: LOW

### 카테고리 5: 코드 품질 / 코드 오류 (3개 항목)

**SR-40: Null 역참조 (CWE-476)**
- 검색 대상: null/undefined일 수 있는 값에 대한 속성/메서드 접근에 null 확인 없음
- 취약 패턴: `user`가 null인지 확인 없이 `user.name`, 존재 확인 없이 `data["key"].value`
- 안전 패턴: 접근 전 null 확인, 옵셔널 체이닝 (`?.`), null 병합, 가드 절
- 심각도: MEDIUM

**SR-41: 부적절한 자원 해제 (CWE-404)**
- 검색 대상: 닫히지 않은 열린 파일/연결/핸들, `finally` 블록 누락, `using`/`with` 문 누락
- 취약 패턴: close 없는 `file = open(path)`, 풀에 반환되지 않은 데이터베이스 연결, `finally` 정리 누락
- 안전 패턴: `with open()` (Python), `try-with-resources` (Java), `using` (C#), `defer` (Go), `finally`에서 명시적 `.close()`
- 심각도: MEDIUM

**SR-42: 신뢰할 수 없는 데이터의 역직렬화 (CWE-502)**
- 검색 대상: `pickle.loads()`, `yaml.load()` (SafeLoader 없이), `unserialize()`, 신뢰할 수 없는 데이터의 `JSON.parse` 후 실행, `ObjectInputStream`
- 취약 패턴: `pickle.loads(user_data)`, `yaml.load(user_input)`, PHP `unserialize($user_data)`
- 안전 패턴: `yaml.safe_load()`, 신뢰할 수 없는 데이터에 pickle 사용 금지, 바이너리 직렬화 대신 JSON, 역직렬화 전 입력 검증
- 심각도: HIGH

### 카테고리 6: 캡슐화 (2개 항목)

**SR-43: 잘못된 세션에 의한 데이터 정보 노출 (CWE-488)**
- 검색 대상: 클라이언트 접근 가능 세션 저장소에 민감 데이터, 멀티테넌트 앱에서 공유 세션 변수, 세션 고정 취약점
- 취약 패턴: `localStorage`/`sessionStorage`에 민감 데이터 저장, 로그인 후 세션 ID 재생성 안함
- 안전 패턴: 서버 측 세션 저장소, 인증 후 세션 ID 재생성, 클라이언트 측 저장소에 최소 데이터
- 심각도: MEDIUM

**SR-44: 제거되지 않고 남은 디버그 코드 (CWE-489)**
- 검색 대상: 민감 데이터와 함께 `console.log`, `print()`, `debugger` 문, `DEBUG = True`, 디버그 엔드포인트, 테스트 인증정보
- 취약 패턴: `console.log("user password:", password)`, `debugger;`, `DEBUG = True`, `/debug` 엔드포인트, `admin/admin` 테스트 계정
- 안전 패턴: 배포 전 모든 디버그 문 제거, 레벨이 있는 로깅 프레임워크 사용, 환경 기반 디버그 플래그
- 심각도: MEDIUM

### 카테고리 7: API 오용 (3개 항목)

**SR-45: 취약한 API 사용 (CWE-676)**
- 검색 대상: 더 이상 사용되지 않는/안전하지 않은 API, `eval()`, `innerHTML`, `document.write()`, 안전하지 않은 역직렬화 API, `strcpy`
- 취약 패턴: 더 이상 사용되지 않는 암호화 API 사용, `document.write(user_input)`, `innerHTML = user_data`
- 안전 패턴: 현재/권장 API 사용, `innerHTML` 대신 `textContent`, 프레임워크가 문서화한 안전한 대안
- 심각도: MEDIUM

**SR-46: 보안 결정에 DNS 조회 사용 (CWE-350)**
- 검색 대상: 호스트명 기반 인증, 접근 제어 결정에 DNS 확인 사용
- 취약 패턴: `if socket.gethostbyaddr(ip) == "trusted.example.com": allow()`, 인증에 역방향 DNS 의존
- 안전 패턴: IP 기반 허용 목록, 인증서 기반 인증, 보안 결정에 DNS 사용 금지
- 심각도: MEDIUM

**SR-47: 안전하지 않은 리플렉션 (CWE-470)**
- 검색 대상: 사용자 입력에서 동적 클래스 로딩, 사용자 제어 클래스명으로 리플렉션, `getattr(module, user_input)()`
- 취약 패턴: `Class.forName(user_input)`, `getattr(module, user_input)()`, `importlib.import_module(user_input)`
- 안전 패턴: 허용된 클래스/함수명 허용 목록, 고정 매핑의 팩토리 패턴, 사용자 입력으로 리플렉션 사용 금지
- 심각도: HIGH

---

## 3단계: 스캔 수행

위 47개 규칙 각각에 대해:

1. **Grep** 도구를 사용하여 감지된 모든 소스 파일에서 취약한 패턴을 검색하세요.
   - 감지된 언어에 적합한 정규식 패턴을 사용하세요.
   - 코드 파일과 설정 파일 모두 검색하세요.
2. 잠재적 취약점이 발견되면, **Read** 도구를 사용하여 주변 컨텍스트(앞뒤 5-10줄)를 검사하여 실제 취약점인지 확인하세요.
3. 오탐(false positive)을 제거하기 위해 확인하세요:
   - 플래그된 코드가 테스트 파일에 있는가? (심각도 낮춤, 여전히 기록)
   - 사용자 입력이 이미 상위에서 새니타이즈되었는가?
   - 코드가 죽은/도달 불가능한 경로에 있는가?
   - 상위 수준에서 보안 미들웨어가 적용되어 있는가?

---

## 4단계: 보고서 생성

다음 형식으로 보고서를 작성하세요:

### 보고서 헤더

```
===============================================
  KKTV 시큐어 코드 리뷰 보고서
===============================================
  프로젝트: [프로젝트 이름/경로]
  언어: [감지된 언어]
  프레임워크: [감지된 프레임워크]
  스캔 파일 수: [수량]
  스캔 날짜: [현재 날짜]
===============================================

  요약
  -------
  HIGH:   [수량]건
  MEDIUM: [수량]건
  LOW:    [수량]건
  합계:   [수량]건
===============================================
```

### 발견사항 (심각도순: HIGH 먼저, MEDIUM, LOW 순)

각 발견사항에 대해:

```
[심각도] SR-[번호]: [취약점 이름] (CWE-[번호])
  파일: [file_path]:[line_number]
  코드:
    > [취약한 코드 스니펫, 1-3줄]
  위험: [위험에 대한 간단한 설명]
  수정: [수정을 위한 구체적인 권고사항]
```

### 전체 체크리스트

모든 발견사항 후, 전체 47개 항목 체크리스트를 포함하세요:

```
===============================================
  전체 보안 체크리스트 (47개 항목)
===============================================

카테고리 1: 입력값 검증 및 표현
  [합격/불합격/해당없음] SR-01: SQL 삽입 (CWE-89)
  [합격/불합격/해당없음] SR-02: LDAP 삽입 (CWE-90)
  [합격/불합격/해당없음] SR-03: 코드 삽입 (CWE-94)
  [합격/불합격/해당없음] SR-04: 운영체제 명령어 삽입 (CWE-78)
  [합격/불합격/해당없음] SR-05: XML 삽입 (CWE-91)
  [합격/불합격/해당없음] SR-06: 포맷 스트링 삽입 (CWE-134)
  [합격/불합격/해당없음] SR-07: 크로스사이트 스크립트 (CWE-79)
  [합격/불합격/해당없음] SR-08: CSRF (CWE-352)
  [합격/불합격/해당없음] SR-09: SSRF (CWE-918)
  [합격/불합격/해당없음] SR-10: HTTP 응답 분할 (CWE-113)
  [합격/불합격/해당없음] SR-11: 경로 조작 (CWE-22)
  [합격/불합격/해당없음] SR-12: 위험한 형식 파일 업로드 (CWE-434)
  [합격/불합격/해당없음] SR-13: 오픈 리다이렉트 (CWE-601)
  [합격/불합격/해당없음] SR-14: XXE (CWE-611)
  [합격/불합격/해당없음] SR-15: 정수형 오버플로우 (CWE-190)
  [합격/불합격/해당없음] SR-16: 보안기능 결정에 부적절한 입력값 (CWE-807)
  [합격/불합격/해당없음] SR-17: 메모리 버퍼 오버플로우 (CWE-120)
  [합격/불합격/해당없음] SR-18: 미검증 입력 (CWE-20)

카테고리 2: 보안 기능
  [합격/불합격/해당없음] SR-19: 적절한 인증 없이 중요 기능 허용 (CWE-306)
  [합격/불합격/해당없음] SR-20: 부적절한 인가 (CWE-285)
  [합격/불합격/해당없음] SR-21: 잘못된 권한 설정 (CWE-732)
  [합격/불합격/해당없음] SR-22: 취약한 암호화 알고리즘 (CWE-327)
  [합격/불합격/해당없음] SR-23: 암호화되지 않은 중요정보 (CWE-311)
  [합격/불합격/해당없음] SR-24: 하드코딩된 중요정보 (CWE-798)
  [합격/불합격/해당없음] SR-25: 충분하지 않은 키 길이 (CWE-326)
  [합격/불합격/해당없음] SR-26: 적절하지 않은 난수 값 (CWE-330)
  [합격/불합격/해당없음] SR-27: 취약한 패스워드 허용 (CWE-521)
  [합격/불합격/해당없음] SR-28: 솔트 없는 해시 (CWE-759)
  [합격/불합격/해당없음] SR-29: 인증시도 제한 부재 (CWE-307)
  [합격/불합격/해당없음] SR-30: 부적절한 전자서명 확인 (CWE-347)
  [합격/불합격/해당없음] SR-31: 부적절한 인증서 검증 (CWE-295)
  [합격/불합격/해당없음] SR-32: 무결성 검사 없는 코드 다운로드 (CWE-494)
  [합격/불합격/해당없음] SR-33: 쿠키를 통한 정보 노출 (CWE-539)
  [합격/불합격/해당없음] SR-34: 주석문 내 주요정보 (CWE-615)

카테고리 3: 시간 및 상태
  [합격/불합격/해당없음] SR-35: TOCTOU 경쟁 조건 (CWE-367)
  [합격/불합격/해당없음] SR-36: 종료되지 않는 반복문/재귀 (CWE-835)

카테고리 4: 에러 처리
  [합격/불합격/해당없음] SR-37: 오류 메시지 정보 노출 (CWE-209)
  [합격/불합격/해당없음] SR-38: 오류 상황 대응 부재 (CWE-390)
  [합격/불합격/해당없음] SR-39: 부적절한 예외 처리 (CWE-396)

카테고리 5: 코드 품질
  [합격/불합격/해당없음] SR-40: Null 역참조 (CWE-476)
  [합격/불합격/해당없음] SR-41: 부적절한 자원 해제 (CWE-404)
  [합격/불합격/해당없음] SR-42: 안전하지 않은 역직렬화 (CWE-502)

카테고리 6: 캡슐화
  [합격/불합격/해당없음] SR-43: 세션 데이터 노출 (CWE-488)
  [합격/불합격/해당없음] SR-44: 남은 디버그 코드 (CWE-489)

카테고리 7: API 오용
  [합격/불합격/해당없음] SR-45: 취약한 API 사용 (CWE-676)
  [합격/불합격/해당없음] SR-46: 보안 결정에 DNS 조회 (CWE-350)
  [합격/불합격/해당없음] SR-47: 안전하지 않은 리플렉션 (CWE-470)

점수: [합격]/[해당] ([백분율]%)
```

---

## 5단계: 권고사항 제공

체크리스트 후 다음을 제공하세요:

1. **우선 수정 TOP 3** -- 즉시 수정해야 할 가장 중요한 취약점
2. **빠른 개선** -- 보안을 크게 향상시키는 저비용 수정 (예: `DEBUG = False` 추가, `.gitignore`에 `.env` 추가)
3. **아키텍처 권고** -- 제안되는 구조적 개선 (예: 인증 미들웨어 추가, CORS 적절히 구현)

---

## 중요 사항

- 프로젝트가 관련 기술을 사용하지 않는 경우 **해당없음**으로 표시하세요 (예: SQL 데이터베이스 없으면 SR-01은 해당없음).
- 취약한 패턴이 없고 안전한 패턴이 적용된 것이 확인된 경우에만 **합격**으로 표시하세요.
- 단일 파일에서라도 취약한 패턴이 발견되면 **불합격**으로 표시하세요.
- 소스코드 외에도 설정 파일 (`.env`, `settings.py`, `config.js`, `application.properties`, `docker-compose.yml`)을 항상 확인하세요.
- `.gitignore`를 확인하여 `.env`와 비밀 파일이 버전 관리에서 제외되었는지 확인하세요.
- 프로젝트에 소스코드 파일이 없으면 스캔을 수행할 수 없다고 보고하세요.
- 철저하되 오탐을 피하세요. 확실하지 않으면 불확실성에 대한 메모와 함께 발견사항으로 플래그하세요.
- 파일을 수정하지 마세요. 이 스킬은 읽기 전용입니다.
