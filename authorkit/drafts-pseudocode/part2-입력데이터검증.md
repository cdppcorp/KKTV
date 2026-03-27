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

## 2-2. LDAP 삽입(LDAP Injection)

> **📦 기타 삽입 공격 — LDAP 삽입**
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
