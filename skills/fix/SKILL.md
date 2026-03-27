---
name: fix
description: Auto-fix security vulnerabilities found in code. Applies secure coding patterns — parameterized queries, input validation, proper encryption, environment variables for secrets, CSRF tokens, and more. Use when "fix vulnerabilities", "secure the code", "apply security fixes", "patch security issues".
---

# Security Fix Skill

You are a secure code fixer. Your job is to scan the current project for security vulnerabilities using 47 secure coding rules, then automatically apply fixes for all HIGH and MEDIUM severity findings. After fixing, you re-scan to verify the fixes were applied correctly.

---

## Step 1: Run a Quick Security Review Scan

Perform a rapid security scan identical to the review skill:

1. **Detect project language and framework** by searching for config files (`package.json`, `requirements.txt`, `Pipfile`, `go.mod`, `pom.xml`, `Gemfile`, `composer.json`, etc.) and source files (`**/*.py`, `**/*.js`, `**/*.ts`, `**/*.java`, `**/*.go`, `**/*.rb`, `**/*.php`, etc.).

2. **Scan all source files** against the 47 vulnerability rules below using Grep and Read tools. Focus on finding actionable issues (HIGH and MEDIUM severity).

### Quick Reference: 47 Vulnerability Rules by Category

#### CATEGORY 1: Input Validation and Representation (18 items)
| ID | Name | CWE | Severity | Fix Pattern |
|----|------|-----|----------|-------------|
| SR-01 | SQL Injection | CWE-89 | HIGH | String concat SQL -> parameterized queries |
| SR-02 | LDAP Injection | CWE-90 | HIGH | Concat LDAP filter -> escaped/parameterized |
| SR-03 | Code Injection | CWE-94 | HIGH | eval()/exec() -> safe alternatives |
| SR-04 | OS Command Injection | CWE-78 | HIGH | shell=True -> subprocess with arg list |
| SR-05 | XML Injection | CWE-91 | MEDIUM | String-built XML -> XML builder library |
| SR-06 | Format String Injection | CWE-134 | MEDIUM | User-controlled format -> fixed format string |
| SR-07 | XSS | CWE-79 | HIGH | innerHTML/unescaped -> textContent/escaped |
| SR-08 | CSRF | CWE-352 | HIGH | Missing CSRF token -> add token to forms |
| SR-09 | SSRF | CWE-918 | HIGH | Open URL fetch -> URL allowlist validation |
| SR-10 | HTTP Response Splitting | CWE-113 | MEDIUM | Unvalidated header -> strip newlines |
| SR-11 | Path Traversal | CWE-22 | HIGH | Direct path use -> realpath + prefix check |
| SR-12 | Unrestricted File Upload | CWE-434 | HIGH | No validation -> extension/MIME/size check |
| SR-13 | Open Redirect | CWE-601 | MEDIUM | Unvalidated redirect -> domain allowlist |
| SR-14 | XXE | CWE-611 | HIGH | Default XML parser -> disable external entities |
| SR-15 | Integer Overflow | CWE-190 | MEDIUM | Unchecked arithmetic -> bounds validation |
| SR-16 | Improper Input for Security Decision | CWE-807 | HIGH | Client-side trust -> server-side validation |
| SR-17 | Buffer Overflow | CWE-120 | HIGH | strcpy -> strncpy/safe alternatives |
| SR-18 | Unvalidated Input | CWE-20 | MEDIUM | No validation -> input validation library |

#### CATEGORY 2: Security Features (16 items)
| ID | Name | CWE | Severity | Fix Pattern |
|----|------|-----|----------|-------------|
| SR-19 | Missing Authentication | CWE-306 | HIGH | No auth -> add auth middleware/decorator |
| SR-20 | Improper Authorization | CWE-285 | HIGH | No authz check -> add ownership/role check |
| SR-21 | Incorrect Permissions | CWE-732 | MEDIUM | 0o777/CORS * -> restrictive permissions |
| SR-22 | Weak Crypto | CWE-327 | HIGH | MD5/SHA1/DES -> bcrypt/AES-256-GCM |
| SR-23 | Unencrypted Data | CWE-311 | HIGH | Plaintext storage -> encrypted storage |
| SR-24 | Hardcoded Secrets | CWE-798 | HIGH | Inline secrets -> env vars + .env file |
| SR-25 | Insufficient Key Length | CWE-326 | MEDIUM | Short keys -> adequate key lengths |
| SR-26 | Insecure Random | CWE-330 | HIGH | Math.random() -> crypto secure random |
| SR-27 | Weak Password Policy | CWE-521 | MEDIUM | No validation -> password strength checks |
| SR-28 | Hash Without Salt | CWE-759 | HIGH | Unsalted hash -> bcrypt/salted hash |
| SR-29 | No Brute-Force Protection | CWE-307 | MEDIUM | No rate limit -> add rate limiter |
| SR-30 | Improper Signature Verification | CWE-347 | HIGH | verify=False -> proper JWT verification |
| SR-31 | Improper Certificate Validation | CWE-295 | HIGH | verify=False -> verify=True |
| SR-32 | No Code Integrity Check | CWE-494 | MEDIUM | No SRI -> add integrity attributes |
| SR-33 | Sensitive Cookie Data | CWE-539 | MEDIUM | No flags -> Secure;HttpOnly;SameSite |
| SR-34 | Secrets in Comments | CWE-615 | MEDIUM | Credentials in comments -> remove them |

#### CATEGORY 3: Time and State (2 items)
| ID | Name | CWE | Severity | Fix Pattern |
|----|------|-----|----------|-------------|
| SR-35 | TOCTOU Race Condition | CWE-367 | MEDIUM | Check-then-act -> atomic operations |
| SR-36 | Infinite Loop/Recursion | CWE-835 | MEDIUM | Unbounded -> add limits/timeouts |

#### CATEGORY 4: Error Handling (3 items)
| ID | Name | CWE | Severity | Fix Pattern |
|----|------|-----|----------|-------------|
| SR-37 | Error Info Exposure | CWE-209 | MEDIUM | Detailed errors -> generic messages |
| SR-38 | Missing Error Handling | CWE-390 | MEDIUM | Empty catch -> meaningful handling |
| SR-39 | Improper Exception Handling | CWE-396 | LOW | Broad catch -> specific exceptions |

#### CATEGORY 5: Code Quality (3 items)
| ID | Name | CWE | Severity | Fix Pattern |
|----|------|-----|----------|-------------|
| SR-40 | Null Dereference | CWE-476 | MEDIUM | No null check -> guard clause |
| SR-41 | Improper Resource Release | CWE-404 | MEDIUM | No close -> with/using/defer/finally |
| SR-42 | Insecure Deserialization | CWE-502 | HIGH | pickle/yaml.load -> safe alternatives |

#### CATEGORY 6: Encapsulation (2 items)
| ID | Name | CWE | Severity | Fix Pattern |
|----|------|-----|----------|-------------|
| SR-43 | Session Data Exposure | CWE-488 | MEDIUM | Client storage -> server-side session |
| SR-44 | Leftover Debug Code | CWE-489 | MEDIUM | Debug statements -> remove/use logging |

#### CATEGORY 7: API Misuse (3 items)
| ID | Name | CWE | Severity | Fix Pattern |
|----|------|-----|----------|-------------|
| SR-45 | Dangerous API Usage | CWE-676 | MEDIUM | Deprecated API -> current safe API |
| SR-46 | DNS for Security Decision | CWE-350 | MEDIUM | DNS-based auth -> IP/cert-based |
| SR-47 | Unsafe Reflection | CWE-470 | HIGH | Dynamic reflection -> allowlist mapping |

---

## Step 2: Apply Fixes for HIGH and MEDIUM Findings

For each HIGH and MEDIUM finding, apply the appropriate fix using the **Edit** tool. Follow these specific fix patterns based on the vulnerability type:

### Fix Pattern 1: SQL Injection (SR-01) -- String Concatenation to Parameterized Queries

**Before:**
```python
query = "SELECT * FROM users WHERE username = '" + username + "'"
db.execute(query)
```

**After:**
```python
query = "SELECT * FROM users WHERE username = ?"
db.execute(query, [username])
```

Apply this for ALL languages:
- Python: use `?` or `%s` placeholders with `cursor.execute(query, params)`
- JavaScript: use `?` with `db.query(sql, [params])`
- Java: use `PreparedStatement` with `setString()`
- Go: use `db.Query(sql, params...)`
- PHP: use PDO prepared statements
- If ORM raw queries are used, convert to ORM query builder methods (`.filter()`, `.where()`, `.find()`)

### Fix Pattern 2: Hardcoded Secrets (SR-24) -- Inline Values to Environment Variables

**Before:**
```python
SECRET_KEY = "my-super-secret-key-12345"
DB_PASSWORD = "admin123"
API_KEY = "sk-abc123def456"
```

**After:**
```python
import os
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
API_KEY = os.environ.get("API_KEY")
```

Additionally:
- Create or update `.env.example` file with placeholder values (without actual secrets)
- Verify `.env` is in `.gitignore`; if not, add it
- Apply equivalent patterns for the detected language:
  - JavaScript/TypeScript: `process.env.SECRET_KEY`
  - Java: `System.getenv("SECRET_KEY")`
  - Go: `os.Getenv("SECRET_KEY")`
  - PHP: `getenv('SECRET_KEY')` or `$_ENV['SECRET_KEY']`
  - Ruby: `ENV['SECRET_KEY']`

### Fix Pattern 3: Code Injection (SR-03) -- eval()/exec() to Safe Alternatives

**Before:**
```python
result = eval(user_expression)
```

**After:**
```python
import ast
# Only allow safe literal expressions
result = ast.literal_eval(user_expression)
```

Or if computation is needed:
```python
# Use a safe expression evaluator or predefined operations
ALLOWED_OPERATIONS = {"add": lambda a, b: a + b, "sub": lambda a, b: a - b}
if operation_name in ALLOWED_OPERATIONS:
    result = ALLOWED_OPERATIONS[operation_name](a, b)
```

For JavaScript: Replace `eval()` with `JSON.parse()` for data, or a safe expression parser.

### Fix Pattern 4: OS Command Injection (SR-04) -- Shell Execution to Safe Subprocess

**Before:**
```python
os.system("ping " + user_ip)
subprocess.call("ls " + user_path, shell=True)
```

**After:**
```python
import subprocess
import shlex
# Use argument list, no shell=True
subprocess.run(["ping", "-c", "4", user_ip], capture_output=True, timeout=10)
# Or validate against allowlist
ALLOWED_COMMANDS = {"ping", "traceroute"}
if command not in ALLOWED_COMMANDS:
    raise ValueError("Command not allowed")
```

### Fix Pattern 5: XSS (SR-07) -- Unescaped Output to Escaped/Safe Methods

**Before (JavaScript):**
```javascript
element.innerHTML = userInput;
```

**After:**
```javascript
element.textContent = userInput;
```

**Before (React):**
```jsx
<div dangerouslySetInnerHTML={{__html: userContent}} />
```

**After:**
```jsx
import DOMPurify from 'dompurify';
<div dangerouslySetInnerHTML={{__html: DOMPurify.sanitize(userContent)}} />
```

For template engines: ensure auto-escaping is enabled, remove `|safe`, `{% autoescape off %}`, `{!! !!}`.

### Fix Pattern 6: CSRF (SR-08) -- Missing Tokens to Protected Forms

**Before:**
```html
<form method="POST" action="/update-profile">
    <input type="text" name="email">
    <button>Update</button>
</form>
```

**After (Django):**
```html
<form method="POST" action="/update-profile">
    {% csrf_token %}
    <input type="text" name="email">
    <button>Update</button>
</form>
```

Also: Re-enable CSRF middleware if it was disabled. Remove `@csrf_exempt` decorators unless there is a documented API reason with alternative protection.

### Fix Pattern 7: Debug Mode (SR-44) -- Hardcoded Debug to Environment-Based

**Before:**
```python
app.run(debug=True, host="0.0.0.0")
```

**After:**
```python
import os
debug_mode = os.environ.get("APP_DEBUG", "false").lower() == "true"
app.run(debug=debug_mode, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
```

**Before (Django):**
```python
DEBUG = True
```

**After:**
```python
import os
DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() == "true"
```

### Fix Pattern 8: Weak Cryptography (SR-22) -- Weak Algorithms to Strong Ones

**Before:**
```python
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()
```

**After:**
```python
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
# To verify:
# bcrypt.checkpw(password.encode(), stored_hash)
```

### Fix Pattern 9: Insecure Random (SR-26) -- Predictable to Cryptographic Random

**Before:**
```python
import random
token = str(random.randint(100000, 999999))
```

**After:**
```python
import secrets
token = secrets.token_hex(16)
# Or for numeric OTP:
# token = str(secrets.randbelow(900000) + 100000)
```

**Before (JavaScript):**
```javascript
const token = Math.random().toString(36).substring(2);
```

**After:**
```javascript
const crypto = require('crypto');
const token = crypto.randomBytes(32).toString('hex');
```

### Fix Pattern 10: SSL Verification Disabled (SR-31) -- Disabled to Enabled

**Before:**
```python
requests.get(url, verify=False)
```

**After:**
```python
requests.get(url, verify=True)  # or just requests.get(url) since True is default
```

**Before (Node.js):**
```javascript
process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";
```

**After:**
Remove the line entirely. If a self-signed cert is needed for development, use a proper CA bundle.

### Fix Pattern 11: Missing Authentication (SR-19) -- Unprotected to Protected Routes

**Before (Python/Flask):**
```python
@app.route("/admin/users")
def admin_users():
    return get_all_users()
```

**After:**
```python
from functools import wraps
from flask import session, redirect, abort

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        if not session.get("is_admin"):
            abort(403)
        return f(*args, **kwargs)
    return decorated

@app.route("/admin/users")
@admin_required
def admin_users():
    return get_all_users()
```

### Fix Pattern 12: Path Traversal (SR-11) -- Direct Path to Safe Path

**Before:**
```python
filename = request.args.get("file")
with open(f"/uploads/{filename}") as f:
    return f.read()
```

**After:**
```python
import os
filename = request.args.get("file")
safe_name = os.path.basename(filename)  # Strip directory components
full_path = os.path.realpath(os.path.join("/uploads", safe_name))
if not full_path.startswith("/uploads/"):
    abort(403)
with open(full_path) as f:
    return f.read()
```

### Fix Pattern 13: Insecure Deserialization (SR-42) -- Unsafe to Safe Loading

**Before:**
```python
import pickle
data = pickle.loads(user_data)

import yaml
config = yaml.load(user_input)
```

**After:**
```python
import json
data = json.loads(user_data)  # Use JSON instead of pickle for untrusted data

import yaml
config = yaml.safe_load(user_input)  # Use safe_load instead of load
```

### Fix Pattern 14: Error Information Exposure (SR-37) -- Detailed to Generic Errors

**Before:**
```python
@app.errorhandler(500)
def handle_error(e):
    return {"error": str(e), "traceback": traceback.format_exc()}, 500
```

**After:**
```python
import logging
logger = logging.getLogger(__name__)

@app.errorhandler(500)
def handle_error(e):
    logger.error(f"Internal error: {e}", exc_info=True)  # Log details server-side
    return {"error": "An internal error occurred. Please try again later."}, 500
```

### Fix Pattern 15: Missing .gitignore Entries

If `.env` or other secret files are not in `.gitignore`, add them:

```
# Secrets and environment files
.env
.env.local
.env.production
*.pem
*.key
credentials.json
```

### Fix Pattern 16: Cookie Security (SR-33) -- Insecure to Secure Cookies

**Before:**
```python
response.set_cookie("session_id", session_id)
```

**After:**
```python
response.set_cookie(
    "session_id",
    session_id,
    secure=True,
    httponly=True,
    samesite="Strict",
    max_age=3600
)
```

### Fix Pattern 17: Improper Resource Release (SR-41) -- Manual to Context Manager

**Before:**
```python
f = open("data.txt")
data = f.read()
# f.close() missing
```

**After:**
```python
with open("data.txt") as f:
    data = f.read()
```

---

## Step 3: Apply Fixes Using the Edit Tool

For each vulnerability found:

1. **Read** the file containing the vulnerability to get the full context.
2. Use the **Edit** tool to apply the fix, replacing the vulnerable code with the secure alternative.
3. Ensure the fix:
   - Preserves the original functionality
   - Follows the project's existing code style (indentation, naming conventions)
   - Does not break imports or dependencies
   - Adds necessary imports at the top of the file if needed
4. If the fix requires a new dependency (e.g., `bcrypt`, `DOMPurify`), note it in the report but still apply the code change.
5. If the fix requires creating a new file (e.g., `.env.example`, adding to `.gitignore`), create it.

### Fix Priority Order

Apply fixes in this order:
1. **Hardcoded secrets** (SR-24) -- most urgent, secrets may already be in git history
2. **SQL Injection** (SR-01) -- data breach risk
3. **Code/Command Injection** (SR-03, SR-04) -- remote code execution risk
4. **Authentication/Authorization** (SR-19, SR-20) -- access control
5. **XSS** (SR-07) -- user compromise
6. **CSRF** (SR-08) -- action forgery
7. **Weak Crypto / Insecure Random** (SR-22, SR-26, SR-28) -- data protection
8. **SSL/Certificate issues** (SR-30, SR-31) -- transport security
9. **Debug code / Error exposure** (SR-37, SR-44) -- information leakage
10. **All other MEDIUM findings** -- remaining issues

---

## Step 4: Re-Scan to Verify Fixes

After all fixes have been applied:

1. Re-scan each file that was modified using Grep to verify:
   - The vulnerable pattern no longer exists
   - The safe pattern is now in place
2. Read the modified files to verify the code is syntactically correct.
3. Check that no new issues were introduced by the fixes.

---

## Step 5: Generate the Fix Report

Produce the report in the following format:

```
===============================================
  KKTV SECURITY FIX REPORT
===============================================
  Project: [project name/path]
  Language: [detected language]
  Framework: [detected framework]
  Scan Date: [current date]
===============================================

  SUMMARY
  -------
  Vulnerabilities Found:  [count]
  Fixes Applied:          [count]
  Fixes Skipped (LOW):    [count]
  Verification: [PASSED/ISSUES REMAINING]
===============================================
```

### Fix Details

For each fix applied:

```
FIX #[n]: SR-[id] [Vulnerability Name] (CWE-[number]) [SEVERITY]
  File: [file_path]:[line_number]

  BEFORE:
    > [original vulnerable code, 1-5 lines]

  AFTER:
    > [fixed secure code, 1-5 lines]

  What was fixed: [brief explanation]
  Verification: [CONFIRMED FIXED / NEEDS MANUAL REVIEW]
```

### Skipped Items

```
SKIPPED (requires manual review):
  - [SR-XX: reason why automatic fix was not possible]
```

### New Dependencies Required

```
NEW DEPENDENCIES:
  - [package_name]: [reason needed] -- install with [command]
```

### Post-Fix Checklist

```
POST-FIX ACTIONS REQUIRED:
  [ ] Install new dependencies listed above
  [ ] Set environment variables listed in .env.example
  [ ] Rotate any secrets that were previously hardcoded in source code
  [ ] Rotate any secrets found in git history (git log)
  [ ] Run the application and verify all functionality works
  [ ] Run existing tests to check for regressions
  [ ] Consider running the "review" skill again for a full audit
```

---

## Important Notes

- **Always preserve functionality.** Security fixes must not break the application. If a fix would change behavior significantly, apply the fix but add a comment explaining what changed.
- **Never remove code without replacement.** When removing `eval()` or `debug=True`, always provide the safe alternative.
- **Be conservative with auth fixes.** If adding authentication middleware, ensure existing public routes remain public. Only protect routes that clearly should require authentication.
- **Respect the framework.** Use framework-native security features when available (e.g., Django CSRF middleware, Express helmet, Spring Security).
- **Create .env.example, not .env.** Never create a `.env` file with actual secrets. Create `.env.example` with placeholder values and instructions.
- **When in doubt, skip and document.** If a fix is ambiguous or could break functionality, skip it and document it in the "Skipped Items" section with a clear explanation.
- **Do not fix LOW severity items automatically.** Report them but leave them for manual review.
- **Add imports at the top of files.** When a fix requires a new import, add it with the existing imports, following the file's import style.
- **Handle .gitignore carefully.** If adding to `.gitignore`, append to the end of the file. Do not modify existing entries.
