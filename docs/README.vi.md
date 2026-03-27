<div align="center">

# KKTV

### Ap dung Huong dan Lap trinh An toan KISA vao ma nguon cua ban

Ky nang lap trinh an toan danh cho vibe coder xay dung website bang AI

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../LICENSE)
[![KISA](https://img.shields.io/badge/Based_on-KISA_Secure_Coding_Guide_2023-003DAD)](https://www.kisa.or.kr)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-0078D6)](https://github.com/cdppcorp/KKTV)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-6B4FBB)](https://docs.anthropic.com/en/docs/claude-code)
[![CWE](https://img.shields.io/badge/47_Rules-CWE_Mapped-E34F26)](https://cwe.mitre.org)

</div>

---

## Languages / Ngon ngu

[한국어](../README.md) | [English](README.en.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [Русский](README.ru.md) | [Français](README.fr.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [**Tiếng Việt**](README.vi.md) | [ไทย](README.th.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [Türkçe](README.tr.md)

---

## Ma nguon cua ban co thuc su an toan khong?

Ban co dang trien khai ma nguon do AI tao ra ma khong kiem tra gi khong?

```python
# Ma nguon do AI tao — ban co biet co bao nhieu lo hong bao mat trong nay khong?
app.config['SECRET_KEY'] = 'super-secret-key-123'
query = f"SELECT * FROM users WHERE id = '{user_input}'"
app.run(debug=True)
```

Doan ma tren chua **3 lo hong bao mat**: khoa bi mat duoc ma hoa cung (hardcoded), SQL injection va che do debug trong moi truong production. Ma nguon duoc tao boi cac cong cu AI nhu Cursor, Claude Code va Copilot hang ngay duoc trien khai voi nhung lo hong nhu vay.

**Van de la hau het cac vibe coder khong he biet dieu nay va de mac nhung lo hong do.**

---

## Neu ban phuc vu tai Han Quoc, huong dan KISA khong phai la tuy chon

Co quan Internet va An ninh Han Quoc (KISA) da xuat ban **Huong dan Lap trinh An toan Python (ban sua doi 2023)**, dinh nghia 47 diem yeu bao mat va cac bien phap doi pho. Neu ban van hanh dich vu web tai Han Quoc hoac tham gia cac du an khu vuc cong, viec tuan thu cac huong dan nay **gan nhu la nghia vu phap ly**.

- **Luat Chinh phu Dien tu, Dieu 45**: Bat buoc ap dung bao mat phat trien phan mem khi xay dung he thong thong tin cho cac co quan chinh phu
- **Luat Bao ve Thong tin Ca nhan**: Bat buoc thuc hien cac bien phap an toan khi xu ly thong tin ca nhan
- **Luat Mang Thong tin va Truyen thong**: Bat buoc kiem tra lo hong bao mat doi voi nha cung cap dich vu thong tin va truyen thong

> Ngay ca khi ban la nha phat trien nuoc ngoai, neu ban dang tham nhap thi truong Han Quoc hoac lam viec voi cac cong ty Han Quoc, ban phai nam ro huong dan KISA.

---

## KKTV giai quyet van de nay

KKTV la mot plugin chuyen doi 47 quy tac tu huong dan lap trinh an toan KISA thanh cac ky nang Claude Code. Chi voi mot lenh, no kiem tra du an cua ban ve viec tuan thu huong dan va tu dong sua cac lo hong.

### Truoc: Bo mac va pho bay

- Trien khai ma nguon do AI tao ra ma khong kiem tra gi
- Khong biet rang huong dan bao mat ton tai
- "De sau hay" — roi cuong cuong sau khi xay ra su co
- Khong co chuyen gia bao mat trong nhom, khong biet bat dau tu dau

### Sau: Voi KKTV

- Mot lenh `/kktv.start` kiem tra tat ca 47 quy tac
- Bao cao theo danh muc cho thay chinh xac noi nao co lo hong
- `/kktv.fix` tu dong va cac lo hong duoc phat hien
- `/kktv.guide` tao prompt de AI viet ma an toan ngay tu dau

---

## Bat dau nhanh

### 1. Cai dat

```bash
# Dang ky marketplace
/plugin marketplace add cdppcorp/KKTV

# Phien ban tieng Anh
/plugin install kktv-en@kktv

# Phien ban tieng Han
/plugin install kktv-ko@kktv
```

### 2. Bat dau kiem tra bao mat

```bash
/kktv.start
```

Khi chay lan dau, bang cau hoi moi truong se xuat hien:
- Tu dong phat hien he dieu hanh (Windows/Linux)
- Tu dong phat hien ngon ngu va framework
- Xac nhan muc tieu trien khai, co so du lieu va phuong thuc xac thuc
- Tu dong chan doan tinh tuong thich hook plugin tren Windows

### 3. Xem bao cao va sua loi

```
reports/security/
├── summary.md              ← Tom tat tong quan
├── cat1-input-validation.md ← Chi tiet theo danh muc
├── cat2-security-features.md
├── ...
└── cat7-api-misuse.md
```

Khi phat hien lo hong:

```bash
/kktv.fix      # Tu dong sua
/kktv.check    # Kiem tra lan cuoi truoc khi trien khai
```

---

## Skills

| Skill | Lenh | Mo ta |
|-------|------|-------|
| Start | `/kktv.start` | Kiem tra bao mat dua tren 47 quy tac KISA + tao bao cao theo danh muc |
| Fix | `/kktv.fix` | Tu dong sua cac lo hong voi cac mau an toan |
| Check | `/kktv.check` | Danh sach kiem tra tuong tac 47 muc truoc khi trien khai |
| Guide | `/kktv.guide` | Tao prompt de cac cong cu AI viet ma an toan |

---

## 47 Quy tac Bao mat KISA

KKTV dua tren 47 diem yeu bao mat tu Huong dan Lap trinh An toan Python cua KISA (ban sua doi 2023). Tat ca cac quy tac deu duoc anh xa toi tieu chuan quoc te CWE (Common Weakness Enumeration).

| Danh muc | So quy tac | Cac muc chinh |
|----------|------------|----------------|
| Xac thuc du lieu dau vao va bieu dien | 18 | SQL injection, XSS, CSRF, SSRF, code injection, command injection |
| Tinh nang bao mat | 16 | Xac thuc, uy quyen, ma hoa, bi mat ma hoa cung, chinh sach mat khau |
| Thoi gian va trang thai | 2 | Dieu kien canh tranh TOCTOU, vong lap vo han/de quy |
| Xu ly loi | 3 | Lo thong tin qua thong bao loi, thieu phan hoi, xu ly ngoai le khong phu hop |
| Loi ma nguon | 3 | Tham chieu null, giai phong tai nguyen, deserialization |
| Dong goi | 2 | Lo du lieu phien, ma debug con sot |
| Lam dung API | 3 | Quyet dinh bao mat dua tren DNS, su dung API de bi tan cong |

---

## Ai can dieu nay

| Doi tuong | Tinh huong |
|-----------|------------|
| **Vibe coder** | Xay dung va trien khai website bang AI, nhung chua bao gio kiem tra bao mat |
| **Nha phat trien startup** | Can ra mat nhanh nhung khong co nhan su bao mat chuyen trach |
| **Nguoi tham gia du an chinh phu/SI** | Du an ma lap trinh an toan la bat buoc theo Luat Chinh phu Dien tu |
| **Nha phat trien nuoc ngoai** | Tham nhap thi truong Han Quoc hoac hop tac voi cong ty Han Quoc va can tuan thu huong dan KISA |
| **Freelancer** | Can nop bao cao kiem tra bao mat cho khach hang |

---

## Ban thao

Thu muc `authorkit/manuscript/` cung cap huong dan lap trinh an toan day du trong 3 phien ban. Mot ban thao hoan chinh bao gom 17 chuong, 6 PART va 47 loai lo hong.

| Phien ban | Tap tin | Doi tuong |
|-----------|---------|-----------|
| Django/Flask | `시큐어코딩_가이드라인_Skills_Django.md` | Nguoi dung Django, Flask |
| FastAPI | `시큐어코딩_가이드라인_Skills_FastAPI.md` | Nguoi dung FastAPI, SQLAlchemy, Pydantic |
| Pseudocode | `시큐어코딩_가이드라인_Skills_Pseudocode.md` | Nguoi dung moi ngon ngu/framework |

---

## Tai lieu tham khao

- [KISA Huong dan Lap trinh An toan Python (ban sua doi 2023)](https://www.kisa.or.kr)
- [CWE - Common Weakness Enumeration](https://cwe.mitre.org)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Luat Chinh phu Dien tu, Dieu 45](https://www.law.go.kr)

---

## Giay phep

MIT
