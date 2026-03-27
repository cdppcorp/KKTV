<div align="center">

# KKTV

### KISA Guvenli Kodlama Yonergelerini Kodunuza Uygulayin

AI ile web sitesi olusturan vibe coder'lar icin guvenli kodlama becerisi

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../LICENSE)
[![KISA](https://img.shields.io/badge/Based_on-KISA_Secure_Coding_Guide_2023-003DAD)](https://www.kisa.or.kr)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-0078D6)](https://github.com/cdppcorp/KKTV)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-6B4FBB)](https://docs.anthropic.com/en/docs/claude-code)
[![CWE](https://img.shields.io/badge/47_Rules-CWE_Mapped-E34F26)](https://cwe.mitre.org)

</div>

---

## Languages / Diller

[한국어](../README.md) | [English](README.en.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [Русский](README.ru.md) | [Français](README.fr.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Tiếng Việt](README.vi.md) | [ไทย](README.th.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [**Türkçe**](README.tr.md)

---

## Kodunuz gercekten guvenli mi?

AI tarafindan olusturulan kodu hicbir inceleme yapmadan deploy ediyor musunuz?

```python
# AI tarafindan olusturulan kod — burada kac guvenlik acigi oldugunu biliyor musunuz?
app.config['SECRET_KEY'] = 'super-secret-key-123'
query = f"SELECT * FROM users WHERE id = '{user_input}'"
app.run(debug=True)
```

Yukaridaki kod **3 guvenlik acigi** icerir: sabit kodlanmis gizli anahtar, SQL injection ve uretim ortaminda debug modu. Cursor, Claude Code ve Copilot gibi AI araclari tarafindan olusturulan kod, her gun bu tur aciklar ile deploy edilmektedir.

**Sorun su ki, vibe coder'larin cogu bunu bilmiyor bile ve bu aciklari ele almadan birakiyor.**

---

## Kore'de hizmet veriyorsaniz, KISA yonergeleri istege bagli degildir

Kore Internet ve Guvenlik Ajansi (KISA), 47 guvenlik zayifligini ve bunlarin onlemlerini tanimlayan **Python Guvenli Kodlama Kilavuzu'nu (2023 Revizyonu)** yayimlamistir. Kore'de bir web hizmeti isletiyorsaniz veya kamu sektoru projelerine katiliyorsaniz, bu yonergelere uymak **pratik olarak yasal bir zorunluluktur**.

- **Elektronik Devlet Kanunu, Madde 45**: Devlet kurumlari icin bilgi sistemleri gelistirirken yazilim gelistirme guvenliginin zorunlu uygulanmasi
- **Kisisel Bilgi Koruma Kanunu**: Kisisel bilgilerin islenmesinde zorunlu guvenlik onlemleri
- **Bilgi ve Iletisim Agi Kanunu**: Bilgi ve iletisim hizmeti saglayicilari icin zorunlu guvenlik acigi denetimleri

> Yabanci bir gelistirici olsaniz bile, Kore pazarina giriyorsaniz veya Koreli sirketlerle calisiyorsaniz, KISA yonergelerini bilmeniz gerekir.

---

## KKTV bu sorunu cozer

KKTV, KISA Guvenli Kodlama Kilavuzu'ndaki 47 kurali Claude Code becerilerine donusturen bir eklentidir. Tek bir komutla projenizi yonerge uyumlulugu acisindan denetler ve guvenlik aciklarini otomatik olarak duzeltir.

### Once: Ihmal ve acik kalma

- AI tarafindan olusturulan kodu hicbir inceleme yapmadan deploy etmek
- Guvenlik yonergelerinin var oldugunu bile bilmemek
- "Sonra hallederim" — ardindan bir olay sonrasi panik
- Ekipte guvenlik uzmani yok, nereden baslayacagini bilmemek

### Sonra: KKTV ile

- Tek bir `/kktv.start` komutu tum 47 kurali denetler
- Kategorilere gore raporlar tam olarak nerede acik oldugunu gosterir
- `/kktv.fix` kesfedilen guvenlik aciklarini otomatik olarak duzeltir
- `/kktv.guide` AI'nin basindan itibaren guvenli kod yazmasini saglayan promptlar olusturur

---

## Hizli Baslangic

### 1. Kurulum

```bash
# Marketplace kaydı
/plugin marketplace add cdppcorp/KKTV

# Ingilizce versiyon
/plugin install kktv-en@kktv

# Korece versiyon
/plugin install kktv-ko@kktv
```

### 2. Guvenlik denetimini baslatin

```bash
/kktv.start
```

Ilk calistirmada ortam anketi gorunur:
- Otomatik isletim sistemi algilama (Windows/Linux)
- Otomatik dil ve framework algilama
- Dagitim hedefi, veritabani ve kimlik dogrulama yontemi onaylama
- Windows'ta eklenti hook uyumlulugu otomatik tanilama

### 3. Raporlari inceleyin ve duzeltin

```
reports/security/
├── summary.md              ← Genel ozet
├── cat1-input-validation.md ← Kategoriye gore detay
├── cat2-security-features.md
├── ...
└── cat7-api-misuse.md
```

Guvenlik aciklari bulundugunda:

```bash
/kktv.fix      # Otomatik duzeltme
/kktv.check    # Deploy oncesi son kontrol
```

---

## Skills

| Skill | Komut | Aciklama |
|-------|-------|----------|
| Start | `/kktv.start` | KISA 47 kuralina dayali guvenlik denetimi + kategoriye gore rapor olusturma |
| Fix | `/kktv.fix` | Guvenli kaliplarla guvenlik aciklarinin otomatik duzeltilmesi |
| Check | `/kktv.check` | Deploy oncesi 47 maddelik etkilesimli kontrol listesi |
| Guide | `/kktv.guide` | AI araclarinin guvenli kod yazmasini saglayan prompt olusturma |

---

## KISA 47 Guvenlik Kurali

KKTV, KISA Python Guvenli Kodlama Kilavuzu'ndaki (2023 Revizyonu) 47 guvenlik zayifligina dayanmaktadir. Tum kurallar uluslararasi standart CWE (Common Weakness Enumeration) ile eslestirilmistir.

| Kategori | Kural Sayisi | Temel Maddeler |
|----------|--------------|----------------|
| Giris verisi dogrulama ve temsil | 18 | SQL injection, XSS, CSRF, SSRF, kod injection, komut injection |
| Guvenlik ozellikleri | 16 | Kimlik dogrulama, yetkilendirme, sifreleme, sabit kodlanmis gizli bilgiler, parola politikasi |
| Zaman ve durum | 2 | TOCTOU yaris durumu, sonsuz dongu/ozyineleme |
| Hata yonetimi | 3 | Hata mesaji ifsa, yanit eksikligi, uygunsuz istisna isleme |
| Kod hatalari | 3 | Null referans, kaynak serbest birakma, seri durumdan cikarma |
| Kapsulleme | 2 | Oturum verisi ifsa, kalan debug kodu |
| API kotuye kullanimi | 3 | DNS tabanli guvenlik kararlari, savunmasiz API kullanimi |

---

## Buna kimin ihtiyaci var

| Hedef Kitle | Durum |
|-------------|-------|
| **Vibe coder'lar** | AI ile web sitesi olusturup deploy ediyorlar ama hic guvenlik incelemesi yapmamis |
| **Startup gelistiriciler** | Hizli cikmak gerekiyor ama ozel guvenlik personeli yok |
| **Devlet/SI proje katilimcilari** | Elektronik Devlet Kanunu geregi guvenli kodlamanin zorunlu oldugu projeler |
| **Yabanci gelistiriciler** | Kore pazarina giren veya Koreli sirketlerle is birligi yapan ve KISA yonergelerine uymasi gereken gelistiriciler |
| **Serbest calisan gelistiriciler** | Musterilere guvenlik denetim raporlari sunmasi gerekenler |

---

## El Yazmasi

`authorkit/manuscript/` dizini, 3 versiyonda tam guvenli kodlama kilavuzu saglar. 17 bolum, 6 PART ve 47 guvenlik acigi turunu kapsayan eksiksiz bir el yazmasi.

| Versiyon | Dosya | Hedef Kitle |
|----------|-------|-------------|
| Django/Flask | `시큐어코딩_가이드라인_Skills_Django.md` | Django, Flask kullanicilari |
| FastAPI | `시큐어코딩_가이드라인_Skills_FastAPI.md` | FastAPI, SQLAlchemy, Pydantic kullanicilari |
| Pseudocode | `시큐어코딩_가이드라인_Skills_Pseudocode.md` | Tum dil/framework kullanicilari |

---

## Kaynaklar

- [KISA Python Guvenli Kodlama Kilavuzu (2023 Revizyonu)](https://www.kisa.or.kr)
- [CWE - Common Weakness Enumeration](https://cwe.mitre.org)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Elektronik Devlet Kanunu, Madde 45](https://www.law.go.kr)

---

## Lisans

MIT
