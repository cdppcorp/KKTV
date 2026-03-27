---
name: start
description: Run a full security audit on the current project based on 47 CWE-mapped secure coding rules. Produces a summary report plus per-category detail reports for easy reading. Use when "security review", "start security scan", "audit code", "scan for vulnerabilities", "보안 검토 시작".
---

# Security Audit Skill

You are a secure code auditor. Scan the current project against 47 secure coding rules in 7 categories. Produce a **summary report** plus **per-category detail reports** as separate markdown files for easy reading.

## Report Output Structure

Save reports to the project root under `reports/security/`:

```
reports/security/
├── summary.md                    ← One-page overview (pass rate, severity counts, top 5 critical)
├── cat1-input-validation.md      ← Category 1: Input Validation (18 rules)
├── cat2-security-features.md     ← Category 2: Security Features (16 rules)
├── cat3-time-state.md            ← Category 3: Time & State (2 rules)
├── cat4-error-handling.md        ← Category 4: Error Handling (3 rules)
├── cat5-code-quality.md          ← Category 5: Code Quality (3 rules)
├── cat6-encapsulation.md         ← Category 6: Encapsulation (2 rules)
└── cat7-api-misuse.md            ← Category 7: API Misuse (3 rules)
```

### summary.md format:
- Project name, tech stack, scan date
- Overall pass rate with visual bar
- Severity breakdown: HIGH / MEDIUM / LOW counts
- Top 5 most critical findings (one-liner each with file:line)
- Per-category pass rates
- Link to each category file for details

### Category file format:
- Category name and description
- Each rule: ID, name, CWE, severity, PASS/FAIL/SKIP status
- For FAIL items: file:line, vulnerable code snippet, fix recommendation
- Category-level summary at the end

After writing all files, display the summary.md content to the user directly.

---

## Step 1: Detect Project Language and Framework

Before scanning, identify the project's technology stack:

1. Use the Glob tool to find configuration files: `package.json`, `requirements.txt`, `Pipfile`, `Cargo.toml`, `go.mod`, `pom.xml`, `build.gradle`, `Gemfile`, `composer.json`, `*.csproj`, `pubspec.yaml`
2. Use Glob to find source files: `**/*.py`, `**/*.js`, `**/*.ts`, `**/*.java`, `**/*.go`, `**/*.rb`, `**/*.php`, `**/*.rs`, `**/*.cs`, `**/*.dart`
3. Look for framework indicators:
   - Python: `manage.py` (Django), `app.py`/`wsgi.py` (Flask), `main.py` (FastAPI)
   - JavaScript/TypeScript: `next.config.*` (Next.js), `nuxt.config.*` (Nuxt), `angular.json` (Angular), `vite.config.*`, `express` in package.json
   - Java: `@SpringBootApplication` (Spring Boot)
   - Go: `gin`, `echo`, `fiber` imports
   - Ruby: `config/routes.rb` (Rails)
   - PHP: `artisan` (Laravel)
4. Record the detected language, framework, and list of source files to scan.

---

## Step 2: Scan Against 47 Vulnerability Rules

Scan all source files against the following 47 rules organized into 7 categories. Use Grep and Read tools to search for vulnerable patterns.

### CATEGORY 1: Input Validation and Representation (18 items)

**SR-01: SQL Injection (CWE-89)**
- Search for: string concatenation in SQL queries, f-strings in queries, `+` operator building SQL, `.format()` in SQL, raw SQL without parameterized binding
- Vulnerable patterns: `"SELECT * FROM users WHERE id='" + user_input + "'"`, `f"SELECT * FROM users WHERE id={user_id}"`, `query = "... %s ..." % variable`
- Safe patterns: parameterized queries with `?` or `%s` placeholders and separate binding, ORM query builders like `.filter()`, `.where()`, `.find()`
- Severity: HIGH

**SR-02: LDAP Injection (CWE-90)**
- Search for: LDAP queries constructed with string concatenation, unescaped user input in LDAP filters
- Vulnerable patterns: `"(uid=" + username + ")"`, LDAP filter strings with direct variable insertion
- Safe patterns: LDAP escape functions applied to user input, parameterized LDAP queries
- Severity: HIGH

**SR-03: Code Injection (CWE-94)**
- Search for: `eval()`, `exec()`, `Function()` constructor, `setTimeout(string)`, `setInterval(string)`, dynamic code execution with user input
- Vulnerable patterns: `eval(user_input)`, `exec(user_code)`, `new Function(user_string)`
- Safe patterns: avoid `eval`/`exec` entirely, use AST parsing, use safe expression evaluators
- Severity: HIGH

**SR-04: OS Command Injection (CWE-78)**
- Search for: `os.system()`, `subprocess.call(shell=True)`, `child_process.exec()`, `Runtime.exec()`, backtick execution with user input
- Vulnerable patterns: `os.system("ping " + user_ip)`, `exec("ls " + user_path)`, shell=True with unsanitized input
- Safe patterns: `subprocess.run()` with argument list (no shell=True), allowlist validation of commands, `shlex.quote()` for escaping
- Severity: HIGH

**SR-05: XML Injection (CWE-91)**
- Search for: XML strings built with concatenation, user input inserted directly into XML documents
- Vulnerable patterns: `"<user>" + username + "</user>"`, string-built XML with unescaped input
- Safe patterns: XML builder libraries, proper escaping of special characters (`<`, `>`, `&`, `"`, `'`)
- Severity: MEDIUM

**SR-06: Format String Injection (CWE-134)**
- Search for: user-controlled format strings, `printf`-style formatting with user input as format string
- Vulnerable patterns: `printf(user_input)`, `String.format(user_input)`, `logging.info(user_input)` (when user_input contains format specifiers)
- Safe patterns: fixed format strings with user input as arguments only
- Severity: MEDIUM

**SR-07: Cross-Site Scripting / XSS (CWE-79)**
- Search for: unescaped user input in HTML output, `innerHTML`, `dangerouslySetInnerHTML`, `v-html`, `|safe` filter, `{% autoescape off %}`, `{!! !!}` in Blade
- Vulnerable patterns: `document.innerHTML = user_input`, `<div dangerouslySetInnerHTML={{__html: userInput}}>`, template rendering without auto-escaping
- Safe patterns: auto-escaping template engines, `textContent` instead of `innerHTML`, sanitization libraries (DOMPurify), Content-Security-Policy headers
- Severity: HIGH

**SR-08: Cross-Site Request Forgery / CSRF (CWE-352)**
- Search for: POST/PUT/DELETE forms without CSRF tokens, state-changing GET requests, disabled CSRF middleware
- Vulnerable patterns: `<form method="POST">` without csrf_token, `@csrf_exempt`, `csrf: false`, CSRF middleware commented out or removed
- Safe patterns: CSRF tokens in all state-changing forms, SameSite cookie attribute, framework CSRF middleware enabled
- Severity: HIGH

**SR-09: Server-Side Request Forgery / SSRF (CWE-918)**
- Search for: HTTP requests using user-supplied URLs without validation, `requests.get(user_url)`, `fetch(user_url)`, `urllib.urlopen(user_url)`
- Vulnerable patterns: fetching arbitrary URLs from user input, no domain allowlist
- Safe patterns: URL allowlist validation, block private IP ranges (10.x, 172.16-31.x, 192.168.x, 127.x, 169.254.x), DNS rebinding protection
- Severity: HIGH

**SR-10: HTTP Response Splitting (CWE-113)**
- Search for: user input in HTTP headers without sanitization, newline characters in header values
- Vulnerable patterns: `response.setHeader("Location", user_input)` without stripping `\r\n`
- Safe patterns: strip/reject newline characters from header values, use framework header-setting functions
- Severity: MEDIUM

**SR-11: Path Traversal (CWE-22)**
- Search for: file operations using user input for paths, `../` not blocked, `os.path.join` with user input without validation
- Vulnerable patterns: `open("/uploads/" + filename)`, path construction with user-controlled components without canonicalization
- Safe patterns: `os.path.realpath()` + prefix check, basename extraction, allowlist of permitted directories
- Severity: HIGH

**SR-12: Unrestricted File Upload (CWE-434)**
- Search for: file upload endpoints, missing file type validation, missing file size limits, executable upload paths
- Vulnerable patterns: accepting any file extension, storing uploads in web-accessible directories with original names, no MIME type check
- Safe patterns: extension allowlist, MIME type validation, file size limits, random filename generation, storage outside web root
- Severity: HIGH

**SR-13: Open Redirect (CWE-601)**
- Search for: redirect URLs from user input, `redirect(request.params["url"])`, `Location` header from user input
- Vulnerable patterns: `return redirect(request.GET["next"])` without validation
- Safe patterns: allowlist of permitted redirect domains, relative-path-only redirects, URL parsing and domain verification
- Severity: MEDIUM

**SR-14: XML External Entity / XXE (CWE-611)**
- Search for: XML parsing without disabling external entities, `XMLParser`, `DocumentBuilder`, `lxml.etree.parse` without security flags
- Vulnerable patterns: default XML parser configuration, DTD processing enabled
- Safe patterns: `defusedxml` (Python), disable DTDs/external entities in parser config, `FEATURE_SECURE_PROCESSING`
- Severity: HIGH

**SR-15: Integer Overflow (CWE-190)**
- Search for: arithmetic operations without overflow checks, unchecked type casting of large numbers, size calculations
- Vulnerable patterns: multiplication without overflow check, casting large values to smaller integer types
- Safe patterns: overflow-safe arithmetic functions, range validation before arithmetic, using big integer types
- Severity: MEDIUM

**SR-16: Improper Input for Security Decision (CWE-807)**
- Search for: security decisions based on client-controlled values (cookies, hidden fields, HTTP headers, user-agent)
- Vulnerable patterns: `if request.headers["X-Role"] == "admin"`, trusting client-side role/permission claims
- Safe patterns: server-side session/token validation, role stored in server-side session, JWT with signature verification
- Severity: HIGH

**SR-17: Buffer Overflow (CWE-120)**
- Search for: unsafe buffer operations in C/C++/Rust unsafe blocks, `strcpy`, `strcat`, `sprintf`, `gets`, fixed-size buffers with unchecked input
- Vulnerable patterns: `strcpy(buffer, user_input)`, `gets(buffer)`, `sprintf(buf, "%s", input)` without length check
- Safe patterns: `strncpy`, `snprintf`, bounded buffer operations, Rust safe string types
- Severity: HIGH

**SR-18: Unvalidated Input (General) (CWE-20)**
- Search for: endpoints that use request parameters without any validation, missing type checks, missing length limits, missing format validation
- Vulnerable patterns: directly using `request.body` / `request.params` without validation
- Safe patterns: input validation libraries (Joi, Zod, Pydantic, marshmallow), type checking, length limits, format regex
- Severity: MEDIUM

### CATEGORY 2: Security Features (16 items)

**SR-19: Missing Authentication for Critical Function (CWE-306)**
- Search for: admin/management endpoints without auth middleware, unprotected API routes for sensitive operations
- Vulnerable patterns: admin routes without `@login_required`, `@auth`, or auth middleware; direct database modification endpoints open to public
- Safe patterns: authentication middleware/decorators on all sensitive routes, centralized auth check
- Severity: HIGH

**SR-20: Improper Authorization (CWE-285)**
- Search for: missing role/permission checks after authentication, horizontal privilege escalation (user accessing other users' data)
- Vulnerable patterns: `get_user(request.params["user_id"])` without verifying the requester owns that resource
- Safe patterns: verify `request.user.id == resource.owner_id`, role-based access control (RBAC), policy-based authorization
- Severity: HIGH

**SR-21: Incorrect Permission Assignment (CWE-732)**
- Search for: world-readable file permissions, overly permissive CORS, `chmod 777`, `0o777`, public S3 buckets, permissive ACLs
- Vulnerable patterns: `os.chmod(file, 0o777)`, `CORS(origins="*")`, `Access-Control-Allow-Origin: *` for authenticated APIs
- Safe patterns: principle of least privilege, restrictive file permissions (0o600, 0o644), specific CORS origins
- Severity: MEDIUM

**SR-22: Weak Cryptographic Algorithm (CWE-327)**
- Search for: MD5, SHA1 for password hashing, DES, RC4, ECB mode, custom encryption algorithms
- Vulnerable patterns: `hashlib.md5(password)`, `SHA1`, `DES`, `AES-ECB`, `RC4`
- Safe patterns: bcrypt/scrypt/Argon2 for passwords, AES-256-GCM for encryption, SHA-256+ for integrity
- Severity: HIGH

**SR-23: Unencrypted Sensitive Data (CWE-311)**
- Search for: plaintext passwords in databases, sensitive data transmitted over HTTP, unencrypted PII storage
- Vulnerable patterns: `user.password = plain_password`, storing credit card numbers in plain text, HTTP-only APIs for sensitive data
- Safe patterns: encrypt at rest (AES-256), encrypt in transit (TLS/HTTPS), field-level encryption for PII
- Severity: HIGH

**SR-24: Hardcoded Secrets (CWE-798)**
- Search for: hardcoded API keys, passwords, tokens, secret keys in source code; strings matching patterns like `password = "..."`, `api_key = "..."`, `secret = "..."`, `token = "..."`
- Vulnerable patterns: `SECRET_KEY = "my-secret-key"`, `DB_PASSWORD = "admin123"`, `API_KEY = "sk-..."`, `token = "ghp_..."`, AWS access keys in code
- Safe patterns: environment variables (`os.environ`, `process.env`), `.env` files (in `.gitignore`), secret managers (AWS Secrets Manager, HashiCorp Vault)
- Severity: HIGH

**SR-25: Insufficient Key Length (CWE-326)**
- Search for: RSA keys < 2048 bits, AES keys < 128 bits, HMAC keys < 256 bits, short JWT secrets
- Vulnerable patterns: `RSA(1024)`, `AES-64`, short string JWT secrets (< 32 characters)
- Safe patterns: RSA >= 2048 bits, AES >= 128 bits (256 recommended), HMAC >= 256 bits
- Severity: MEDIUM

**SR-26: Insecure Random Number Generation (CWE-330)**
- Search for: `Math.random()`, `random.random()`, `rand()` used for security purposes (tokens, passwords, session IDs, OTPs)
- Vulnerable patterns: `token = Math.random().toString(36)`, `random.randint()` for OTP, `rand()` for session ID
- Safe patterns: `crypto.randomBytes()`, `secrets.token_hex()`, `SecureRandom`, `/dev/urandom`, `crypto.getRandomValues()`
- Severity: HIGH

**SR-27: Weak Password Policy (CWE-521)**
- Search for: password fields without length/complexity requirements, no password validation logic
- Vulnerable patterns: accepting any string as password, minimum length < 8, no complexity requirements
- Safe patterns: minimum 8+ characters, require mixed case + numbers + special chars, check against breached password lists
- Severity: MEDIUM

**SR-28: Hash Without Salt (CWE-759)**
- Search for: password hashing without salt, direct `SHA256(password)`, `hashlib.sha256(password.encode())`
- Vulnerable patterns: `hash = SHA256(password)`, `hashlib.sha256(password)` without salt
- Safe patterns: bcrypt (has built-in salt), `hashlib.pbkdf2_hmac()` with random salt, Argon2
- Severity: HIGH

**SR-29: Missing Brute-Force Protection (CWE-307)**
- Search for: login endpoints without rate limiting, no account lockout, no CAPTCHA after failed attempts
- Vulnerable patterns: login endpoint with no rate limiter middleware, unlimited retry allowed
- Safe patterns: rate limiting middleware (express-rate-limit, django-ratelimit), account lockout after N failures, CAPTCHA on repeated failures
- Severity: MEDIUM

**SR-30: Improper Digital Signature Verification (CWE-347)**
- Search for: JWT verification without algorithm specification, signature verification that can be bypassed, `algorithms=["none"]`
- Vulnerable patterns: `jwt.decode(token, verify=False)`, `jwt.decode(token, algorithms=["none", "HS256"])`, missing signature check
- Safe patterns: explicit algorithm specification, always verify signatures, reject `none` algorithm
- Severity: HIGH

**SR-31: Improper Certificate Validation (CWE-295)**
- Search for: `verify=False` in HTTP requests, SSL verification disabled, `NODE_TLS_REJECT_UNAUTHORIZED=0`, `rejectUnauthorized: false`
- Vulnerable patterns: `requests.get(url, verify=False)`, `process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0"`, `ssl: { rejectUnauthorized: false }`
- Safe patterns: always verify SSL certificates, use system CA bundle, pin certificates for critical services
- Severity: HIGH

**SR-32: Code Download Without Integrity Check (CWE-494)**
- Search for: downloading scripts/code from URLs without hash verification, `curl | bash`, CDN resources without SRI
- Vulnerable patterns: `<script src="https://cdn.example.com/lib.js">` without `integrity` attribute, `curl https://... | sh`
- Safe patterns: Subresource Integrity (SRI) hashes, package lock files, hash verification before execution
- Severity: MEDIUM

**SR-33: Sensitive Data in Cookies (CWE-539)**
- Search for: cookies without `Secure`, `HttpOnly`, `SameSite` flags; sensitive data stored in cookies
- Vulnerable patterns: `Set-Cookie: session=abc123` (no flags), storing user role/PII in cookies
- Safe patterns: `Secure; HttpOnly; SameSite=Strict`, store only session IDs in cookies, server-side session storage
- Severity: MEDIUM

**SR-34: Sensitive Information in Comments (CWE-615)**
- Search for: passwords, API keys, TODO with credentials, internal URLs, database connection strings in code comments
- Vulnerable patterns: `// password: admin123`, `// TODO: remove this API key`, `/* DB: mysql://root:pass@... */`
- Safe patterns: no secrets in comments, use secret management tools, clean up TODO comments before deployment
- Severity: MEDIUM

### CATEGORY 3: Time and State (2 items)

**SR-35: TOCTOU Race Condition (CWE-367)**
- Search for: file existence check followed by file operation, permission check followed by access, check-then-act patterns without locking
- Vulnerable patterns: `if file_exists(path): open(path)`, `if user.has_permission(): do_action()` without atomic operation
- Safe patterns: atomic file operations, database transactions with locking, optimistic concurrency control
- Severity: MEDIUM

**SR-36: Infinite Loop / Unbounded Recursion (CWE-835)**
- Search for: while/for loops without clear termination, recursive functions without base case limits, no timeout on loops
- Vulnerable patterns: `while True:` without break condition, recursion without depth limit, missing loop counter bounds
- Safe patterns: explicit loop bounds, recursion depth limits, timeout mechanisms, maximum iteration counts
- Severity: MEDIUM

### CATEGORY 4: Error Handling (3 items)

**SR-37: Information Exposure Through Error Messages (CWE-209)**
- Search for: detailed error messages returned to users, stack traces in API responses, database errors exposed to clients
- Vulnerable patterns: `return {"error": str(exception)}`, `res.status(500).send(err.stack)`, `DEBUG = True` in production
- Safe patterns: generic error messages for users, detailed logging server-side only, custom error pages, `DEBUG = False`
- Severity: MEDIUM

**SR-38: Missing Error Handling (CWE-390)**
- Search for: empty catch blocks, ignored exceptions, no error handling around I/O operations, database calls without try/catch
- Vulnerable patterns: `except: pass`, `catch(e) {}`, no try/catch around file/network/DB operations
- Safe patterns: meaningful error handling in every catch block, logging errors, graceful degradation
- Severity: MEDIUM

**SR-39: Improper Exception Handling (CWE-396)**
- Search for: overly broad catch blocks (`catch(Exception)`, `except Exception`), catching and swallowing all errors
- Vulnerable patterns: `except Exception as e: pass`, `catch(Exception e) { return null; }`, generic catch hiding specific errors
- Safe patterns: catch specific exceptions, handle each exception type appropriately, re-raise unknown exceptions
- Severity: LOW

### CATEGORY 5: Code Quality / Code Errors (3 items)

**SR-40: Null Pointer Dereference (CWE-476)**
- Search for: accessing properties/methods on potentially null/undefined values without null checks
- Vulnerable patterns: `user.name` without checking if `user` is null, `data["key"].value` without existence check
- Safe patterns: null checks before access, optional chaining (`?.`), null coalescing, guard clauses
- Severity: MEDIUM

**SR-41: Improper Resource Release (CWE-404)**
- Search for: opened files/connections/handles not closed, missing `finally` blocks, missing `using`/`with` statements
- Vulnerable patterns: `file = open(path)` without close, database connections not returned to pool, missing `finally` cleanup
- Safe patterns: `with open()` (Python), `try-with-resources` (Java), `using` (C#), `defer` (Go), explicit `.close()` in `finally`
- Severity: MEDIUM

**SR-42: Insecure Deserialization (CWE-502)**
- Search for: `pickle.loads()`, `yaml.load()` (without SafeLoader), `unserialize()`, `JSON.parse` of untrusted data followed by execution, `ObjectInputStream`
- Vulnerable patterns: `pickle.loads(user_data)`, `yaml.load(user_input)`, PHP `unserialize($user_data)`
- Safe patterns: `yaml.safe_load()`, avoid pickle for untrusted data, JSON instead of binary serialization, input validation before deserialization
- Severity: HIGH

### CATEGORY 6: Encapsulation (2 items)

**SR-43: Session Data Exposure (CWE-488)**
- Search for: sensitive data stored in client-accessible session storage, shared session variables in multi-tenant apps, session fixation vulnerabilities
- Vulnerable patterns: storing sensitive data in `localStorage`/`sessionStorage`, not regenerating session ID after login
- Safe patterns: server-side session storage, session ID regeneration after authentication, minimal data in client-side storage
- Severity: MEDIUM

**SR-44: Leftover Debug Code (CWE-489)**
- Search for: `console.log`, `print()` with sensitive data, `debugger` statements, `DEBUG = True`, debug endpoints, test credentials
- Vulnerable patterns: `console.log("user password:", password)`, `debugger;`, `DEBUG = True`, `/debug` endpoints, `admin/admin` test accounts
- Safe patterns: remove all debug statements before deployment, use logging framework with levels, environment-based debug flags
- Severity: MEDIUM

### CATEGORY 7: API Misuse (3 items)

**SR-45: Dangerous API Usage (CWE-676)**
- Search for: deprecated/unsafe APIs, `eval()`, `innerHTML`, `document.write()`, unsafe deserialization APIs, `strcpy`
- Vulnerable patterns: using deprecated crypto APIs, `document.write(user_input)`, `innerHTML = user_data`
- Safe patterns: use current/recommended APIs, `textContent` instead of `innerHTML`, safe alternatives documented by framework
- Severity: MEDIUM

**SR-46: DNS Lookup for Security Decision (CWE-350)**
- Search for: hostname-based authentication, DNS resolution used for access control decisions
- Vulnerable patterns: `if socket.gethostbyaddr(ip) == "trusted.example.com": allow()`, relying on reverse DNS for auth
- Safe patterns: IP-based allowlists, certificate-based authentication, avoid DNS for security decisions
- Severity: MEDIUM

**SR-47: Unsafe Reflection (CWE-470)**
- Search for: dynamic class loading from user input, reflection with user-controlled class names, `getattr(module, user_input)()`
- Vulnerable patterns: `Class.forName(user_input)`, `getattr(module, user_input)()`, `importlib.import_module(user_input)`
- Safe patterns: allowlist of permitted class/function names, factory pattern with fixed mappings, avoid reflection with user input
- Severity: HIGH

---

## Step 3: Perform the Scan

For each of the 47 rules above:

1. Use the **Grep** tool to search for vulnerable patterns across all detected source files.
   - Use appropriate regex patterns for the language detected.
   - Search both code files and configuration files.
2. When a potential vulnerability is found, use the **Read** tool to examine the surrounding context (5-10 lines before and after) to confirm it is a true positive.
3. Eliminate false positives by checking:
   - Is the flagged code in a test file? (lower severity, still note it)
   - Is the user input already sanitized upstream?
   - Is the code in a dead/unreachable path?
   - Is there a security middleware applied at a higher level?

---

## Step 4: Generate the Report

Produce the report in the following format:

### Report Header

```
===============================================
  KKTV SECURE CODE REVIEW REPORT
===============================================
  Project: [project name/path]
  Language: [detected language]
  Framework: [detected framework]
  Files Scanned: [count]
  Scan Date: [current date]
===============================================

  SUMMARY
  -------
  HIGH:   [count] findings
  MEDIUM: [count] findings
  LOW:    [count] findings
  TOTAL:  [count] findings
===============================================
```

### Findings (sorted by severity: HIGH first, then MEDIUM, then LOW)

For each finding, report:

```
[SEVERITY] SR-[number]: [Vulnerability Name] (CWE-[number])
  File: [file_path]:[line_number]
  Code:
    > [vulnerable code snippet, 1-3 lines]
  Risk: [brief explanation of the risk]
  Fix:  [specific recommendation for fixing]
```

### Full Checklist

After all findings, include the complete 47-item checklist:

```
===============================================
  FULL SECURITY CHECKLIST (47 Items)
===============================================

CATEGORY 1: Input Validation and Representation
  [PASS/FAIL/N/A] SR-01: SQL Injection (CWE-89)
  [PASS/FAIL/N/A] SR-02: LDAP Injection (CWE-90)
  [PASS/FAIL/N/A] SR-03: Code Injection (CWE-94)
  [PASS/FAIL/N/A] SR-04: OS Command Injection (CWE-78)
  [PASS/FAIL/N/A] SR-05: XML Injection (CWE-91)
  [PASS/FAIL/N/A] SR-06: Format String Injection (CWE-134)
  [PASS/FAIL/N/A] SR-07: Cross-Site Scripting (CWE-79)
  [PASS/FAIL/N/A] SR-08: CSRF (CWE-352)
  [PASS/FAIL/N/A] SR-09: SSRF (CWE-918)
  [PASS/FAIL/N/A] SR-10: HTTP Response Splitting (CWE-113)
  [PASS/FAIL/N/A] SR-11: Path Traversal (CWE-22)
  [PASS/FAIL/N/A] SR-12: Unrestricted File Upload (CWE-434)
  [PASS/FAIL/N/A] SR-13: Open Redirect (CWE-601)
  [PASS/FAIL/N/A] SR-14: XXE (CWE-611)
  [PASS/FAIL/N/A] SR-15: Integer Overflow (CWE-190)
  [PASS/FAIL/N/A] SR-16: Improper Input for Security Decision (CWE-807)
  [PASS/FAIL/N/A] SR-17: Buffer Overflow (CWE-120)
  [PASS/FAIL/N/A] SR-18: Unvalidated Input (CWE-20)

CATEGORY 2: Security Features
  [PASS/FAIL/N/A] SR-19: Missing Authentication (CWE-306)
  [PASS/FAIL/N/A] SR-20: Improper Authorization (CWE-285)
  [PASS/FAIL/N/A] SR-21: Incorrect Permission Assignment (CWE-732)
  [PASS/FAIL/N/A] SR-22: Weak Cryptographic Algorithm (CWE-327)
  [PASS/FAIL/N/A] SR-23: Unencrypted Sensitive Data (CWE-311)
  [PASS/FAIL/N/A] SR-24: Hardcoded Secrets (CWE-798)
  [PASS/FAIL/N/A] SR-25: Insufficient Key Length (CWE-326)
  [PASS/FAIL/N/A] SR-26: Insecure Random Number (CWE-330)
  [PASS/FAIL/N/A] SR-27: Weak Password Policy (CWE-521)
  [PASS/FAIL/N/A] SR-28: Hash Without Salt (CWE-759)
  [PASS/FAIL/N/A] SR-29: Missing Brute-Force Protection (CWE-307)
  [PASS/FAIL/N/A] SR-30: Improper Signature Verification (CWE-347)
  [PASS/FAIL/N/A] SR-31: Improper Certificate Validation (CWE-295)
  [PASS/FAIL/N/A] SR-32: Code Download Without Integrity (CWE-494)
  [PASS/FAIL/N/A] SR-33: Sensitive Data in Cookies (CWE-539)
  [PASS/FAIL/N/A] SR-34: Sensitive Info in Comments (CWE-615)

CATEGORY 3: Time and State
  [PASS/FAIL/N/A] SR-35: TOCTOU Race Condition (CWE-367)
  [PASS/FAIL/N/A] SR-36: Infinite Loop / Unbounded Recursion (CWE-835)

CATEGORY 4: Error Handling
  [PASS/FAIL/N/A] SR-37: Error Message Information Exposure (CWE-209)
  [PASS/FAIL/N/A] SR-38: Missing Error Handling (CWE-390)
  [PASS/FAIL/N/A] SR-39: Improper Exception Handling (CWE-396)

CATEGORY 5: Code Quality
  [PASS/FAIL/N/A] SR-40: Null Pointer Dereference (CWE-476)
  [PASS/FAIL/N/A] SR-41: Improper Resource Release (CWE-404)
  [PASS/FAIL/N/A] SR-42: Insecure Deserialization (CWE-502)

CATEGORY 6: Encapsulation
  [PASS/FAIL/N/A] SR-43: Session Data Exposure (CWE-488)
  [PASS/FAIL/N/A] SR-44: Leftover Debug Code (CWE-489)

CATEGORY 7: API Misuse
  [PASS/FAIL/N/A] SR-45: Dangerous API Usage (CWE-676)
  [PASS/FAIL/N/A] SR-46: DNS Lookup for Security Decision (CWE-350)
  [PASS/FAIL/N/A] SR-47: Unsafe Reflection (CWE-470)

SCORE: [passed]/[applicable] ([percentage]%)
```

---

## Step 5: Provide Recommendations

After the checklist, provide:

1. **Top 3 Priority Fixes** -- the most critical vulnerabilities that should be fixed immediately
2. **Quick Wins** -- low-effort fixes that improve security significantly (e.g., adding `DEBUG = False`, adding `.env` to `.gitignore`)
3. **Architecture Recommendations** -- any structural improvements suggested (e.g., adding authentication middleware, implementing CORS properly)

---

## Important Notes

- Mark a rule as **N/A** (Not Applicable) if the project does not use the relevant technology (e.g., no SQL database means SR-01 is N/A).
- Mark a rule as **PASS** only if you have confirmed no vulnerable patterns exist AND safe patterns are in place.
- Mark a rule as **FAIL** if any vulnerable pattern is found, even in a single file.
- Always check configuration files (`.env`, `settings.py`, `config.js`, `application.properties`, `docker-compose.yml`) in addition to source code.
- Check `.gitignore` to verify `.env` and secret files are excluded from version control.
- If the project has no source code files, report that no scan could be performed.
- Be thorough but avoid false positives. When in doubt, flag it as a finding with a note about uncertainty.
- Do NOT modify any files. This skill is read-only.
