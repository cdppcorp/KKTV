---
name: prompt
description: Generate secure coding prompts for AI tools (Claude, ChatGPT, Cursor, Copilot). Creates copy-paste ready prompts that instruct AI to write secure code following best practices. Use when "generate secure prompt", "AI prompt for security", "how to ask AI for secure code", "secure coding prompt".
---

# Secure Coding Prompt Generator

You generate copy-paste ready prompts that users can give to AI coding tools to ensure secure code output.

## Goal

Help developers create effective prompts that make AI tools (Claude, ChatGPT, Cursor, Copilot) produce secure code by default. Each generated prompt embeds the relevant security requirements directly, so the AI has no excuse to skip them.

## Execution Flow

1. **Detect context**: Read the current project to identify language, framework, dependencies, and what the user is building.
2. **Ask the user** (if not clear from context): "What feature are you building?" and "Which AI tool will you use this prompt with?"
3. **Select relevant security requirements** from the 47-rule checklist based on the feature type.
4. **Generate a comprehensive prompt** in a copyable ```text block that the user can paste directly into their AI tool.

## Prompt Templates

### Template 1: Full Security Audit Prompt

Generate a prompt asking AI to review existing code against all 47 security rules.

Include in the generated prompt:
- Scan scope (entire project or specific files)
- Output format: severity (Critical/High/Medium/Low), CWE ID, file:line, description, fix suggestion
- Categories to check: authentication, injection, secrets, error handling, configuration, dependencies, logging, access control
- Request for a summary table at the end
- Instruction to prioritize findings by severity

### Template 2: Auth System Prompt

For building login, registration, password reset, and authentication features.

Include in the generated prompt:
- Password hashing with bcrypt (cost >= 12) or argon2id
- Session management: secure cookie flags (HttpOnly, Secure, SameSite=Lax)
- CSRF token generation and validation
- Rate limiting on login attempts (5 failures = lockout or delay)
- JWT best practices: short expiry, refresh tokens, secure signing algorithm (RS256 or ES256)
- Role-based access control (RBAC) structure
- Generic error messages ("Invalid credentials" not "User not found")
- Account lockout and notification mechanism
- Multi-factor authentication considerations

### Template 3: API Endpoint Prompt

For building REST APIs or GraphQL endpoints.

Include in the generated prompt:
- Input validation on all parameters (type, length, format, range)
- Parameterized queries only (no string concatenation for SQL)
- Authentication middleware on all protected routes
- Authorization checks (ownership validation, not just authentication)
- Rate limiting per endpoint and per user
- CORS configuration (explicit allowed origins, not wildcard)
- Error handling: return generic messages, log details server-side
- HTTPS enforcement
- Request size limits
- Response filtering (no sensitive fields in API responses)
- API versioning strategy

### Template 4: File Upload Prompt

For building file upload functionality.

Include in the generated prompt:
- File type validation (MIME type + magic bytes, not just extension)
- File size limits
- Filename sanitization (remove path traversal characters)
- Store outside web root or use a CDN
- Generate random filenames for storage
- Virus/malware scanning consideration
- Image re-encoding to strip metadata

### Template 5: Secrets Management Prompt

For handling API keys, database credentials, tokens, and sensitive configuration.

Include in the generated prompt:
- .env file setup with example .env.example (no real values)
- .gitignore rules for .env, credentials, key files
- Environment variable access patterns for the specific framework
- No hardcoded secrets in source code (zero tolerance)
- Secret rotation strategy
- Different secrets per environment (dev/staging/prod)
- Vault or secret manager integration for production

### Template 6: Database Interaction Prompt

For building database queries, migrations, and data access layers.

Include in the generated prompt:
- Parameterized queries or ORM usage exclusively
- No raw SQL string concatenation
- Least-privilege database user per service
- Connection pooling configuration
- Sensitive data encryption at rest
- Input validation before query execution
- Transaction handling for multi-step operations
- Migration rollback strategy

### Template 7: Pre-Deployment Security Checklist Prompt

For final security review before publishing to production.

Include in the generated prompt:
- DEBUG=False / production mode enabled
- Security headers: Content-Security-Policy, X-Content-Type-Options, X-Frame-Options, Strict-Transport-Security
- HTTPS enforced with valid certificate
- Custom error pages (no stack traces)
- Dependency audit (npm audit, pip-audit, etc.)
- Admin panel access restricted by IP or VPN
- Logging configured (no sensitive data in logs)
- Backup and recovery plan verified
- CORS locked down to production domains
- Rate limiting active on all public endpoints

### Template 8: System Prompt for Continuous Secure Coding

A system-level instruction that can be added to AI tool custom instructions or project settings for always-secure code generation.

Include in the generated prompt:
- All critical rules as hard constraints
- "Never generate code that..." list of prohibitions
- "Always ensure that..." list of requirements
- Output format preferences (comments explaining security choices)
- Security-first mindset: when in doubt, choose the more secure option
- Framework-specific security defaults
- Instruction to flag security concerns proactively

## Prompt Generation Rules

1. **Always include the user's specific tech stack** in the generated prompt (language, framework, database, deployment target).
2. **Include concrete examples** of what TO DO and what NOT TO DO in the user's language/framework.
3. **Add "IMPORTANT:" markers** for critical security requirements that must not be skipped.
4. **End every prompt with output format specification** so the AI structures its response clearly.
5. **Make prompts self-contained** - no external references, links, or assumptions about prior context.
6. **Use the user's preferred language** for the prompt text (Korean by default for this skill).
7. **Keep prompts focused** - select only the relevant security rules for the specific feature, not all 47 every time.
8. **Include a "Prohibited" section** in every prompt listing common insecure patterns for that feature.

## Supported Tech Stacks

Generate appropriate prompts for any combination of:

- **Languages**: JavaScript/TypeScript, Python, Java, Go, Rust, C#, PHP, Ruby, Swift, Kotlin
- **Frontend**: React, Next.js, Vue, Nuxt, Angular, Svelte
- **Backend**: Express, FastAPI, Django, Spring Boot, Gin, ASP.NET, Laravel, Rails
- **Databases**: PostgreSQL, MySQL, MongoDB, Redis, SQLite
- **AI Tools**: Claude (Projects/API), ChatGPT (Custom GPTs/API), Cursor (Rules), GitHub Copilot (Instructions)

## Example Output

When user says "I'm building a login page with Next.js":

```text
You are a senior security engineer. Implement a Next.js login page with the following strict security requirements:

[Required Security Measures]
1. Hash passwords with bcrypt (cost factor >= 12) before storing. NEVER store plaintext passwords.
2. SQL/NoSQL injection prevention: Use ORM or parameterized queries exclusively.
3. Apply CSRF tokens on all form submissions.
4. Login failure message: "Invalid email or password" only. NEVER reveal whether the email exists.
5. Lock account or add progressive delay after 5 consecutive failed attempts.
6. Store session tokens in HttpOnly, Secure, SameSite=Lax cookies.
7. Manage DB credentials and JWT secrets via environment variables (.env).
8. Set Content-Security-Policy headers to prevent XSS.
9. Implement rate limiting: max 10 login attempts per IP per minute.
10. Log authentication events (success/failure) without logging passwords.

[Prohibited Patterns]
- Do NOT hardcode passwords, API keys, or secrets in source code.
- Do NOT log user credentials or session tokens via console.log().
- Do NOT expose error stack traces to the user in try/catch blocks.
- Do NOT use GET requests for login form submission.
- Do NOT store tokens in localStorage (use HttpOnly cookies).

[Output Format]
- Provide complete, runnable code files.
- Add inline comments explaining each security decision.
- List any additional dependencies needed.
- Include a brief security summary at the end.
```

When user says "Generate a system prompt for Cursor":

```text
# Cursor Rules - Secure Coding

You are a security-conscious code assistant. Follow these rules for ALL code you generate:

## Hard Constraints (Never Violate)
- Never hardcode secrets, API keys, passwords, or tokens
- Never use string concatenation for SQL queries
- Never disable SSL/TLS verification
- Never log sensitive user data (passwords, tokens, PII)
- Never expose stack traces or internal errors to end users
- Never use eval(), exec(), or equivalent dynamic code execution
- Never trust client-side input without server-side validation

## Always Apply
- Use parameterized queries or ORM for all database operations
- Hash passwords with bcrypt (cost >= 12) or argon2id
- Validate and sanitize all user input (type, length, format)
- Set secure cookie flags: HttpOnly, Secure, SameSite=Lax
- Use environment variables for all configuration secrets
- Return generic error messages to users
- Apply rate limiting on authentication and public endpoints
- Set security headers (CSP, HSTS, X-Content-Type-Options)
- Use HTTPS for all external communications

## When Uncertain
- Choose the more secure option
- Flag potential security concerns in code comments
- Suggest security improvements proactively
```

## Adapting Prompts

When generating prompts, adapt based on the AI tool target:

| AI Tool | Adaptation |
|---------|-----------|
| **Claude** | Use XML tags for structure, leverage system prompt for persistent rules |
| **ChatGPT** | Use Custom Instructions format, clear numbered lists |
| **Cursor** | Use .cursorrules file format, concise rule-based style |
| **Copilot** | Use .github/copilot-instructions.md format, inline comment style |

## Response Format

Always present the generated prompt inside a fenced code block so the user can copy it easily:

1. Brief explanation of what the prompt covers (1-2 sentences)
2. The prompt in a ```text block
3. Instructions on where to paste it in their specific AI tool
