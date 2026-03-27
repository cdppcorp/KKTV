# Review Summary: Cross-Reference & Coherence

**Date**: 2026-03-27
**Scope**: All 17 chapters (ch01-ch17)
**Detailed report**: `xref-coherence-review.md`

---

## Total Issue Counts by Severity

| Severity | Count |
|----------|-------|
| :red_circle: HIGH | 5 |
| :yellow_circle: MEDIUM | 12 |
| :green_circle: LOW | 5 |
| **Total** | **22** |

---

## Top 10 Most Critical Fixes Needed

### 1. :red_circle: ch01 PART description table is wrong (PART 3, 4, 5)

**Location**: `ch01/draft.md`, lines 222-229 (section 1-2, "가이드의 전체 구조" table)

**Problem**: The table describes PART 3 as "인증과 인가", PART 4 as "민감정보 보호", PART 5 as "배포와 설정". The actual content is completely different:
- PART 3 = "보안 기능을 제대로 구현하세요" (auth, encryption, passwords, certificates, info exposure)
- PART 4 = "안정적인 코드를 작성하세요" (time/state, error handling, code quality)
- PART 5 = "구조와 설계로 지키세요" (encapsulation, API misuse)

**Fix**: Update the table in ch01 to match structure.md and actual chapter content. Also update the "상황별 추천 경로" table on lines 270-276.

---

### 2. :red_circle: Missing section 6-3 (메모리 버퍼 오버플로우)

**Location**: `ch06/draft.md`

**Problem**: structure.md defines three sections for ch06: 6-1 (정수형 오버플로우), 6-2 (보안기능 결정에 사용되는 부적절한 입력값), 6-3 (메모리 버퍼 오버플로우). The draft only contains 6-1 and 6-2. Section 6-3 is entirely missing.

**Fix**: Either write section 6-3 content or update structure.md to remove it (with a note that Python's memory management makes buffer overflow less relevant, similar to how LDAP was handled in ch02).

---

### 3. :red_circle: Section title mismatch: ch03 section 3-4

**Location**: `ch03/draft.md` and `structure.md`

**Problem**: structure.md lists "3-4. 정규 표현식 삽입" but the draft contains "3-4. 포맷 스트링 삽입(Format String Injection)". These are entirely different vulnerabilities. "정규 표현식 삽입 (ReDoS)" is a legitimate security concern not covered anywhere in the book.

**Fix**: Either (a) rename structure.md to match the draft, or (b) replace draft content to cover regex injection, or (c) add a 3-5 section for the missing topic and update structure.md.

---

### 4. :red_circle: Missing promised content: HTTPS/TLS setup and security headers

**Location**: ch01 promises "배포와 설정" covering "서버 설정, HTTPS, 보안 헤더" in PART 5

**Problem**: No chapter provides a dedicated guide on HTTPS/TLS server configuration or HTTP security headers (HSTS, CSP, X-Frame-Options, etc.). These are only mentioned as checklist items in ch17. This leaves a significant content gap for readers who expected deployment security guidance.

**Fix**: Either (a) add a dedicated chapter or section covering HTTPS setup and security headers (could be added to PART 5 or as a new section in ch17), or (b) correct the ch01 table to not promise this content, or (c) expand ch17 deployment checklist items with full explanations.

---

### 5. :red_circle: ch01 situational reading guide table is misaligned

**Location**: `ch01/draft.md`, lines 270-276 (상황별 추천 경로 table)

**Problem**: The table says:
- "로그인 기능을 AI로 만들었다" -> "PART 3: 인증과 인가" (correct target but wrong PART description)
- "API 키를 코드에 넣었다" -> "PART 4: 민감정보 보호" (WRONG - hardcoded secrets are in ch08 which is PART 3, not PART 4)
- This table will misdirect readers.

**Fix**: Realign the table to match actual PART assignments from structure.md.

---

### 6. :yellow_circle: 8 diagram files exist but are never referenced

**Location**: `ch02/diagram.md`, `ch04/diagram.md`, `ch04/diagram-csrf.md`, `ch04/diagram-ssrf.md`, `ch07/diagram.md`, `ch08/diagram.md`, `ch09/diagram.md`, `ch17/diagram.md`

**Problem**: Diagrams were created but no draft.md file references them. Readers will never see these diagrams unless they are integrated into the text.

**Fix**: Add diagram references at appropriate points in each chapter's draft.md (e.g., "아래 다이어그램은 SQL 삽입 공격의 흐름을 보여줍니다").

---

### 7. :yellow_circle: No inter-chapter cross-references in entire book

**Problem**: Not a single chapter references another chapter. When ch04 discusses session theft via XSS, it doesn't point to ch11 for cookie security. When ch06 uses `@login_required`, it doesn't point to ch07 where this is explained.

**Fix**: Add cross-references using the standard format "N장 M절 참고" at key points where related content exists in other chapters. Priority locations:
- ch04 (4-1) XSS session theft -> "11장 11-1절 참고"
- ch04 (4-2) CSRF cookie -> "11장 11-1절 참고"
- ch06 (6-2) session/auth -> "7장 7-1절 참고"
- ch08 (8-3) hardcoded secrets -> "11장 11-2절 참고"
- ch11 (11-1) XSS/CSRF references -> "4장 4-1절, 4-2절 참고"

---

### 8. :yellow_circle: ch15 and ch16 have collapsed sections

**Problem**: structure.md defines:
- ch15: 15-1, 15-2, 15-3, 15-4 (4 full sections)
- ch16: 16-1, 16-2 (2 full sections)

But in the drafts:
- ch15 has only 15-1 and 15-2 as full sections; 15-3 and 15-4 are a brief callout box
- ch16 has only 16-2 as a full section; 16-1 is a brief callout box

**Fix**: Either expand collapsed topics into full sections to match structure.md, or update structure.md to reflect the actual section structure.

---

### 9. :yellow_circle: Prerequisite ordering: concepts used before explanation

**Problem**: Several chapters use concepts that are explained in later chapters:
- ch01 uses `bcrypt`, `.env`/`os.environ` (explained in ch08, ch09)
- ch04 uses session/cookie concepts (explained in ch11, ch15)
- ch06 uses `@login_required` (explained in ch07)

**Fix**: Add brief inline explanations or footnotes when using concepts ahead of their dedicated chapters. For example, in ch01: "bcrypt는 패스워드 해싱 라이브러리입니다 (자세한 내용은 9장 9-3절에서 다룹니다)."

---

### 10. :yellow_circle: Multiple chapter titles differ between structure.md and drafts

**Problem**: 6 chapters have notably different titles between structure.md and drafts:
- ch02: "데이터베이스를 지키는 법" vs "데이터베이스를 노리는 삽입 공격"
- ch03: "코드와 명령어 삽입 차단" vs "코드와 명령어를 노리는 삽입 공격"
- ch04: "웹 공격의 핵심 - XSS와 위조 공격" vs "웹 요청을 노리는 공격"
- ch06: "기타 입력값 취약점" vs "데이터 타입과 보안 결정을 노리는 공격"
- ch08: "암호화와 키 관리" vs "암호화, 제대로 하고 계십니까"
- ch01, ch17: missing descriptive chapter titles entirely

**Fix**: Align titles. Decide whether structure.md or drafts have the authoritative titles and update the other to match. The draft titles (using "~를 노리는 공격" pattern) are more engaging but should be consistent with the table of contents.

---

## Action Priority Matrix

| Priority | Actions | Estimated Effort |
|----------|---------|-----------------|
| Immediate | Fix ch01 PART description table (#1, #5) | 30 min |
| Immediate | Resolve ch03 section 3-4 title mismatch (#3) | Decision needed, then 1-4 hours |
| High | Write or formally omit ch06 section 6-3 (#2) | 1-4 hours |
| High | Address missing HTTPS/security headers content (#4) | 4-8 hours if writing new content |
| Medium | Add inter-chapter cross-references (#7) | 2-3 hours |
| Medium | Integrate diagram references (#6) | 1-2 hours |
| Medium | Expand or reconcile collapsed sections in ch15/ch16 (#8) | 2-4 hours |
| Medium | Add prerequisite context for forward-used concepts (#9) | 1-2 hours |
| Low | Align chapter titles (#10) | 1 hour |
| Low | Add chapter-level intro paragraphs to ch01-ch11 | 2-3 hours |
