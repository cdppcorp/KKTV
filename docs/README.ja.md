<div align="center">

# KKTV

### KISAセキュアコーディングガイドラインをあなたのコードに

AIでウェブサイトを構築するバイブコーダーのためのセキュアコーディングスキル

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../LICENSE)
[![KISA](https://img.shields.io/badge/Based_on-KISA_Secure_Coding_Guide_2023-003DAD)](https://www.kisa.or.kr)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-0078D6)](https://github.com/cdppcorp/KKTV)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-6B4FBB)](https://docs.anthropic.com/en/docs/claude-code)
[![CWE](https://img.shields.io/badge/47_Rules-CWE_Mapped-E34F26)](https://cwe.mitre.org)

</div>

---

## Languages / 言語

[한국어](../README.md) | [English](README.en.md) | [简体中文](README.zh-CN.md) | [**日本語**](README.ja.md) | [Русский](README.ru.md) | [Français](README.fr.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Tiếng Việt](README.vi.md) | [ไทย](README.th.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [Türkçe](README.tr.md)

---

## あなたのコード、本当に安全ですか？

AIが生成したコードをそのままデプロイしていませんか？

```python
# AI生成コード — この中に脆弱性がいくつあるかご存知ですか？
app.config['SECRET_KEY'] = 'super-secret-key-123'
query = f"SELECT * FROM users WHERE id = '{user_input}'"
app.run(debug=True)
```

上記のコードには **3つのセキュリティ脆弱性** があります。ハードコードされたシークレットキー、SQLインジェクション、本番環境でのデバッグモード。Cursor、Claude Code、Copilotなどの AIツールが生成したコードに、このような脆弱性が含まれたまま日々デプロイされています。

**問題は、ほとんどのバイブコーダーがこの事実を知らず、脆弱性を放置していることです。**

---

## 韓国でサービスを提供するなら、KISAガイドラインは任意ではありません

韓国インターネット振興院（KISA）は **Pythonセキュアコーディングガイド（2023年改訂版）** を通じて、47個のセキュリティ弱点とその対策を提示しています。韓国でWebサービスを運営したり、公共事業に参加する場合、このガイドラインに従うことは **法的義務に近い** ものです。

- **電子政府法第45条**: 行政機関等の情報システム開発時、ソフトウェア開発セキュリティの適用が義務
- **個人情報保護法**: 個人情報処理時の安全性確保措置が義務
- **情報通信網法**: 情報通信サービス提供者のセキュリティ脆弱性点検が義務

> 海外の開発者であっても、韓国市場に進出したり、韓国企業と協業する場合は、KISAガイドラインを熟知する必要があります。

---

## KKTVが解決します

KKTVは、KISAセキュアコーディングガイドの47個のルールをClaude Codeスキルにしたプラグインです。コマンド一つで、あなたのプロジェクトがガイドラインを遵守しているか検査し、脆弱性を自動的に修正します。

### Before: 放置と無防備

- AI生成コードをレビューなしでデプロイ
- セキュリティガイドラインの存在自体を知らない
- 「後でやろう」 → 事故発生後に慌てて対応
- セキュリティ専門家がいないので、何から始めればいいかわからない

### After: KKTV適用

- `/kktv.start` 一回で47個のルール全数検査
- カテゴリ別レポートで、どこが脆弱かを即座に把握
- `/kktv.fix` で発見された脆弱性を自動修正
- `/kktv.guide` でAIに最初から安全なコードを要求

---

## クイックスタート

### 1. インストール

```bash
# マーケットプレイス登録
/plugin marketplace add cdppcorp/KKTV

# 英語版
/plugin install kktv-en@kktv

# 韓国語版
/plugin install kktv-ko@kktv
```

### 2. セキュリティ監査開始

```bash
/kktv.start
```

初回実行時に環境アンケートが表示されます：
- OS自動検出（Windows/Linux）
- 言語・フレームワーク自動検出
- デプロイ先、DB、認証方式の確認
- Windows環境でのプラグインフック互換性自動診断

### 3. レポート確認と修正

```
reports/security/
├── summary.md              ← 一目でわかる要約
├── cat1-input-validation.md ← カテゴリ別詳細
├── cat2-security-features.md
├── ...
└── cat7-api-misuse.md
```

脆弱性が発見された場合：

```bash
/kktv.fix      # 自動修正
/kktv.check    # デプロイ前最終点検
```

---

## Skills

| Skill | コマンド | 説明 |
|-------|----------|------|
| Start | `/kktv.start` | KISA 47ルール基準のセキュリティ監査 + カテゴリ別レポート生成 |
| Fix | `/kktv.fix` | 発見された脆弱性を安全なパターンで自動修正 |
| Check | `/kktv.check` | デプロイ前47項目のインタラクティブチェックリスト |
| Guide | `/kktv.guide` | AIツールに安全なコードを書かせるプロンプト生成 |

---

## KISA 47セキュリティルール

KKTVはKISA Pythonセキュアコーディングガイド（2023年改訂版）の47個のセキュリティ弱点に基づいています。すべてのルールは国際標準CWE（Common Weakness Enumeration）にマッピングされています。

| カテゴリ | ルール数 | 主要項目 |
|----------|----------|----------|
| 入力データ検証及び表現 | 18 | SQLインジェクション、XSS、CSRF、SSRF、コードインジェクション、コマンドインジェクション |
| セキュリティ機能 | 16 | 認証、認可、暗号化、ハードコードされた秘密情報、パスワードポリシー |
| 時間及び状態 | 2 | TOCTOU競合状態、無限ループ/再帰 |
| エラー処理 | 3 | エラーメッセージ漏洩、対応不在、不適切な例外処理 |
| コードエラー | 3 | Null参照、リソース解放、デシリアライゼーション |
| カプセル化 | 2 | セッションデータ漏洩、デバッグコード残存 |
| API誤用 | 3 | DNSベースのセキュリティ判断、脆弱なAPI使用 |

---

## こんな方に必要です

| 対象 | 状況 |
|------|------|
| **バイブコーダー** | AIでウェブサイトを作ってデプロイしているが、セキュリティレビューを一度もしたことがない |
| **スタートアップ開発者** | 素早くサービスをリリースしたいが、専任のセキュリティ担当者がいない |
| **SI/公共事業参加者** | 電子政府法に基づきセキュアコーディング適用が義務のプロジェクト |
| **海外開発者** | 韓国市場に進出したり、韓国企業と協業し、KISAガイドラインを遵守する必要がある |
| **フリーランサー** | クライアントにセキュリティレビューレポートを提出する必要がある |

---

## マニュスクリプト

`authorkit/manuscript/` ディレクトリで3つのバージョンのセキュアコーディングガイド全文を提供しています。17章、6つのPART、47個の脆弱性項目を網羅する完成原稿です。

| バージョン | ファイル | 対象 |
|------------|----------|------|
| Django/Flask | `시큐어코딩_가이드라인_Skills_Django.md` | Django、Flaskユーザー |
| FastAPI | `시큐어코딩_가이드라인_Skills_FastAPI.md` | FastAPI、SQLAlchemy、Pydanticユーザー |
| Pseudocode | `시큐어코딩_가이드라인_Skills_Pseudocode.md` | すべての言語/フレームワークユーザー |

---

## 参考資料

- [KISA Pythonセキュアコーディングガイド（2023年改訂版）](https://www.kisa.or.kr)
- [CWE - Common Weakness Enumeration](https://cwe.mitre.org)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [電子政府法第45条](https://www.law.go.kr)

---

## ライセンス

MIT
