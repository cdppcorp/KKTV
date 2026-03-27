<div align="center">

# KKTV

### Aplique as diretrizes de codificacao segura da KISA ao seu codigo

Um skill de codificacao segura para vibe coders que criam sites com IA

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../LICENSE)
[![KISA](https://img.shields.io/badge/Based_on-KISA_Secure_Coding_Guide_2023-003DAD)](https://www.kisa.or.kr)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-0078D6)](https://github.com/cdppcorp/KKTV)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-6B4FBB)](https://docs.anthropic.com/en/docs/claude-code)
[![CWE](https://img.shields.io/badge/47_Rules-CWE_Mapped-E34F26)](https://cwe.mitre.org)

</div>

---

## Languages / Idiomas

[한국어](../README.md) | [English](README.en.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [Русский](README.ru.md) | [Français](README.fr.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [**Português**](README.pt.md) | [Tiếng Việt](README.vi.md) | [ไทย](README.th.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [Türkçe](README.tr.md)

---

## Seu codigo e realmente seguro?

Voce esta implantando codigo gerado por IA sem nenhuma revisao?

```python
# Codigo gerado por IA — voce sabe quantas vulnerabilidades existem aqui?
app.config['SECRET_KEY'] = 'super-secret-key-123'
query = f"SELECT * FROM users WHERE id = '{user_input}'"
app.run(debug=True)
```

O codigo acima contem **3 vulnerabilidades de seguranca**: uma chave secreta codificada diretamente, injecao SQL e modo de depuracao em producao. Codigo gerado por ferramentas de IA como Cursor, Claude Code e Copilot e implantado diariamente com vulnerabilidades como essas.

**O problema e que a maioria dos vibe coders nem sabe disso e deixa essas vulnerabilidades sem tratamento.**

---

## Se voce opera na Coreia, as diretrizes da KISA nao sao opcionais

A Agencia Coreana de Internet e Seguranca (KISA) publicou o **Guia de Codificacao Segura em Python (revisao 2023)**, que define 47 fraquezas de seguranca e suas contramedidas. Se voce opera um servico web na Coreia ou participa de projetos do setor publico, seguir essas diretrizes e **praticamente uma obrigacao legal**.

- **Lei de Governo Eletronico, Artigo 45**: aplicacao obrigatoria de seguranca no desenvolvimento de software para sistemas de informacao de orgaos governamentais
- **Lei de Protecao de Informacoes Pessoais**: medidas de seguranca obrigatorias ao processar informacoes pessoais
- **Lei de Redes de Informacao e Comunicacao**: auditorias de vulnerabilidade de seguranca obrigatorias para provedores de servicos de informacao e comunicacao

> Mesmo sendo um desenvolvedor estrangeiro, se voce esta entrando no mercado coreano ou trabalhando com empresas coreanas, deve conhecer as diretrizes da KISA.

---

## KKTV resolve isso

KKTV e um plugin que transforma as 47 regras do guia de codificacao segura da KISA em skills do Claude Code. Com um unico comando, ele audita seu projeto quanto a conformidade com as diretrizes e corrige vulnerabilidades automaticamente.

### Antes: Negligencia e exposicao

- Implantar codigo gerado por IA sem nenhuma revisao
- Nem saber que diretrizes de seguranca existem
- "Vou resolver depois" — e entao correr apos um incidente
- Sem especialista em seguranca na equipe, sem saber por onde comecar

### Depois: Com KKTV

- Um unico comando `/kktv.start` audita todas as 47 regras
- Relatorios por categoria mostram exatamente onde estao as vulnerabilidades
- `/kktv.fix` corrige automaticamente as vulnerabilidades descobertas
- `/kktv.guide` gera prompts para que a IA escreva codigo seguro desde o inicio

---

## Inicio rapido

### 1. Instalacao

```bash
# Registro no marketplace
/plugin marketplace add cdppcorp/KKTV

# Versao em ingles
/plugin install kktv-en@kktv

# Versao em coreano
/plugin install kktv-ko@kktv
```

### 2. Iniciar auditoria de seguranca

```bash
/kktv.start
```

Na primeira execucao, um questionario de ambiente aparece:
- Deteccao automatica do SO (Windows/Linux)
- Deteccao automatica de linguagem e framework
- Confirmacao do alvo de implantacao, banco de dados e metodo de autenticacao
- Diagnostico automatico de compatibilidade de hooks do plugin no Windows

### 3. Revisar relatorios e corrigir

```
reports/security/
├── summary.md              ← Resumo geral
├── cat1-input-validation.md ← Detalhamento por categoria
├── cat2-security-features.md
├── ...
└── cat7-api-misuse.md
```

Quando vulnerabilidades sao encontradas:

```bash
/kktv.fix      # Correcao automatica
/kktv.check    # Verificacao final antes da implantacao
```

---

## Skills

| Skill | Comando | Descricao |
|-------|---------|-----------|
| Start | `/kktv.start` | Auditoria de seguranca baseada nas 47 regras da KISA + geracao de relatorios por categoria |
| Fix | `/kktv.fix` | Correcao automatica de vulnerabilidades com padroes seguros |
| Check | `/kktv.check` | Checklist interativo de 47 itens antes da implantacao |
| Guide | `/kktv.guide` | Geracao de prompts para que ferramentas de IA escrevam codigo seguro |

---

## 47 regras de seguranca da KISA

KKTV e baseado nas 47 fraquezas de seguranca do guia de codificacao segura em Python da KISA (revisao 2023). Todas as regras sao mapeadas para o padrao internacional CWE (Common Weakness Enumeration).

| Categoria | Regras | Itens principais |
|-----------|--------|------------------|
| Validacao de dados de entrada e representacao | 18 | Injecao SQL, XSS, CSRF, SSRF, injecao de codigo, injecao de comandos |
| Funcionalidades de seguranca | 16 | Autenticacao, autorizacao, criptografia, segredos codificados diretamente, politica de senhas |
| Tempo e estado | 2 | Condicao de corrida TOCTOU, loop infinito/recursao |
| Tratamento de erros | 3 | Exposicao de mensagens de erro, ausencia de resposta, tratamento inadequado de excecoes |
| Erros de codigo | 3 | Desreferencia null, liberacao de recursos, desserializacao |
| Encapsulamento | 2 | Exposicao de dados de sessao, codigo de depuracao residual |
| Uso indevido de API | 3 | Decisoes de seguranca baseadas em DNS, uso de APIs vulneraveis |

---

## Quem precisa disso

| Publico | Situacao |
|---------|----------|
| **Vibe coders** | Criam e implantam sites com IA, mas nunca fizeram uma revisao de seguranca |
| **Desenvolvedores de startups** | Precisam lancar rapido, mas nao tem pessoal dedicado a seguranca |
| **Participantes de projetos governamentais/SI** | Projetos onde codificacao segura e obrigatoria pela Lei de Governo Eletronico |
| **Desenvolvedores estrangeiros** | Entrando no mercado coreano ou colaborando com empresas coreanas e precisam cumprir as diretrizes da KISA |
| **Freelancers** | Precisam entregar relatorios de auditoria de seguranca aos clientes |

---

## Manuscrito

O diretorio `authorkit/manuscript/` fornece o guia completo de codificacao segura em 3 versoes. Um manuscrito completo cobrindo 17 capitulos, 6 PARTs e 47 tipos de vulnerabilidades.

| Versao | Arquivo | Publico-alvo |
|--------|---------|--------------|
| Django/Flask | `시큐어코딩_가이드라인_Skills_Django.md` | Usuarios de Django, Flask |
| FastAPI | `시큐어코딩_가이드라인_Skills_FastAPI.md` | Usuarios de FastAPI, SQLAlchemy, Pydantic |
| Pseudocode | `시큐어코딩_가이드라인_Skills_Pseudocode.md` | Usuarios de todas as linguagens/frameworks |

---

## Referencias

- [KISA Guia de Codificacao Segura em Python (revisao 2023)](https://www.kisa.or.kr)
- [CWE - Common Weakness Enumeration](https://cwe.mitre.org)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Lei de Governo Eletronico, Artigo 45](https://www.law.go.kr)

---

## Licenca

MIT
