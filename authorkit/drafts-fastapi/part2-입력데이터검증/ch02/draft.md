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

예를 들어, 로그인 폼에서 비밀번호 입력란에 `' OR '1'='1` 이라고 입력하면, 원래 의도된 쿼리가 완전히 다른 의미로 변환됩니다:

```sql
-- 원래 의도된 쿼리
SELECT * FROM users WHERE username='admin' AND password='입력값'

-- 공격자의 입력으로 변조된 쿼리
SELECT * FROM users WHERE username='admin' AND password='' OR '1'='1'
```

조건절 `'1'='1'`은 항상 참이므로 비밀번호 없이 로그인에 성공하게 됩니다.

### 취약한 코드

#### ❌ 취약한 코드: SQLAlchemy에서 text()와 문자열 결합 사용

```python
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/update-board")
async def update_board(
    request: Request,
    name: str = Form(...),
    content_id: str = Form(...),
    db: AsyncSession = Depends(get_async_session),
):
    # 문자열 결합으로 쿼리를 생성하면 SQL 삽입에 취약합니다
    sql_query = "UPDATE board SET name='" + name + "' WHERE content_id='" + content_id + "'"
    await db.execute(text(sql_query))
    await db.commit()

    return templates.TemplateResponse("success.html", {"request": request})
```

이 코드에서 `content_id` 값으로 `a' OR 'a'='a`를 입력하면, 조건절이 `content_id='a' OR 'a'='a'`로 바뀌어 board 테이블의 **모든 레코드**가 변경됩니다.

> **⚠️ 주의:** AI 도구에 "게시판 수정 기능 만들어줘"라고 요청하면, 간혹 위와 같은 문자열 결합 방식의 코드가 생성될 수 있습니다. 특히 "간단한 예제"를 요청하면 보안이 생략되는 경우가 많습니다.

#### ❌ 취약한 코드: SQLAlchemy에서 raw SQL 오용

```python
from fastapi import FastAPI, Form, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/member-search")
async def member_search(
    request: Request,
    name: str = Form(...),
    db: AsyncSession = Depends(get_async_session),
):
    # text()에 문자열 결합으로 쿼리를 전달하면 취약합니다
    query = "SELECT * FROM member WHERE name='" + name + "'"
    result = await db.execute(text(query))
    member_list = result.fetchall()

    return templates.TemplateResponse(
        "member_list.html", {"request": request, "member_list": member_list}
    )
```

SQLAlchemy의 ORM(Object-Relational Mapping)을 사용하면서도 `text()`에 문자열 결합을 하면 ORM의 보호 기능이 완전히 무력화됩니다.

### 안전한 코드

#### ✅ 안전한 코드: 바인드 파라미터(Bind Parameter) 사용

```python
from fastapi import FastAPI, Form, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/update-board")
async def update_board(
    request: Request,
    name: str = Form(...),
    content_id: str = Form(...),
    db: AsyncSession = Depends(get_async_session),
):
    # 바인드 파라미터(:name, :content_id)를 사용합니다
    sql_query = text("UPDATE board SET name=:name WHERE content_id=:content_id")
    # bindparams로 값을 안전하게 바인딩합니다
    await db.execute(sql_query, {"name": name, "content_id": content_id})
    await db.commit()

    return templates.TemplateResponse("success.html", {"request": request})
```

바인드 파라미터(Bind Parameter)를 사용하면 사용자 입력값이 SQL 구문이 아닌 **순수한 데이터**로만 처리됩니다. 공격자가 어떤 값을 넣더라도 쿼리 구조 자체는 변경할 수 없습니다.

#### ✅ 안전한 코드: SQLAlchemy text()의 올바른 사용

```python
from fastapi import FastAPI, Form, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/member-search")
async def member_search(
    request: Request,
    name: str = Form(...),
    db: AsyncSession = Depends(get_async_session),
):
    # 바인드 파라미터와 딕셔너리를 사용합니다
    query = text("SELECT * FROM member WHERE name=:name")
    result = await db.execute(query, {"name": name})
    member_list = result.fetchall()

    return templates.TemplateResponse(
        "member_list.html", {"request": request, "member_list": member_list}
    )
```

#### ✅ 가장 안전한 코드: SQLAlchemy ORM + Pydantic 모델 활용

```python
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Pydantic 모델로 입력값을 사전 검증합니다
class MemberSearchRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

@app.post("/member-search")
async def member_search(
    request: Request,
    search: MemberSearchRequest,
    db: AsyncSession = Depends(get_async_session),
):
    # SQLAlchemy ORM의 select()는 자동으로 바인드 파라미터를 생성합니다
    stmt = select(Member).where(Member.name == search.name)
    result = await db.execute(stmt)
    member_list = result.scalars().all()

    return templates.TemplateResponse(
        "member_list.html", {"request": request, "member_list": member_list}
    )
```

> **💡 팁:** SQLAlchemy ORM의 `select()`, `where()`, `filter()` 등의 메서드를 사용하면 프레임워크(Framework)가 자동으로 SQL 삽입을 방지합니다. 여기에 Pydantic 모델을 결합하면 입력값의 타입과 길이까지 사전 검증할 수 있어 가장 안전합니다.

#### ✅ 안전한 코드: SQLite에서의 바인드 파라미터

```python
import sqlite3

def get_user(username):
    conn = sqlite3.connect('mydb.sqlite3')
    cursor = conn.cursor()

    # ? 플레이스홀더 사용 (SQLite 방식)
    cursor.execute('SELECT * FROM users WHERE username=?', (username,))
    result = cursor.fetchone()

    conn.close()
    return result
```

SQLite에서는 `?`를 플레이스홀더(Placeholder)로 사용하거나, `:name` 형식의 Named Placeholder를 사용할 수 있습니다.

### 바이브 코딩 시 체크포인트

AI 도구로 데이터베이스 관련 코드를 생성할 때 다음 항목을 반드시 확인하십시오:

- [ ] **문자열 결합으로 SQL 쿼리를 만들고 있지 않은가?** `+` 연산자나 f-string으로 쿼리를 조합하는 코드는 모두 위험합니다
- [ ] **ORM의 기본 기능을 사용하고 있는가?** SQLAlchemy의 `select()`, `where()`, `filter()` 등 ORM 기본 메서드가 가장 안전합니다
- [ ] **raw SQL이 꼭 필요한가?** 복잡한 쿼리라도 대부분 ORM으로 표현할 수 있습니다. `text()` 사용은 최소화하십시오
- [ ] **바인드 파라미터를 사용하고 있는가?** raw SQL이 불가피한 경우 반드시 `:name` 등의 바인드 파라미터와 딕셔너리 바인딩을 사용하십시오
- [ ] **Pydantic 모델로 입력값을 검증하고 있는가?** FastAPI의 Pydantic 통합은 타입, 길이, 패턴 등 다양한 검증을 자동으로 수행합니다
- [ ] **AI에게 보안 요구사항을 명시했는가?** 프롬프트에 "SQL 인젝션 방지를 위해 파라미터 바인딩을 사용해줘"라고 명시하면 훨씬 안전한 코드가 생성됩니다

> **💡 팁:** AI 도구에 코드를 요청할 때 "SQLAlchemy ORM을 사용해서 안전하게 만들어줘"라고 추가하면, 대부분 ORM 기반의 안전한 코드를 생성합니다. "raw SQL 없이"라는 조건을 붙이는 것도 좋은 방법입니다.

---

## 2-2. LDAP 삽입(LDAP Injection)

> **기타 삽입 공격 — LDAP 삽입**
>
> **우선순위: 낮음** — 대부분의 바이브 코딩 프로젝트에서는 LDAP를 직접 다루는 경우가 드뭅니다. 하지만 기업용 사내 시스템이나 Active Directory 연동 기능을 구현할 때는 주의가 필요합니다.
>
> **LDAP(Lightweight Directory Access Protocol)**은 조직 내 사용자 정보를 관리하는 디렉터리 서비스 프로토콜입니다. SQL 삽입과 동일한 원리로, 사용자 입력값이 LDAP 쿼리문에 검증 없이 포함되면 공격자가 쿼리 구조를 변경하여 권한 상승이나 정보 유출을 시도할 수 있습니다.
>
> **핵심 방어 방법:**
> - `ldap3` 라이브러리 사용 시 `escape_filter_chars()` 함수로 입력값을 이스케이프(Escape) 처리합니다
> - 화이트리스트(Whitelist) 방식으로 검색 가능한 값을 제한합니다
>
> ```python
> # ❌ 취약한 코드
> search_str = '(&(objectclass=%s))' % search_keyword
>
> # ✅ 안전한 코드
> from ldap3.utils.conv import escape_filter_chars
> escaped = escape_filter_chars(search_keyword)
> search_str = '(&(objectclass=%s))' % escaped
> ```
>
> AI 도구가 LDAP 관련 코드를 생성할 때는 반드시 입력값 이스케이프 처리가 포함되어 있는지 확인하십시오.
