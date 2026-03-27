<div align="center">

# KKTV

### 将 KISA 安全编码指南应用于您的代码

为使用 AI 构建网站的氛围编码者打造的安全编码技能

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../LICENSE)
[![KISA](https://img.shields.io/badge/Based_on-KISA_Secure_Coding_Guide_2023-003DAD)](https://www.kisa.or.kr)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-0078D6)](https://github.com/cdppcorp/KKTV)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-6B4FBB)](https://docs.anthropic.com/en/docs/claude-code)
[![CWE](https://img.shields.io/badge/47_Rules-CWE_Mapped-E34F26)](https://cwe.mitre.org)

</div>

---

## Languages / 语言

[한국어](../README.md) | [English](README.en.md) | [**简体中文**](README.zh-CN.md) | [日本語](README.ja.md) | [Русский](README.ru.md) | [Français](README.fr.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Tiếng Việt](README.vi.md) | [ไทย](README.th.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [Türkçe](README.tr.md)

---

## 您的代码真的安全吗？

您是否在没有任何审查的情况下直接部署 AI 生成的代码？

```python
# AI 生成的代码 ——  您知道这里面有多少个漏洞吗？
app.config['SECRET_KEY'] = 'super-secret-key-123'
query = f"SELECT * FROM users WHERE id = '{user_input}'"
app.run(debug=True)
```

上述代码包含 **3 个安全漏洞**：硬编码的密钥、SQL 注入和生产环境的调试模式。Cursor、Claude Code、Copilot 等 AI 工具生成的代码中，这些漏洞每天都在随代码一起部署。

**问题在于，大多数氛围编码者根本不知道这一点，任由这些漏洞存在。**

---

## 如果您在韩国提供服务，KISA 指南不是可选项

韩国互联网振兴院（KISA）发布了 **Python 安全编码指南（2023 年修订版）**，定义了 47 个安全弱点及其对策。如果您在韩国运营 Web 服务或参与公共部门项目，遵循这些指南 **几乎是法律义务**。

- **电子政务法第 45 条**：政府机关信息系统开发时必须应用软件开发安全
- **个人信息保护法**：处理个人信息时必须采取安全保障措施
- **信息通信网法**：信息通信服务提供者必须进行安全漏洞检查

> 即使您是外国开发者，如果您正在进入韩国市场或与韩国企业合作，也必须熟悉 KISA 指南。

---

## KKTV 为您解决这一切

KKTV 是一款将 KISA 安全编码指南的 47 条规则转化为 Claude Code 技能的插件。只需一条命令，即可审计您的项目是否符合指南要求，并自动修复漏洞。

### Before：放任与忽视

- 未经审查即部署 AI 生成的代码
- 甚至不知道安全指南的存在
- "以后再处理" —— 然后在事故发生后才手忙脚乱
- 团队没有安全专家，不知道从哪里开始

### After：应用 KKTV

- 一条 `/kktv.start` 命令即可检查全部 47 条规则
- 分类报告让您立即了解哪里存在漏洞
- `/kktv.fix` 自动修复发现的漏洞
- `/kktv.guide` 生成提示词，让 AI 从一开始就编写安全代码

---

## 快速开始

### 1. 安装

```bash
# 市场注册
/plugin marketplace add cdppcorp/KKTV

# 英文版
/plugin install kktv-en@kktv

# 韩文版
/plugin install kktv-ko@kktv
```

### 2. 开始安全审计

```bash
/kktv.start
```

首次运行时会出现环境问卷：
- 自动检测操作系统（Windows/Linux）
- 自动检测语言和框架
- 确认部署目标、数据库和认证方式
- Windows 环境下自动诊断插件钩子兼容性

### 3. 查看报告并修复

```
reports/security/
├── summary.md              ← 一目了然的摘要
├── cat1-input-validation.md ← 按类别详细报告
├── cat2-security-features.md
├── ...
└── cat7-api-misuse.md
```

发现漏洞时：

```bash
/kktv.fix      # 自动修复
/kktv.check    # 部署前最终检查
```

---

## Skills

| Skill | 命令 | 说明 |
|-------|------|------|
| Start | `/kktv.start` | 基于 KISA 47 条规则的安全审计 + 分类报告生成 |
| Fix | `/kktv.fix` | 以安全模式自动修复发现的漏洞 |
| Check | `/kktv.check` | 部署前 47 项交互式检查清单 |
| Guide | `/kktv.guide` | 为 AI 工具生成安全编码提示词 |

---

## KISA 47 条安全规则

KKTV 基于 KISA Python 安全编码指南（2023 年修订版）的 47 个安全弱点。所有规则均映射到国际标准 CWE（通用弱点枚举）。

| 类别 | 规则数 | 主要项目 |
|------|--------|----------|
| 输入数据验证及表示 | 18 | SQL 注入、XSS、CSRF、SSRF、代码注入、命令注入 |
| 安全功能 | 16 | 认证、授权、加密、硬编码密钥、密码策略 |
| 时间与状态 | 2 | TOCTOU 竞态条件、无限循环/递归 |
| 错误处理 | 3 | 错误信息泄露、缺少响应、不当异常处理 |
| 代码错误 | 3 | 空引用、资源释放、反序列化 |
| 封装 | 2 | 会话数据泄露、残留调试代码 |
| API 误用 | 3 | 基于 DNS 的安全决策、使用不安全的 API |

---

## 谁需要这个

| 对象 | 场景 |
|------|------|
| **氛围编码者** | 使用 AI 构建并部署网站，但从未进行过安全审查 |
| **初创企业开发者** | 需要快速上线，但没有专职安全人员 |
| **政府/SI 项目参与者** | 依据电子政务法必须应用安全编码的项目 |
| **外国开发者** | 进入韩国市场或与韩国企业合作，需要遵守 KISA 指南 |
| **自由职业者** | 需要向客户提交安全审查报告 |

---

## 手稿

`authorkit/manuscript/` 目录提供了 3 个版本的安全编码指南全文。涵盖 17 章、6 个 PART、47 个漏洞项目的完整手稿。

| 版本 | 文件 | 目标用户 |
|------|------|----------|
| Django/Flask | `시큐어코딩_가이드라인_Skills_Django.md` | Django、Flask 用户 |
| FastAPI | `시큐어코딩_가이드라인_Skills_FastAPI.md` | FastAPI、SQLAlchemy、Pydantic 用户 |
| Pseudocode | `시큐어코딩_가이드라인_Skills_Pseudocode.md` | 所有语言/框架用户 |

---

## 参考资料

- [KISA Python 安全编码指南（2023 年修订版）](https://www.kisa.or.kr)
- [CWE - 通用弱点枚举](https://cwe.mitre.org)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [电子政务法第 45 条](https://www.law.go.kr)

---

## 许可证

MIT
