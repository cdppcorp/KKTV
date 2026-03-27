<div align="center">

# KKTV

### Appliquez les directives de codage securise KISA a votre code

Un skill de codage securise pour les vibe coders qui creent des sites web avec l'IA

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../LICENSE)
[![KISA](https://img.shields.io/badge/Based_on-KISA_Secure_Coding_Guide_2023-003DAD)](https://www.kisa.or.kr)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-0078D6)](https://github.com/cdppcorp/KKTV)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-6B4FBB)](https://docs.anthropic.com/en/docs/claude-code)
[![CWE](https://img.shields.io/badge/47_Rules-CWE_Mapped-E34F26)](https://cwe.mitre.org)

</div>

---

## Languages / Langues

[한국어](../README.md) | [English](README.en.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [Русский](README.ru.md) | [**Français**](README.fr.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Tiếng Việt](README.vi.md) | [ไทย](README.th.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [Türkçe](README.tr.md)

---

## Votre code est-il vraiment securise ?

Deployez-vous du code genere par l'IA sans aucune verification ?

```python
# Code genere par l'IA — savez-vous combien de vulnerabilites s'y cachent ?
app.config['SECRET_KEY'] = 'super-secret-key-123'
query = f"SELECT * FROM users WHERE id = '{user_input}'"
app.run(debug=True)
```

Le code ci-dessus contient **3 vulnerabilites de securite** : une cle secrete codee en dur, une injection SQL et le mode debug en production. Le code genere par des outils IA comme Cursor, Claude Code et Copilot est deploye chaque jour avec de telles vulnerabilites.

**Le probleme, c'est que la plupart des vibe coders ne le savent meme pas et laissent ces vulnerabilites sans traitement.**

---

## Si vous operez en Coree, les directives KISA ne sont pas optionnelles

L'Agence coreenne de l'internet et de la securite (KISA) a publie le **Guide de codage securise Python (revision 2023)**, qui definit 47 faiblesses de securite et leurs contre-mesures. Si vous exploitez un service web en Coree ou participez a des projets du secteur public, suivre ces directives est **pratiquement une obligation legale**.

- **Loi sur l'administration electronique, article 45** : application obligatoire de la securite du developpement logiciel pour les systemes d'information des organismes gouvernementaux
- **Loi sur la protection des informations personnelles** : mesures de securite obligatoires lors du traitement des donnees personnelles
- **Loi sur les reseaux d'information et de communication** : audits de vulnerabilite de securite obligatoires pour les fournisseurs de services d'information et de communication

> Meme si vous etes un developpeur etranger, si vous entrez sur le marche coreen ou travaillez avec des entreprises coreennes, vous devez connaitre les directives KISA.

---

## KKTV resout ce probleme

KKTV est un plugin qui transforme les 47 regles du guide de codage securise KISA en skills Claude Code. Une seule commande suffit pour auditer la conformite de votre projet aux directives et corriger automatiquement les vulnerabilites.

### Avant : Negligence et exposition

- Deploiement de code genere par l'IA sans aucune verification
- Ignorance de l'existence meme des directives de securite
- "Je m'en occuperai plus tard" — puis panique apres un incident
- Pas d'expert en securite dans l'equipe, aucune idee par ou commencer

### Apres : Avec KKTV

- Une seule commande `/kktv.start` audite les 47 regles
- Des rapports par categorie montrent exactement ou se trouvent les vulnerabilites
- `/kktv.fix` corrige automatiquement les vulnerabilites decouvertes
- `/kktv.guide` genere des prompts pour que l'IA ecrive du code securise des le depart

---

## Demarrage rapide

### 1. Installation

```bash
# Enregistrement sur le marketplace
/plugin marketplace add cdppcorp/KKTV

# Version anglaise
/plugin install kktv-en@kktv

# Version coreenne
/plugin install kktv-ko@kktv
```

### 2. Lancer l'audit de securite

```bash
/kktv.start
```

Au premier lancement, un questionnaire d'environnement apparait :
- Detection automatique de l'OS (Windows/Linux)
- Detection automatique du langage et du framework
- Confirmation de la cible de deploiement, de la base de donnees et de la methode d'authentification
- Diagnostic automatique de compatibilite des hooks du plugin sous Windows

### 3. Consulter les rapports et corriger

```
reports/security/
├── summary.md              ← Resume synthetique
├── cat1-input-validation.md ← Detail par categorie
├── cat2-security-features.md
├── ...
└── cat7-api-misuse.md
```

Lorsque des vulnerabilites sont detectees :

```bash
/kktv.fix      # Correction automatique
/kktv.check    # Verification finale avant deploiement
```

---

## Skills

| Skill | Commande | Description |
|-------|----------|-------------|
| Start | `/kktv.start` | Audit de securite base sur les 47 regles KISA + generation de rapports par categorie |
| Fix | `/kktv.fix` | Correction automatique des vulnerabilites avec des modeles securises |
| Check | `/kktv.check` | Checklist interactive de 47 points avant deploiement |
| Guide | `/kktv.guide` | Generation de prompts pour que les outils IA ecrivent du code securise |

---

## 47 regles de securite KISA

KKTV est base sur les 47 faiblesses de securite du guide de codage securise Python de KISA (revision 2023). Toutes les regles sont mappees sur le standard international CWE (Common Weakness Enumeration).

| Categorie | Regles | Elements principaux |
|-----------|--------|---------------------|
| Validation des donnees d'entree et representation | 18 | Injection SQL, XSS, CSRF, SSRF, injection de code, injection de commandes |
| Fonctionnalites de securite | 16 | Authentification, autorisation, chiffrement, secrets codes en dur, politique de mots de passe |
| Temps et etat | 2 | Condition de concurrence TOCTOU, boucle infinie/recursion |
| Gestion des erreurs | 3 | Exposition des messages d'erreur, absence de reponse, gestion inappropriee des exceptions |
| Erreurs de code | 3 | Dereferencement null, liberation de ressources, deserialisation |
| Encapsulation | 2 | Exposition des donnees de session, code de debogage residuel |
| Mauvaise utilisation des API | 3 | Decisions de securite basees sur le DNS, utilisation d'API vulnerables |

---

## Qui en a besoin

| Public | Situation |
|--------|-----------|
| **Vibe coders** | Creent et deployent des sites web avec l'IA, mais n'ont jamais effectue de revue de securite |
| **Developpeurs de startups** | Doivent livrer rapidement, mais n'ont pas de personnel dedie a la securite |
| **Participants aux projets gouvernementaux/SI** | Projets ou le codage securise est obligatoire en vertu de la loi sur l'administration electronique |
| **Developpeurs etrangers** | Entrent sur le marche coreen ou collaborent avec des entreprises coreennes et doivent se conformer aux directives KISA |
| **Freelances** | Doivent fournir des rapports d'audit de securite a leurs clients |

---

## Manuscrit

Le repertoire `authorkit/manuscript/` fournit le guide complet de codage securise en 3 versions. Un manuscrit complet couvrant 17 chapitres, 6 PARTs et 47 types de vulnerabilites.

| Version | Fichier | Public cible |
|---------|---------|--------------|
| Django/Flask | `시큐어코딩_가이드라인_Skills_Django.md` | Utilisateurs Django, Flask |
| FastAPI | `시큐어코딩_가이드라인_Skills_FastAPI.md` | Utilisateurs FastAPI, SQLAlchemy, Pydantic |
| Pseudocode | `시큐어코딩_가이드라인_Skills_Pseudocode.md` | Utilisateurs de tous langages/frameworks |

---

## References

- [KISA Guide de codage securise Python (revision 2023)](https://www.kisa.or.kr)
- [CWE - Common Weakness Enumeration](https://cwe.mitre.org)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Loi sur l'administration electronique, article 45](https://www.law.go.kr)

---

## Licence

MIT
