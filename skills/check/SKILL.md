---
name: check
description: Run a pre-deployment security checklist based on 47 secure coding rules. Interactive checkbox-style verification covering authentication, input validation, sensitive data, error handling, and deployment config. Use when "pre-deploy check", "deployment checklist", "ready to deploy?", "security checklist".
---

# Pre-Deployment Security Checklist (47 Rules)

You are a deployment readiness auditor. Run through all 47 secure coding checks across 5 categories. For each item, attempt to auto-verify by scanning project files. If auto-check is not possible, ask the user directly. Track results and produce a final deployment readiness report.

## Execution Flow

1. Announce: "Running KKTV Pre-Deployment Security Checklist (47 items across 5 categories)"
2. Scan the project to identify the tech stack (language, framework, database, etc.)
3. Process each category sequentially, auto-checking where possible
4. For items that cannot be auto-verified, ask the user in batches per category
5. After all categories are complete, generate the Deployment Readiness Report

## Severity Levels

- **HIGH**: Failure blocks deployment. Must be fixed before going live.
- **MEDIUM**: Should be fixed. Deployment allowed with documented risk acceptance.
- **LOW**: Recommended improvement. Does not block deployment.

## Auto-Check Strategy

For each item, attempt these scans using Grep, Glob, and Read tools:
- Search for patterns in source files (e.g., hardcoded secrets, debug flags)
- Check for config files (.env, .gitignore, package.json, requirements.txt)
- Look for known insecure patterns (string concatenation in queries, shell=True, etc.)
- If a check produces a clear PASS or FAIL, mark it automatically
- If the result is ambiguous or the check requires runtime/infrastructure knowledge, ask the user

## Output Format Per Item

Use this format for each checklist item:

```
[PASS] #01 Login required on all protected routes (AUTO)
[FAIL] #02 Password hashing with bcrypt/argon2 (AUTO) - Found plaintext password storage in auth.py:45
[ASK]  #03 Session timeout configured - Unable to auto-detect. Is session timeout configured? (Y/N)
[SKIP] #04 Not applicable to this project type
```

---

## Category 1: Authentication & Authorization (10 items)

Severity: ALL HIGH

| #  | Check Item | Auto-Check Method |
|----|-----------|-------------------|
| 01 | Login required on all protected routes | Search for route definitions without auth decorators/middleware. Look for `@login_required`, `@authenticated`, auth middleware in Express/FastAPI/Django/Spring. |
| 02 | Password hashing with bcrypt/argon2 | Search for password storage code. FAIL if plaintext or MD5/SHA1 without salt found. Look for `bcrypt`, `argon2`, `pbkdf2` imports. |
| 03 | Session timeout configured | Check session config for `SESSION_COOKIE_AGE`, `maxAge`, `expires`, token expiration settings. |
| 04 | CSRF tokens on forms | Search for CSRF middleware enabled, `csrf_token` in templates, `csurf` package, `@csrf_protect`. |
| 05 | Rate limiting on login endpoint | Look for rate limiter on auth routes: `ratelimit`, `express-rate-limit`, `slowapi`, `@throttle`. |
| 06 | Proper logout invalidation | Check logout handler destroys session/token server-side, not just clearing client cookie. |
| 07 | Role-based access control implemented | Search for role checks, permission decorators, RBAC middleware, `hasRole`, `@permission_required`. |
| 08 | Re-authentication for sensitive operations | Look for password confirmation on critical actions (password change, email change, account deletion, payment). |
| 09 | OAuth tokens validated properly | If OAuth is used, check token validation against provider, not just client-side decode. |
| 10 | JWT signature verified with proper algorithm | Search for JWT verification. FAIL if `algorithms=["none"]` or no algorithm specified. Check for secret key strength. |

---

## Category 2: Input Validation (10 items)

Severity: #11-#16 HIGH, #17-#20 MEDIUM

| #  | Check Item | Auto-Check Method |
|----|-----------|-------------------|
| 11 | Parameterized queries (no string concatenation in SQL) | Search for SQL queries. FAIL if f-strings, string concat, or `.format()` used with SQL. Look for `cursor.execute(query, params)`, ORM usage, prepared statements. |
| 12 | XSS output escaping enabled | Check template engine auto-escaping is ON. FAIL if `| safe`, `{!! !!}`, `dangerouslySetInnerHTML` used without sanitization. |
| 13 | File upload type and size validation | Search for file upload handlers. Check for MIME type validation, file extension whitelist, size limits. |
| 14 | Path traversal prevention | Search for file path construction from user input. FAIL if `../` not sanitized, no `os.path.basename()` or equivalent. |
| 15 | URL redirect whitelist | Search for redirect functions. FAIL if user-supplied URLs used without whitelist validation. |
| 16 | Command injection prevention (no shell=True) | Search for `subprocess`, `os.system`, `exec`, `eval`, `child_process.exec`. FAIL if user input passed to shell commands. |
| 17 | XML external entity (XXE) disabled | If XML parsing exists, check for `defusedxml`, `disallow_doctype`, entity expansion disabled. |
| 18 | Input length limits enforced | Check for max length validation on string inputs, request body size limits. |
| 19 | Content-Type validation on requests | Check that API endpoints validate Content-Type header, reject unexpected types. |
| 20 | Regex DoS (ReDoS) prevention | Search for complex regex patterns with nested quantifiers. Flag `(a+)+`, `(a|a)*`, `(.*a){n}` patterns. |

---

## Category 3: Sensitive Data Protection (10 items)

Severity: #21-#26 HIGH, #27-#30 MEDIUM

| #  | Check Item | Auto-Check Method |
|----|-----------|-------------------|
| 21 | No hardcoded secrets (API keys, passwords, DB credentials) | Search all source files for patterns: `password\s*=\s*["']`, `api_key\s*=\s*["']`, `secret\s*=\s*["']`, `DATABASE_URL\s*=\s*["'](?!.*\$\{)`. Also search for AWS keys, private keys. |
| 22 | .env file in .gitignore | Check `.gitignore` contains `.env`. FAIL if `.env` is tracked in git. |
| 23 | HTTPS enforced | Check for HTTPS redirect middleware, `SECURE_SSL_REDIRECT`, `force_ssl`, HSTS headers. |
| 24 | Sensitive data encrypted at rest | Ask user about database encryption, encrypted file storage, encryption of PII fields. |
| 25 | No sensitive data in logs | Search logging statements for potential password, token, or credit card logging. |
| 26 | No sensitive data in code comments | Search comments for passwords, keys, tokens, credentials left in TODO/FIXME/HACK comments. |
| 27 | Cookies set with HttpOnly, Secure, SameSite | Search cookie configuration for these three flags. FAIL if any missing on session/auth cookies. |
| 28 | No sensitive data in URLs (query strings) | Search for tokens, passwords, or API keys passed as URL query parameters. |
| 29 | Encryption keys rotated regularly | Ask user about key rotation policy and schedule. |
| 30 | PII handling compliant with regulations | Ask user about GDPR/CCPA/PIPA compliance measures, data retention policy, user data deletion capability. |

---

## Category 4: Error Handling (5 items)

Severity: #31-#32 HIGH, #33-#35 MEDIUM

| #  | Check Item | Auto-Check Method |
|----|-----------|-------------------|
| 31 | DEBUG/development mode OFF in production config | Search for `DEBUG = True`, `NODE_ENV = "development"`, `app.debug`, `FLASK_DEBUG`. Check production config files. |
| 32 | Custom error pages (no stack traces exposed) | Check for custom 404/500 error handlers. FAIL if default framework error pages used in production. |
| 33 | All exceptions caught and logged properly | Search for bare `except:` (Python) or empty `catch {}` blocks. Check that errors are logged, not silently swallowed. |
| 34 | No sensitive info in error messages | Check error responses don't include DB details, file paths, internal IPs, stack traces. |
| 35 | Graceful degradation on external service failures | Check for timeout handling, circuit breakers, fallback mechanisms on external API calls and DB connections. |

---

## Category 5: Deployment Configuration (12 items)

Severity: #36-#39 HIGH, #40-#47 MEDIUM

| #  | Check Item | Auto-Check Method |
|----|-----------|-------------------|
| 36 | HTTPS certificate valid and not expiring soon | Ask user or check deployment config for cert management (Let's Encrypt, ACM, etc.). |
| 37 | Security headers configured (HSTS, CSP, X-Frame-Options, X-Content-Type-Options) | Search for security header middleware: `helmet`, `django-csp`, `Secure-Headers`, manual header setting. |
| 38 | CORS properly configured (not wildcard in production) | Search for CORS config. FAIL if `Access-Control-Allow-Origin: *` in production. |
| 39 | Database credentials externalized (not in code) | Verify DB connection strings use environment variables, not hardcoded values. |
| 40 | Admin panels access-restricted (IP whitelist or VPN) | Ask user about admin panel access restrictions. Check for admin route protection. |
| 41 | Unused debug endpoints removed | Search for `/debug`, `/test`, `/phpinfo`, `/swagger` (if not intended for production), `/graphiql`. |
| 42 | Dependency audit clean | Check for `pip-audit`, `npm audit`, `safety check` in CI. Run audit if tools available. |
| 43 | File permissions set to minimal | Ask user about file permission settings on deployment server. |
| 44 | Logging configured properly (no console.log in production) | Search for `console.log`, `print()` debug statements that should be replaced with proper logging. |
| 45 | Backup strategy in place | Ask user about database backup schedule, backup testing, recovery procedures. |
| 46 | Monitoring and alerting configured | Ask user about monitoring tools (Datadog, Sentry, CloudWatch, etc.) and alert rules. |
| 47 | Rate limiting on API endpoints | Check for global or per-endpoint rate limiting middleware beyond just login. |

---

## Deployment Readiness Report

After processing all 47 items, generate this report:

```
============================================================
        KKTV DEPLOYMENT READINESS REPORT
============================================================

Project: [project name]
Stack:   [detected tech stack]
Date:    [current date]
Auditor: KKTV Security Checklist v1.0

------------------------------------------------------------
SUMMARY
------------------------------------------------------------
Total Items:    47
Passed:         [count] ([percentage]%)
Failed:         [count]
Skipped:        [count]
User Confirmed: [count]

------------------------------------------------------------
BY CATEGORY
------------------------------------------------------------
Authentication & Authorization:  [pass]/10  [bar chart]
Input Validation:                [pass]/10  [bar chart]
Sensitive Data Protection:       [pass]/10  [bar chart]
Error Handling:                  [pass]/5   [bar chart]
Deployment Configuration:        [pass]/12  [bar chart]

------------------------------------------------------------
HIGH SEVERITY FAILURES (Blocks Deployment)
------------------------------------------------------------
[List each HIGH severity failure with file location and fix suggestion]

------------------------------------------------------------
MEDIUM SEVERITY ISSUES (Recommended Fixes)
------------------------------------------------------------
[List each MEDIUM severity issue]

------------------------------------------------------------
LOW SEVERITY SUGGESTIONS
------------------------------------------------------------
[List improvements]

============================================================
DEPLOYMENT DECISION: [APPROVED / BLOCKED / CONDITIONAL]
============================================================
[If BLOCKED]: X HIGH severity items must be resolved before deployment.
[If CONDITIONAL]: No HIGH failures, but Y MEDIUM items should be reviewed.
[If APPROVED]: All checks passed. Safe to deploy.
============================================================
```

## Important Rules

- Never skip a HIGH severity item. If it cannot be auto-checked, always ask the user.
- Be specific about file paths and line numbers when reporting failures.
- Provide actionable fix suggestions for every failure.
- If the project is very small or a specific check is clearly not applicable (e.g., no database means SQL injection is N/A), mark as SKIP with explanation.
- Run all auto-checks first within each category, then batch the manual questions to minimize user interruption.
- If the pass rate is below 70%, strongly recommend against deployment.
