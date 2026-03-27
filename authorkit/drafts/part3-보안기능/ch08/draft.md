# Chapter 08. 암호화, 제대로 하고 계십니까

## 8-1. 취약한 암호화 알고리즘 사용

암호화 알고리즘 분류표는 `diagram.md`를 참고하십시오.

### 개요

암호화 알고리즘(Encryption Algorithm)은 중요한 정보를 보호하기 위한 핵심 수단입니다. 그러나 과거에 안전하다고 여겨졌던 알고리즘 중 상당수가 컴퓨터 성능의 향상과 함께 취약해졌습니다. MD5, SHA-1, DES, RC4와 같은 알고리즘이 대표적입니다.

바이브 코딩에서 특히 주의해야 할 점은, AI가 학습한 데이터에 오래된 코드 예제가 다수 포함되어 있다는 것입니다. 따라서 AI는 여전히 MD5나 SHA-1을 사용하는 코드를 생성할 수 있습니다. 여러분이 직접 알고리즘의 안전성을 판단할 수 있어야 합니다.

### 왜 위험한가

취약한 암호화 알고리즘을 사용하면 다음과 같은 위험이 발생합니다.

- **해시 충돌(Hash Collision)**: MD5와 SHA-1은 서로 다른 입력에서 같은 해시값이 생성되는 충돌이 실제로 발견되었습니다. 이를 통해 위조된 인증서나 문서를 만들 수 있습니다.
- **브루트포스 공격(Brute-Force Attack)**: DES는 56비트 키를 사용하므로, 현대 컴퓨터로 수 시간 내에 모든 키를 시도할 수 있습니다.
- **레인보우 테이블(Rainbow Table) 공격**: MD5 해시값은 이미 방대한 레인보우 테이블이 존재하여, 해시값만으로 원문을 역추적할 수 있습니다.

### 취약한 코드

다음은 취약한 DES 알고리즘과 MD5 해시를 사용하는 ❌ 취약한 코드입니다.

```python
# ❌ 취약한 코드: DES 암호화 사용
from Crypto.Cipher import DES
import base64

def encrypt_data(plain_text, key):
    # DES는 56비트 키로 현대 컴퓨터에서 쉽게 해독 가능
    cipher = DES.new(key, DES.MODE_ECB)
    encrypted = base64.b64encode(cipher.encrypt(plain_text.ljust(8)))
    return encrypted.decode('ASCII')
```

```python
# ❌ 취약한 코드: MD5 해시 사용
import hashlib

def hash_password(password):
    # MD5는 충돌이 발견되어 더 이상 안전하지 않음
    return hashlib.md5(password.encode('utf-8')).hexdigest()
```

### 안전한 코드

AES-256과 SHA-256을 사용하는 ✅ 안전한 코드입니다.

```python
# ✅ 안전한 코드: AES-256 CBC 모드 암호화
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

def encrypt_data(plain_text, key):
    # AES-256 CBC 모드 사용 (키 길이 32바이트 = 256비트)
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(plain_text.encode('utf-8'), AES.block_size))
    # IV를 암호문 앞에 결합하여 저장
    return base64.b64encode(iv + encrypted).decode('ASCII')

def decrypt_data(encrypted_text, key):
    raw = base64.b64decode(encrypted_text)
    iv = raw[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(raw[AES.block_size:]), AES.block_size)
    return decrypted.decode('utf-8')
```

```python
# ✅ 안전한 코드: SHA-256 해시 사용
import hashlib

def hash_data(data):
    # SHA-256은 현재 안전한 해시 알고리즘
    return hashlib.sha256(data.encode('utf-8')).hexdigest()
```

> **⚠️ 주의:** ECB(Electronic Code Block) 모드는 같은 평문 블록이 항상 같은 암호문을 생성하므로 패턴이 노출됩니다. 반드시 CBC, CTR, GCM 등의 운영 모드를 사용하십시오.

### 바이브 코딩 시 체크포인트

- [ ] AI가 생성한 코드에서 `DES`, `MD5`, `SHA1`, `RC4`, `Blowfish`를 사용하는 부분이 없는지 검색합니다.
- [ ] 대칭키 암호화는 AES-128 이상(권장 AES-256)을 사용합니다.
- [ ] 해시 함수는 SHA-256 이상을 사용합니다.
- [ ] ECB 모드 대신 CBC, GCM 등의 안전한 운영 모드를 사용하는지 확인합니다.
- [ ] AI에게 "안전한 암호화 알고리즘을 사용해줘"라고 명시합니다.

---

## 8-2. 암호화되지 않은 중요정보

### 개요

많은 웹 애플리케이션은 패스워드, 주민등록번호, 신용카드 번호 등의 중요정보(Sensitive Information)를 다루게 됩니다. 이러한 정보가 평문(Plaintext)으로 저장되거나 전송되면, 데이터베이스 유출이나 네트워크 도청 시 모든 정보가 그대로 노출됩니다.

바이브 코딩으로 빠르게 프로토타입을 만들 때, "일단 동작하게 만들고 나중에 암호화를 추가하자"라는 생각은 매우 위험합니다. 나중에 암호화를 추가하는 일은 처음부터 적용하는 것보다 훨씬 어렵고, 종종 잊혀지기도 합니다.

### 왜 위험한가

- **데이터베이스 유출**: 평문으로 저장된 패스워드는 DB 유출 사고 시 즉시 악용됩니다. 사용자들은 여러 사이트에서 같은 패스워드를 사용하는 경우가 많아 피해가 확대됩니다.
- **네트워크 도청**: 평문으로 전송된 정보는 패킷 스니핑(Packet Sniffing)을 통해 중간에서 가로챌 수 있습니다.
- **법적 책임**: 개인정보보호법에 따라 개인정보를 안전하게 관리하지 않을 경우 법적 제재를 받을 수 있습니다.

### 취약한 코드

다음은 패스워드를 평문으로 데이터베이스에 저장하는 ❌ 취약한 코드입니다.

```python
# ❌ 취약한 코드: 패스워드 평문 저장
def register_user(dbconn, username, password):
    cursor = dbconn.cursor()
    # 패스워드가 암호화 없이 그대로 저장됨
    cursor.execute(
        'INSERT INTO users (username, password) VALUES (%s, %s)',
        (username, password)
    )
    dbconn.commit()
```

```python
# ❌ 취약한 코드: 중요정보 평문 전송
import socket

def send_user_data(user_data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('api.example.com', 80))
        # HTTP(평문)로 개인정보 전송
        s.sendall(user_data.encode('utf-8'))
```

### 안전한 코드

패스워드를 해시화하여 저장하고, HTTPS를 통해 전송하는 ✅ 안전한 코드입니다.

```python
# ✅ 안전한 코드: 패스워드를 해시화하여 저장
from Crypto.Hash import SHA256
import os

def register_user(dbconn, username, password):
    # 솔트 생성 후 패스워드와 결합하여 해시
    salt = os.urandom(32).hex()
    hash_obj = SHA256.new()
    hash_obj.update(bytes(password + salt, 'utf-8'))
    hashed_password = hash_obj.hexdigest()

    cursor = dbconn.cursor()
    cursor.execute(
        'INSERT INTO users (username, password, salt) VALUES (%s, %s, %s)',
        (username, hashed_password, salt)
    )
    dbconn.commit()
```

```python
# ✅ 안전한 코드: HTTPS를 사용한 안전한 전송
import requests

def send_user_data(user_data):
    # HTTPS를 사용하여 암호화된 채널로 전송
    response = requests.post(
        'https://api.example.com/users',  # HTTP가 아닌 HTTPS 사용
        json=user_data,
        verify=True  # SSL 인증서 검증 활성화
    )
    return response.json()
```

### 바이브 코딩 시 체크포인트

- [ ] 패스워드는 반드시 해시화(Hashing)하여 저장하고, 평문 저장 코드가 없는지 확인합니다.
- [ ] 외부 API 통신 시 `http://`가 아닌 `https://`를 사용하는지 확인합니다.
- [ ] 개인정보(이름, 전화번호, 주소 등)를 데이터베이스에 저장할 때 암호화를 적용하는지 확인합니다.
- [ ] AI에게 "패스워드는 해시로 저장하고, 통신은 HTTPS를 사용해줘"라고 명시합니다.

---

## 8-3. 하드코딩된 중요정보

### 개요

하드코딩(Hardcoding)이란 소스 코드 내부에 패스워드, API 키(API Key), 데이터베이스 접속 정보 등의 중요정보를 직접 문자열로 작성하는 것을 말합니다. **이것은 바이브 코딩에서 가장 빈번하게 발생하는 보안 실수입니다.**

AI에게 "데이터베이스에 연결하는 코드를 만들어줘"라고 요청하면, AI는 높은 확률로 코드 안에 예시 패스워드와 호스트 정보를 직접 작성합니다. 여러분이 이 코드를 그대로 사용하여 GitHub에 Push하면, 전 세계 누구나 여러분의 데이터베이스 접속 정보를 볼 수 있게 됩니다.

> **⚠️ 주의:** GitHub에는 API 키와 패스워드를 자동으로 수집하는 봇(Bot)이 활동하고 있습니다. 한번 Push된 정보는 커밋 기록에 남아 삭제해도 복구할 수 있습니다. 실수를 발견하면 키를 즉시 폐기하고 새로 발급받아야 합니다.

### 왜 위험한가

> **💡 팁:** AI가 생성한 주석에 민감정보가 포함되는 문제는 11장 11-2절에서 다룹니다.

하드코딩된 중요정보는 다음과 같은 경로로 유출됩니다.

- **소스코드 저장소(Repository) 노출**: GitHub, GitLab 등에 코드를 Push하면 공개 저장소의 경우 즉시 노출됩니다. 비공개 저장소라도 접근 권한이 있는 모든 개발자에게 노출됩니다.
- **로그(Log) 파일 노출**: 코드에 하드코딩된 값이 에러 메시지나 디버그 로그에 포함되어 출력될 수 있습니다.
- **빌드 산출물(Build Artifact) 노출**: 컴파일된 바이너리나 패키지에서 문자열을 추출하여 중요 정보를 획득할 수 있습니다.
- **AI 학습 데이터 오염**: 하드코딩된 키가 포함된 코드가 공개되면, AI 학습 데이터에 포함되어 다른 사람의 AI 응답에 여러분의 키가 노출될 수도 있습니다.

### 취약한 코드

다음은 AI가 흔히 생성하는 형태의 ❌ 취약한 코드입니다.

```python
# ❌ 취약한 코드: API 키와 DB 정보가 소스코드에 하드코딩
import pymysql
import openai

# OpenAI API 키가 소스코드에 그대로 노출
openai.api_key = "sk-proj-abc123xyz456..."

def get_db_connection():
    # 데이터베이스 접속 정보가 하드코딩됨
    return pymysql.connect(
        host='db.example.com',
        port=3306,
        user='admin',
        passwd='SuperSecret123!',
        db='production_db',
        charset='utf8'
    )

def call_stripe_api(amount):
    import stripe
    # 결제 API 키가 소스코드에 노출
    stripe.api_key = "sk_live_51ABC..."
    return stripe.Charge.create(amount=amount, currency="krw")
```

### 안전한 코드

환경 변수(Environment Variable)와 `.env` 파일을 활용하는 ✅ 안전한 코드입니다.

**Step 1: `.env` 파일 생성 (절대 Git에 커밋하지 않습니다)**

```bash
# .env 파일 (이 파일은 .gitignore에 반드시 추가)
OPENAI_API_KEY=sk-proj-abc123xyz456...
DB_HOST=db.example.com
DB_PORT=3306
DB_USER=admin
DB_PASSWORD=SuperSecret123!
DB_NAME=production_db
STRIPE_API_KEY=sk_live_51ABC...
```

**Step 2: `.gitignore`에 `.env` 추가**

```text
# .gitignore
.env
.env.local
.env.production
*.pem
*.key
```

**Step 3: 코드에서 환경 변수 사용**

```python
# ✅ 안전한 코드: 환경 변수를 통한 중요정보 관리
import os
import pymysql
from dotenv import load_dotenv
import openai

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수에서 API 키를 가져옴
openai.api_key = os.environ.get('OPENAI_API_KEY')

def get_db_connection():
    return pymysql.connect(
        host=os.environ.get('DB_HOST'),
        port=int(os.environ.get('DB_PORT', 3306)),
        user=os.environ.get('DB_USER'),
        passwd=os.environ.get('DB_PASSWORD'),
        db=os.environ.get('DB_NAME'),
        charset='utf8'
    )

def call_stripe_api(amount):
    import stripe
    stripe.api_key = os.environ.get('STRIPE_API_KEY')
    return stripe.Charge.create(amount=amount, currency="krw")
```

> **💡 팁:** `os.environ['KEY']`는 키가 없으면 `KeyError`를 발생시키고, `os.environ.get('KEY')`는 `None`을 반환합니다. 필수 환경 변수의 경우 애플리케이션 시작 시 존재 여부를 확인하는 것이 좋습니다.

```python
# ✅ 환경 변수 존재 여부를 시작 시 검증
REQUIRED_ENV_VARS = ['OPENAI_API_KEY', 'DB_HOST', 'DB_PASSWORD']

def validate_env():
    missing = [var for var in REQUIRED_ENV_VARS if not os.environ.get(var)]
    if missing:
        raise EnvironmentError(f"필수 환경 변수가 설정되지 않았습니다: {', '.join(missing)}")
```

### 바이브 코딩 시 체크포인트

- [ ] AI가 생성한 코드에서 API 키, 패스워드, 시크릿 키(Secret Key)가 문자열로 하드코딩되어 있지 않은지 확인합니다.
- [ ] `.env` 파일을 생성하고, 반드시 `.gitignore`에 추가합니다.
- [ ] `python-dotenv` 라이브러리를 설치하여 환경 변수를 관리합니다.
- [ ] Git 커밋 전, `git diff`로 중요 정보가 포함되어 있지 않은지 확인합니다.
- [ ] 이미 커밋된 키가 있다면 즉시 해당 키를 폐기하고 새로 발급받습니다.
- [ ] AI에게 코드를 요청할 때 "API 키는 환경 변수에서 가져와줘"라고 반드시 명시합니다.

> **⚠️ 주의:** `.env.example` 파일을 만들어 필요한 환경 변수의 목록을 공유하되, 실제 값은 절대 포함하지 마십시오.

```text
# .env.example (이 파일은 Git에 커밋해도 됩니다)
OPENAI_API_KEY=your_api_key_here
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
```

---

## 8-4. 충분하지 않은 키 길이

### 개요

암호화 키의 길이(Key Length)는 암호화의 강도를 결정하는 핵심 요소입니다. 아무리 안전한 알고리즘을 사용하더라도 키 길이가 충분하지 않으면, 공격자가 모든 가능한 키를 시도하는 브루트포스 공격으로 암호를 해독할 수 있습니다.

### 왜 위험한가

짧은 키 길이를 사용하면 공격자가 합리적인 시간 내에 모든 키 조합을 시도할 수 있습니다. 예를 들어 RSA 1024비트 키는 이미 안전하지 않은 것으로 분류되어 있으며, 2030년 이후에는 RSA 2048비트도 재검토가 필요할 수 있습니다.

### 권장 키 길이 표

다음은 알고리즘별 최소 권장 키 길이입니다.

| 알고리즘 유형 | 알고리즘 | ❌ 취약한 키 길이 | ✅ 권장 키 길이 |
|---|---|---|---|
| 대칭키 암호(Symmetric) | AES | 64비트 이하 | **128비트 이상** (권장 256비트) |
| 비대칭키 암호(Asymmetric) | RSA | 1024비트 이하 | **2048비트 이상** (권장 3072비트) |
| 비대칭키 암호 | DSA | 1024비트 이하 | **2048비트 이상** |
| 타원곡선 암호(ECC) | ECDSA | 160비트 이하 | **224비트 이상** (권장 256비트) |
| 해시 함수(Hash) | SHA | SHA-1 (160비트) | **SHA-256 이상** |

### 취약한 코드

```python
# ❌ 취약한 코드: RSA 1024비트 키 사용
from Crypto.PublicKey import RSA

def generate_key_pair():
    # 1024비트는 현대 컴퓨터로 해독 가능
    private_key = RSA.generate(1024)
    return private_key, private_key.publickey()
```

### 안전한 코드

```python
# ✅ 안전한 코드: RSA 2048비트 이상 키 사용
from Crypto.PublicKey import RSA

def generate_key_pair():
    # 2048비트 이상으로 설정 (권장: 3072비트 이상)
    private_key = RSA.generate(2048)
    return private_key, private_key.publickey()
```

```python
# ✅ 안전한 코드: ECC 256비트 키 사용
from Crypto.PublicKey import ECC

def generate_ecc_key():
    # P-256 곡선 사용 (224비트 이상)
    key = ECC.generate(curve='P-256')
    return key
```

### 바이브 코딩 시 체크포인트

- [ ] AI가 생성한 암호화 코드에서 키 길이 설정값을 확인합니다.
- [ ] RSA는 최소 2048비트, AES는 최소 128비트, ECC는 최소 224비트인지 확인합니다.
- [ ] `RSA.generate()`, `DSA.generate()` 등의 함수 호출에서 인자값을 반드시 확인합니다.
- [ ] AI에게 "RSA 2048비트 이상으로 키를 생성해줘"라고 명시합니다.

> **💡 팁:** 2030년 이후까지의 안전성을 고려한다면 RSA 3072비트, AES 256비트를 사용하는 것이 바람직합니다.
