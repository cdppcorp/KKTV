<div align="center">

# KKTV

### Wenden Sie die KISA Secure Coding Richtlinien auf Ihren Code an

Ein Secure-Coding-Skill fuer Vibe Coder, die Websites mit KI erstellen

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../LICENSE)
[![KISA](https://img.shields.io/badge/Based_on-KISA_Secure_Coding_Guide_2023-003DAD)](https://www.kisa.or.kr)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-0078D6)](https://github.com/cdppcorp/KKTV)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-6B4FBB)](https://docs.anthropic.com/en/docs/claude-code)
[![CWE](https://img.shields.io/badge/47_Rules-CWE_Mapped-E34F26)](https://cwe.mitre.org)

</div>

---

## Languages / Sprachen

[한국어](../README.md) | [English](README.en.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [Русский](README.ru.md) | [Français](README.fr.md) | [Español](README.es.md) | [**Deutsch**](README.de.md) | [Português](README.pt.md) | [Tiếng Việt](README.vi.md) | [ไทย](README.th.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [Türkçe](README.tr.md)

---

## Ist Ihr Code wirklich sicher?

Deployen Sie KI-generierten Code ohne jegliche Ueberpruefung?

```python
# KI-generierter Code — wissen Sie, wie viele Schwachstellen hier enthalten sind?
app.config['SECRET_KEY'] = 'super-secret-key-123'
query = f"SELECT * FROM users WHERE id = '{user_input}'"
app.run(debug=True)
```

Der obige Code enthaelt **3 Sicherheitsschwachstellen**: einen hartcodierten geheimen Schluessel, SQL-Injection und den Debug-Modus in der Produktion. Code, der von KI-Tools wie Cursor, Claude Code und Copilot generiert wird, wird taeglich mit solchen Schwachstellen deployed.

**Das Problem ist, dass die meisten Vibe Coder das nicht einmal wissen und diese Schwachstellen unbehandelt lassen.**

---

## Wenn Sie in Korea operieren, sind die KISA-Richtlinien keine Option

Die Korea Internet & Security Agency (KISA) hat den **Python Secure Coding Guide (Revision 2023)** veroeffentlicht, der 47 Sicherheitsschwaechen und deren Gegenmassnahmen definiert. Wenn Sie einen Webdienst in Korea betreiben oder an oeffentlichen Projekten teilnehmen, ist die Einhaltung dieser Richtlinien **praktisch eine gesetzliche Pflicht**.

- **E-Government-Gesetz, Artikel 45**: Verpflichtende Anwendung von Softwareentwicklungssicherheit bei der Entwicklung von Informationssystemen fuer Regierungsbehoerden
- **Gesetz zum Schutz personenbezogener Daten**: Verpflichtende Sicherheitsmassnahmen bei der Verarbeitung personenbezogener Daten
- **Gesetz ueber Informations- und Kommunikationsnetze**: Verpflichtende Sicherheitsaudits fuer Anbieter von Informations- und Kommunikationsdiensten

> Auch wenn Sie ein auslaendischer Entwickler sind — wenn Sie in den koreanischen Markt eintreten oder mit koreanischen Unternehmen zusammenarbeiten, muessen Sie die KISA-Richtlinien kennen.

---

## KKTV loest dieses Problem

KKTV ist ein Plugin, das die 47 Regeln des KISA Secure Coding Guide in Claude Code Skills umwandelt. Mit einem einzigen Befehl pruefen Sie Ihr Projekt auf Richtlinienkonformitaet und beheben Schwachstellen automatisch.

### Vorher: Vernachlaessigung und Verwundbarkeit

- Deployment von KI-generiertem Code ohne jegliche Ueberpruefung
- Nicht einmal wissen, dass Sicherheitsrichtlinien existieren
- "Das mache ich spaeter" — dann Panik nach einem Vorfall
- Kein Sicherheitsexperte im Team, keine Ahnung, wo man anfangen soll

### Nachher: Mit KKTV

- Ein einziger `/kktv.start`-Befehl prueft alle 47 Regeln
- Kategorisierte Berichte zeigen genau, wo Schwachstellen liegen
- `/kktv.fix` behebt entdeckte Schwachstellen automatisch
- `/kktv.guide` generiert Prompts, damit KI von Anfang an sicheren Code schreibt

---

## Schnellstart

### 1. Installation

```bash
# Marketplace-Registrierung
/plugin marketplace add cdppcorp/KKTV

# Englische Version
/plugin install kktv-en@kktv

# Koreanische Version
/plugin install kktv-ko@kktv
```

### 2. Sicherheitsaudit starten

```bash
/kktv.start
```

Beim ersten Start erscheint ein Umgebungsfragebogen:
- Automatische OS-Erkennung (Windows/Linux)
- Automatische Sprach- und Framework-Erkennung
- Bestaetigung von Deployment-Ziel, Datenbank und Authentifizierungsmethode
- Automatische Diagnose der Plugin-Hook-Kompatibilitaet unter Windows

### 3. Berichte pruefen und beheben

```
reports/security/
├── summary.md              ← Uebersichtliche Zusammenfassung
├── cat1-input-validation.md ← Detail nach Kategorie
├── cat2-security-features.md
├── ...
└── cat7-api-misuse.md
```

Wenn Schwachstellen gefunden werden:

```bash
/kktv.fix      # Automatische Behebung
/kktv.check    # Letzte Pruefung vor dem Deployment
```

---

## Skills

| Skill | Befehl | Beschreibung |
|-------|--------|--------------|
| Start | `/kktv.start` | Sicherheitsaudit basierend auf 47 KISA-Regeln + kategorisierte Berichterstellung |
| Fix | `/kktv.fix` | Automatische Behebung von Schwachstellen mit sicheren Mustern |
| Check | `/kktv.check` | Interaktive 47-Punkte-Checkliste vor dem Deployment |
| Guide | `/kktv.guide` | Prompt-Generierung, damit KI-Tools sicheren Code schreiben |

---

## KISA 47 Sicherheitsregeln

KKTV basiert auf den 47 Sicherheitsschwaechen des KISA Python Secure Coding Guide (Revision 2023). Alle Regeln sind dem internationalen Standard CWE (Common Weakness Enumeration) zugeordnet.

| Kategorie | Regeln | Wichtige Punkte |
|-----------|--------|-----------------|
| Eingabedatenvalidierung und Darstellung | 18 | SQL-Injection, XSS, CSRF, SSRF, Code-Injection, Command-Injection |
| Sicherheitsfunktionen | 16 | Authentifizierung, Autorisierung, Verschluesselung, hartcodierte Geheimnisse, Passwortrichtlinien |
| Zeit und Zustand | 2 | TOCTOU-Race-Condition, Endlosschleife/Rekursion |
| Fehlerbehandlung | 3 | Offenlegung von Fehlermeldungen, fehlende Reaktion, unsachgemaesse Ausnahmebehandlung |
| Codefehler | 3 | Null-Dereferenzierung, Ressourcenfreigabe, Deserialisierung |
| Kapselung | 2 | Offenlegung von Sitzungsdaten, verbliebener Debug-Code |
| API-Missbrauch | 3 | DNS-basierte Sicherheitsentscheidungen, Verwendung verwundbarer APIs |

---

## Wer braucht das

| Zielgruppe | Situation |
|------------|-----------|
| **Vibe Coder** | Erstellen und deployen Websites mit KI, haben aber nie eine Sicherheitsueberpruefung durchgefuehrt |
| **Startup-Entwickler** | Muessen schnell ausliefern, haben aber kein dediziertes Sicherheitspersonal |
| **Teilnehmer an Regierungs-/SI-Projekten** | Projekte, bei denen Secure Coding gemaess E-Government-Gesetz verpflichtend ist |
| **Auslaendische Entwickler** | Treten in den koreanischen Markt ein oder arbeiten mit koreanischen Unternehmen und muessen die KISA-Richtlinien einhalten |
| **Freelancer** | Muessen Sicherheitsaudit-Berichte an Kunden liefern |

---

## Manuskript

Das Verzeichnis `authorkit/manuscript/` stellt den vollstaendigen Secure-Coding-Leitfaden in 3 Versionen bereit. Ein komplettes Manuskript mit 17 Kapiteln, 6 PARTs und 47 Schwachstellentypen.

| Version | Datei | Zielgruppe |
|---------|-------|------------|
| Django/Flask | `시큐어코딩_가이드라인_Skills_Django.md` | Django-, Flask-Benutzer |
| FastAPI | `시큐어코딩_가이드라인_Skills_FastAPI.md` | FastAPI-, SQLAlchemy-, Pydantic-Benutzer |
| Pseudocode | `시큐어코딩_가이드라인_Skills_Pseudocode.md` | Benutzer aller Sprachen/Frameworks |

---

## Referenzen

- [KISA Python Secure Coding Guide (Revision 2023)](https://www.kisa.or.kr)
- [CWE - Common Weakness Enumeration](https://cwe.mitre.org)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [E-Government-Gesetz, Artikel 45](https://www.law.go.kr)

---

## Lizenz

MIT
