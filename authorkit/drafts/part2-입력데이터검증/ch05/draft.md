# Chapter 05. 파일과 URL을 노리는 공격

## 5-1. 경로 조작 및 자원 삽입(Path Traversal & Resource Injection)

### 개요

경로 조작(Path Traversal)은 검증되지 않은 외부 입력값을 사용하여 파일 시스템의 경로를 조작함으로써, 공격자가 허가되지 않은 파일이나 디렉터리(Directory)에 접근할 수 있는 보안약점입니다. 자원 삽입(Resource Injection)은 이 원리를 파일뿐 아니라 소켓 포트, 네트워크 자원 등에까지 확장한 개념입니다.

바이브 코딩으로 파일 업로드/다운로드 기능, 이미지 뷰어, 문서 관리 시스템 등을 만들 때 이 취약점이 자주 발생합니다. AI 도구가 생성하는 파일 처리 코드에서 경로 검증이 누락되는 경우가 많으므로 반드시 확인해야 합니다.

### 왜 위험한가

공격자가 파일명에 `../`(상위 디렉터리 이동) 문자열을 삽입하면, 서버의 의도된 디렉터리를 벗어나 시스템의 모든 파일에 접근할 수 있습니다:

```text
# 정상적인 요청
GET /download?file=report.txt
# 서버에서 열리는 파일: /var/www/uploads/report.txt

# 공격자의 요청
GET /download?file=../../../../etc/passwd
# 서버에서 열리는 파일: /etc/passwd (운영체제 사용자 정보!)
```

이를 통해 공격자는 다음과 같은 행위를 할 수 있습니다:

- **시스템 파일 열람**: `/etc/passwd`, `/etc/shadow`, 환경설정 파일 등
- **소스 코드 유출**: 애플리케이션의 소스 코드나 설정 파일에서 데이터베이스 비밀번호 등을 탈취
- **서버 설정 파일 변경**: 설정 파일을 변경하여 시스템 제어권 획득

### 취약한 코드

#### ❌ 취약한 코드: 외부 입력값을 파일 경로에 직접 사용

```python
import os
from django.shortcuts import render

def get_info(request):
    # 외부 입력값으로부터 파일명을 입력 받습니다
    request_file = request.POST.get('request_file')
    (filename, file_ext) = os.path.splitext(request_file)
    file_ext = file_ext.lower()

    if file_ext not in ['.txt', '.csv']:
        return render(request, '/error.html', {'error': '파일을 열 수 없습니다.'})

    # 확장자만 검증하고 경로 조작 문자열은 검증하지 않습니다
    # ../../../../etc/passwd.txt 같은 입력이 가능합니다
    with open(request_file) as f:
        data = f.read()

    return render(request, '/success.html', {'data': data})
```

#### ❌ 취약한 코드: 외부 입력값을 소켓 포트 번호로 사용

```python
import socket
from django.shortcuts import render

def get_info(request):
    port = int(request.POST.get('port'))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # 검증되지 않은 포트 번호로 소켓을 바인딩합니다
        # 기존 서비스와 충돌하거나 특권 포트에 접근할 수 있습니다
        s.bind(('127.0.0.1', port))
        ...
```

### 안전한 코드

#### ✅ 안전한 코드: 경로 조작 문자열 필터링

```python
import os
from django.shortcuts import render

def get_info(request):
    request_file = request.POST.get('request_file')
    (filename, file_ext) = os.path.splitext(request_file)
    file_ext = file_ext.lower()

    if file_ext not in ['.txt', '.csv']:
        return render(request, '/error.html', {'error': '파일을 열 수 없습니다.'})

    # 경로 조작 문자열을 필터링합니다
    filename = filename.replace('.', '')
    filename = filename.replace('/', '')
    filename = filename.replace('\\', '')

    try:
        with open(filename + file_ext) as f:
            data = f.read()
    except FileNotFoundError:
        return render(request, '/error.html',
                      {'error': '파일이 존재하지 않거나 열 수 없는 파일입니다.'})

    return render(request, '/success.html', {'data': data})
```

#### ✅ 더 안전한 코드: 기본 디렉터리(Base Directory) 제한

```python
import os
from django.shortcuts import render

# 파일 접근이 허용된 기본 디렉터리를 지정합니다
BASE_DIR = '/var/www/uploads'

def get_info(request):
    request_file = request.POST.get('request_file')
    (filename, file_ext) = os.path.splitext(request_file)
    file_ext = file_ext.lower()

    if file_ext not in ['.txt', '.csv']:
        return render(request, '/error.html', {'error': '파일을 열 수 없습니다.'})

    # 절대 경로를 생성하고, 기본 디렉터리 내에 있는지 확인합니다
    safe_path = os.path.realpath(os.path.join(BASE_DIR, filename + file_ext))

    if not safe_path.startswith(os.path.realpath(BASE_DIR)):
        return render(request, '/error.html', {'error': '접근이 허용되지 않은 경로입니다.'})

    try:
        with open(safe_path) as f:
            data = f.read()
    except FileNotFoundError:
        return render(request, '/error.html', {'error': '파일을 찾을 수 없습니다.'})

    return render(request, '/success.html', {'data': data})
```

> **💡 팁:** `os.path.realpath()`는 심볼릭 링크(Symbolic Link)와 `../` 등의 경로 조작을 모두 해석하여 실제 절대 경로를 반환합니다. 이 결과가 허용된 기본 디렉터리로 시작하는지 확인하면 경로 조작 공격을 효과적으로 방어할 수 있습니다.

#### ✅ 안전한 코드: 자원 삽입 방지 - 포트 번호 화이트리스트

```python
import socket
from django.shortcuts import render

ALLOW_PORT = [4000, 6000, 9000]

def get_info(request):
    port = int(request.POST.get('port'))

    # 허용된 포트 번호만 사용할 수 있도록 제한합니다
    if port not in ALLOW_PORT:
        return render(request, '/error.html', {'error': '소켓연결 실패'})

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', port))
        ...
```

### 바이브 코딩 시 체크포인트

- [ ] **파일 경로에 사용자 입력이 포함되는 경우 `../`, `/`, `\` 등의 경로 조작 문자가 필터링되고 있는가?**
- [ ] **`os.path.realpath()`로 실제 경로를 해석한 후 기본 디렉터리 범위 내인지 확인하고 있는가?**
- [ ] **파일 다운로드 기능에서 사용자가 임의의 시스템 파일에 접근할 수 없도록 제한되어 있는가?**
- [ ] **외부 입력값이 포트 번호, 소켓 주소 등 시스템 자원 식별자로 사용되는 경우 화이트리스트로 제한하고 있는가?**

---

## 5-2. 위험한 형식 파일 업로드(Unrestricted File Upload)

### 개요

파일 업로드 기능에서 서버 측 실행 가능한 스크립트 파일(`.py`, `.php`, `.jsp`, `.sh` 등)의 업로드를 허용하면, 공격자가 웹 쉘(Web Shell)을 업로드하여 서버를 완전히 장악할 수 있습니다.

바이브 코딩으로 이미지 업로드, 첨부파일 기능 등을 구현할 때 가장 흔하게 발생하는 취약점 중 하나입니다. AI가 생성한 파일 업로드 코드에서 검증 로직이 누락되는 경우가 많습니다.

### 왜 위험한가

공격자가 악성 스크립트를 업로드하면:

1. 서버에서 해당 파일을 직접 실행할 수 있습니다 (웹 쉘)
2. 서버의 모든 파일에 접근하고, 데이터베이스를 조작하고, 다른 서버를 공격하는 거점으로 활용할 수 있습니다
3. 대용량 파일을 반복 업로드하여 디스크를 가득 채우는 서비스 거부(DoS) 공격도 가능합니다

확장자만 검사하는 것으로는 부족합니다. 공격자는 `malware.py.jpg`처럼 이중 확장자를 사용하거나, 실제 파일 내용은 스크립트이면서 확장자만 `.jpg`로 변경하는 방법을 사용합니다.

### 취약한 코드

#### ❌ 취약한 코드: 파일 검증 없이 업로드 허용

```python
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

def file_upload(request):
    if request.FILES['upload_file']:
        upload_file = request.FILES['upload_file']
        fs = FileSystemStorage(location='media/screenshot', base_url='media/screenshot')

        # 파일의 크기, 개수, 확장자, 내용을 전혀 검증하지 않습니다
        filename = fs.save(upload_file.name, upload_file)
        return render(request, '/success.html', {'filename': filename})

    return render(request, '/error.html', {'error': '파일 업로드 실패'})
```

### 안전한 코드

#### ✅ 안전한 코드: 다중 검증 적용

```python
import os
import uuid
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

# 업로드 제한 설정
FILE_COUNT_LIMIT = 5
FILE_SIZE_LIMIT = 5 * 1024 * 1024  # 5MB

# 허용하는 확장자를 화이트리스트로 관리합니다
WHITE_LIST_EXT = ['.jpg', '.jpeg', '.png', '.gif']

# 허용하는 MIME 타입
WHITE_LIST_MIME = ['image/jpeg', 'image/png', 'image/gif']

def file_upload(request):
    # 1단계: 파일 개수 제한
    if len(request.FILES) == 0 or len(request.FILES) > FILE_COUNT_LIMIT:
        return render(request, '/error.html', {'error': '파일 개수 초과'})

    filename_list = []
    for key, upload_file in request.FILES.items():
        # 2단계: MIME 타입 검사
        if upload_file.content_type not in WHITE_LIST_MIME:
            return render(request, '/error.html', {'error': '허용되지 않은 파일 형식입니다.'})

        # 3단계: 파일 크기 제한
        if upload_file.size > FILE_SIZE_LIMIT:
            return render(request, '/error.html', {'error': '파일 크기가 초과되었습니다.'})

        # 4단계: 파일 확장자 검사
        file_name, file_ext = os.path.splitext(upload_file.name)
        if file_ext.lower() not in WHITE_LIST_EXT:
            return render(request, '/error.html', {'error': '허용되지 않은 확장자입니다.'})

        # 5단계: 파일명을 랜덤으로 변경하여 저장합니다
        safe_filename = str(uuid.uuid4()) + file_ext.lower()
        fs = FileSystemStorage(location='media/screenshot', base_url='media/screenshot')
        saved_name = fs.save(safe_filename, upload_file)
        filename_list.append(saved_name)

    return render(request, '/success.html', {'filename_list': filename_list})
```

#### ✅ 보너스: 매직 바이트(Magic Bytes) 검증

```python
import struct

# 파일의 실제 형식을 매직 바이트로 확인합니다
MAGIC_BYTES = {
    'jpg': [b'\xff\xd8\xff'],
    'png': [b'\x89\x50\x4e\x47'],
    'gif': [b'\x47\x49\x46\x38'],
    'pdf': [b'\x25\x50\x44\x46'],
}

def verify_file_type(file_obj, expected_type):
    """파일의 매직 바이트를 확인하여 실제 파일 형식을 검증합니다."""
    header = file_obj.read(8)
    file_obj.seek(0)  # 파일 포인터를 처음으로 되돌립니다

    if expected_type not in MAGIC_BYTES:
        return False

    for magic in MAGIC_BYTES[expected_type]:
        if header.startswith(magic):
            return True

    return False
```

> **💡 팁:** 확장자와 Content-Type은 공격자가 쉽게 변조할 수 있습니다. 파일의 첫 몇 바이트에 위치한 매직 바이트(Magic Bytes, 파일 시그니처)를 확인하면 실제 파일 형식을 보다 정확하게 판별할 수 있습니다.

### 바이브 코딩 시 체크포인트

- [ ] **파일 확장자를 화이트리스트 방식으로 검증하고 있는가?**
- [ ] **Content-Type(MIME 타입)을 검사하고 있는가?**
- [ ] **파일 크기와 업로드 개수에 제한이 있는가?**
- [ ] **업로드된 파일명을 UUID 등으로 변경하여 저장하고 있는가?**
- [ ] **업로드 디렉터리가 웹 루트 외부에 위치하는가?** (URL로 직접 접근하여 실행할 수 없도록)
- [ ] **업로드된 파일에 실행 권한이 부여되지 않았는가?**

---

## 5-3. 신뢰되지 않는 URL 자동 연결(Open Redirect)

### 개요

오픈 리다이렉트(Open Redirect)는 사용자 입력값을 외부 사이트 주소로 사용하여 리다이렉트(Redirect)하는 경우, 공격자가 이를 악용하여 피해자를 피싱(Phishing) 사이트로 유도할 수 있는 취약점입니다.

바이브 코딩으로 로그인 후 원래 페이지로 돌아가는 기능, 외부 링크 연결 기능 등을 구현할 때 이 취약점에 노출됩니다.

### 왜 위험한가

공격자는 신뢰할 수 있는 도메인을 경유하여 피해자를 악성 사이트로 유도합니다:

```text
# 정상적인 URL
https://your-site.com/redirect?url=/dashboard

# 공격자가 조작한 URL (your-site.com의 신뢰도를 악용)
https://your-site.com/redirect?url=https://evil-phishing-site.com/login
```

피해자는 `your-site.com` 도메인을 보고 안전하다고 판단하지만, 실제로는 피싱 사이트로 이동합니다.

### 취약한 코드

#### ❌ 취약한 코드: 사용자 입력 URL로 직접 리다이렉트

```python
from django.shortcuts import redirect

def redirect_url(request):
    url_string = request.POST.get('url', '')

    # 사용자 입력값을 검증 없이 리다이렉트에 사용합니다
    return redirect(url_string)
```

### 안전한 코드

#### ✅ 안전한 코드: 화이트리스트로 리다이렉트 URL 제한

```python
from django.shortcuts import render, redirect

ALLOW_URL_LIST = [
    '127.0.0.1',
    '192.168.0.1',
    'https://login.myservice.com',
    '/notice',
    '/dashboard',
]

def redirect_url(request):
    url_string = request.POST.get('url', '')

    # 화이트리스트에 포함된 URL만 리다이렉트를 허용합니다
    if url_string not in ALLOW_URL_LIST:
        return render(request, '/error.html', {'error': '허용되지 않는 주소입니다.'})

    return redirect(url_string)
```

#### ✅ 안전한 코드: 상대 URL만 허용

```python
from urllib.parse import urlparse
from django.shortcuts import render, redirect

def redirect_url(request):
    url_string = request.POST.get('url', '')
    parsed = urlparse(url_string)

    # 외부 도메인으로의 리다이렉트를 차단합니다
    # scheme(http, https)이나 netloc(도메인)이 포함되면 외부 URL입니다
    if parsed.scheme or parsed.netloc:
        return render(request, '/error.html', {'error': '외부 URL로는 이동할 수 없습니다.'})

    return redirect(url_string)
```

> **💡 팁:** 로그인 후 리다이렉트 기능을 구현할 때, 가능한 한 상대 경로(Relative URL)만 허용하십시오. `/dashboard`, `/profile`과 같은 내부 경로만 허용하면 외부 사이트로의 리다이렉트를 원천적으로 차단할 수 있습니다.

### 바이브 코딩 시 체크포인트

- [ ] **`redirect()` 함수에 사용자 입력값이 직접 전달되고 있지 않은가?**
- [ ] **리다이렉트 대상 URL을 화이트리스트로 관리하거나, 상대 URL만 허용하고 있는가?**
- [ ] **Django, Flask의 redirect 관련 알려진 취약점이 패치된 최신 버전을 사용하고 있는가?**

---

## 5-4. 부적절한 XML 외부 개체 참조(XXE)

### 개요

XML 외부 엔티티(XML External Entity, XXE) 공격은 XML 문서에 포함된 DTD(Document Type Definition)의 외부 엔티티 참조 기능을 악용하여, 서버의 파일을 읽거나 내부 네트워크에 접근하는 공격입니다.

바이브 코딩 환경에서 XML 파일을 직접 파싱(Parsing)하는 경우는 비교적 적지만, API 연동이나 데이터 가져오기(Import) 기능에서 XML을 처리할 때 이 취약점에 노출될 수 있습니다.

### 왜 위험한가

공격자는 다음과 같은 악성 XML을 전송하여 서버 파일을 읽을 수 있습니다:

```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [
  <!ELEMENT foo ANY >
  <!ENTITY xxe1 SYSTEM "file:///etc/passwd" >
  <!ENTITY xxe2 SYSTEM "http://attacker.com/text.txt">
]>
<foo>&xxe1;&xxe2;</foo>
```

XML 파서(Parser)가 외부 엔티티를 처리하도록 설정되어 있으면, `&xxe1;`이 `/etc/passwd` 파일의 내용으로 치환됩니다.

### 취약한 코드

#### ❌ 취약한 코드: 외부 엔티티 처리 활성화

```python
from xml.sax import make_parser
from xml.sax.handler import feature_external_ges
from xml.dom.pulldom import parseString, START_ELEMENT
from django.shortcuts import render

def get_xml(request):
    if request.method == "POST":
        parser = make_parser()
        # 외부 엔티티 처리를 True로 설정하면 XXE 공격에 취약합니다
        parser.setFeature(feature_external_ges, True)
        doc = parseString(request.body.decode('utf-8'), parser=parser)
        ...
```

### 안전한 코드

#### ✅ 안전한 코드: 외부 엔티티 처리 비활성화

```python
from xml.sax import make_parser
from xml.sax.handler import feature_external_ges
from xml.dom.pulldom import parseString, START_ELEMENT
from django.shortcuts import render

def get_xml(request):
    if request.method == "POST":
        parser = make_parser()
        # 외부 엔티티 처리를 반드시 False로 설정합니다
        parser.setFeature(feature_external_ges, False)
        doc = parseString(request.body.decode('utf-8'), parser=parser)
        ...
```

#### ✅ 안전한 코드: lxml 라이브러리 사용 시 설정

```python
from lxml import etree

# resolve_entities=False로 외부 엔티티 해석을 비활성화합니다
# no_network=True로 네트워크를 통한 외부 문서 조회를 차단합니다
parser = etree.XMLParser(
    resolve_entities=False,
    no_network=True,
    dtd_validation=False,
    load_dtd=False
)

tree = etree.parse('data.xml', parser)
```

> **💡 팁:** 파이썬 기본 XML 파서(`xml.etree.ElementTree`)는 외부 엔티티를 지원하지 않아 비교적 안전하지만, 다른 유형의 XML 공격에는 취약할 수 있습니다. `lxml` 등 외부 라이브러리를 사용할 때는 반드시 `resolve_entities=False`와 `no_network=True` 옵션을 설정하십시오. 가능하다면 XML 대신 JSON 형식을 사용하는 것을 권장합니다.

### 바이브 코딩 시 체크포인트

- [ ] **XML 파서의 외부 엔티티 처리 옵션이 비활성화되어 있는가?**
- [ ] **`lxml` 사용 시 `resolve_entities=False`, `no_network=True`가 설정되어 있는가?**
- [ ] **XML 대신 JSON을 사용할 수 있는지 검토했는가?**
- [ ] **사용자가 업로드하는 XML 파일을 서버에서 파싱하는 경우, DTD 처리가 비활성화되어 있는가?**
