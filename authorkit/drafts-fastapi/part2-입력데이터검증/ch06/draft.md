# Chapter 06. 데이터 타입과 보안 결정을 노리는 공격

## 6-1. 정수형 오버플로우(Integer Overflow)

### 개요

정수형 오버플로우(Integer Overflow)는 변수가 저장할 수 있는 범위를 넘어선 값이 할당될 때, 실제 저장되는 값이 의도치 않게 아주 작은 수나 음수가 되어 프로그램이 예기치 않게 동작하는 취약점입니다.

파이썬(Python)은 다른 언어와 달리 기본 정수형에 대해 **임의 정밀도 연산(Arbitrary-Precision Arithmetic)**을 지원하므로, 순수 파이썬 코드에서는 정수형 오버플로우가 발생하지 않습니다. 하지만 `numpy`, `pandas` 등 C 기반 라이브러리를 사용할 때는 고정 크기 정수형이 사용되므로 오버플로우가 발생할 수 있습니다.

### 왜 위험한가

바이브 코딩(Vibe Coding)으로 데이터 분석이나 과학 계산 기능을 구현할 때 `numpy` 등의 라이브러리를 많이 사용합니다. 이 라이브러리들은 성능을 위해 C 언어와 동일한 방식으로 정수를 처리하므로 오버플로우에 주의해야 합니다:

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
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/calculate-price")
async def calculate_price(
    request: Request,
    quantity: int = Form(...),
    unit_price: int = Form(...),
):
    # numpy 배열 연산에서 오버플로우 발생 가능
    total = np.int64(quantity) * np.int64(unit_price)
    # 매우 큰 수를 입력하면 total이 음수가 될 수 있습니다

    return templates.TemplateResponse(
        "price.html", {"request": request, "total": int(total)}
    )
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

#### ✅ 안전한 코드: Pydantic 모델로 입력값 범위 제한

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

app = FastAPI()
templates = Jinja2Templates(directory="templates")

MAX_QUANTITY = 10000
MAX_PRICE = 100_000_000  # 1억

class PriceRequest(BaseModel):
    # Pydantic의 Field로 최소/최대 범위를 선언적으로 지정합니다
    quantity: int = Field(..., ge=0, le=MAX_QUANTITY)
    unit_price: int = Field(..., ge=0, le=MAX_PRICE)

@app.post("/calculate-price")
async def calculate_price(request: Request, body: PriceRequest):
    # Pydantic이 이미 범위를 검증했으므로 안전한 범위 내에서 계산합니다
    total = body.quantity * body.unit_price  # 파이썬 기본 정수형 사용

    return templates.TemplateResponse(
        "price.html", {"request": request, "total": total}
    )
```

#### ✅ 안전한 코드: Form 데이터에서 입력값 범위 제한

```python
from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

MAX_QUANTITY = 10000
MAX_PRICE = 100_000_000  # 1억

@app.post("/calculate-price")
async def calculate_price(
    request: Request,
    quantity: int = Form(...),
    unit_price: int = Form(...),
):
    # 입력값의 범위를 사전에 제한합니다
    if quantity < 0 or quantity > MAX_QUANTITY:
        raise HTTPException(status_code=400, detail="수량 범위를 초과했습니다.")

    if unit_price < 0 or unit_price > MAX_PRICE:
        raise HTTPException(status_code=400, detail="가격 범위를 초과했습니다.")

    # 안전한 범위 내에서 계산합니다
    total = quantity * unit_price  # 파이썬 기본 정수형 사용

    return templates.TemplateResponse(
        "price.html", {"request": request, "total": total}
    )
```

> **💡 팁:** 파이썬 기본 정수형(`int`)은 오버플로우가 발생하지 않으므로, 금액 계산 등 정확성이 중요한 연산은 `numpy` 대신 파이썬 기본 자료형을 사용하는 것이 안전합니다. `numpy`는 대량의 수치 데이터 처리에만 사용하고, 비즈니스 로직에서의 단일 값 계산에는 기본 자료형을 권장합니다. FastAPI에서는 Pydantic의 `Field(ge=0, le=10000)`처럼 선언적으로 범위를 지정하면 자동 검증이 수행되어 매우 편리합니다.

### 바이브 코딩 시 체크포인트

- [ ] **`numpy`, `pandas` 등 C 기반 라이브러리에서 정수 연산을 수행할 때 입력값의 범위를 검증하고 있는가?**
- [ ] **금액, 수량 등 비즈니스 로직의 계산에 파이썬 기본 자료형을 사용하고 있는가?**
- [ ] **외부 입력값이 수치 연산에 사용될 때 Pydantic `Field`의 `ge`, `le`, `gt`, `lt` 옵션으로 최소/최대 범위가 설정되어 있는가?**

---

## 6-2. 보안기능 결정에 사용되는 부적절한 입력값

### 개요

보안기능 결정에 사용되는 부적절한 입력값(Reliance on Untrusted Inputs in a Security Decision)은 쿠키(Cookie), 히든 필드(Hidden Field), 환경변수 등 클라이언트 측에서 조작 가능한 값을 기반으로 인증이나 인가 같은 보안 결정을 내리는 취약점입니다.

바이브 코딩으로 회원 시스템, 관리자 페이지, 결제 기능 등을 구현할 때, AI가 생성한 코드에서 클라이언트 측 데이터를 신뢰하는 패턴이 자주 나타납니다. 여러분이 반드시 인지해야 할 중요한 원칙은 **클라이언트에서 오는 모든 데이터는 조작될 수 있다**는 것입니다.

### 왜 위험한가

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
from fastapi import FastAPI, Form, Request, Cookie
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/reset-password")
async def reset_password(
    request: Request,
    target_user: str = Form(...),
    # 쿠키에서 사용자 권한 등급을 가져옵니다
    # 쿠키는 클라이언트에서 언제든 조작할 수 있습니다!
    user_role: str = Cookie(default="user"),
):
    if user_role == 'admin':
        # 관리자 기능: 모든 사용자의 비밀번호를 초기화합니다
        new_password = generate_temp_password()
        reset_user_password(target_user, new_password)
        send_reset_email(target_user, new_password)
        return templates.TemplateResponse(
            "admin/success.html", {"request": request}
        )

    raise HTTPException(status_code=403, detail="권한이 없습니다.")
```

#### ❌ 취약한 코드: 히든 필드의 가격으로 결제 처리

```python
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/checkout")
async def checkout(
    request: Request,
    # 히든 필드에서 가격 정보를 받습니다
    # 클라이언트에서 가격을 1원으로 변조할 수 있습니다!
    price: int = Form(...),
    product_id: str = Form(...),
):
    # 클라이언트가 보낸 가격을 그대로 결제에 사용합니다
    process_payment(product_id, price)
    return templates.TemplateResponse(
        "checkout_success.html", {"request": request}
    )
```

#### ❌ 취약한 코드: URL 파라미터로 사용자 식별

```python
from fastapi import FastAPI, Query, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/profile")
async def view_profile(request: Request, user_id: int = Query(...)):
    # URL에서 사용자 ID를 가져와 프로필을 표시합니다
    # /profile?user_id=123 → /profile?user_id=456으로 변경하면
    # 다른 사용자의 정보를 볼 수 있습니다
    user_data = get_user_info(user_id)
    return templates.TemplateResponse(
        "profile.html", {"request": request, "user": user_data}
    )
```

> **⚠️ 주의:** AI 도구에 "관리자만 접근할 수 있는 페이지를 만들어줘"라고 요청하면, 쿠키나 히든 필드 기반의 간단한 권한 체크 코드가 생성될 수 있습니다. 이는 매우 취약한 구현입니다.

### 안전한 코드

#### ✅ 안전한 코드: 서버 세션 기반 JWT 토큰으로 권한 관리

```python
from fastapi import FastAPI, Form, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

app = FastAPI()
templates = Jinja2Templates(directory="templates")
security = HTTPBearer()

SECRET_KEY = "환경변수에서-불러와야-합니다"

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """JWT 토큰을 검증하여 현재 사용자를 확인합니다."""
    try:
        payload = jwt.decode(
            credentials.credentials, SECRET_KEY, algorithms=["HS256"]
        )
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="인증에 실패했습니다.")

async def require_admin(user: dict = Depends(get_current_user)):
    """사용자가 관리자인지 서버 측 데이터로 확인합니다."""
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="관리자 권한이 필요합니다.")
    return user

@app.post("/reset-password")
async def reset_password(
    request: Request,
    target_user: str = Form(...),
    admin: dict = Depends(require_admin),
):
    # JWT 토큰의 서버 측 검증이 완료된 관리자만 접근 가능합니다
    new_password = generate_temp_password()
    reset_user_password(target_user, new_password)
    send_reset_email(target_user, new_password)
    return templates.TemplateResponse(
        "admin/success.html", {"request": request}
    )
```

#### ✅ 안전한 코드: 서버에서 가격 조회 후 결제

```python
from fastapi import FastAPI, Form, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/checkout")
async def checkout(
    request: Request,
    product_id: str = Form(...),
    db: AsyncSession = Depends(get_async_session),
):
    # 가격을 클라이언트에서 받지 않고, 서버 데이터베이스에서 조회합니다
    stmt = select(Product).where(Product.id == product_id)
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")

    # 서버에 저장된 실제 가격으로 결제를 처리합니다
    process_payment(product.id, product.price)
    return templates.TemplateResponse(
        "checkout_success.html", {"request": request}
    )
```

#### ✅ 안전한 코드: 인증된 사용자 정보로 프로필 접근

```python
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/profile")
async def view_profile(
    request: Request,
    current_user: dict = Depends(get_current_user),
):
    # URL 파라미터가 아닌, 서버 측 JWT 토큰의 인증된 사용자 정보를 사용합니다
    user_data = get_user_info(current_user["user_id"])
    return templates.TemplateResponse(
        "profile.html", {"request": request, "user": user_data}
    )

@app.get("/profile/{user_id}")
async def view_other_profile(
    request: Request,
    user_id: int,
    current_user: dict = Depends(get_current_user),
):
    # 다른 사용자의 프로필을 보려면 권한 확인이 필요합니다
    if current_user.get("role") != "admin" and current_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")

    user_data = get_user_info(user_id)
    return templates.TemplateResponse(
        "profile.html", {"request": request, "user": user_data}
    )
```

> **💡 팁:** 보안 결정에 사용되는 데이터(사용자 권한, 가격, 수량 등)는 반드시 **서버 측에서 관리하고 검증**해야 합니다. 클라이언트에서 전달되는 값은 참고용으로만 사용하고, 실제 로직 실행 전에 서버의 데이터베이스나 JWT 토큰에서 확인하십시오.

### FastAPI 인증/인가 시스템 활용

FastAPI 프레임워크는 안전한 인증과 권한 관리를 위한 다양한 도구를 제공합니다:

```python
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

# 세션 미들웨어 설정
app.add_middleware(
    SessionMiddleware,
    secret_key="환경변수에서-불러와야-합니다",
    https_only=True,        # HTTPS에서만 쿠키 전송
    same_site="lax",        # SameSite 속성 설정
    max_age=3600,           # 세션 만료 시간 (초)
)

# OAuth2 기반 인증 (JWT 토큰)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# 의존성 주입(Dependency Injection)으로 인증 체계 구성
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """모든 요청에서 자동으로 토큰을 검증합니다."""
    user = verify_token(token)
    if user is None:
        raise HTTPException(status_code=401, detail="인증에 실패했습니다.")
    return user

async def require_role(required_role: str):
    """특정 역할이 필요한 엔드포인트에서 사용합니다."""
    async def role_checker(user: dict = Depends(get_current_user)):
        if user.get("role") != required_role:
            raise HTTPException(status_code=403, detail=f"{required_role} 권한이 필요합니다.")
        return user
    return role_checker
```

### 바이브 코딩 시 체크포인트

- [ ] **쿠키, 히든 필드, URL 파라미터 값을 보안 결정(인증, 인가, 결제)에 사용하고 있지 않은가?**
- [ ] **사용자 권한 확인은 서버 측 JWT 토큰 검증 또는 데이터베이스 조회를 기반으로 수행하고 있는가?**
- [ ] **가격, 할인율 등 금전적 가치가 있는 데이터를 서버에서 조회하고 있는가?**
- [ ] **FastAPI의 `Depends()`를 활용하여 인증/인가 의존성을 체계적으로 관리하고 있는가?**
- [ ] **세션 쿠키에 `https_only`, `same_site` 속성이 설정되어 있는가?**
- [ ] **AI가 생성한 관리자 기능 코드에서 서버 측 권한 검증이 이루어지고 있는가?**

> **⚠️ 주의:** "클라이언트에서 보내는 데이터는 모두 거짓말일 수 있다"라는 원칙을 항상 기억하십시오. AI 도구에 관리자 기능을 요청할 때는 "FastAPI의 Depends()와 JWT 인증을 사용해서 서버 측에서 권한을 확인해줘"라고 명시하면 보다 안전한 코드가 생성됩니다.
