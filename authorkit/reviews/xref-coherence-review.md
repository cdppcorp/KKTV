# Cross-Reference & Coherence Review

**Reviewer**: Automated Book Editor Review
**Date**: 2026-03-27
**Scope**: ch01 through ch17, all draft.md files

---

## PART A: CROSS-REFERENCE REVIEW

### A-1. Internal References Found

A systematic scan of all 17 chapters found **no explicit internal cross-references** using the "N장 M절 참고" or "위의 OO 참고" format. No chapter uses a direct "N장" or "N-M절" reference to point to another chapter.

This is itself a significant finding: the chapters are written as fully self-contained units with **zero inter-chapter linking**. While this supports the "필요한 부분만 골라 읽기" (pick-and-choose) reading mode described in ch01 (1-2), it means readers who follow the sequential path receive no guidance on related content in other chapters.

#### Implicit Cross-References (Content Overlap)

The following implicit references exist where one chapter discusses topics covered in detail by another, without explicit cross-reference links:

| Source | Referenced Topic | Target Chapter | Severity |
|--------|-----------------|----------------|----------|
| ch01 (1-1) | SQL Injection example | ch02 (2-1) | -- |
| ch01 (1-1) | CSRF token example | ch04 (4-2) | -- |
| ch01 (1-1) | Hardcoded secrets example | ch08 (8-3) | -- |
| ch01 (1-1) | Debug mode example | ch15 (15-2) / ch13 (13-1) | -- |
| ch04 (4-1) XSS | Mentions "세션 탈취" via document.cookie | ch11 (11-1) cookie security | -- |
| ch06 (6-2) | Mentions "서버 세션" for security decisions | ch15 (15-1) session data exposure | -- |
| ch11 (11-1) | References XSS, CSRF as attack vectors | ch04 (4-1, 4-2) | -- |
| ch17 (17-1) | "PART 2~5에서 다룬 모든 핵심 보안 주제" | All chapters | -- |

### A-2. Broken Cross-References

No broken cross-references found (because no explicit cross-references exist).

### A-3. Forward References

No explicit forward references found. However, several chapters discuss concepts that are formally explained later:

| Chapter | Concept Used | Where Formally Explained | Severity |
|---------|-------------|------------------------|----------|
| ch01 (1-1) | CSRF token, SQL Injection, hardcoded secrets | ch04, ch02, ch08 | Forward reference without context, but this is intentional as ch01 is an overview/motivation chapter |
| ch04 (4-2) CSRF | "세션" (session), "쿠키" (cookie) concepts | ch11 (11-1), ch15 (15-1) | Forward use of session/cookie concepts before they are formally defined |
| ch06 (6-2) | "서버 세션" for security decisions, Django session settings | ch11 (11-1), ch15 (15-1) | Forward use of session concept |

### A-4. Figure/Diagram References

No chapters contain explicit references to diagram files (e.g., "그림 X 참고" or similar). The following diagram.md files exist but are **never referenced** from their respective draft.md files:

| Diagram File | Parent Chapter | Referenced in draft.md? |
|-------------|---------------|----------------------|
| ch02/diagram.md | ch02 (SQL Injection) | No |
| ch04/diagram.md | ch04 (XSS) | No |
| ch04/diagram-csrf.md | ch04 (CSRF) | No |
| ch04/diagram-ssrf.md | ch04 (SSRF) | No |
| ch07/diagram.md | ch07 (Authentication) | No |
| ch08/diagram.md | ch08 (Encryption) | No |
| ch09/diagram.md | ch09 (Password/Auth) | No |
| ch17/diagram.md | ch17 (Checklist) | No |

### A-5. External URL References

The following external URLs were found across all chapters:

| Chapter | URL/Reference | Format Correct? | Notes |
|---------|--------------|-----------------|-------|
| ch04 (4-3) | `http://169.254.169.254/latest/meta-data/` | Yes (example URL) | AWS metadata endpoint, used in attack example |
| ch10 (10-3) | `http://example.com/install.sh` | Yes (example URL) | Vulnerable code example |
| ch16 | `https://nvd.nist.gov` | Yes | NIST NVD reference |
| ch16 | `https://cvedetails.com` | Yes | CVE details reference |
| ch01 (1-2) | OWASP reference (text only, no URL) | Missing URL | Should include `https://owasp.org` |

---

## PART B: COHERENCE REVIEW

### B-1. Prerequisite Ordering Issues

| Issue | Chapter | Detail | Severity |
|-------|---------|--------|----------|
| Session concept used before explanation | ch04 (4-2) | CSRF section uses "쿠키(Cookie)", "세션" concepts extensively. Cookie security attributes (HttpOnly, Secure, SameSite) are not explained until ch11 (11-1). Sessions as a concept are not formally introduced until ch06 (6-2) and ch15 (15-1). | :yellow_circle: MEDIUM |
| `.env` usage before explanation | ch01 (1-1) | The secure code example uses `os.environ.get("JWT_SECRET_KEY")` but `.env` files and environment variable management are not explained until ch08 (8-3). Readers following sequential order may not understand this pattern. | :yellow_circle: MEDIUM |
| `bcrypt` usage before explanation | ch01 (1-1) | The secure code example uses `bcrypt.checkpw()` but bcrypt is not explained until ch09 (9-3). | :yellow_circle: MEDIUM |
| Django decorator `@login_required` used before auth chapter | ch06 (6-2) | Safe code uses `@login_required` and `@user_passes_test`, but authentication decorators are formally explained in ch07 (7-1). | :yellow_circle: MEDIUM |
| `secrets` module referenced in ch13 | ch13 (13-2) | Uses `secrets.token_bytes()` in safe code, but `secrets` module is formally introduced in ch09 (9-1). Since ch13 comes after ch09, this is fine for sequential readers but not for pick-and-choose readers. | :green_circle: LOW |

### B-2. Depth Consistency

#### Within PART 2 (ch02-ch06): Input Data Validation

| Chapter | Sections | Depth Level | Consistency |
|---------|----------|-------------|-------------|
| ch02 | 2 sections (SQL Injection + LDAP) | SQL Injection: very deep with 5 code examples. LDAP: condensed as a callout box (lower priority). | Acceptable - LDAP is correctly flagged as lower priority |
| ch03 | 4 sections (Code Injection, OS Command, XML, Format String) | Consistent depth across sections, each with vulnerable/safe code | Good |
| ch04 | 4 sections (XSS, CSRF, SSRF, HTTP Response Splitting) | XSS and CSRF are very deep; SSRF is moderate; HTTP Response Splitting is relatively brief | :yellow_circle: MEDIUM - HTTP Response Splitting (4-4) is noticeably thinner than other sections in ch04 |
| ch05 | 4 sections (Path Traversal, File Upload, Open Redirect, XXE) | Consistent depth | Good |
| ch06 | 2 sections (Integer Overflow, Improper Input for Security) | Section 6-2 is very deep; 6-1 is moderate | Acceptable |

#### Within PART 3 (ch07-ch11): Security Functions

| Chapter | Depth Level | Consistency |
|---------|-------------|-------------|
| ch07 | 3 sections, all moderate depth with Django + Flask + FastAPI examples | Good |
| ch08 | 4 sections, deep with algorithm tables and key length recommendations | Good |
| ch09 | 4 sections, deep with multiple safe alternatives (bcrypt, argon2, secrets) | Good |
| ch10 | 3 sections, moderate depth | Good |
| ch11 | 2 sections, moderate depth for cookies, deep for comment security | Good |

#### Within PART 4 (ch12-ch14): Stable Code

| Chapter | Depth Level | Consistency |
|---------|-------------|-------------|
| ch12 | 2 sections, moderate depth | Good |
| ch13 | 3 sections, moderate depth | Good |
| ch14 | 3 sections, moderate depth with JSON alternative for pickle | Good |

#### Within PART 5 (ch15-ch16): Design

| Chapter | Depth Level | Consistency |
|---------|-------------|-------------|
| ch15 | 2 full sections + 1 callout for remaining topics (15-3, 15-4) | :yellow_circle: MEDIUM - Sections 15-3 and 15-4 from structure.md are collapsed into a brief callout box instead of full sections |
| ch16 | 1 full section + 1 callout for DNS lookup topic (16-1) | :yellow_circle: MEDIUM - Section 16-1 (DNS lookup) from structure.md is collapsed into a brief callout box instead of a full section. The full section covers 16-2 (Vulnerable API), while 16-1 is demoted. |

### B-3. Intro/Summary Presence

| Chapter | Opening Paragraph? | Chapter-level Intro? | Severity |
|---------|-------------------|---------------------|----------|
| ch01 | Yes - clear overview paragraph for each section | No chapter-level heading description (just "# Chapter 1") | :green_circle: LOW |
| ch02 | Yes - "개요" section present for each topic | No chapter-level intro paragraph | :green_circle: LOW |
| ch03 | Yes - "개요" section present for each topic | No chapter-level intro paragraph | :green_circle: LOW |
| ch04 | Yes - "개요" section present for each topic | No chapter-level intro paragraph | :green_circle: LOW |
| ch05 | Yes - "개요" section present for each topic | No chapter-level intro paragraph | :green_circle: LOW |
| ch06 | Yes - "개요" section present for each topic | No chapter-level intro paragraph | :green_circle: LOW |
| ch07 | Yes - "개요" section present for each topic | No chapter-level intro paragraph | :green_circle: LOW |
| ch08 | Yes - "개요" section present for each topic | No chapter-level intro paragraph | :green_circle: LOW |
| ch09 | Yes - "개요" section present for each topic | No chapter-level intro paragraph | :green_circle: LOW |
| ch10 | Yes - "개요" section present for each topic | No chapter-level intro paragraph | :green_circle: LOW |
| ch11 | Yes - "개요" section present for each topic | No chapter-level intro paragraph | :green_circle: LOW |
| ch12 | Yes - has chapter-level intro paragraph | Best practice example | Good |
| ch13 | Yes - has chapter-level intro paragraph | Best practice example | Good |
| ch14 | Yes - has chapter-level intro paragraph | Best practice example | Good |
| ch15 | Yes - has chapter-level intro paragraph | Best practice example | Good |
| ch16 | Yes - has chapter-level intro paragraph | Best practice example | Good |
| ch17 | Yes - "개요" section present for each topic | No chapter-level intro paragraph | :green_circle: LOW |

**Pattern**: Chapters 12-16 (PART 4 and PART 5) have chapter-level introductory paragraphs that set context before diving into sections. Chapters 01-11 and 17 lack this chapter-level intro and jump directly to section headings. This is an inconsistency in style.

### B-4. Promise Fulfillment (ch01 Promises)

Ch01 section 1-2 describes the book structure with a table:

| Promised in ch01 | Actual Structure | Match? |
|-------------------|-----------------|--------|
| PART 1: "시작하기" - AI 코드 보안의 필요성과 가이드 활용법 | ch01 covers this | Yes |
| PART 2: "입력값 검증" - SQL 삽입, XSS, 명령어 삽입 등 입력 관련 취약점 | ch02-06 cover this | Yes |
| PART 3: "인증과 인가" - 로그인, 세션, 권한 관리의 보안 | ch07-11 cover auth, encryption, passwords, certificates, info exposure | :red_circle: HIGH - PART 3 description says "인증과 인가" but actual content is much broader: "보안 기능을 제대로 구현하세요" including encryption (ch08), passwords (ch09), certificates (ch10), info exposure (ch11) |
| PART 4: "민감정보 보호" - 비밀키 관리, 암호화, 개인정보 처리 | ch12-14 cover timing/state, error handling, code errors | :red_circle: HIGH - PART 4 description in ch01 says "민감정보 보호" but actual content is "안정적인 코드를 작성하세요" covering race conditions, error handling, code quality |
| PART 5: "배포와 설정" - 서버 설정, HTTPS, 보안 헤더 등 | ch15-16 cover encapsulation and API misuse | :red_circle: HIGH - PART 5 description in ch01 says "배포와 설정" but actual content is "구조와 설계로 지키세요" covering encapsulation and API misuse |
| PART 6: "바이브 코딩 보안 체크리스트" | ch17 covers this | Yes |

**Critical Finding**: The PART descriptions in ch01 (1-2) section's table do NOT match the actual content of PARTs 3, 4, and 5. The table in ch01 appears to describe a different outline than what was actually written.

- ch01 says PART 3 = "인증과 인가" but structure.md says "보안 기능을 제대로 구현하세요"
- ch01 says PART 4 = "민감정보 보호" but structure.md says "안정적인 코드를 작성하세요"
- ch01 says PART 5 = "배포와 설정" but structure.md says "구조와 설계로 지키세요"

### B-5. Gap Detection

| Gap | Detail | Severity |
|-----|--------|----------|
| No HTTPS/TLS setup guide | ch01 promises "배포와 설정" covering "서버 설정, HTTPS, 보안 헤더" but no chapter provides a dedicated HTTPS setup guide. ch17 mentions HTTPS in the checklist but doesn't explain how to set it up. ch10 (10-2) covers SSL certificate validation in code but not server TLS configuration. | :red_circle: HIGH (promised content missing) |
| No security headers chapter | HTTP security headers (HSTS, CSP, X-Frame-Options, etc.) are only mentioned in ch17's checklist but never explained in detail. ch01 promises this in PART 5. | :red_circle: HIGH (promised content missing) |
| Session management not comprehensively covered | "세션" is used across ch04, ch06, ch11, ch15 but there is no dedicated section on session management best practices (session timeout, regeneration after login, server-side session stores). | :yellow_circle: MEDIUM |
| No "메모리 버퍼 오버플로우" content | structure.md lists "6-3. 메모리 버퍼 오버플로우" but ch06 draft only has sections 6-1 and 6-2. Section 6-3 is missing entirely. | :red_circle: HIGH (structural gap) |
| structure.md section title mismatch for ch03 | structure.md lists "3-4. 정규 표현식 삽입" but ch03 draft has "3-4. 포맷 스트링 삽입(Format String Injection)" instead. | :red_circle: HIGH (title mismatch with structure) |
| Diagram files never referenced | 8 diagram files exist across ch02, ch04, ch07, ch08, ch09, ch17 but none are referenced from any draft.md | :yellow_circle: MEDIUM |
| No inter-chapter cross-references | Despite the book being designed for both sequential and random-access reading, no chapter links to another for deeper information | :yellow_circle: MEDIUM |
| CORS only mentioned in ch17 | CORS (Cross-Origin Resource Sharing) is listed as a common mistake (#8 in ch17's TOP 10) but is never covered in a dedicated section | :green_circle: LOW |
| Logging best practices scattered | Logging appears in ch13 (error handling) and ch15 (debug code) but no unified section on secure logging practices | :green_circle: LOW |

### B-6. Chapter Title Consistency with structure.md

| structure.md Title | draft.md Title | Match? |
|-------------------|---------------|--------|
| 1장. 왜 바이브 코딩에도 보안이 필요한가 | "# PART 1: 시작하기 / # Chapter 1" (no descriptive title) | :yellow_circle: MEDIUM - missing descriptive title |
| 2장. 데이터베이스를 지키는 법 | "# Chapter 02. 데이터베이스를 노리는 삽입 공격" | :yellow_circle: MEDIUM - different wording ("지키는 법" vs "노리는 삽입 공격") |
| 3장. 코드와 명령어 삽입 차단 | "# Chapter 03. 코드와 명령어를 노리는 삽입 공격" | :yellow_circle: MEDIUM - different wording |
| 4장. 웹 공격의 핵심 - XSS와 위조 공격 | "# Chapter 04. 웹 요청을 노리는 공격" | :yellow_circle: MEDIUM - different wording |
| 5장. 파일과 경로, URL 관련 취약점 | "# Chapter 05. 파일과 URL을 노리는 공격" | :green_circle: LOW - minor difference |
| 6장. 기타 입력값 취약점 | "# Chapter 06. 데이터 타입과 보안 결정을 노리는 공격" | :yellow_circle: MEDIUM - different wording |
| 7장. 인증과 인가 | "# Chapter 07. 인증과 인가, 그리고 권한 설정" | :green_circle: LOW - minor addition |
| 8장. 암호화와 키 관리 | "# Chapter 08. 암호화, 제대로 하고 계십니까" | :yellow_circle: MEDIUM - different wording |
| 9장. 패스워드와 인증 강화 | "# Chapter 09. 난수, 패스워드, 그리고 인증 방어" | :green_circle: LOW - minor difference |
| 10장. 인증서와 무결성 | "# Chapter 10. 서명, 인증서, 무결성 검증" | :green_circle: LOW - minor addition |
| 11장. 민감 정보 노출 방지 | "# Chapter 11. 정보 노출을 차단하세요" | :green_circle: LOW - minor difference |
| 12장. 시간 및 상태 | "# Chapter 12. 시간 및 상태 - 타이밍이 만드는 버그" | :green_circle: LOW - subtitle added |
| 13장. 에러 처리 | "# Chapter 13. 에러 처리 - 오류가 보안 구멍이 되는 순간" | :green_circle: LOW - subtitle added |
| 14장. 코드 오류 | "# Chapter 14. 코드 오류 - 개발자가 놓치기 쉬운 함정들" | :green_circle: LOW - subtitle added |
| 15장. 캡슐화 | "# Chapter 15. 캡슐화 - 보여서는 안 되는 것들" | :green_circle: LOW - subtitle added |
| 16장. API 오용 | "# Chapter 16. API 오용 - 편리함 뒤에 숨은 위험" | :green_circle: LOW - subtitle added |
| 17장. 퍼블리싱 전 최종 점검 | "# PART 6: 바이브 코딩 보안 체크리스트 / # Chapter 17" (no descriptive title) | :yellow_circle: MEDIUM - missing descriptive title |

---

## SUMMARY OF ISSUES BY SEVERITY

### :red_circle: HIGH (5 issues)

1. **ch01 PART description table mismatch**: PART 3, 4, 5 descriptions in ch01's table ("인증과 인가", "민감정보 보호", "배포와 설정") do not match actual book content. This will confuse readers using the table for navigation.
2. **Missing section 6-3 (메모리 버퍼 오버플로우)**: Listed in structure.md but not present in ch06 draft.
3. **Section title mismatch ch03 3-4**: structure.md says "정규 표현식 삽입" but draft has "포맷 스트링 삽입".
4. **Missing promised content: HTTPS/TLS setup**: ch01 promises coverage of "서버 설정, HTTPS" in PART 5 but this is never covered.
5. **Missing promised content: Security headers**: ch01 promises "보안 헤더" coverage but no chapter explains them in detail.

### :yellow_circle: MEDIUM (12 issues)

1. Session/cookie concepts used in ch04 before formal explanation in ch11/ch15
2. `.env` and `os.environ` used in ch01 before explanation in ch08
3. `bcrypt` used in ch01 before explanation in ch09
4. `@login_required` used in ch06 before explanation in ch07
5. HTTP Response Splitting (4-4) is noticeably thinner than other sections in ch04
6. ch15 sections 15-3 and 15-4 collapsed into callout box instead of full sections
7. ch16 section 16-1 (DNS lookup) collapsed into callout box instead of full section
8. 8 diagram files exist but are never referenced from draft.md files
9. No inter-chapter cross-references throughout the entire book
10. Session management lacks comprehensive coverage
11. Multiple chapter title mismatches between structure.md and draft.md (ch02, ch03, ch04, ch06, ch08)
12. ch01 and ch17 missing descriptive chapter titles in draft headings

### :green_circle: LOW (5 issues)

1. Chapters 01-11 and 17 lack chapter-level introductory paragraphs (inconsistent with ch12-16 style)
2. Minor chapter title differences between structure.md and drafts (ch05, ch07, ch09, ch10, ch11, ch12-16)
3. CORS only mentioned in ch17 TOP 10 but not covered in a dedicated section
4. Logging best practices scattered across ch13 and ch15 without unified treatment
5. OWASP reference in ch01 mentions OWASP but provides no URL
