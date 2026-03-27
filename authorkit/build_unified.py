#!/usr/bin/env python3
"""Build unified pseudocode book document."""
import os

base = 'C:/Users/Nowzero/PycharmProjects/Skills/KKTV/authorkit'

# Read all part files
parts = {}
for i, name in enumerate([
    'drafts-pseudocode/part1-시작하기.md',
    'drafts-pseudocode/part2-입력데이터검증.md',
    'drafts-pseudocode/part3-보안기능.md',
    'drafts-pseudocode/part4-안정적코드.md',
    'drafts-pseudocode/part5-구조설계.md',
    'drafts-pseudocode/part6-체크리스트.md',
], 1):
    with open(os.path.join(base, name), 'r', encoding='utf-8') as f:
        parts[i] = f.read()

# Read diagram files
diagrams = {}
diagram_files = {
    'sql': 'drafts/part2-입력데이터검증/ch02/diagram.md',
    'xss': 'drafts/part2-입력데이터검증/ch04/diagram.md',
    'csrf': 'drafts/part2-입력데이터검증/ch04/diagram-csrf.md',
    'ssrf': 'drafts/part2-입력데이터검증/ch04/diagram-ssrf.md',
    'auth': 'drafts/part3-보안기능/ch07/diagram.md',
    'crypto': 'drafts/part3-보안기능/ch08/diagram.md',
    'password': 'drafts/part3-보안기능/ch09/diagram.md',
    'checklist': 'drafts/part6-체크리스트/ch17/diagram.md',
}
for key, path in diagram_files.items():
    with open(os.path.join(base, path), 'r', encoding='utf-8') as f:
        diagrams[key] = f.read()

# Insert diagrams into parts
# Part 2: SQL injection diagram
p2 = parts[2]
marker = '## 2-2. LDAP 삽입'
insert = '\n\n> **[참고 다이어그램] SQL 삽입 공격 흐름도**\n\n' + diagrams['sql'] + '\n\n---\n\n'
p2 = p2.replace(marker, insert + marker)

# XSS diagram
marker = '## 4-2. 크로스사이트 요청 위조'
insert = '\n\n> **[참고 다이어그램] XSS 3가지 유형 비교도**\n\n' + diagrams['xss'] + '\n\n---\n\n'
p2 = p2.replace(marker, insert + marker)

# CSRF diagram
marker = '## 4-3. 서버사이드 요청 위조'
insert = '\n\n> **[참고 다이어그램] CSRF 공격 시퀀스**\n\n' + diagrams['csrf'] + '\n\n---\n\n'
p2 = p2.replace(marker, insert + marker)

# SSRF diagram
marker = '## 4-4. HTTP 응답 분할'
insert = '\n\n> **[참고 다이어그램] SSRF 공격 흐름도**\n\n' + diagrams['ssrf'] + '\n\n---\n\n'
p2 = p2.replace(marker, insert + marker)

parts[2] = p2

# Part 3: Auth diagram
p3 = parts[3]
marker = '### 7-2. 부적절한 인가'
insert = '\n\n> **[참고 다이어그램] 인증 vs 인가 비교도**\n\n' + diagrams['auth'] + '\n\n---\n\n'
p3 = p3.replace(marker, insert + marker)

# Crypto diagram
marker = '### 8-2. 암호화되지 않은 중요정보'
insert = '\n\n> **[참고 다이어그램] 암호화 알고리즘 안전/위험 분류표**\n\n' + diagrams['crypto'] + '\n\n---\n\n'
p3 = p3.replace(marker, insert + marker)

# Password diagram
marker = '### 9-4. 반복된 인증시도 제한 기능 부재'
insert = '\n\n> **[참고 다이어그램] 패스워드 해싱 흐름도**\n\n' + diagrams['password'] + '\n\n---\n\n'
p3 = p3.replace(marker, insert + marker)

parts[3] = p3

# Part 6: Checklist flowchart
p6 = parts[6]
marker = '## 17-1. 배포 전 보안 체크리스트'
insert_checklist = marker + '\n\n> **[참고 다이어그램] 바이브 코딩 배포 전 보안 체크 플로우차트**\n\n' + diagrams['checklist'] + '\n'
p6 = p6.replace(marker, insert_checklist, 1)
parts[6] = p6

# Build TOC
toc = """# 목차

## PART 1: 시작하기
- **Chapter 1**
  - 1-1. AI가 만든 코드도 취약할 수 있습니다
  - 1-2. 이 가이드의 활용법

## PART 2: 입력값을 믿지 마세요
- **Chapter 2. 데이터베이스를 노리는 삽입 공격**
  - 2-1. SQL 삽입(SQL Injection)
  - 2-2. LDAP 삽입(LDAP Injection)
- **Chapter 3. 코드와 명령어를 노리는 삽입 공격**
  - 3-1. 코드 삽입(Code Injection)
  - 3-2. 운영체제 명령어 삽입(OS Command Injection)
  - 3-3. XML 삽입(XML Injection)
  - 3-4. 포맷 스트링 삽입(Format String Injection)
- **Chapter 4. 웹 요청을 노리는 공격**
  - 4-1. 크로스사이트 스크립트(XSS)
  - 4-2. 크로스사이트 요청 위조(CSRF)
  - 4-3. 서버사이드 요청 위조(SSRF)
  - 4-4. HTTP 응답 분할(HTTP Response Splitting)
- **Chapter 5. 파일과 URL을 노리는 공격**
  - 5-1. 경로 조작 및 자원 삽입(Path Traversal)
  - 5-2. 위험한 형식 파일 업로드(Unrestricted File Upload)
  - 5-3. 신뢰되지 않는 URL 자동 연결(Open Redirect)
  - 5-4. 부적절한 XML 외부 개체 참조(XXE)
- **Chapter 6. 데이터 타입과 보안 결정을 노리는 공격**
  - 6-1. 정수형 오버플로우(Integer Overflow)
  - 6-2. 보안기능 결정에 사용되는 부적절한 입력값
  - 6-3. 메모리 버퍼 오버플로우(Buffer Overflow)

## PART 3: 보안 기능을 제대로 구현하세요
- **Chapter 7. 인증과 인가, 그리고 권한 설정**
  - 7-1. 적절한 인증 없이 중요 기능 허용
  - 7-2. 부적절한 인가
  - 7-3. 중요한 자원에 대한 잘못된 권한 설정
- **Chapter 8. 암호화, 제대로 하고 계십니까**
  - 8-1. 취약한 암호화 알고리즘 사용
  - 8-2. 암호화되지 않은 중요정보
  - 8-3. 하드코딩된 중요정보
  - 8-4. 충분하지 않은 키 길이
- **Chapter 9. 난수, 패스워드, 그리고 인증 방어**
  - 9-1. 적절하지 않은 난수 값 사용
  - 9-2. 취약한 패스워드 허용
  - 9-3. 솔트 없는 일방향 해시 함수 사용
  - 9-4. 반복된 인증시도 제한 기능 부재
- **Chapter 10. 서명, 인증서, 무결성 검증**
  - 10-1. 부적절한 전자서명 확인
  - 10-2. 부적절한 인증서 유효성 검증
  - 10-3. 무결성 검사 없는 코드 다운로드
- **Chapter 11. 정보 노출을 차단하세요**
  - 11-1. 쿠키를 통한 정보 노출
  - 11-2. 주석문 안에 포함된 시스템 주요정보

## PART 4: 안정적인 코드를 작성하세요
- **Chapter 12. 시간 및 상태 -- 타이밍이 만드는 버그**
  - 12-1. 경쟁 조건: 검사 시점과 사용 시점(TOCTOU)
  - 12-2. 종료되지 않는 반복문 또는 재귀 함수
- **Chapter 13. 에러 처리 -- 오류가 보안 구멍이 되는 순간**
  - 13-1. 오류 메시지 정보 노출
  - 13-2. 오류 상황 대응 부재
  - 13-3. 부적절한 예외 처리
- **Chapter 14. 코드 오류 -- 개발자가 놓치기 쉬운 함정들**
  - 14-1. Null 역참조
  - 14-2. 부적절한 자원 해제
  - 14-3. 신뢰할 수 없는 데이터의 역직렬화

## PART 5: 구조와 설계로 지키세요
- **Chapter 15. 캡슐화 -- 보여서는 안 되는 것들**
  - 15-1. 잘못된 세션에 의한 데이터 정보 노출
  - 15-2. 제거되지 않고 남은 디버그 코드
- **Chapter 16. API 오용 -- 편리함 뒤에 숨은 위험**
  - 16-1. 취약한 API 사용

## PART 6: 바이브 코딩 보안 체크리스트
- **Chapter 17**
  - 17-1. 배포 전 보안 체크리스트
  - 17-2. AI에게 보안 검토 요청하는 프롬프트 예시
  - 17-3. 자주 발생하는 바이브 코딩 보안 실수 TOP 10
"""

# Build final document
header = """# 시큐어코딩 가이드라인 Skills
## 수도 코드(Pseudocode) 버전

> 바이브 코딩을 하는 모든 사람을 위한 보안 가이드
> 언어와 프레임워크에 구애받지 않는 보편적 보안 원칙
> ❌ 취약한 수도 코드 → ✅ 안전한 수도 코드 → 💬 AI에게 요청할 프롬프트

---

"""

doc = header + toc + '\n---\n\n'

for i in range(1, 7):
    doc += parts[i]
    if i < 6:
        doc += '\n\n---\n\n'

doc = doc.rstrip() + '\n'

output_path = os.path.join(base, 'manuscript', '시큐어코딩_가이드라인_Skills_Pseudocode.md')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(doc)

print(f'Written {len(doc)} characters to {output_path}')
print(f'Line count: {doc.count(chr(10))}')
