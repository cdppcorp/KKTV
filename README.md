<div align="center">

# KKTV

### KISA 시큐어코딩 가이드라인을 당신의 코드에

AI로 웹사이트를 만드는 바이브 코더를 위한 시큐어코딩 스킬

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![KISA](https://img.shields.io/badge/Based_on-KISA_Secure_Coding_Guide_2023-003DAD)](https://www.kisa.or.kr)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-0078D6)](https://github.com/cdppcorp/KKTV)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-6B4FBB)](https://docs.anthropic.com/en/docs/claude-code)
[![CWE](https://img.shields.io/badge/47_Rules-CWE_Mapped-E34F26)](https://cwe.mitre.org)

</div>

---

## Languages / 언어

[**한국어**](README.md) | [English](docs/README.en.md) | [简体中文](docs/README.zh-CN.md) | [日本語](docs/README.ja.md) | [Русский](docs/README.ru.md) | [Français](docs/README.fr.md) | [Español](docs/README.es.md) | [Deutsch](docs/README.de.md) | [Português](docs/README.pt.md) | [Tiếng Việt](docs/README.vi.md) | [ไทย](docs/README.th.md) | [العربية](docs/README.ar.md) | [हिन्दी](docs/README.hi.md) | [Bahasa Indonesia](docs/README.id.md) | [Türkçe](docs/README.tr.md)

---

## 당신의 코드, 정말 안전합니까?

AI가 만들어준 코드를 그대로 배포하고 있지 않습니까?

```python
# AI가 생성한 코드 — 이 안에 취약점이 몇 개인지 아십니까?
app.config['SECRET_KEY'] = 'super-secret-key-123'
query = f"SELECT * FROM users WHERE id = '{user_input}'"
app.run(debug=True)
```

위 코드에는 **3가지 보안 취약점**이 있습니다. 하드코딩된 시크릿 키, SQL 삽입, 디버그 모드 배포. Cursor, Claude Code, Copilot 등 AI 도구가 생성한 코드에 이런 취약점이 그대로 포함되어 배포되고 있습니다.

**문제는 대부분의 바이브 코더가 이 사실을 모른 채 방치하고 있다는 것입니다.**

---

## 한국에서 서비스한다면, KISA 가이드라인은 선택이 아닙니다

한국인터넷진흥원(KISA)은 **Python 시큐어코딩 가이드(2023년 개정본)**를 통해 47개 보안 약점과 대응 방안을 제시하고 있습니다. 대한민국에서 웹 서비스를 운영하거나 공공 사업에 참여한다면, 이 가이드라인을 따르는 것은 **법적 의무에 가깝습니다**.

- **전자정부법 제45조**: 행정기관 등 정보시스템 개발 시 소프트웨어 개발보안 적용 의무
- **개인정보보호법**: 개인정보 처리 시 안전성 확보 조치 의무
- **정보통신망법**: 정보통신서비스 제공자의 보안 취약점 점검 의무

> 해외 개발자라도 한국 시장에 진출하거나, 한국 기업과 협업한다면 KISA 가이드라인을 숙지해야 합니다.

---

## KKTV가 해결합니다

KKTV는 KISA 시큐어코딩 가이드의 47개 규칙을 Claude Code 스킬로 만든 플러그인입니다. 명령어 하나로 당신의 프로젝트가 가이드라인을 준수하는지 검사하고, 취약점을 자동으로 수정합니다.

### Before: 방치와 방임

- AI가 생성한 코드를 검토 없이 배포
- 보안 가이드라인의 존재 자체를 모름
- "나중에 해야지" → 사고 발생 후 뒤늦은 대응
- 보안 전문가가 없으니 무엇부터 해야 할지 모름

### After: KKTV 적용

- `/kktv.start` 한 번으로 47개 규칙 전수 검사
- 카테고리별 보고서로 어디가 취약한지 즉시 파악
- `/kktv.fix`로 발견된 취약점 자동 수정
- `/kktv.guide`로 AI에게 처음부터 안전한 코드를 요청

---

## 빠른 시작

### 1. 설치

```bash
# 마켓플레이스 등록
/plugin marketplace add cdppcorp/KKTV

# 한국어 버전
/plugin install kktv-ko@kktv

# English version
/plugin install kktv-en@kktv
```

### 2. 보안 감사 시작

```bash
/kktv.start
```

처음 실행하면 환경 질문지가 나타납니다:
- OS 자동 감지 (Windows/Linux)
- 언어, 프레임워크 자동 감지
- 배포 대상, DB, 인증 방식 확인
- Windows 환경에서는 플러그인 훅 호환성 자동 진단

### 3. 보고서 확인 및 수정

```
reports/security/
├── summary.md          ← 한눈에 보는 요약
├── cat1-입력검증.md     ← 카테고리별 상세
├── cat2-보안기능.md
├── ...
└── cat7-API오용.md
```

취약점이 발견되면:

```bash
/kktv.fix      # 자동 수정
/kktv.check    # 배포 전 최종 점검
```

---

## Skills

| Skill | 명령어 | 설명 |
|-------|--------|------|
| Start | `/kktv.start` | KISA 47개 규칙 기반 보안 감사 + 카테고리별 보고서 생성 |
| Fix | `/kktv.fix` | 발견된 취약점을 안전한 패턴으로 자동 수정 |
| Check | `/kktv.check` | 배포 전 47개 항목 대화형 체크리스트 |
| Guide | `/kktv.guide` | AI 도구에게 안전한 코드를 요청하는 프롬프트 생성 |

---

## KISA 47개 보안 규칙

KKTV는 KISA Python 시큐어코딩 가이드(2023년 개정본)의 47개 보안 약점을 기반으로 합니다. 모든 규칙은 국제 표준 CWE(Common Weakness Enumeration)에 매핑되어 있습니다.

| 카테고리 | 규칙 수 | 주요 항목 |
|----------|---------|----------|
| 입력데이터 검증 및 표현 | 18 | SQL 삽입, XSS, CSRF, SSRF, 코드 삽입, 명령어 삽입 |
| 보안기능 | 16 | 인증, 인가, 암호화, 하드코딩 비밀정보, 패스워드 정책 |
| 시간 및 상태 | 2 | TOCTOU 경쟁조건, 무한 반복/재귀 |
| 에러처리 | 3 | 오류 메시지 노출, 대응 부재, 부적절한 예외 처리 |
| 코드오류 | 3 | Null 역참조, 자원 해제, 역직렬화 |
| 캡슐화 | 2 | 세션 데이터 노출, 디버그 코드 잔존 |
| API 오용 | 3 | DNS 보안결정, 취약 API 사용 |

---

## 이런 분들에게 필요합니다

| 대상 | 상황 |
|------|------|
| **바이브 코더** | AI로 웹사이트를 만들어 배포하지만, 보안 검토를 한 번도 하지 않은 경우 |
| **스타트업 개발자** | 빠르게 서비스를 출시해야 하지만, 전담 보안 인력이 없는 경우 |
| **SI/공공 사업 참여자** | 전자정부법에 따라 시큐어코딩 적용이 의무인 프로젝트 |
| **해외 개발자** | 한국 시장에 진출하거나 한국 기업과 협업하며 KISA 가이드라인을 준수해야 하는 경우 |
| **프리랜서** | 클라이언트에게 보안 검토 보고서를 제출해야 하는 경우 |

---

## 매뉴스크립트

`authorkit/manuscript/` 디렉토리에서 3가지 버전의 시큐어코딩 가이드 전문을 제공합니다. 17장, 6개 PART, 47개 취약점 항목을 다루는 완성된 원고입니다.

| 버전 | 파일 | 대상 |
|------|------|------|
| Django/Flask | `시큐어코딩_가이드라인_Skills_Django.md` | Django, Flask 사용자 |
| FastAPI | `시큐어코딩_가이드라인_Skills_FastAPI.md` | FastAPI, SQLAlchemy, Pydantic 사용자 |
| Pseudocode | `시큐어코딩_가이드라인_Skills_Pseudocode.md` | 모든 언어/프레임워크 사용자 |

---

## Built with authorkit

이 프로젝트의 17장 분량 시큐어코딩 가이드라인 원고는 [authorkit](https://github.com/nowzero1702/authorkit) 플러그인으로 제작되었습니다. authorkit은 Claude Code 기반의 책 집필 워크플로우 스킬입니다.

| 단계 | authorkit 스킬 | 이 프로젝트에서의 활용 |
|------|---------------|---------------------|
| 프로젝트 설정 | `/authorkit.init` | constitution(문체 규칙), glossary(용어 사전), structure(목차) 자동 생성 |
| 레퍼런스 분석 | `/authorkit.analyze` | KISA PDF 176페이지 구조/용어/CWE 추출 |
| 마크다운 변환 | `/authorkit.juice` | PDF를 깨끗한 마크다운으로 변환 (토큰 절약) |
| 대조 분석 | `/authorkit.compare` | 레퍼런스 ↔ 목차 대조, 채택/생략/독창 분류 |
| 초안 작성 | `/authorkit.draft` | 17장 x 3버전(Django, FastAPI, Pseudocode) 초안 |
| 도해 생성 | `/authorkit.diagram` | SQL 삽입 흐름도, XSS 비교도 등 8개 텍스트 블록도 |
| 검증 | `/authorkit.review` | 문체/용어/상호참조/개연성 4영역 66건 검토 |
| 구조 재배치 | `/authorkit.restructure` | 장 순서 최적화 |

레퍼런스 PDF 한 권에서 3개 프레임워크 버전의 완성된 원고까지, 전 과정을 authorkit 워크플로우로 체계화했습니다.

```bash
# authorkit 설치
/plugin marketplace add nowzero1702/authorkit
/plugin install authorkit-ko@authorkit
```

---

## 참고 자료

- [KISA Python 시큐어코딩 가이드(2023년 개정본)](https://www.kisa.or.kr)
- [CWE - Common Weakness Enumeration](https://cwe.mitre.org)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [전자정부법 제45조](https://www.law.go.kr)

---

## 라이선스

MIT
