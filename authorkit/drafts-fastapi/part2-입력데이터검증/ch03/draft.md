# Chapter 03. 코드와 명령어를 노리는 삽입 공격

## 3-1. 코드 삽입(Code Injection)

### 개요

코드 삽입(Code Injection)은 공격자가 애플리케이션에 임의의 프로그래밍 코드를 삽입하여 실행시키는 공격입니다. SQL 삽입이 데이터베이스를 대상으로 한다면, 코드 삽입은 **프로그래밍 언어 자체**를 대상으로 합니다.

파이썬(Python)에서 코드 삽입 공격을 유발하는 대표적인 함수는 `eval()`과 `exec()`입니다. 이 함수들은 문자열을 코드로 해석하여 실행하는 기능을 제공하며, 바이브 코딩(Vibe Coding) 시 AI가 "동적으로 값을 계산해줘"라는 요청에 이 함수들을 사용하는 코드를 생성하는 경우가 있어 각별한 주의가 필요합니다.

### 왜 위험한가

`eval()`이나 `exec()` 함수에 사용자 입력값이 그대로 전달되면, 공격자는 서버에서 **어떤 파이썬 코드든** 실행할 수 있습니다:

- **시스템 정보 탈취**: `__import__('platform').system()` 입력으로 서버 OS 정보 노출
- **파일 시스템 접근**: `__import__('os').listdir('/')` 입력으로 서버 파일 목록 조회
- **원격 쉘 실행**: 공격자가 서버에 원격으로 접속하여 완전한 제어권을 획득
- **서비스 거부**: `time.sleep(99999)` 등으로 서버를 마비시키는 것도 가능

예를 들어, 공격자가 다음과 같은 값을 입력하면 서버가 20초 동안 응답 불능 상태에 빠집니다:

```
compile('for x in range(1):\n import time\n time.sleep(20)','a','single')
```

### 취약한 코드

#### ❌ 취약한 코드: eval() 함수에 외부 입력값 직접 전달

```python
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/route")
async def route(request: Request, message: str = Form(...)):
    # eval() 함수에 사용자 입력을 그대로 전달하면
    # 임의의 파이썬 코드가 실행될 수 있습니다
    ret = eval(message)
    return templates.TemplateResponse(
        "success.html", {"request": request, "data": ret}
    )
```

#### ❌ 취약한 코드: exec() 함수로 동적 함수 호출

```python
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/request-rest-api")
async def request_rest_api(request: Request, function_name: str = Form(...)):
    # 사용자에게 전달받은 함수명을 검증하지 않고 실행
    # "__import__('platform').system()" 등을 입력하면
    # 시스템 정보가 노출됩니다
    exec('{}()'.format(function_name))
    return templates.TemplateResponse("success.html", {"request": request})
```

> **⚠️ 주의:** AI 도구에 "사용자가 입력한 수식을 계산해주는 기능 만들어줘"라고 요청하면 `eval()`을 사용하는 코드가 높은 확률로 생성됩니다. 이는 매우 위험합니다.

### 안전한 코드

#### ✅ 안전한 코드: Pydantic 검증 후 eval() 사용

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, field_validator

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class MessageRequest(BaseModel):
    message: str

    @field_validator("message")
    @classmethod
    def validate_message(cls, v: str) -> str:
        # 입력값이 영문과 숫자로만 구성되었는지 검증합니다
        if not v.isalnum():
            raise ValueError("영문과 숫자만 입력 가능합니다.")
        return v

@app.post("/route")
async def route(request: Request, body: MessageRequest):
    ret = eval(body.message)
    return templates.TemplateResponse(
        "success.html", {"request": request, "data": ret}
    )
```

#### ✅ 안전한 코드: 화이트리스트(Whitelist) 기반 함수 실행 제한

```python
from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 실행 가능한 함수를 사전에 정의합니다
WHITE_LIST = ['get_friends_list', 'get_address', 'get_phone_number']

@app.post("/request-rest-api")
async def request_rest_api(request: Request, function_name: str = Form(...)):
    # 허용된 함수 목록에 포함된 경우에만 실행합니다
    if function_name not in WHITE_LIST:
        raise HTTPException(status_code=400, detail="허용되지 않은 함수입니다.")

    exec('{}()'.format(function_name))
    return templates.TemplateResponse("success.html", {"request": request})
```

#### ✅ 가장 안전한 코드: eval()/exec() 자체를 사용하지 않기

```python
import ast
from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/calculate")
async def calculate(request: Request, expression: str = Form(...)):
    try:
        # ast.literal_eval()은 리터럴 표현식만 평가합니다
        # 함수 호출이나 import 등 위험한 코드는 실행되지 않습니다
        result = ast.literal_eval(expression)
        return templates.TemplateResponse(
            "success.html", {"request": request, "data": result}
        )
    except (ValueError, SyntaxError):
        raise HTTPException(status_code=400, detail="올바른 값을 입력해주세요.")
```

> **💡 팁:** 수식 계산이 필요한 경우 `ast.literal_eval()`을 사용하거나, 수학 전용 라이브러리인 `numexpr`, `sympy` 등을 활용하는 것이 `eval()`보다 훨씬 안전합니다.

### 바이브 코딩 시 체크포인트

- [ ] **코드에 `eval()` 또는 `exec()`가 포함되어 있지 않은가?** AI가 생성한 코드에서 이 함수들이 보이면 반드시 대안을 검토하십시오
- [ ] **동적 코드 실행이 정말 필요한가?** 대부분의 경우 `eval()` 없이도 동일한 기능을 구현할 수 있습니다
- [ ] **사용자 입력값이 코드 실행 함수에 직접 전달되지 않는가?** 불가피한 경우 화이트리스트로 실행 가능한 범위를 제한하십시오

---

## 3-2. 운영체제 명령어 삽입(OS Command Injection)

### 개요

운영체제 명령어 삽입(OS Command Injection)은 사용자 입력값이 시스템 명령어의 일부로 사용되어, 공격자가 의도하지 않은 운영체제 명령을 실행할 수 있는 취약점입니다.

파이썬에서는 `os.system()`, `subprocess.run()`, `subprocess.Popen()` 등의 함수가 운영체제 명령어를 실행합니다. 바이브 코딩으로 파일 처리, 시스템 유틸리티 호출, 외부 프로그램 연동 등의 기능을 구현할 때 이 취약점에 노출되기 쉽습니다.

### 왜 위험한가

공격자가 시스템 명령어를 주입하면 서버의 운영체제 수준에서 명령이 실행됩니다. 이는 코드 삽입보다 더 심각한 결과를 초래할 수 있습니다:

- **서버 파일 열람/삭제**: `cat /etc/passwd`, `rm -rf /` 등의 명령 실행 가능
- **악성 프로그램 설치**: `wget`이나 `curl`로 악성코드를 다운로드하여 실행
- **서버 장악**: 리버스 쉘(Reverse Shell)을 열어 서버를 완전히 제어

특수문자 `|`, `;`, `&`, `` ` `` 등을 사용하면 여러 명령어를 연결하여 실행할 수 있습니다:

```
# 원래 의도: 날짜를 인자로 백업 실행
backuplog.bat 2024-01-01

# 공격자 입력: 2024-01-01; cat /etc/passwd
# 실제 실행: backuplog.bat 2024-01-01; cat /etc/passwd
```

### 취약한 코드

#### ❌ 취약한 코드: os.system()에 외부 입력값 직접 사용

```python
import os
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/execute-command")
async def execute_command(request: Request, app_name: str = Form(...)):
    # 입력 파라미터를 제한하지 않아 외부 입력값으로
    # 전달된 모든 프로그램이 실행될 수 있습니다
    os.system(app_name)
    return templates.TemplateResponse("success.html", {"request": request})
```

#### ❌ 취약한 코드: subprocess에서 shell=True 사용

```python
import subprocess
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/execute-command")
async def execute_command(request: Request, date: str = Form(...)):
    # shell=True와 문자열 결합은 명령어 삽입의 원인이 됩니다
    cmd_str = "cmd /c backuplog.bat " + date
    subprocess.run(cmd_str, shell=True)
    return templates.TemplateResponse("success.html", {"request": request})
```

> **⚠️ 주의:** `subprocess.run()`의 `shell=True` 옵션은 중간 프로세스(쉘)를 통해 명령을 실행하므로, 와일드카드(Wildcard) 확장, 환경변수 참조, 명령어 연결 등이 모두 가능해져 매우 위험합니다.

### 안전한 코드

#### ✅ 안전한 코드: 화이트리스트로 실행 가능한 프로그램 제한

```python
import os
from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

ALLOW_PROGRAM = ['notepad', 'calc']

@app.post("/execute-command")
async def execute_command(request: Request, app_name: str = Form(...)):
    # 허용된 프로그램 목록에 포함되는지 검사합니다
    if app_name not in ALLOW_PROGRAM:
        raise HTTPException(status_code=400, detail="허용되지 않은 프로그램입니다.")

    os.system(app_name)
    return templates.TemplateResponse("success.html", {"request": request})
```

#### ✅ 안전한 코드: 특수문자 필터링 + 배열 형태 인자 전달

```python
import subprocess
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/execute-command")
async def execute_command(request: Request, date: str = Form(...)):
    # 명령어 연결에 사용되는 특수문자를 필터링합니다
    for word in ['|', ';', '&', ':', '>', '<', '`', '\\', '!']:
        date = date.replace(word, "")

    # shell=True를 사용하지 않고, 명령과 인자를 배열로 전달합니다
    subprocess.run(["cmd", "/c", "backuplog.bat", date])
    return templates.TemplateResponse("success.html", {"request": request})
```

> **💡 팁:** `subprocess` 사용 시 `shell=True`를 절대 사용하지 마십시오. 명령어와 인자를 리스트(List) 형태로 분리하여 전달하면 쉘 해석 과정 없이 직접 실행되므로 훨씬 안전합니다.

### 바이브 코딩 시 체크포인트

- [ ] **`os.system()` 대신 `subprocess.run()`을 리스트 인자로 사용하고 있는가?**
- [ ] **`shell=True` 옵션이 사용되고 있지 않은가?**
- [ ] **사용자 입력이 명령어의 일부로 사용된다면 특수문자 필터링이 적용되어 있는가?**
- [ ] **정말 시스템 명령어를 호출해야 하는가?** 파이썬 내장 라이브러리로 대체할 수 있는 경우가 많습니다 (예: `shutil` 모듈로 파일 복사)

---

## 3-3. XML 삽입(XML Injection)

### 개요

XML 삽입(XML Injection)은 XQuery 또는 XPath 쿼리문에 검증되지 않은 외부 입력값이 포함되어, 공격자가 쿼리 구조를 변경하고 허가되지 않은 데이터에 접근할 수 있는 보안약점입니다.

바이브 코딩 환경에서 XML 데이터를 직접 다루는 경우는 비교적 적지만, 레거시 시스템(Legacy System)과의 연동이나 SOAP API 호출 시 이 취약점을 마주할 수 있습니다.

### 왜 위험한가

XML 기반 데이터 조회에서 XPath를 사용할 때, SQL 삽입과 동일한 원리로 쿼리가 변조될 수 있습니다:

```xpath
# 원래 의도된 쿼리
/collection/users/user[@name='kim']/home/text()

# 공격자가 name에 ' or '1'='1 입력 시
/collection/users/user[@name='' or '1'='1']/home/text()
```

이렇게 되면 모든 사용자의 정보가 노출됩니다.

### 취약한 코드

#### ❌ 취약한 코드: XPath 쿼리에 문자열 결합 사용

```python
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from lxml import etree

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/parse-xml")
async def parse_xml(request: Request, user_name: str = Form(...)):
    parser = etree.XMLParser(resolve_entities=False)
    tree = etree.parse('user.xml', parser)
    root = tree.getroot()

    # 검증되지 않은 입력값을 문자열 결합으로 쿼리에 포함합니다
    query = "/collection/users/user[@name='" + user_name + "']/home/text()"
    elmts = root.xpath(query)

    return templates.TemplateResponse(
        "parse_xml.html", {"request": request, "xml_element": elmts}
    )
```

### 안전한 코드

#### ✅ 안전한 코드: XPath 파라미터 바인딩 사용

```python
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from lxml import etree

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/parse-xml")
async def parse_xml(request: Request, user_name: str = Form(...)):
    parser = etree.XMLParser(resolve_entities=False)
    tree = etree.parse('user.xml', parser)
    root = tree.getroot()

    # 외부 입력값을 $paramname으로 인자화하여 사용합니다
    query = '/collection/users/user[@name = $paramname]/home/text()'
    elmts = root.xpath(query, paramname=user_name)

    return templates.TemplateResponse(
        "parse_xml.html", {"request": request, "xml_element": elmts}
    )
```

> **💡 팁:** `lxml` 라이브러리의 XPath는 `$변수명` 형식의 파라미터 바인딩을 지원합니다. SQL의 바인드 파라미터와 동일한 원리이므로, 항상 파라미터 바인딩을 사용하십시오.

---

## 3-4. 포맷 스트링 삽입(Format String Injection)

### 개요

포맷 스트링 삽입(Format String Injection)은 파이썬의 f-string이나 `.format()` 메서드를 사용할 때, 사용자 입력값이 포맷 문자열 자체에 포함되어 의도하지 않은 정보가 노출되는 취약점입니다.

전통적인 C 언어의 포맷 스트링 공격과는 다소 다르지만, 파이썬에서도 `.format()` 메서드를 통해 객체의 속성(Attribute)에 접근하거나 내부 정보를 유출할 수 있습니다.

### 왜 위험한가

파이썬의 `.format()` 메서드는 객체의 속성에 접근하는 기능을 제공합니다. 공격자가 이를 악용하면 서버의 내부 정보를 탈취할 수 있습니다:

```python
# 의도된 사용
"Hello, {name}!".format(name="Kim")

# 공격자가 name에 다음과 같은 값을 전달하면?
# {user.__class__.__init__.__globals__}
# -> 글로벌 변수에 저장된 비밀키, 설정값 등이 노출됩니다
```

### 취약한 코드

#### ❌ 취약한 코드: 사용자 입력으로 포맷 문자열 구성

```python
from fastapi import FastAPI, Form, Request, Depends
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/greeting")
async def greeting(request: Request, template: str = Form(...)):
    # 사용자 입력을 포맷 문자열 자체로 사용하면 위험합니다
    # 예: template = "{user.__class__.__init__.__globals__}"
    message = template.format(user=request)
    return templates.TemplateResponse(
        "greeting.html", {"request": request, "message": message}
    )
```

#### ❌ 취약한 코드: f-string에서의 위험한 패턴

```python
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/render-message")
async def render_message(request: Request, user_input: str = Form(...)):
    # 사용자 입력을 eval()과 f-string으로 결합하면 코드 실행이 가능합니다
    # 이 패턴은 AI가 "동적 메시지 생성"을 구현할 때 생성할 수 있습니다
    message = eval(f"f'{user_input}'")
    return templates.TemplateResponse(
        "result.html", {"request": request, "message": message}
    )
```

> **⚠️ 주의:** `eval()`과 f-string의 조합은 코드 삽입과 포맷 스트링 삽입이 동시에 발생하는 매우 위험한 패턴입니다. AI가 이런 코드를 생성하면 즉시 수정하십시오.

### 안전한 코드

#### ✅ 안전한 코드: 고정된 포맷 문자열 사용

```python
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/greeting")
async def greeting(request: Request, name: str = Form(...)):
    # 포맷 문자열은 코드에서 고정하고, 사용자 입력은 인자로만 전달합니다
    message = "안녕하세요, {}님!".format(name)
    return templates.TemplateResponse(
        "greeting.html", {"request": request, "message": message}
    )
```

#### ✅ 안전한 코드: Jinja2 템플릿 활용

```python
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/greeting")
async def greeting(request: Request, name: str = Form(...)):
    # Jinja2 템플릿에서 변수를 렌더링하면 자동으로 이스케이프됩니다
    return templates.TemplateResponse(
        "greeting.html", {"request": request, "name": name}
    )
```

```html
<!-- templates/greeting.html -->
<p>안녕하세요, {{ name }}님!</p>
```

> **💡 팁:** 동적 메시지 생성이 필요한 경우, 포맷 문자열을 코드에 고정하고 사용자 입력은 **인자(Argument)**로만 전달하십시오. 사용자가 포맷 문자열 자체를 제어할 수 있게 하면 안 됩니다.

### 바이브 코딩 시 체크포인트

- [ ] **사용자 입력이 `.format()` 또는 f-string의 템플릿 부분에 사용되고 있지 않은가?**
- [ ] **`eval()`과 f-string이 조합되어 있지 않은가?**
- [ ] **동적 메시지는 Jinja2 템플릿으로 처리하고 있는가?**
- [ ] **포맷 문자열은 코드에 하드코딩(Hardcode)되어 있는가?**
