# Chapter 16. API 오용 — 편리함 뒤에 숨은 위험

현대 소프트웨어 개발에서 외부 라이브러리(Library)와 API(Application Programming Interface) 없이 프로그램을 만드는 것은 거의 불가능합니다. 특히 파이썬 생태계는 PyPI(Python Package Index)에 등록된 수십만 개의 패키지를 기반으로 돌아갑니다. 바이브 코딩에서 AI는 다양한 외부 패키지를 자유롭게 활용하는 코드를 생성하지만, 해당 패키지가 안전한지, 더 이상 유지보수되지 않는 것은 아닌지 검증하지 않습니다. 이 장에서는 취약한 API 사용(Use of Vulnerable API)에 따른 위험과 대응 방법을 살펴봅니다.

---

## 16-1. 취약한 API 사용

### 개요

취약한 API란 보안상 사용이 금지되었거나 더 이상 유지보수되지 않는(Deprecated) 함수 및 패키지, 또는 부주의하게 사용될 가능성이 높은 API를 의미합니다. 파이썬은 외부 의존성(External Dependency)을 기반으로 하는 생태계이므로, 사용하는 패키지의 보안 상태를 지속적으로 관리하는 것이 필수적입니다.

취약한 API 사용으로 인한 보안 문제는 크게 두 가지 원인으로 분류됩니다:

1. **사용자 배포 패키지 내의 결함**: PyPI에 등록된 패키지 코드 내에 보안 취약점이 존재하는 경우
2. **언어 엔진 자체의 결함**: 파이썬 기본 내장 패키지(Built-in Package)에서 보안 결함이 발견되는 경우

### 왜 위험한가

바이브 코딩에서 AI는 특정 기능을 구현할 때 가장 널리 알려진 패키지를 자동으로 선택합니다. 하지만 AI의 학습 데이터에는 오래된 코드도 포함되어 있어 이미 보안 취약점이 발견된 구 버전의 API를 사용하거나, 더 안전한 대안이 있는데도 레거시(Legacy) 방식의 코드를 생성하는 경우가 있습니다.

대표적인 사례를 살펴봅니다:

- **`urllib` vs `requests`**: 파이썬 기본 내장 `urllib` 모듈의 일부 버전에서 CRLF 인젝션 취약점이 발견된 바 있습니다.
- **`md5`, `sha1` 해시**: 충돌 공격(Collision Attack)에 취약한 것으로 알려져 있으나, AI가 비밀번호 해싱이나 데이터 검증에 여전히 이를 사용하는 코드를 생성할 수 있습니다.
- **`yaml.load()` vs `yaml.safe_load()`**: `yaml.load()`는 임의 코드 실행이 가능한 반면, `yaml.safe_load()`는 기본 데이터 타입만 파싱합니다.
- **`eval()`, `exec()`**: 문자열을 코드로 실행하는 함수로, 외부 입력과 결합되면 원격 코드 실행 취약점이 됩니다.

### ❌ 취약한 코드

**위험한 YAML 파싱**

```python
import yaml

def load_config(config_path):
    with open(config_path) as f:
        # yaml.load()는 임의 코드 실행 가능 — 절대 사용 금지
        config = yaml.load(f)
    return config
```

**취약한 해시 함수 사용**

```python
import hashlib

def hash_password(password):
    # MD5는 충돌 공격에 취약 — 비밀번호 해싱에 부적합
    return hashlib.md5(password.encode()).hexdigest()
```

**eval()을 사용한 위험한 동적 실행**

```python
def calculate(expression):
    # 사용자 입력을 eval()로 실행 — 원격 코드 실행 가능
    result = eval(expression)
    return result
```

**오래된 패키지 의존**

```text
# requirements.txt
Django==2.2.0       # 알려진 보안 취약점 다수 존재
requests==2.20.0    # CVE-2018-18074 취약점 포함
Pillow==6.0.0       # 다수의 버퍼 오버플로우 취약점
```

### ✅ 안전한 코드

**안전한 YAML 파싱**

```python
import yaml

def load_config(config_path):
    with open(config_path) as f:
        # safe_load()는 기본 데이터 타입만 허용
        config = yaml.safe_load(f)
    return config
```

**안전한 비밀번호 해싱**

```python
# Django의 내장 해싱 사용 (PBKDF2, bcrypt, argon2 지원)
from django.contrib.auth.hashers import make_password, check_password

hashed = make_password("user_password")
is_valid = check_password("user_password", hashed)
```

```python
# 또는 bcrypt 직접 사용
import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)
```

**eval() 대신 안전한 대안 사용**

```python
import ast

def calculate(expression):
    # ast.literal_eval()은 리터럴 표현식만 평가 — 코드 실행 불가
    try:
        result = ast.literal_eval(expression)
        return result
    except (ValueError, SyntaxError):
        return None
```

**최신 패키지 버전 관리**

```text
# requirements.txt — 최신 안정 버전 사용
Django>=4.2,<5.0
requests>=2.31.0
Pillow>=10.0.0
```

### 안전한 패키지 선택 기준

AI가 제안한 패키지를 사용하기 전에 다음 항목을 확인하십시오:

1. **사용 통계**: 얼마나 많은 사람들이 해당 패키지를 다운로드하고 사용하고 있는지 확인합니다. PyPI 통계나 GitHub 스타(Star) 수를 참고할 수 있습니다.
2. **이슈 관리**: 버그 리포트와 보안 이슈가 적시에 처리되고 있는지 확인합니다.
3. **마지막 업데이트**: 최근 6개월 이내에 업데이트가 있었는지 확인합니다. 오랫동안 업데이트가 없는 패키지는 유지보수가 중단되었을 가능성이 높습니다.
4. **알려진 취약점**: NIST NVD(https://nvd.nist.gov) 또는 CVEdetails(https://cvedetails.com)에서 패키지명으로 검색하여 알려진 취약점을 확인합니다.

### 사후 관리: SBOM 도입

모든 API는 보안 취약점에서 완전히 자유로울 수 없습니다. 안전한 패키지를 선택했더라도 지속적인 모니터링이 필요합니다. **SBOM(Software Bill of Materials, 소프트웨어 자재 명세서)**을 도입하면 프로젝트에 사용된 모든 패키지의 이름, 버전, 라이선스, 보안 상태를 체계적으로 관리할 수 있습니다.

파이썬에서는 다음 도구들을 활용할 수 있습니다:

```bash
# pip-audit: 설치된 패키지의 알려진 취약점 검사
pip install pip-audit
pip-audit

# safety: requirements.txt 기반 취약점 검사
pip install safety
safety check -r requirements.txt
```

> **💡 팁:** CI/CD 파이프라인에 `pip-audit`이나 `safety check`를 포함시키면, 취약한 패키지가 포함된 코드가 배포되기 전에 자동으로 차단할 수 있습니다. GitHub의 Dependabot이나 Snyk 같은 서비스를 활용하면 패키지 취약점이 발견될 때 자동으로 알림을 받을 수 있습니다.

### 바이브 코딩 시 체크포인트

| 점검 항목 | 확인 방법 |
|-----------|-----------|
| `yaml.load()` 사용 여부 | `yaml.safe_load()`로 대체 |
| `eval()`, `exec()` 사용 여부 | `ast.literal_eval()` 또는 안전한 대안으로 대체 |
| `md5`, `sha1` 해시 사용 | 비밀번호에는 `bcrypt` 또는 `argon2`, 무결성 검증에는 `sha256` 이상 사용 |
| `pickle.loads()` 외부 데이터 처리 | `json.loads()`로 대체하거나 HMAC 검증 추가 |
| 패키지 버전 고정 | `requirements.txt`에 최소 버전 명시, 주기적 업데이트 |
| 패키지 취약점 검사 | `pip-audit` 또는 `safety check` 실행 |
| Deprecated API 사용 | 패키지 공식 문서에서 대체 API 확인 |
| SBOM 관리 | 프로젝트에 사용된 모든 외부 의존성 목록 관리 |

---

> **📦 기타 API 주의사항**
>
> 이 장에서 다루지 않은 API 관련 보안약점으로 **DNS lookup에 의존한 보안 결정** 문제가 있습니다. 도메인명(Domain Name)을 기반으로 접근 제어나 인증을 수행하면 DNS 스푸핑(DNS Spoofing) 공격에 취약해집니다. 공격자가 DNS 캐시를 오염시키면 신뢰할 수 없는 서버가 마치 정상 서버인 것처럼 위장할 수 있습니다. 보안 결정에는 도메인명 대신 IP 주소를 직접 비교하거나, TLS 인증서(Certificate) 검증을 통해 상대방의 신원을 확인하는 방식을 사용해야 합니다. 바이브 코딩에서 AI가 `socket.gethostbyname()`의 결과를 보안 판단에 사용하는 코드를 생성하면 주의 깊게 검토하십시오.
