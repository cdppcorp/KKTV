# Chapter 06. 데이터 타입과 보안 결정을 노리는 공격

## 6-1. 정수형 오버플로우(Integer Overflow)

### 개요

정수형 오버플로우(Integer Overflow)는 변수가 저장할 수 있는 범위를 넘어선 값이 할당될 때, 실제 저장되는 값이 의도치 않게 아주 작은 수나 음수가 되어 프로그램이 예기치 않게 동작하는 취약점입니다.

파이썬(Python)은 다른 언어와 달리 기본 정수형에 대해 **임의 정밀도 연산(Arbitrary-Precision Arithmetic)**을 지원하므로, 순수 파이썬 코드에서는 정수형 오버플로우가 발생하지 않습니다. 하지만 `numpy`, `pandas` 등 C 기반 라이브러리를 사용할 때는 고정 크기 정수형이 사용되므로 오버플로우가 발생할 수 있습니다.

### 왜 위험한가

바이브 코딩으로 데이터 분석이나 과학 계산 기능을 구현할 때 `numpy` 등의 라이브러리를 많이 사용합니다. 이 라이브러리들은 성능을 위해 C 언어와 동일한 방식으로 정수를 처리하므로 오버플로우에 주의해야 합니다:

```python
import numpy as np

# 파이썬 기본 정수: 오버플로우 없음
result = 2 ** 100  # 정상적으로 큰 수가 저장됩니다

# numpy 64비트 정수: 오버플로우 발생!
result = np.int64(2) ** 63  # -9223372036854775808 (음수가 됩니다!)
```

오버플로우가 발생하면:

- **금액 계산 오류**: 큰 금액의 연산에서 음수가 되어 결제 로직에 이상 발생
- **반복문 무한루프**: 카운터 변수의 오버플로우로 종료 조건을 만족하지 못하는 경우
- **메모리 할당 오류**: 할당할 크기가 0이나 음수가 되어 보안 문제 유발

### 취약한 코드

#### ❌ 취약한 코드: numpy 연산에서 범위 검증 없음

```python
import numpy as np

def handle_data(number, pow):
    # 64비트를 넘어서는 숫자와 지수가 입력될 경우
    # 오버플로우가 발생하여 결과값이 0이 됩니다
    res = np.power(number, pow, dtype=np.int64)
    return res
```

#### ❌ 취약한 코드: 외부 입력값으로 numpy 연산 수행

```python
import numpy as np
from django.shortcuts import render

def calculate_price(request):
    quantity = int(request.POST.get('quantity', '0'))
    unit_price = int(request.POST.get('unit_price', '0'))

    # numpy 배열 연산에서 오버플로우 발생 가능
    total = np.int64(quantity) * np.int64(unit_price)
    # 매우 큰 수를 입력하면 total이 음수가 될 수 있습니다

    return render(request, '/price.html', {'total': total})
```

### 안전한 코드

#### ✅ 안전한 코드: 파이썬 기본 자료형으로 사전 검증

```python
import numpy as np

MAX_NUMBER = np.iinfo(np.int64).max  # 9223372036854775807
MIN_NUMBER = np.iinfo(np.int64).min  # -9223372036854775808

def handle_data(number, pow):
    # 파이썬 기본 자료형으로 먼저 계산합니다 (오버플로우 없음)
    calculated = number ** pow

    # 결과가 numpy int64 범위 내인지 확인합니다
    if calculated > MAX_NUMBER or calculated < MIN_NUMBER:
        return -1  # 오버플로우 탐지 시 에러 반환

    res = np.power(number, pow, dtype=np.int64)
    return res
```

#### ✅ 안전한 코드: 입력값 범위 제한

```python
import numpy as np
from django.shortcuts import render

MAX_QUANTITY = 10000
MAX_PRICE = 100000000  # 1억

def calculate_price(request):
    try:
        quantity = int(request.POST.get('quantity', '0'))
        unit_price = int(request.POST.get('unit_price', '0'))
    except ValueError:
        return render(request, '/error.html', {'error': '올바른 숫자를 입력해주세요.'})

    # 입력값의 범위를 사전에 제한합니다
    if quantity < 0 or quantity > MAX_QUANTITY:
        return render(request, '/error.html', {'error': '수량 범위를 초과했습니다.'})

    if unit_price < 0 or unit_price > MAX_PRICE:
        return render(request, '/error.html', {'error': '가격 범위를 초과했습니다.'})

    # 안전한 범위 내에서 계산합니다
    total = quantity * unit_price  # 파이썬 기본 정수형 사용
    return render(request, '/price.html', {'total': total})
```

> **💡 팁:** 파이썬 기본 정수형(`int`)은 오버플로우가 발생하지 않으므로, 금액 계산 등 정확성이 중요한 연산은 `numpy` 대신 파이썬 기본 자료형을 사용하는 것이 안전합니다. `numpy`는 대량의 수치 데이터 처리에만 사용하고, 비즈니스 로직에서의 단일 값 계산에는 기본 자료형을 권장합니다.

### 바이브 코딩 시 체크포인트

- [ ] **`numpy`, `pandas` 등 C 기반 라이브러리에서 정수 연산을 수행할 때 입력값의 범위를 검증하고 있는가?**
- [ ] **금액, 수량 등 비즈니스 로직의 계산에 파이썬 기본 자료형을 사용하고 있는가?**
- [ ] **외부 입력값이 수치 연산에 사용될 때 최소/최대 범위가 설정되어 있는가?**

---

## 6-2. 보안기능 결정에 사용되는 부적절한 입력값

### 개요

보안기능 결정에 사용되는 부적절한 입력값(Reliance on Untrusted Inputs in a Security Decision)은 쿠키(Cookie), 히든 필드(Hidden Field), 환경변수 등 클라이언트 측에서 조작 가능한 값을 기반으로 인증이나 인가 같은 보안 결정을 내리는 취약점입니다.

바이브 코딩으로 회원 시스템, 관리자 페이지, 결제 기능 등을 구현할 때, AI가 생성한 코드에서 클라이언트 측 데이터를 신뢰하는 패턴이 자주 나타납니다. 여러분이 반드시 인지해야 할 중요한 원칙은 **클라이언트에서 오는 모든 데이터는 조작될 수 있다**는 것입니다.

### 왜 위험한가

> **💡 팁:** 인증과 인가의 올바른 구현 방법은 7장을 참고하십시오.

개발자들이 흔히 간과하는 사항이 있습니다:

- **쿠키**: 브라우저 개발자 도구(DevTools)나 프록시 도구(Burp Suite 등)로 언제든 수정 가능합니다
- **히든 필드**: HTML 소스를 보면 그대로 노출되며, 요청 시 값을 변경할 수 있습니다
- **URL 파라미터**: 주소창에서 직접 수정 가능합니다
- **HTTP 헤더**: 프록시 도구로 모든 헤더 값을 변조할 수 있습니다

다음과 같은 시나리오를 생각해보십시오:

```html
<!-- 쇼핑몰 결제 폼의 히든 필드 -->
<form action="/checkout" method="POST">
    <input type="hidden" name="price" value="50000" />
    <input type="hidden" name="user_role" value="customer" />
    <input type="submit" value="결제하기" />
</form>
```

공격자는 브라우저 개발자 도구로 `price` 값을 `1`로, `user_role`을 `admin`으로 변경한 후 폼을 전송할 수 있습니다.

### 취약한 코드

#### ❌ 취약한 코드: 쿠키로 관리자 여부 판단

```python
from django.shortcuts import render

def reset_password(request):
    # 쿠키에서 사용자 권한 등급을 가져옵니다
    # 쿠키는 클라이언트에서 언제든 조작할 수 있습니다!
    user_role = request.COOKIES.get('user_role', 'user')

    if user_role == 'admin':
        # 관리자 기능: 모든 사용자의 비밀번호를 초기화합니다
        target_user = request.POST.get('target_user', '')
        new_password = generate_temp_password()
        reset_user_password(target_user, new_password)
        send_reset_email(target_user, new_password)
        return render(request, '/admin/success.html')

    return render(request, '/error.html', {'error': '권한이 없습니다.'})
```

#### ❌ 취약한 코드: 히든 필드의 가격으로 결제 처리

```python
from django.shortcuts import render

def checkout(request):
    # 히든 필드에서 가격 정보를 받습니다
    # 클라이언트에서 가격을 1원으로 변조할 수 있습니다!
    price = int(request.POST.get('price', '0'))
    product_id = request.POST.get('product_id', '')

    # 클라이언트가 보낸 가격을 그대로 결제에 사용합니다
    process_payment(product_id, price)
    return render(request, '/checkout_success.html')
```

#### ❌ 취약한 코드: URL 파라미터로 사용자 식별

```python
from django.shortcuts import render

def view_profile(request):
    # URL에서 사용자 ID를 가져와 프로필을 표시합니다
    # /profile?user_id=123 → /profile?user_id=456으로 변경하면
    # 다른 사용자의 정보를 볼 수 있습니다
    user_id = request.GET.get('user_id')
    user_data = get_user_info(user_id)

    return render(request, '/profile.html', {'user': user_data})
```

> **⚠️ 주의:** AI 도구에 "관리자만 접근할 수 있는 페이지를 만들어줘"라고 요청하면, 쿠키나 히든 필드 기반의 간단한 권한 체크 코드가 생성될 수 있습니다. 이는 매우 취약한 구현입니다.

### 안전한 코드

#### ✅ 안전한 코드: 서버 세션(Session)으로 권한 관리

```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    """사용자가 관리자인지 서버 측 데이터로 확인합니다."""
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def reset_password(request):
    # Django의 인증 시스템이 서버 세션을 기반으로
    # 사용자 인증과 권한을 검증합니다
    target_user = request.POST.get('target_user', '')
    new_password = generate_temp_password()
    reset_user_password(target_user, new_password)
    send_reset_email(target_user, new_password)
    return render(request, '/admin/success.html')
```

#### ✅ 안전한 코드: 서버에서 가격 조회 후 결제

```python
from django.shortcuts import render
from app.models import Product

def checkout(request):
    product_id = request.POST.get('product_id', '')

    # 가격을 클라이언트에서 받지 않고, 서버 데이터베이스에서 조회합니다
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return render(request, '/error.html', {'error': '상품을 찾을 수 없습니다.'})

    # 서버에 저장된 실제 가격으로 결제를 처리합니다
    process_payment(product.id, product.price)
    return render(request, '/checkout_success.html')
```

#### ✅ 안전한 코드: 인증된 사용자 정보로 프로필 접근

```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def view_profile(request):
    # URL 파라미터가 아닌, 서버 세션의 인증된 사용자 정보를 사용합니다
    user_data = get_user_info(request.user.id)
    return render(request, '/profile.html', {'user': user_data})


@login_required
def view_other_profile(request, user_id):
    # 다른 사용자의 프로필을 보려면 권한 확인이 필요합니다
    if not request.user.is_staff and request.user.id != user_id:
        return render(request, '/error.html', {'error': '권한이 없습니다.'})

    user_data = get_user_info(user_id)
    return render(request, '/profile.html', {'user': user_data})
```

> **💡 팁:** 보안 결정에 사용되는 데이터(사용자 권한, 가격, 수량 등)는 반드시 **서버 측에서 관리하고 검증**해야 합니다. 클라이언트에서 전달되는 값은 참고용으로만 사용하고, 실제 로직 실행 전에 서버의 데이터베이스나 세션에서 확인하십시오.

### Django 인증 시스템 활용

Django 프레임워크는 안전한 인증과 권한 관리를 위한 기능을 기본으로 제공합니다:

```python
# settings.py - 세션 보안 설정
SESSION_COOKIE_HTTPONLY = True    # JavaScript에서 쿠키 접근 차단
SESSION_COOKIE_SECURE = True     # HTTPS에서만 쿠키 전송
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # 브라우저 종료 시 세션 만료
CSRF_COOKIE_HTTPONLY = True      # CSRF 토큰 쿠키도 보호

# DRF(Django REST Framework) 사용 시
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

### 바이브 코딩 시 체크포인트

- [ ] **쿠키, 히든 필드, URL 파라미터 값을 보안 결정(인증, 인가, 결제)에 사용하고 있지 않은가?**
- [ ] **사용자 권한 확인은 서버 세션 또는 데이터베이스를 기반으로 수행하고 있는가?**
- [ ] **가격, 할인율 등 금전적 가치가 있는 데이터를 서버에서 조회하고 있는가?**
- [ ] **Django의 `@login_required`, `@user_passes_test`, `@permission_required` 등 내장 데코레이터를 활용하고 있는가?**
- [ ] **세션 쿠키에 `HttpOnly`, `Secure`, `SameSite` 속성이 설정되어 있는가?**
- [ ] **AI가 생성한 관리자 기능 코드에서 서버 측 권한 검증이 이루어지고 있는가?**

> **⚠️ 주의:** "클라이언트에서 보내는 데이터는 모두 거짓말일 수 있다"라는 원칙을 항상 기억하십시오. AI 도구에 관리자 기능을 요청할 때는 "Django 인증 시스템을 사용해서 서버 측에서 권한을 확인해줘"라고 명시하면 보다 안전한 코드가 생성됩니다.

---

## 6-3. 메모리 버퍼 오버플로우(Buffer Overflow)

### 개요

메모리 버퍼 오버플로우(Buffer Overflow)는 프로그램이 할당된 메모리 영역을 넘어서 데이터를 쓰는 취약점입니다. C/C++ 같은 저수준 언어에서 주로 발생합니다.

> **💡 팁:** Python은 자체적으로 메모리를 관리하므로 전통적인 버퍼 오버플로우가 발생하지 않습니다. 하지만 C 확장 모듈(예: numpy, PIL의 내부)이나 ctypes를 사용할 때는 주의가 필요합니다.

### 바이브 코딩 시 체크포인트

- [ ] C 확장 모듈을 직접 작성하지 않았는가?
- [ ] ctypes나 cffi로 외부 라이브러리를 호출할 때 입력 크기를 검증하는가?
- [ ] 사용하는 라이브러리(numpy, Pillow 등)를 최신 버전으로 유지하는가?

> **⚠️ 주의:** 바이브 코딩에서 이 취약점을 직접 마주칠 일은 거의 없지만, 의존 라이브러리의 보안 업데이트는 반드시 적용하십시오. `pip audit` 명령어로 취약한 패키지를 확인할 수 있습니다.
