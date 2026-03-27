<div align="center">

# KKTV

### Terapkan Pedoman Secure Coding KISA pada Kode Anda

Skill secure coding untuk vibe coder yang membangun website dengan AI

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../LICENSE)
[![KISA](https://img.shields.io/badge/Based_on-KISA_Secure_Coding_Guide_2023-003DAD)](https://www.kisa.or.kr)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-0078D6)](https://github.com/cdppcorp/KKTV)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-6B4FBB)](https://docs.anthropic.com/en/docs/claude-code)
[![CWE](https://img.shields.io/badge/47_Rules-CWE_Mapped-E34F26)](https://cwe.mitre.org)

</div>

---

## Languages / Bahasa

[한국어](../README.md) | [English](README.en.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [Русский](README.ru.md) | [Français](README.fr.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Tiếng Việt](README.vi.md) | [ไทย](README.th.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [**Bahasa Indonesia**](README.id.md) | [Türkçe](README.tr.md)

---

## Apakah kode Anda benar-benar aman?

Apakah Anda men-deploy kode yang dihasilkan AI tanpa tinjauan apa pun?

```python
# Kode yang dihasilkan AI — tahukah Anda berapa banyak kerentanan di sini?
app.config['SECRET_KEY'] = 'super-secret-key-123'
query = f"SELECT * FROM users WHERE id = '{user_input}'"
app.run(debug=True)
```

Kode di atas mengandung **3 kerentanan keamanan**: secret key yang di-hardcode, SQL injection, dan mode debug di production. Kode yang dihasilkan oleh alat AI seperti Cursor, Claude Code, dan Copilot di-deploy setiap hari dengan kerentanan seperti ini.

**Masalahnya adalah sebagian besar vibe coder bahkan tidak mengetahui hal ini, dan membiarkan kerentanan tersebut tanpa penanganan.**

---

## Jika Anda beroperasi di Korea, pedoman KISA bukan pilihan

Korea Internet & Security Agency (KISA) telah menerbitkan **Panduan Secure Coding Python (Revisi 2023)**, yang mendefinisikan 47 kelemahan keamanan dan tindakan penanggulangannya. Jika Anda mengoperasikan layanan web di Korea atau berpartisipasi dalam proyek sektor publik, mengikuti pedoman ini **secara praktis merupakan kewajiban hukum**.

- **Undang-Undang Pemerintahan Elektronik, Pasal 45**: Penerapan wajib keamanan pengembangan perangkat lunak saat membangun sistem informasi untuk lembaga pemerintah
- **Undang-Undang Perlindungan Informasi Pribadi**: Tindakan keamanan wajib saat memproses informasi pribadi
- **Undang-Undang Jaringan Informasi dan Komunikasi**: Audit kerentanan keamanan wajib bagi penyedia layanan informasi dan komunikasi

> Bahkan jika Anda pengembang asing, jika Anda memasuki pasar Korea atau bekerja sama dengan perusahaan Korea, Anda harus memahami pedoman KISA.

---

## KKTV menyelesaikan masalah ini

KKTV adalah plugin yang mengubah 47 aturan dari panduan secure coding KISA menjadi skill Claude Code. Dengan satu perintah, ia mengaudit proyek Anda untuk kepatuhan terhadap pedoman dan secara otomatis memperbaiki kerentanan.

### Sebelum: Kelalaian dan paparan

- Men-deploy kode yang dihasilkan AI tanpa tinjauan apa pun
- Bahkan tidak tahu bahwa pedoman keamanan ada
- "Nanti saja" — lalu panik setelah terjadi insiden
- Tidak ada ahli keamanan di tim, tidak tahu harus mulai dari mana

### Sesudah: Dengan KKTV

- Satu perintah `/kktv.start` mengaudit semua 47 aturan
- Laporan berdasarkan kategori menunjukkan persis di mana kerentanan berada
- `/kktv.fix` secara otomatis memperbaiki kerentanan yang ditemukan
- `/kktv.guide` menghasilkan prompt agar AI menulis kode aman sejak awal

---

## Mulai Cepat

### 1. Instalasi

```bash
# Registrasi marketplace
/plugin marketplace add cdppcorp/KKTV

# Versi bahasa Inggris
/plugin install kktv-en@kktv

# Versi bahasa Korea
/plugin install kktv-ko@kktv
```

### 2. Mulai audit keamanan

```bash
/kktv.start
```

Pada eksekusi pertama, kuesioner lingkungan akan muncul:
- Deteksi OS otomatis (Windows/Linux)
- Deteksi bahasa dan framework otomatis
- Konfirmasi target deployment, database, dan metode autentikasi
- Diagnosis otomatis kompatibilitas hook plugin di Windows

### 3. Tinjau laporan dan perbaiki

```
reports/security/
├── summary.md              ← Ringkasan umum
├── cat1-input-validation.md ← Detail per kategori
├── cat2-security-features.md
├── ...
└── cat7-api-misuse.md
```

Ketika kerentanan ditemukan:

```bash
/kktv.fix      # Perbaikan otomatis
/kktv.check    # Pemeriksaan akhir sebelum deployment
```

---

## Skills

| Skill | Perintah | Deskripsi |
|-------|----------|-----------|
| Start | `/kktv.start` | Audit keamanan berdasarkan 47 aturan KISA + pembuatan laporan per kategori |
| Fix | `/kktv.fix` | Perbaikan otomatis kerentanan dengan pola aman |
| Check | `/kktv.check` | Daftar periksa interaktif 47 item sebelum deployment |
| Guide | `/kktv.guide` | Pembuatan prompt agar alat AI menulis kode aman |

---

## 47 Aturan Keamanan KISA

KKTV didasarkan pada 47 kelemahan keamanan dari Panduan Secure Coding Python KISA (Revisi 2023). Semua aturan dipetakan ke standar internasional CWE (Common Weakness Enumeration).

| Kategori | Jumlah Aturan | Item Utama |
|----------|---------------|------------|
| Validasi data input dan representasi | 18 | SQL injection, XSS, CSRF, SSRF, code injection, command injection |
| Fitur keamanan | 16 | Autentikasi, otorisasi, enkripsi, secret yang di-hardcode, kebijakan password |
| Waktu dan status | 2 | Kondisi balapan TOCTOU, loop tak terbatas/rekursi |
| Penanganan error | 3 | Paparan pesan error, tidak ada respons, penanganan exception yang tidak tepat |
| Error kode | 3 | Null dereference, pelepasan resource, deserialisasi |
| Enkapsulasi | 2 | Paparan data sesi, kode debug yang tersisa |
| Penyalahgunaan API | 3 | Keputusan keamanan berbasis DNS, penggunaan API yang rentan |

---

## Siapa yang membutuhkan ini

| Target | Situasi |
|--------|---------|
| **Vibe coder** | Membangun dan men-deploy website dengan AI, tetapi tidak pernah melakukan tinjauan keamanan |
| **Pengembang startup** | Perlu meluncurkan cepat, tetapi tidak memiliki personel keamanan khusus |
| **Peserta proyek pemerintah/SI** | Proyek di mana secure coding wajib berdasarkan Undang-Undang Pemerintahan Elektronik |
| **Pengembang asing** | Memasuki pasar Korea atau berkolaborasi dengan perusahaan Korea dan perlu mematuhi pedoman KISA |
| **Freelancer** | Perlu menyerahkan laporan audit keamanan kepada klien |

---

## Manuskrip

Direktori `authorkit/manuscript/` menyediakan panduan secure coding lengkap dalam 3 versi. Manuskrip lengkap yang mencakup 17 bab, 6 PART, dan 47 jenis kerentanan.

| Versi | File | Target |
|-------|------|--------|
| Django/Flask | `시큐어코딩_가이드라인_Skills_Django.md` | Pengguna Django, Flask |
| FastAPI | `시큐어코딩_가이드라인_Skills_FastAPI.md` | Pengguna FastAPI, SQLAlchemy, Pydantic |
| Pseudocode | `시큐어코딩_가이드라인_Skills_Pseudocode.md` | Pengguna semua bahasa/framework |

---

## Referensi

- [KISA Panduan Secure Coding Python (Revisi 2023)](https://www.kisa.or.kr)
- [CWE - Common Weakness Enumeration](https://cwe.mitre.org)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Undang-Undang Pemerintahan Elektronik, Pasal 45](https://www.law.go.kr)

---

## Lisensi

MIT
