
**제2절 보안기능**

보안기능(인증, 접근제어, 기밀성, 암호화, 권한관리 등)을 부적절하게 구현 시 발생할 수 있는 보안약점에는
적절한 인증 없는 중요기능 허용, 부적절한 인가 등이 있다.
1. 적절한 인증 없는 중요 기능 허용
가. 개요
보안기능(인증, 접근제어, 기밀성, 암호화, 권한관리 등)을 부적절하게 구현 시 발생할 수 있는 보안약점으로
적절한 인증 없는 중요기능 허용, 부적절한 인가 등이 포함된다.
파이썬의 Django 프레임워크에서 django.contrib.auth 앱을 통해 기본적인 인증 로그인 및 로그아웃 기능을
제공하고 있으며 DRF(Django REST Framework)에서는 토큰 및 세션 인증을 제공하고 있다.
나. 안전한 코딩기법
클라이언트의 보안 검사를 우회하여 서버에 접근하지 못하도록 설계하고 중요한 정보가 있는 페이지는 재인증을
적용한다. 또한 안전하다고 검증된 라이브러리나 프레임워크(Django authentication system, Flask-Login 등)를
사용해야 한다.
다. 코드예제
다음은 패스워드 수정 시 수정을 요청한 패스워드와 DB에 저장된 사용자 패스워드 일치 여부를 확인하지
않고 처리하고 있으며 패스워드의 재확인 절차도 생략되어 취약한 코드 예시를 보여 준다.

![p75 이미지](images/p75_img0.png)


**안전하지 않은 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
11:
12:
13:
14:
15:
from django.shortcuts import render
from re import escape
import hashlib
def change_password(request):
new_pwd = request.POST.get('new_password','')
# 로그인한 사용자 정보
user = '%s' % escape(request.session['userid'])
# 현재 password와 일치 여부를 확인하지 않고 수정함
sha = hashlib.sha256(new_pwd.encode())
update_password_from_db(user, sha.hexdigest())
return render(request, '/success.html')
DB에 저장된 사용자 패스워드와 변경을 요청한 패스워드의 일치 여부를 확인하고, 변경 요청한 패스워드와
재확인 패스워드가 일치하는지 확인 후 DB의 패스워드를 수정해 안전하게 코드를 적용할 수 있다.

**안전한 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
11:
12:
13:
14:
15:
16:
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from re import escape
import hashlib
# login_required decorator를 사용해 login된 사용자만 접근하도록 처리
@login_required
def change_password(request):
new_pwd = request.POST.get('new_password','')
crnt_pwd = request.POST.get('current_password','')
# 로그인한 사용자 정보를 세션에서 가져온다.
user = '%s' % escape(request.session['userid'])
crnt_h = hashlib.sha256(crnt_pwd.encode())
h_pwd = crnt_h.hexdigest()

![p76 이미지](images/p76_img1.png)


![p76 이미지](images/p76_img2.png)


![p76 이미지](images/p76_img4.png)


![p76 이미지](images/p76_img5.png)


**안전한 코드 예시**

17:
18:
19:
20:
21:
22:
23:
24:
25:
26:
27:
# DB에서 기존 사용자의 Hash된 패스워드 가져오기
old_pwd = get_password_from_db(user)
# 패스워드를 변경하기 전 사용자에 대한 재인증을 수행한다.
if old_pwd == h_pwd:
new_h = hashlib.sha256(new_pwd.encode())
update_password_from_db(user, new_h.hexdigest())
return render(request, '/success.html')
else:
return render(request, ‘failed.html’, {'error': '패스워드가 일치하지 않습니다'})
라. 참고자료
① CWE-306: Missing Authentication for Critical Function, MITRE,
https://cwe.mitre.org/data/definitions/306.html
② Access Control, OWASP,
https://www.owasp.org/index.php/Access_Control_Cheat_Sheet
③ Using the Django authentication system, Django Software Foundation,
https://docs.djangoproject.com/en/3.2/topics/auth/default/
④ Flask-Security,
https://flask-login.readthedocs.io/en/latest/

![p77 이미지](images/p77_img1.png)


![p77 이미지](images/p77_img2.png)

2. 부적절한 인가
가. 개요
프로그램이 모든 가능한 실행 경로에 대해서 접근 제어를 검사하지 않거나 불완전하게 검사하는 경우 공격자는
접근 가능한 실행경로를 통해 정보를 유출할 수 있다.
나. 안전한 코딩기법
응용 프로그램이 제공하는 정보와 기능이 가지는 역할에 맞게 분리 개발함으로써 공격자에게 노출되는 공격
노출면(Attack Surface)3)을 최소화하고 사용자의 권한에 따른 ACL(Access Control List)을 관리한다.
다. 코드예제
사용자 입력값에 따라  삭제 작업을 수행하고 있으며 사용자의 권한 확인을 위한 별도의 통제가 적용되지
않은 예시를 보여 준다.
3) 공격자가 진입 또는 영향을 줄 수 있는 시스템 경계선 지점, 시스템 요소 또는 환경을 의미(https://csrc.nist.g
ov/glossary/term/attack_surface)

![p78 이미지](images/p78_img0.png)


**안전하지 않은 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
11:
12:
from django.shortcuts import render
from .model import Content
def delete_content(request):
action = request.POST.get('action', '')
content_id = request.POST.get('content_id', '')
# 작업 요청을 하는 사용자의 권한 확인 없이 delete를 수행
if action is not None and action == "delete":
Content.objects.filter(id=content_id).delete()
return render(request, '/success.html')
else:
return render(request, '/error.html', {'error':'접근 권한이 없습니다.'})
세션에 저장된 사용자 정보를 통해 해당 사용자가 수행할 작업에 대한 권한이 있는지 확인한 후 권한이 있는
경우에만 작업을 수행하도록 해야 한다.

**안전한 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
11:
12:
13:
14:
15:
16:
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from .model import Content
@login_required
# 해당 기능을 수행할 권한이 있는지 확인
@permission_required('content.delete', raise_exception=True)
def delete_content(request):
action = request.POST.get('action', '')
content_id = request.POST.get('content_id', '')
if action is not None and action == "delete":
Content.objects.filter(id=content_id).delete()
return render(request, '/success.html')
else:
return render(request, '/error.html', {'error':'삭제 실패'})

![p79 이미지](images/p79_img1.png)


![p79 이미지](images/p79_img2.png)


![p79 이미지](images/p79_img4.png)


![p79 이미지](images/p79_img5.png)

라. 참고자료
① CWE-285: Improper Authorization, MITRE,
https://cwe.mitre.org/data/definitions/285.html
② Access Control, OWASP,
https://www.owasp.org/index.php/Access_Control_Cheat_Sheet
③ Using the Django authentication system, Django Software Foundation,
https://docs.djangoproject.com/en/3.2/topics/auth/default/
3. 중요한 자원에 대한 잘못된 권한 설정
가. 개요
응용프로그램이 중요한 보안관련 자원에 대해 읽기 또는 수정하기 권한을 의도하지 않게 허가할 경우 권한을
갖지 않은 사용자가 해당 자원을 사용하게 된다. 파이썬에서는 os.fchmod, os.chmod 등의 함수를 통해 파일
생성, 수정 및 읽기 권한을 설정할 수 있다.
나. 안전한 코딩기법
설정 파일, 실행 파일, 라이브러리 등은 관리자에 의해서만 읽고 쓰기가 가능하도록 설정하고 설정 파일과
같이 중요한 자원을 사용하는 경우 허가 받지 않은 사용자가 중요한 자원에 접근 가능한지 검사한다.
다. 코드예제
다음 예제는 /root/system_config 파일에 대해서 모든 사용자가 읽기, 쓰기, 실행 권한을 가지는 상황을
보여 준다.

**안전하지 않은 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
import os
def write_file():
# 모든 사용자가 읽기, 쓰기, 실행 권한을 가지게 된다.
os.chmod('/root/system_config', 0o777)
with open("/root/system_config",  'w') as f:
f.write("your config is broken")

![p81 이미지](images/p81_img1.png)


![p81 이미지](images/p81_img2.png)


![p81 이미지](images/p81_img3.png)

주요 파일에 대해서는 최소 권한만 할당해야 한다. 구체적으로 파일의 소유자라고 하더라도 기본적으로 읽기
권한만 부여해야 하며, 부득이하게 쓰기 권한이 필요한 경우에만 제한적으로 쓰기 권한을 부여해야 한다.

**안전한 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
import os
def write_file():
# 소유자 외에는 아무런 권한을 주지 않음.
os.chmod('/root/system_config', 0o700)
with open("/root/system_config", ‘'w') as f:
f.write("your config is broken")
라. 참고자료
① CWE-732: Incorrect Permission Assignment for Critical Resource, MITRE,
https://cwe.mitre.org/data/definitions/732.html
② OS – Miscellaneous operating system interfaces, Python Software Foundation,
https://docs.python.org/3/library/os.html

![p82 이미지](images/p82_img1.png)


![p82 이미지](images/p82_img2.png)

4. 취약한 암호화 알고리즘 사용
가. 개요
개발자들은 환경설정 파일에 저장된 패스워드를 보호하기 위해 간단한 인코딩 함수를 이용해 패스워드를
감추는 방법을 사용하기도 한다. 하지만 base64와 같은 지나치게 간단한 인코딩 함수로는 패스워드를 제대로
보호할 수 없다.
정보보호 측면에서 취약하거나 위험한 암호화 알고리즘을 사용해서는 안 된다. 표준화되지 않은 암호화 알고리즘을
사용하는 것은 공격자가 알고리즘을 분석해 무력화시킬 수 있는 가능성을 높일 수도 있다. 몇몇 오래된 암호화
알고리즘의 경우는 컴퓨터의 성능이 향상됨에 따라 취약해지기도 해서, 예전에는 해독하는데 몇 십 억년이 걸릴
것이라고 예상되던 알고리즘이 며칠이나 몇 시간 내에 해독되기도 한다. RC2(ARC2), RC4(ARC4), RC5,
RC6, MD4, MD5, SHA1, DES 알고리즘이 여기에 해당된다.
나. 안전한 코딩기법
자신만의 암호화 알고리즘을 개발하는 것은 위험하며, 학계 및 업계에서 이미 검증된 표준화된 알고리즘을
사용해야 한다. 기존에 취약하다고 알려진 DES, RC5 등의 암호알고리즘을 대신하여 3TDEA, AES, SEED
등의 안전한 암호알고리즘으로 대체하여 사용한다. 또한 업무관련 내용, 개인정보 등에 대한 암호 알고리즘
적용 시 안전한 암호화 알고리즘을 사용해야 한다.

![p83 이미지](images/p83_img0.png)


**< 암호알고리즘 검증기준 ver3.0 (암호모듈시험기관) >**

분류
암호 알고리즘
최소 안전성 수준
⦁112비트
블록암호
(운영모드)
ARIA
⦁운영모드
- 기밀성(ECB, CBC, CFB, OFB, CTR)
- 기밀성/인증(CCM, GCM)
SEED
⦁운영모드
- 기밀성(ECB, CBC, CFB, OFB, CTR)
- 기밀성/인증(CCM, GCM)
LEA
⦁운영모드
- 기밀성(ECB, CBC, CFB, OFB, CTR)
- 기밀성/인증(CCM, GCM)
HIGHT
⦁운영모드
- 기밀성(ECB, CBC, CFB, OFB, CTR)
해시함수
SHA-2
⦁SHA-224/256/384/512
LSH
⦁LSH-224/256/384/512/512-224/512-256
SHA-3
⦁SHA-3-224/256/384/512
메시지
인증
해시함수 기반
⦁HMAC
블록암호 기반
⦁CMAC, GMAC
난수발생기
해시함수 기반
⦁Hash_DRBG, HMAC_DRBG
블록암호 기반
⦁CTR_DRBG
공개키 암호
RSAES
⦁공개키 길이 : 2048, 3072
⦁해시함수 : SHA-224, SHA-256
전자서명
RSA-PSS
⦁공개키 길이 : 2048, 3072
⦁해시함수 : SHA-224, SHA-256
KCDSA
⦁(공개키 길이, 개인키 길이) : (2048, 224), (2048, 256)
⦁해시함수 : SHA-224, SHA-256
EC-KCDSA
⦁p-224, p-256, B-233, B-283, K-233, K-283
⦁해시함수 : SHA-224, SHA-256
ECDSA
⦁p-224, p-256, B-233, B-283, K-233, K-283
⦁해시함수 : SHA-224, SHA-256
키 설정
DH
⦁(공개키 길이, 개인키 길이) : (2048, 224), (2048, 256)
ECDH
⦁P-224, P-256, B-233, B-283, K-233, K-283
키 유도
KBKDF
⦁HMAC, CMAC
PBKDF
⦁HMAC
다. 코드예제
다음 예제는 취약한 DES 알고리즘으로 암호화하는 예시다. DES 이외에 2TDEA, Blowfish, ARC2,
ARC4 등의 취약한 알고리즘을 사용해선 안 된다.

**안전하지 않은 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
import base64
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
def get_enc_text(plain_text, key):
# 취약함 암호화 알고리즘인 DES를 사용하여 안전하지 않음
cipher_des = DES.new(key, DES.MODE_ECB)
encrypted_data = base64.b64encode(cipher_aes.encrypt(pad(plain_text, 32)))
return encrypted_data.decode('ASCII')
파이썬 2.x 버전에서는 PyCrypto를 사용하면 되지만 파이썬 3.x 버전 환경에서 사용 시 동작을 하지 않는
경우가 발생하며, 더 이상 유지 관리 되지 않으므로(deprecated) PyCrypto를 개선한 버전인 pycryptodome를
사용해야 한다. 또한 취약한 DES 알고리즘 대신 안전한 AES 암호화 알고리즘을 사용한다.
블록 암호화에서 운영 모드를 ECB(Electronic Code Block) 모드로 사용할 경우 한 개의 블록만 해독되면
나머지 블록도 해독이 되는 단점이 있다. CBC(Cipher Block Chaining) 모드는 평문의 각 블록이 XOR 연산을
통해 이전 암호문과 연산이 되기 때문에 같은 평문이라도 암호문이 서로 다르다. 이러한 특성으로 보안성이
ECB 모드보다 높다.

**안전한 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
def get_enc_text(plain_text, key, iv):
# 안전한 알고리즘인 AES 를 사용하여 안전함.
cipher_aes = AES.new(key, AES.MODE_CBC, iv)
encrypted_data = base64.b64encode(cipher_aes.encrypt(pad(plain_text, 32)))
return encrypted_data.decode('ASCII')

![p85 이미지](images/p85_img1.png)


![p85 이미지](images/p85_img2.png)


![p85 이미지](images/p85_img4.png)


![p85 이미지](images/p85_img5.png)

다음 예제는 취약한 MD5 해시함수를 사용하는 예시다. 암호 알고리즘과 마찬가지로 해시함수도 수학적으로
취약한 것으로 확인된 MD5와 같은 함수를 사용하면 해시값을 역계산해 평문이 유출될 수 있다.

**안전하지 않은 코드 예시**

1:
2:
3:
4:
5:
6:
7:
import hashlib
def make_md5(plain_text):
# 취약한 md5 해시함수 사용
hash_text = hashlib.md5(plain_text.encode('utf-8')).hexdigest()
return hash_text
아래 코드처럼 수학적으로 안전하다고 알려진 sha-256 해시함수 등을 적용해야 한다.

**안전한 코드 예시**

1:
2:
3:
4:
5:
6:
7:
import hashlib
def make_sha256(plain_text):
# 안전한 sha-256 해시함수 사용
hash_text = hashlib.sha256(plain_text.encode('utf-8')).hexdigest()
return hash_text
라. 참고자료
① CWE-327: Use of a Broken or Risky Cryptographic Algorithm, MITRE,
https://cwe.mitre.org/data/definitions/327.html
② Welcome to pyca/cryptography, Cryptography,
https://cryptography.io/en/latest/
③ Welcome to PyCryptodome’s documentation, PyCryptodome,
https://www.pycryptodome.org/en/latest/
④ Cryptographic Services, Python Software Foundation,
https://docs.python.org/3/library/crypto.html

![p86 이미지](images/p86_img1.png)


![p86 이미지](images/p86_img2.png)


![p86 이미지](images/p86_img4.png)


![p86 이미지](images/p86_img5.png)

5. 암호화되지 않은 중요정보
가. 개요
많은 응용 프로그램은 메모리나 디스크 상에서 중요한 정보(개인정보, 인증정보, 금융정보 등)를 처리한다.
이러한 중요 정보가 제대로 보호되지 않을 경우 보안 문제가 발생하거나 데이터의 무결성이 깨질 수 있다. 특히
사용자 또는 시스템의 중요 정보가 포함된 데이터를 평문으로 송·수신 또는 저장 시 인가되지 않은 사용자에게
민감한 정보가 노출될 수 있다.
나. 안전한 코딩기법
개인정보(주민등록번호, 여권번호 등), 금융정보(카드번호, 계좌번호 등), 패스워드 등 중요정보를 저장하거나
통신채널로 전송할 때는 반드시 암호화 과정을 거쳐야 하며 중요정보를 읽거나 쓸 경우에 권한인증 등을 통해
적합한 사용자만 중요정보에 접근하도록 해야 한다.
가능하다면 SSL 또는 HTTPS 등과 같은 보안 채널을 사용해야 한다. 보안 채널을 사용하지 않고 브라우저
쿠키에 중요 데이터를 저장하는 경우 쿠키 객체에 보안속성을 설정해(Ex. secure = True) 중요 정보의 노출을
방지할 수 있다.
다. 코드예제
⦁중요정보 평문저장
아래 예제는 사용자로부터 전달받은 패스워드 암호화를 누락한 경우이다.

![p87 이미지](images/p87_img0.png)


**안전하지 않은 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
def update_pass(dbconn, password, user_id):
curs = dbconn.cursor()
# 암호화되지 않은 패스워드를 DB에 저장
curs.execute(
'UPDATE USERS SET PASSWORD=%s WHERE USER_ID=%s',
password,
user_id
)
dbconn.commit()
아래는 해시 알고리즘을 이용하여 단방향 암호화 이후에 패스워드를 저장하고 있다. 이 때, 해시함수 또한
SHA256과 같이 안정성이 검증된 알고리즘을 사용해야 한다.

**안전한 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
11:
12:
13:
from Crypto.Hash import SHA256
def update_pass(dbconn, password, user_id, salt):
# 단방향 암호화를 이용하여 패스워드를 암호화
hash_obj = SHA256.new()
hash_obj.update(bytes(password + salt, 'utf-8'))
hash_pwd = hash_obj.hexdigest()
curs = dbconn.cursor()
curs.execute(
'UPDATE USERS SET PASSWORD=%s WHERE USER_ID=%s',
(hash_pwd, user_id)
)
dbconn.commit()

![p88 이미지](images/p88_img1.png)


![p88 이미지](images/p88_img2.png)


![p88 이미지](images/p88_img4.png)


![p88 이미지](images/p88_img5.png)

⦁중요정보 평문전송
아래 예제는 인자값으로 전달 받은 패스워드를 검증 없이 네트워크를 통해 전송하는 예시를 포함한다. 전달
받은 패스워드가 암호화가 되어 있지 않을 경우 패킷 스니핑을 통하여 패스워드가 노출될 수 있다.

**안전하지 않은 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
11:
12:
13:
import socket
HOST = '127.0.0.1'
PORT = 65434
def send_password(password):
......
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
s.connect((HOST, PORT))
# 패스워드를 암호화 하지 않고 전송하여 안전하지 않다.
s.sendall(password.encode('utf-8'))
data = s.recv(1024)
.......
아래는 네트워크를 통해 전달되는 패스워드가 노출되지 않도록 암호화하여 전송하는 예시를 보여 준다.

**안전한 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
11:
12:
13:
14:
15:
import socket
import os
from Crypto.Cipher import AES
HOST = '127.0.0.1'
PORT = 65434
def send_password(password):
# 문자열로 저장되어 있는 블록키를 로드
block_key = os.environ.get('BLOCK_KEY')
aes = AEScipher(block_key)
# 패스워드 등 중요 정보는 암호화하여 전송하는 것이 안전하다
enc_passowrd = aes.encrypt(passowrd)

![p89 이미지](images/p89_img1.png)


![p89 이미지](images/p89_img2.png)


![p89 이미지](images/p89_img4.png)


![p89 이미지](images/p89_img5.png)


**안전한 코드 예시**

16:
17:
18:
19:
20:
21:
22:
23:
24:
25:
26:
27:
28:
29:
30:
31:
32:
33:
34:
35:
36:
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
s.connect((HOST, PORT))
s.sendall(enc_passowrd.encode('utf-8'))
data = s.recv(1024)
.......
class AEScipher:
BS = AES.block_size
def __init__(self, s_key):
self.s_key = hashlib.sha256(s_key.encode("utf-8")).digest()
def pad(self, m):
return m + bytes([self.BS - len(m) % self.BS] * (self.BS - len(m) % self.BS))
def encrypt(self, plain):
plain = self.pad(plain.encode())
iv = Random.new().read(AES.block_size)
cipher = AES.new(self.s_key, AES.MODE_CBC, iv)
return base64.b64encode(iv + cipher.encrypt(plain)).decode("utf-8")
......
라. 참고자료
① CWE-312: Cleartext Storage of Sensitive Information, MITRE,
https://cwe.mitre.org/data/definitions/312.html
② CWE-319: Cleartext Transmission of Sensitive Information, MITRE,
https://cwe.mitre.org/data/definitions/319.html
③ Password Plaintext Storage, OWASP,
https://owasp.org/www-community/vulnerabilities/Password_Plaintext_Storage

![p90 이미지](images/p90_img1.png)


![p90 이미지](images/p90_img2.png)

6. 하드코드된 중요정보
가. 개요
프로그램 코드 내부에 하드코드된 패스워드를 포함하고, 이를 이용해 내부 인증에 사용하거나 외부 컴포넌트와
통신을 하는 경우 관리자의 정보가 노출될 수 있어 위험하다. 또한 하드코드된 암호화 키를 사용해 암호화를
수행하면 암호화된 정보가 유출될 가능성이 높아진다. 암호키의 해시를 계산해 저장하더라도 역계산이 가능해
무차별 공격(Brute-Force)공격에는 취약할 수 있다.
나. 안전한 코딩기법
패스워드는 암호화 후 별도의 파일에 저장하여 사용한다. 또한 중요 정보 암호화 시 상수가 아닌 암호화
키를 사용하도록 하며, 암호화가 잘 되었더라도 소스코드 내부에 상수 형태의 암호화 키를 주석으로 달거나
저장하지 않도록 한다.
다. 코드예제
소스코드에 패스워드 또는 암호화 키와 같은 중요 정보를 하드코딩 하는 경우 중요 정보가 노출될 수 있어
위험하다.

![p91 이미지](images/p91_img0.png)


**안전하지 않은 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
11:
12:
13:
14:
15:
16:
import pymysql
def query_execute(query):
# user, passwd가 소스코드에 평문으로 하드코딩되어 있음
dbconn = pymysql.connect(
host='127.0.0.1',
port='1234',
user='root',
passwd='1234',
db='mydb',
charset='utf8',
)
curs = dbconn.cursor()
curs.execute(query)
dbconn.commit()
dbconn.close()
패스워드와 같은 중요 정보는 안전한 암호화 방식으로 암호화 후 별도의 분리된 공간(파일)에 저장해야 하며,
암호화된 정보 사용 시 복호화 과정을 거친 후 사용해야 한다.

![p92 이미지](images/p92_img1.png)


![p92 이미지](images/p92_img2.png)


**안전한 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
11:
12:
13:
14:
15:
16:
17:
18:
19:
20:
21:
22:
23:
24:
25:
26:
27:
import pymysql
import json
def query_execute(query, config_path):
with open(config_path, 'r') as config:
# 설정 파일에서 user, passwd를 가져와 사용
dbconf = json.load(fp=config)
# 암호화되어 있는 블록 암호화 키를 복호화 해서 가져오는
# 사용자 정의 함수
blockKey = get_decrypt_key(dbconf['blockKey'])
# 설정 파일에 암호화되어 있는 값을 가져와 복호화한 후에 사용
dbUser = decrypt(blockKey, dbconf['user'])
dbPasswd = decrypt(blockKey, dbconf['passwd'])
dbconn = pymysql.connect(
host=dbconf['host']
port=dbconf['port'],
user=dbUser,
passwd=dbPasswd,
db=dbconf['db_name'],
charset='utf8',
)
curs = dbconn.cursor()
curs.execute(query)
dbconn.commit()
dbconn.close()
라. 참고자료
① CWE-259: Use of Hard-coded Password, MITRE,
https://cwe.mitre.org/data/definitions/259.html
② CWE-321: Use of Hard-coded Cryptographic Key, MITRE,
https://cwe.mitre.org/data/definitions/321.html
③ Use of hard-coded password, OWASP,
https://owasp.org/www-community/vulnerabilities/Use_of_hard-coded_password
④ Password Management Hardcoded Password, OWASP,
https://owasp.org/www-community/vulnerabilities/Password_Management_Hardcoded_Password

![p93 이미지](images/p93_img1.png)


![p93 이미지](images/p93_img2.png)

7. 충분하지 않은 키 길이 사용
가. 개요
짧은 길이의 키를 사용하는 것은 암호화 알고리즘을 취약하게 만들 수 있다. 키는 암호화 및 복호화에 사용
되는데, 검증된 암호화 알고리즘을 사용하더라도 키 길이가 충분히 길지 않으면 짧은 시간 안에 키를 찾아낼
수 있고 이를 이용해 공격자가 암호화된 데이터나 패스워드를 복호화 할 수 있게 된다.
암호 알고리즘 및 키 길이 선택 시 암호 알고리즘의 안전성 유지기간과 보안강도별 암호 알고리즘 키 길이
비교표를 기반으로 암호 알고리즘 및 키 길이를 선택해야 한다.

**< 보안강도별 암호 알고리즘 비교표 >**

보안강도
대칭키 암호
알고리즘
(보안강도)
해시함수
(보안강도)
공개키 암호 알고리즘
암호 알고리즘
안전성 유지기간
(년도)
인수분해
(비트)
이산대수
타원곡선
암호(비트)
공개키(비트)
개인키(비트)
112 비트
2048
2048
2011년에서
2030년까지
128 비트
3072
3072
2030년 이후
192 비트
7680
7680
256비트
15360
15360

![p94 이미지](images/p94_img0.png)

나. 안전한 코딩기법
RSA 알고리즘은 적어도 2,048 비트 이상의 길이를 가진 키와 함께 사용해야 하고, 대칭 암호화 알고리즘(Symmetric
Encryption Algorithm)의 경우에는 적어도 128비트 이상의 키를 사용해야 한다(암호 강도 112비트 이상).

**다. 코드예제**

보안성이 강한 RSA 알고리즘을 사용하는 경우에도 키 사이즈를 작게 설정하면 프로그램의 보안약점이 될 수 있다.

**안전하지 않은 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
11:
12:
13:
14:
from Crypto.PublicKey import  RSA, DSA, ECC
from tinyec import registry
import secrets
def make_rsa_key_pair():
# RSA키 길이를 2048 비트 이하로 설정하는 경우 안전하지 않음
private_key = RSA.generate(1024)
public_key = private_key.publickey()
def make_ecc():
# ECC의 키 길이를 224비트 이하로 설정하는 경우 안전하지 않음
ecc_curve = registry.get_curve('secp192r1')
private_key = secrets.randbelow(ecc_curve.field.n)
public_key = private_key * ecc_curve.g
RSA, DSA의 경우 키의 길이는 적어도 2048 비트를, ECC의 경우 224 비트 이상으로 설정해야 안전하다.
다음은 tinyec 모듈을 사용하여 ECC 키를 생성한 예제다.

![p95 이미지](images/p95_img1.png)


![p95 이미지](images/p95_img2.png)


**안전한 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
11:
12:
13:
14:
from Crypto.PublicKey import  RSA, DSA, ECC
from tinyec import registry
import secrets
def make_rsa_key_pair():
# RSA 키 길이를 2048 비트 이상으로 길게 설정
private_key = RSA.generate(2048)
public_key = private_key.publickey()
def make_ecc():
# ECC 키 길이를 224 비트 이상으로 설정
ecc_curve = registry.get_curve('secp224r1')
private_key = secrets.randbelow(ecc_curve.field.n)
public_key = private_key * ecc_curve.g
라. 참고자료
① CWE-326: Inadequate Encryption Strength, MITRE,
https://cwe.mitre.org/data/definitions/326.html
② FEDERAL INFORMATION PROCESSING STANDARDS PUBLICATION (FIPS PUB 186-4), NIST
https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-4.pdf
③ PyCryptodome-RSA,
https://pycryptodome.readthedocs.io/en/latest/src/public_key/rsa.html
④ 암호 알고리즘 및 키 길이 이용 안내서, KISA,
https://www.kisa.or.kr/2060305/form?postSeq=5&lang_type=KO#fnPostAttachDownload
⑤ DSA, Pycryptodome,
https://pycryptodome.readthedocs.io/en/latest/src/public_key/dsa.html
⑥ ECC, Pycryptodome,
https://pycryptodome.readthedocs.io/en/latest/src/public_key/ecc.html

![p96 이미지](images/p96_img1.png)


![p96 이미지](images/p96_img2.png)

8. 적절하지 않은 난수 값 사용
가. 개요
예측 불가능한 숫자가 필요한 상황에서 예측 가능한 난수를 사용한다면 공격자가 생성되는 다음 숫자를 예상해
시스템을 공격할 수 있다.
나. 안전한 코딩기법
난수 발생기에서 시드(Seed)를 사용하는 경우에는 고정된 값을 사용하지 않고 예측하기 어려운 방법으로
생성된 값을 사용한다.
python에서 random 모듈은 주로 보안 목적이 아닌 게임, 퀴즈 및 시뮬레이션을 위해 설계되었다. 세션
ID, 암호화키 등 주요 보안 기능을 위한 값을 생성하고 주요 보안 기능을 수행하는 경우에는 random 모듈보다
암호화 목적으로 설계된 secrets 모듈을 사용해야 한다.
secrets 모듈은 python 3.6 이상에서만 사용 가능하며 암호, 계정 인증, 보안 토큰과 같은 데이터를 관리
하는데 적합한 강력한 난수 생성에 사용할 수 있다. python 3.6 이하에서는 os.urandom(), random.SystemRandom
클래스를 사용하는 것이 안전하다.
다. 코드예제
random 라이브러리 사용 시에는 반드시 유추하기 어려운 seed 값을 이용하여 난수를 생성해야 하며, 이렇게
생성된 난수라 하더라도 강도가 낮기 때문에 주요 보안 기능을 위한 난수 이용 시에는 안전하지 않다. 아래는
안전하지 않은 코드 예제로 고정된 seed 값을 보안이나 암호를 목적으로 사용하는 취약한 random 라이브러리
적용 사례를 보여 준다.

![p97 이미지](images/p97_img0.png)


**안전하지 않은 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
import random
def get_otp_number():
random_str = ''
# 시스템 현재 시간 값을 시드로 사용하고 있으며, 주요 보안 기능을 위한
# 난수로 안전하지 않다
for i in range(6):
random_str += str(random.randrange(10))
return random_str
다음 코드는 secrets 라이브러리를 사용해 6자리의 난수 값을 생성하는 안전한 예제다.

**안전한 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
import secrets
def get_otp_number():
random_str = ''
# 보안기능에 적합한 난수 생성용 secrets 라이브러리 사용
for i in range(6):
random_str += str(secrets.randbelow(10))
return random_str
다음은 세션 토큰값을 생성하는 예제로 random 라이브러리를 사용해 안전하지 않다.

**안전하지 않은 코드 예시**

1:
2:
3:
4:
5:
6:
7:
import random
import string
def generate_session_key():
RANDOM_STRING_CHARS = string.ascii_letters + string.digits
# random 라이브러리를 보안 기능에 사용하면 위험하다
return “”.join(random.choice(RANDOM_STRING_CHARS) for i in range(32))

![p98 이미지](images/p98_img1.png)


![p98 이미지](images/p98_img2.png)


![p98 이미지](images/p98_img4.png)


![p98 이미지](images/p98_img5.png)

패스워드나 인증정보 및 보안토큰 생성에 사용하는 경우 안전한 secrets 라이브러리로 생성한 난수를 이용
해야 한다.

**안전한 코드 예시**

1:
2:
3:
4:
5:
6:
7:
import secrets
import string
def generate_session_key():
RANDOM_STRING_CHARS = string.ascii_letters+string.digits
# 보안 기능과 관련된 난수는 secrets 라이브러리를 사용해야 안전하다
return “”.join(secrets.choice(RANDOM_STRING_CHARS) for i in range(32))
라. 참고자료
① CWE-330: Use of Insufficiently Random Values, MITRE,
https://cwe.mitre.org/data/definitions/330.html
② Insecure Randomness, OWASP,
https://owasp.org/www-community/vulnerabilities/Insecure_Randomness
③ Generate pseudo-random numbers, Python Software Foundation,
https://docs.python.org/3/library/random.html
④ Generate secure random numbers for managing secrets, Python Software Foundation,
https://docs.python.org/3/library/secrets.html

![p99 이미지](images/p99_img1.png)


![p99 이미지](images/p99_img2.png)

9. 취약한 패스워드 허용
가. 개요
사용자에게 강한 패스워드 조합규칙을 요구하지 않으면 사용자 계정이 취약하게 된다. 안전한 패스워드를
생성하기 위해서는 「패스워드 선택 및 이용 안내서」에서 제시하는 패스워드 설정 규칙을 적용해야 한다.
나. 안전한 코딩기법
패스워드 생성 시 강한 조건 검증을 수행한다. 패스워드(패스워드)는 숫자와 영문자, 특수문자 등을 혼합하여
사용하고 주기적으로 변경하여 사용하도록 해야 한다.
다. 코드예제
사용자가 입력한 패스워드에 대한 복잡도 검증 없이 가입 승인 처리를 수행하고 있다.

**안전하지 않은 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
11:
12:
13:
14:
15:
16:
17:
18:
19:
20:
from flask import request, redirect
from Models import User
from Models import db
@app.route('/register', methods=['POST'])
def register():
userid = request.form.get('userid')
password = request.form.get('password')
confirm_password = request.form.get('confirm_password')
if password != confirm_password:
return make_response("패스워드가 일치하지 않습니다", 400)
else:
usertable = User()
usertable.userid = userid
usertable.password = password
# 패스워드 생성 규칙을 확인하지 않고 회원 가입
db.session.add(usertable)
db.session.commit()
return make_response("회원가입 성공", 200)

![p100 이미지](images/p100_img1.png)


![p100 이미지](images/p100_img2.png)


![p100 이미지](images/p100_img3.png)

사용자 계정 보호를 위해 회원가입 시 패스워드 복잡도와 길이를 검증 후 가입 승인처리를 수행해야 한다.
코드 내의 특수문자(‘!@#$%^&*’)는 기업 내부 정책에 따라 변경하여 사용하면 되며, 패스워드를 숫자로만
10자리로 구성할 경우 취약할 수 있으니 사용자가 안전한 패스워드로 변경할 수 있도록 안내해야 한다.

**안전한 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
11:
12:
13:
14:
15:
16:
17:
18:
19:
20:
21:
22:
23:
24:
25:
26:
27:
28:
29:
30:
31:
32:
33:
34:
35:
36:
37:
38:
39:
40:
41:
from flask import request, redirect
from Models import User
from Models import db
import re
@app.route('/register', methods=['POST'])
def register():
userid = request.form.get('userid')
password = request.form.get('password')
confirm_password = request.form.get('confirm_password')
if password != confirm_password:
return make_response("패스워드가 일치하지 않습니다.", 400)
if not check_password(password):
return make_response("패스워드 조합규칙에 맞지 않습니다.", 400)
else:
usertable = User()
usertable.userid = userid
usertable.password = password
db.session.add(usertable)
db.session.commit()
return make_response("회원가입 성공", 200)
def check_password(password):
# 3종 이상 문자로 구성된 8자리 이상 패스워드 검사 정규식 적용
PT1 = re.compile('^(?=.*[A-Z])(?=.*[a-z])[A-Za-z\d!@#$%^&*]{8,}$')
PT2 = re.compile('^(?=.*[A-Z])(?=.*\d)[A-Za-z\d!@#$%^&*]{8,}$')
PT3 = re.compile('^(?=.*[A-Z])(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$')
PT4 = re.compile('^(?=.*[a-z])(?=.*\d)[A-Za-z\d!@#$%^&*]{8,}$')
PT5 = re.compile('^(?=.*[a-z])(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$')
PT6 = re.compile('^(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$')
# 문자 구성 상관없이 10자리 이상 패스워드 검사 정규식
PT7 = re.compile('^[A-Za-z\d!@#$%^&*]{10,}$')
for pattern in [PT1, PT2, PT3, PT4, PT5, PT6, PT7]:
if pattern.match(password):
return True
return False

![p101 이미지](images/p101_img1.png)


![p101 이미지](images/p101_img2.png)

⦁Django 프레임워크의 VALIDATORS 사용
Django에서는 미들웨어의 AUTH_PASSWORD_VALIDATORS 설정에서 패스워드에 대한 검증을 지원하며,
기본적으로 아래와 같은 검증을 수행한다.
⦁UserAttributeSimilarityValidator : 패스워드가 사용자의 다른 속성값(이름, 성, 이메일)등과의 유사도 확인
⦁MinimumLengthValidator : 패스워드 길이의 최소값 확인(default 8)
⦁CommonPasswordValidator : 사람들이 가장 많이 사용하는 패스워드 20,000개에 해당하는지 확인
⦁NumericPasswordValidator : 패스워드가 숫자로만 구성되어있는지 확인
기본 Validator 외에 필요한 추가 검증 기준이 있다면 사용자 정의 Validator를 생성한 후
AUTH_PASSWORD_VALIDATORS에 등록해 적용 가능하다. 아래는 사용자 Validator 정의 예시를 보여
준다(검증 통과 시 None 반환, 실패 시 ValidationError 발생하도록 구현 필요).

**안전한 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
11:
12:
13:
14:
15:
16:
17:
18:
19:
20:
21:
22:
23:
24:
25:
26:
27:
28:
29:
import re
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
class CustomValidator(object):
def validate(self, password, user=None):
# 3종 이상 문자로 구성된 8자리 이상 패스워드 검사 정규식
PT1 = re.compile('^(?=.*[A-Z])(?=.*[a-z])[A-Za-z\d!@#$%^&*]{8,}$')
PT2 = re.compile('^(?=.*[A-Z])(?=.*\d)[A-Za-z\d$@$!%*?&]{8,}$')
PT3 = re.compile('^(?=.*[A-Z])(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$')
PT4 = re.compile('^(?=.*[a-z])(?=.*\d)[A-Za-z\d!@#$%^&*]{8,}$')
PT5 = re.compile('^(?=.*[a-z])(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$')
PT6 = re.compile('^(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$')
# 문자 구성 상관없이 10자리 이상 패스워드 검사 정규식
PT7 = re.compile('^[A-Za-z\d!@#$%^&*]{10,}$')
for pattern in [PT1, PT2, PT3, PT4, PT5, PT6, PT7]:
if pattern.match(password):
return None
raise ValidationError(
_("패스워드 조합규칙에 적합하지 않습니다.."),
code='improper_password',
)
def get_help_text(self):
return _(
"패스워드는 영문 대문자, 소문자, 숫자, 특수문자 조합 중 2가지 이상 8자리이거나 문자 구성
상관없이 10자리 이상이어야 합니다."
)

![p102 이미지](images/p102_img1.png)


![p102 이미지](images/p102_img2.png)

라. 참고자료
① CWE-521: Weak Password Requirements, MITRE,
https://cwe.mitre.org/data/definitions/521.html
② Authentication Cheat Sheet, OWASP,
https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
③ Regular Expression HOWTO, Python Software Foundation,
https://docs.python.org/3/howto/regex.html
④ Password management in Django, Django Software Foundation,
https://docs.djangoproject.com/en/4.0/topics/auth/passwords/
10. 부적절한 전자서명 확인
가. 개요
프로그램, 라이브러리, 코드의 전자서명에 대한 유효성 검증이 적절하지 않아 공격자의 악의적인 코드가 실행
가능한 보안약점으로, 클라이언트와 서버 사이의 주요 데이터 전송, 파일 다운로드 시 발생할 수 있다. 데이터
전송 또는 다운로드 시 함께 전달되는 전자서명은 원문 데이터의 암호화된 해시 값으로, 수신측에서 이 서명을
검증해 데이터 변조 여부를 확인할 수 있다. 단순히 해시 기반 검증만 사용할 경우 해시 자체를 변조해 악성코드를
전달할 수 있지만 전자서명을 사용하게 되면 원문 데이터에 대한 해시 자체도 안전하게 보호할 수 있다.
나. 안전한 코딩기법
주요 데이터 전송 또는 다운로드 시 데이터에 대한 전자서명을 함께 전송하고 수신측에서는 전달 받은 전자
서명을 검증해 파일의 변조 여부를 확인해야 한다.

![p104 이미지](images/p104_img0.png)

다. 코드예제
다음은 송신측이 데이터와 함께 전달한 전자서명을 수신측에서 별도로 처리하지 않고 데이터를 그대로 신뢰해
데이터 내부에 포함된 파이썬 코드가 실행되는 취약한 예시를 보여 준다.

**안전하지 않은 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
11:
12:
13:
14:
15:
16:
17:
18:
19:
20:
21:
22:
23:
24:
25:
26:
27:
28:
import base64
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5 as SIGNATURE_PKCS1_v1_5
from Crypto.Cipher import PKCS1_v1_5, AES
from Crypto.Util.Padding import unpad
...
def verify_data(request):
# 클라이언트로부터 전달받은 데이터(전자서명을 수신 처리 하지 않음)
encrypted_code = request.POST.get("encrypted_msg", "")  # 암호화된 파이썬 코드
# 서버의 대칭키 로드 (송수신측이 대칭키를 이미 공유했다고 가정)
with open(f"{PATH}/keys/secret_key.out", "rb") as f:
secret_key = f.read()
# 대칭키로 클라이언트가 전달한 파이썬 코드 복호화
# (decrypt_with_symmetric_key 함수는 임의의 함수명으로 세부적인 복호화 과정은 생략함)
origin_python_code = decrypt_with_symmetric_key(secret_key, encrypted_code)
# 클라이언트로부터 전달 받은 파이썬 코드 실행
eval(origin_python_code)
return render(
request,
"/verify_success.html",
{"result": "파이썬 코드를 실행했습니다."},
)
중요한 정보 또는 기능 실행으로 연결되는 데이터를 전달하는 경우 반드시 전자서명을 함께 전송해야 하며,
수신측에서는 전자서명을 확인해 송신측에서 보낸 데이터의 무결성을 검증해야 한다. 만약 송수신 측 언어가
다른 경우 사용한 암호 라이브러리에 따라 데이터 인코딩 방식에 차이가 있으니 반드시 코드 배포 전 서명
검증에 필요한 복호화 과정이 정상적으로 잘 처리되는지 검증해야 한다.

![p105 이미지](images/p105_img1.png)


![p105 이미지](images/p105_img2.png)


**안전한 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
11:
12:
13:
14:
15:
16:
17:
18:
19:
20:
21:
22:
23:
24:
25:
26:
27:
28:
29:
30:
31:
32:
33:
34:
35:
36:
37:
38:
39:
# 전자서명 검증에 사용한 코드는 의존한 파이썬 패키지 및 송신측 언어에 따라
# 달라질 수 있으며, 사전에 공유한 공개키로 복호화한 전자서명과 원본 데이터 해시값의
# 일치 여부를 검사하는 코드를 포함
def verify_digit_signature (
origin_data: bytes, origin_signature: bytes, client_pub_key: str ) -> bool:
hashed_data = SHA256.new(origin_data)
signer = SIGNATURE_PKCS1_v1_5.new(RSA.importKey(client_pub_key))
return signer.verify(hashed_data, base64.b64decode(origin_signature))
def verify_data(request):
# 클라이언트로부터 전달받은 데이터
encrypted_code = request.POST.get("encrypted_msg", "")  # 암호화된 파이썬 코드
encrypted_sig = request.POST.get("encrypted_sig", "")  # 암호화된 전자서명
# 서버의 대칭(비밀)키 및 공개키 로드
with open(f"/keys/secret_key.out", "rb") as f:
secret_key = f.read()
with open(f"/keys/public_key.out", "rb") as f:
public_key = f.read()
# 대칭키로 파이썬 코드 및 전자서명 복호화
origin_python_code = decrypt_with_symmetric_key(symmetric_key, encrypted_code)
origin_signature = decrypt_with_symmetric_key(symmetric_key, encrypted_sig)
# 클라이언트의 공개키를 통해 파이썬 코드(원문)와 전자서명을 검증
verify_result = verify_digit_signature(origin_python_code, origin_signature, client_pub_key)
# 전자서명 검증을 통과했다면 파이썬 코드 실행
if verify_result:
eval(origin_python_code)
return render(request, "/verify_success.html",
{"result": "전자서명 검증 통과 및 파이썬 코드를 실행했습니다."},
)
else:
return render(request, "/verify_failed.html",
{"result": "전자서명 또는 파이썬 코드가 위/변조되었습니다."},
)

![p106 이미지](images/p106_img1.png)


![p106 이미지](images/p106_img2.png)

라. 참고자료
① CWE-347: Improper Verification of Cryptographic Signature, MITRE,
https://cwe.mitre.org/data/definitions/347.html
② Security Consideration for Code Signing, NIST,
https://csrc.nist.gov/CSRC/media/Publications/white-paper/2018/01/26/security-considerations-for-code
-signing/final/documents/security-considerations-for-code-signing.pdf
③ Verifying a signature, PyCryptodome.
https://www.pycryptodome.org/src/signature/signature?highlight=verify#verifying-a-signature
11. 부적절한 인증서 유효성 검증
가. 개요
인증서가 유효하지 않거나 악성인 경우 공격자가 호스트와 클라이언트 사이의 통신 구간을 가로채 신뢰하는
엔티티 인 것처럼 속일 수 있다. 이로 인해 대상 호스트가 신뢰 가능한 것으로 믿고 악성 호스트에 연결하거나
신뢰된 호스트로부터 전달받은 것처럼 보이는 스푸핑 된(또는 변조된 데이터)를 아무런 의심 없이 수신하는
상황이 발생할 수 있다.
나. 안전한 코딩기법
데이터 통신에 인증서를 사용하는 경우 송신측에서 전달한 인증서가 유효한지 검증한 후 데이터를 송수신해야
한다. 언어에서 기본으로 제공되는 검증 함수가 존재하지 않거나 일반적이지 않은 방식으로 인증서를 생성한
경우 암호화 패키지를 사용해 별도의 검증 코드를 작성해야 한다.
다. 코드예제
다음은 SSL 기반 소켓 연결 예시로, 클라이언트 측에서 통신 대상 서버를 인증하지 않고 접속하는 상황을
보여 준다. 이 경우 서버를 신뢰할 수 없으며 클라이언트 시스템에 영향을 주는 악성 데이터를 수신할 수 있다.

![p108 이미지](images/p108_img0.png)


**안전하지 않은 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
11:
12:
13:
14:
15:
16:
17:
18:
19:
20:
21:
22:
23:
24:
import os
import socket
import ssl
HOST, PORT = "127.0.0.1", 7917
def connect_with_server():
with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
# 보안 정책 수동 설정
context = ssl.SSLContext()
# SSLContext 생성자를 직접 호출할 때, CERT_NONE이 기본값
# 상대방을 인증하지 않기 때문에 통신하고자하는 서버의 신뢰성을 보장할 수 없음
context.verify_mode = ssl.CERT_NONE
with context.wrap_socket(sock) as ssock:
try:
ssock.connect((HOST, PORT))
ssock.send("Hello I'm a vulnerable client :)".encode("utf-8"))
data = ssock.recv(1024).decode("utf-8")
print(f">> server from ({HOST}, {PORT}): {data}\n")
finally:
ssock.close()
SSL 연결 시 PROTOCOL_TLS_CLIENT 프로토콜을 추가해 인증서 유효성 검사와 호스트 이름 확인을
위한 context를 구성하면 verify_mode가 CERT_REQUIRED로 설정되며 서버의 인증서 유효성을 검증할 수 있다.

![p109 이미지](images/p109_img1.png)


![p109 이미지](images/p109_img2.png)


**안전한 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
11:
12:
13:
14:
15:
16:
17:
18:
19:
20:
21:
22:
23:
24:
25:
26:
27:
28:
29:
30:
31:
32:
33:
34:
35:
import os
import socket
import ssl
CURRENT_PATH = os.getcwd()
HOST_NAME = "test-server"
HOST, PORT = "127.0.0.1", 7917
SERVER_CA_PEM = f"{CURRENT_PATH}/rsa_server/CA.pem"  # 서버로부터 전달받은 CA 인증서
def connect_with_server():
with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
# PROTOCOL_TLS_CLIENT 프로토콜을 추가하여 인증서 유효성 검사와 호스트 이름 확인을 위한
# context를 구성. verify_mode가 CERT_REQUIRED로 설정됨
# check_hostname이 True로 설정됨
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
# 서버로부터 전달받은 CA 인증서를 context에 로드
# CERT_REQUIRED로 인해 필수
context.load_verify_locations(SERVER_CA_PEM)
# 호스트 이름(HOST_NAME)이 일치하지 않으면 통신 불가
# 생성된 소켓과 context wrapping 시 server_hostname이 실제 서버에서
# 등록(server.csr)한 호스트 명과 일치해야 함
with context.wrap_socket(sock, server_hostname=HOST_NAME) as ssock:
try:
ssock.connect((HOST, PORT))
ssock.send("Hello I'm a patched client :)".encode("utf-8"))
data = ssock.recv(1024).decode("utf-8")
print(f">> server from ({HOST}, {PORT}): {data}\n")
finally:
ssock.close()

![p110 이미지](images/p110_img1.png)


![p110 이미지](images/p110_img2.png)

라. 참고자료
① CWE-295: Improper Certificate Validation, MITRE,
https://cwe.mitre.org/data/definitions/295.html
② Identification and Authentication Failures, OWASP,
https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/
③ TLS/SSL Wrapper for Socket Object, Python documentation
https://docs.python.org/ko/3/library/ssl.html
④ Improper Certificate validation, AWS.
https://docs.aws.amazon.com/codeguru/detector-library/python/improper-certificate-validation/
12. 사용자 하드디스크에 저장되는 쿠키를 통한 정보 노출
가. 개요
대부분의 웹 응용프로그램에서 쿠키는 메모리에 상주하며, 브라우저가 종료되면 사라진다. 개발자가 원하는
경우, 브라우저 세션에 관계없이 지속적으로 쿠키 값을 저장하도록 설정할 수 있다. 이 경우 정보는 디스크에
기록되고 다음 브라우저 세션 시작 시 메모리에 로드 된다. 개인정보, 인증 정보 등이 이와 같은 영속적인 쿠키
(Persistent Cookie)에 저장된다면, 공격자는 쿠키에 접근할 수 있는 보다 많은 기회를 가지게 되며, 이는
시스템을 취약하게 만든다.
나. 안전한 코딩기법
쿠키의 만료시간은 세션 지속 시간을 고려하여 최소한으로 설정하고 영속적인 쿠키에는 사용자 권한 등급,
세션 ID 등 중요 정보가 포함되지 않도록 한다.
다. 코드예제
다음은 쿠키의 만료시간을 과도하게 길게 설정해 사용자 하드 디스크에 저장된 쿠키가 도용되는 상황을 보여 준다.

![p112 이미지](images/p112_img0.png)


**안전하지 않은 코드 예시**

1:
2:
3:
4:
5:
6:
7:
from django.http import HttpResponse
def remind_user_state(request):
res = HttpResponse()
# 쿠키의 만료시간을 1년으로 과도하게 길게 설정하고 있어 안전하지 않다
res.set_cookie('rememberme', 1, max_age=60*60*24*365)
return res
만료 시간은 해당 기능에 맞춰 최소로 설정하고 영속적인 쿠키에는 중요 정보가 포함되지 않도록 한다. 쿠키를
HTTPS를 통해서만 전송하도록 secure 속성값을 True(기본값은 False)를 사용할 수 있다. 클라이언트 측에서
JavaScript를 통해 쿠키를 접근하지 못하도록 제한 하고자 할 경우엔 httpOnly 속성을 True(기본값은 False)로
설정한다. 다음은 쿠키 만료 시간을 1시간으로 설정한 예시다.

**안전한 코드 예시**

1:
2:
3:
4:
5:
6:
7:
from django.http import HttpResponse
def remind_user_state(request):
res = HttpResponse()
# 쿠키의 만료시간을 적절하게 부여하고 secure 및 httpOnly 옵션을 활성화 한다.
res.set_cookie('rememberme', 1, max_age=60*60, secure=True, httponly=True)
return res
Django에서는 settings.py에 아래와 같이 추가해 전역으로 설정할 수 있다.

![p113 이미지](images/p113_img1.png)


![p113 이미지](images/p113_img2.png)


![p113 이미지](images/p113_img4.png)


![p113 이미지](images/p113_img5.png)


**안전한 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
11:
12:
13:
14:
15:
16:
17:
18:
19:
20:
21:
22:
23:
24:
25:
from django.http import HttpResponse
from django.conf.global_settings import (
SESSION_COOKIE_AGE,
SESSION_COOKIE_HTTPONLY,
SESSION_COOKIE_HTTPONLY,
)
"""
# settings.py
SESSION_COOKIE_AGE = 60 * 60 * 24 * 14
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
"""
def remind_user_state(request):
res = HttpResponse()
# 서버 세팅(setting.py)에서 default로 쿠키 옵션을 설정한 상태
res.set_cookie(
"rememerme",
1,
max_age=SESSION_COOKIE_AGE,
secure=SESSION_COOKIE_HTTPONLY,
httponly=SESSION_COOKIE_HTTPONLY,
)
return res
라. 참고자료
① CWE-539: Use of Persistent Cookies Containing Sensitive Information, MITRE,
https://cwe.mitre.org/data/definitions/539.html
② Expire and Max-Age Attributes, OWASP,
https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
#expire-and-max-age-attributes
③ HTTP state management, Python Software Foundation,
https://docs.python.org/ko/3/library/http.cookies.html
④ Django set_cookie, Django Software Foundation,
https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpResponse.set_cookie
⑤ Django Settings, Django Software Foundation,
https://docs.djangoproject.com/en/4.0/ref/settings/#sessions

![p114 이미지](images/p114_img1.png)


![p114 이미지](images/p114_img2.png)

13. 주석문 안에 포함된 시스템 주요정보
가. 개요
소프트웨어 개발자가 편의를 위해서 주석문에 패스워드를 적어둔 경우 소프트웨어가 완성된 후에는 그것을
제거하는 것이 매우 어렵게 된다. 만약 공격자가 소스코드에 접근할 수 있다면 시스템에 손쉽게 침입할 수 있다.
나. 안전한 코딩기법
주석에는 아이디, 패스워드 등 보안과 관련된 내용을 기입하지 않는다.
다. 코드예제
편리성을 위해 아이디, 패스워드 등 중요정보를 주석문 안에 작성 후 지우지 않는 경우 정보 노출 보안약점이
발생한다.

**안전하지 않은 코드 예시**

1:
2:
3:
4:
5:
6:
7:
def user_login(id, passwd):
# 주석문에 포함된 중요 시스템의 인증 정보
# id = admin
# passwd = passw0rd
result = login(id, passwd)
return result

![p115 이미지](images/p115_img1.png)


![p115 이미지](images/p115_img2.png)


![p115 이미지](images/p115_img3.png)

프로그램 개발 시에 주석문 등에 남겨놓은 사용자 계정이나 패스워드 등의 정보는 개발 완료 후 확실하게
삭제해야 한다.

**안전한 코드 예시**

1:
2:
3:
4:
def user_login(id, passwd):
# 주석문에 포함된 민감한 정보는 삭제
result = login(id, passwd)
return result
라. 참고자료
① CWE-615: Inclusion of Sensitive Information in Source Code Comments, MITRE,
https://cwe.mitre.org/data/definitions/615.html

![p116 이미지](images/p116_img1.png)


![p116 이미지](images/p116_img2.png)

14. 솔트 없이 일방향 해시 함수 사용
가. 개요
패스워드와 같이 중요정보를 저장할 경우 가변 길이 데이터를 고정된 크기의 해시값으로 변환해주는 일방향
해시함수를 이용해 저장할 수 있다. 만약 중요정보를 솔트(Salt)없이 일방향 해시함수를 사용해 저장한다면
공격자는 미리 계산된 레인보우 테이블을 이용해 해시값을 알아낼 수 있다.
나. 안전한 코딩기법
패스워드와 같은 중요 정보를 저장할 경우 임의의 길이인 데이터를 고정된 크기의 해시값으로 변환해주는
일방향 해시함수를 이용하여 저장한다. 또한 솔트값은 사용자별로 유일하게 생성해야 하며, 이를 위해 사용자별
솔트 값을 별도로 저장하는 과정이 필요하다.
파이썬에서는 hashlib 라이브러리를 사용해 해시값을 생성할 수 있으며 salt 값은 os.urandom() 등 안전한
난수 생성 라이브러리를 사용하여 생성해야 한다.
다. 코드예제
다음은 salt 없이 길이가 짧은 패스워드를 해시 함수에 전달해 원문이 공격자에 의해 쉽게 유추되는 예시를 보여 준다.

**안전하지 않은 코드 예시**

1:
2:
3:
4:
5:
6:
7:
import hashlib
def get_hash_from_pwd(pw):
# salt 없이 생성된 해시값은 강도가 약해 취약하다
h = hashlib.sha256(pw.encode())
return h.digest()

![p117 이미지](images/p117_img1.png)


![p117 이미지](images/p117_img2.png)


![p117 이미지](images/p117_img3.png)

짧은 길이의 패스워드로 강도 높은 해시값을 생성하기 위해서는 반드시 솔트 값을 함께 전달해야 한다.

**안전한 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
import hashlib
import secrets
def get_hash_from_pwd(pw):
# 솔트 값을 사용하면 길이가 짧은 패스워드로도 고강도의 해시를 생성할 수 있다.
# 솔트 값은 사용자별로 유일하게 생성해야 하며, 패스워드와 함께 DB에 저장해야 한다
salt = secrets.token_hex(32)
h = hashlib.sha256(salt.encode() + pw.encode())
return h.digest(), salt
라. 참고자료
① CWE-759: Use of a One-Way Hash without a Salt, MITRE,
https://cwe.mitre.org/data/definitions/759.html
② Password Storage Cheat Sheet – Salting, OWASP,
https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html#salting
③ hashlib – Secure hashes and message digests, Python Software Foundation,
https://docs.python.org/3/library/hashlib.html
④ secrets, Python Software Foundation,
https://docs.python.org/ko/3/library/secrets.html#module-secrets

![p118 이미지](images/p118_img1.png)


![p118 이미지](images/p118_img2.png)

15. 무결성 검사없는 코드 다운로드
가. 개요
원격지에 위치한 소스코드 또는 실행 파일을 무결성 검사 없이 다운로드 후 이를 실행하는 프로그램이  존재
한다. 이러한 프로그램은 호스트 서버의 변조, DNS 스푸핑(Spoofing) 또는 전송 시의 코드 변조 등의 방법을
이용해 공격자가 악의적인 코드를 실행하는 위협에 취약하게 된다.
파일(및 해당 소프트웨어) 무결성을 확인하는 두 가지 주요 방법으로는 암호화 해시 및 디지털 서명이 있다.
무결성을 보장하기 위해 해시를 사용하고 가능하면 적절한 코드 서명 인증서를 사용하고 확인하는 것이 더
안전하다.
나. 안전한 코딩기법
DNS 스푸핑(Spoofing)을 방어할 수 있는 DNS lookup을 수행하고 코드 전송 시 신뢰할 수 있는 암호
기법을 이용해 코드를 암호화한다. 또한 다운로드한 코드는 작업 수행을 위해 필요한 최소한의 권한으로 실행
하도록 한다.
소스코드는 신뢰할 수 있는 사이트에서만 다운로드해야 하고 파일의 인증서 또는 해시값을 검사해 변조되지
않은 파일인지 확인하여야 한다.
다. 코드예제
다음 예제는 requests.get을 통해 원격에서 파일을 다운로드한 뒤 파일에 대한 무결성 검사를 수행하지 않아
파일 변조 등으로 인한 피해가 발생하는 사례를 보여 준다. 이 경우 공격자가 악의적인 코드를 실행할 수 있다.

![p119 이미지](images/p119_img0.png)


**안전하지 않은 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
11:
12:
13:
14:
import requests
def execute_remote_code():
# 신뢰할 수 없는 사이트에서 코드를 다운로드
url = "https://www.somewhere.com/storage/code.py"
# 원격 코드 다운로드
file = requests.get(url)
remote_code = file.content
file_name = 'save.py'
with open(file_name, 'wb') as f:
f.write(file.content)
......
안전한 코드 실행을 위해 다운로드한 파일과 해당 파일의 해시값 비교 등을 통해 무결성 검사를 거치고 코드를
실행해야 한다.

**안전한 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
11:
12:
13:
14:
15:
16:
17:
18:
19:
20:
21:
22:
23:
24:
25:
26:
import requests
import hashlib
import configparser
def execute_remote_code():
config = configparser.RawConfigParser()
config.read(‘sample_config.cfg’)
url = "https://www.somewhere.com/storage/code.py"
remote_code_hash = config.get('HASH', 'file_hash')
# 원격 코드 다운로드
file = requests.get(url)
remote_code = file.content
sha = hashlib.sha256()
sha.update(remote_code)
# 다운로드 받은 파일의 해시값 검증
if sha.hexdigest() != remote_code_hash:
raise Exception(‘파일이 손상되었습니다.’)
file_name = 'save.py'
with open(file_name, 'wb') as f
f.write(file.content)
......

![p120 이미지](images/p120_img1.png)


![p120 이미지](images/p120_img2.png)


![p120 이미지](images/p120_img4.png)


![p120 이미지](images/p120_img5.png)

라. 참고자료
① CWE-494: Download of Code Without Integrity Check, MITRE,
https://cwe.mitre.org/data/definitions/494.html
② Secure hashes and message digests, Python Software Foundation,
https://docs.python.org/3/library/hashlib.html
➂ Top 25 Series – Download of Code Without Integrity Check, SANS,
https://www.sans.org/blog/top-25-series-rank-20-download-of-code-without-integrity-check/
16. 반복된 인증시도 제한 기능 부재
가. 개요
일정 시간 내에 여러 번의 인증 시도 시 계정 잠금 또는 추가 인증 방법 등의 충분한 조치가 수행되지 않는
경우 공격자는 성공할 법한 계정과 패스워드들을 사전(Dictionary)으로 만들고 무차별 대입(brute-force)하여
로그인 성공 및 권한 획득이 가능하다.
Django는 사용자 인증 요청 횟수를 제어하지 않는다. 인증 시스템에 대한 무차별 대입 공격으로부터 보호하기
위해 Django 플러그인(django-defender) 또는 웹 서버 모듈을 사용하여 요청을 제한할 수도 있다.
나. 안전한 코딩기법
최대 인증시도 횟수를 적절한 횟수로 제한하고 설정된 인증 실패 횟수를 초과할 경우 계정을 잠금 하거나
추가적인 인증 과정을 거쳐서 시스템에 접근이 가능하도록 한다. 코드 상에서 인증시도 횟수를 제한하는 방법
외에 CAPTCHA나 Two-Factor 인증 방법도 설계 시부터 고려해야 한다.
다. 코드예제
다음 예제는 사용자 로그인 시도에 대한 횟수를 제한하지 않는 코드를 보여 준다.

![p122 이미지](images/p122_img0.png)


**안전하지 않은 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
11:
12:
13:
14:
15:
16:
17:
import hashlib
from django.shortcuts import render
def login(request):
user_id = request.POST.get('user_id', '')
user_pw = request.POST.get('user_pw', '')
sha = hashlib.sha256()
sha.update(user_pw.encode(‘utf-8’))
hashed_passwd = get_user_pw(user_id)
# 인증 시도에 따른 제한이 없어 반복적인 인증 시도가 가능
if sha.hexdigest() == hashed_passwd:
return render(request, '/index.html', {'state':'login_success'})
else:
return render(request, '/login.html', {'state':'login_failed'})
다음은 사용자 로그인 시도에 대한 횟수를 제한하여 무차별 공격에 대응하는 방법을 보여 준다.

**안전한 코드 예시**

1:
2:
3:
4:
5:
6:
7:
8:
9:
10:
11:
12:
13:
14:
15:
16:
17:
import hashlib
from django.shortcuts import render
from .models import LoginFail
LOGIN_TRY_LIMIT = 5
def login(request):
user_id = request.POST.get('user_id', '')
user_pw = request.POST.get('user_pw', '')
sha = hashlib.sha256()
sha.update(user_pw.encode(‘utf-8’))
hashed_passwd = get_user_pw(user_id)
if sha.hexdigest() == hashed_passwd:
# 로그인 성공 시 실패 횟수 삭제
LoginFail.objects.filter(user_id=user_id).delete()
return render(request, '/index.html', {'state':'login_success'})

![p123 이미지](images/p123_img1.png)


![p123 이미지](images/p123_img2.png)


![p123 이미지](images/p123_img4.png)


![p123 이미지](images/p123_img5.png)


**안전한 코드 예시**

18:
19:
20:
21:
22:
23:
24:
25:
26:
27:
28:
29:
30:
31:
32:
33:
34:
35:
36:
37:
# 로그인 실패 기록 가져오기
if LoginFail.objects.filter(user_id=user_id).exists():
login_fail = LoginFail.objects.get(user_id=user_id)
COUNT = login_fail.count
else:
COUNT = 0
if COUNT >= LOGIN_TRY_LIMIT:
# 로그인 실패횟수 초과로 인해 잠금된 계정에 대한 인증 시도 제한
return render(request, "/account_lock.html", {"state": "account_lock"})
else:
# 로그인 실패 횟수 DB 기록
# 첫 시도라면 DB에 insert,
# 실패 기록이 존재한다면 update
LoginFail.objects.update_or_create(
user_id=user_id,
defaults={"count": COUNT + 1},
)
return render(request, "/login.html", {"state": "login_failed"})
라. 참고자료
① CWE-307: Improper Restriction of Excessive Authentication Attempts, MITRE,
https://cwe.mitre.org/data/definitions/307.html
② Blocking Brute Force Attacks, OWASP,
https://owasp.org/www-community/controls/Blocking_Brute_Force_Attacks
➂ additional security topics, Django Software Foundation,
https://docs.djangoproject.com/en/3.2/topics/security/#additional-security-topics
➃ Django-defender,
https://github.com/jazzband/django-defender

![p124 이미지](images/p124_img1.png)


![p124 이미지](images/p124_img2.png)
