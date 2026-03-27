<div align="center">

# KKTV

### Aplica las directrices de codificacion segura de KISA a tu codigo

Un skill de codificacion segura para vibe coders que crean sitios web con IA

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../LICENSE)
[![KISA](https://img.shields.io/badge/Based_on-KISA_Secure_Coding_Guide_2023-003DAD)](https://www.kisa.or.kr)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-0078D6)](https://github.com/cdppcorp/KKTV)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-6B4FBB)](https://docs.anthropic.com/en/docs/claude-code)
[![CWE](https://img.shields.io/badge/47_Rules-CWE_Mapped-E34F26)](https://cwe.mitre.org)

</div>

---

## Languages / Idiomas

[한국어](../README.md) | [English](README.en.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [Русский](README.ru.md) | [Français](README.fr.md) | [**Español**](README.es.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Tiếng Việt](README.vi.md) | [ไทย](README.th.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [Türkçe](README.tr.md)

---

## Tu codigo, es realmente seguro?

Estas desplegando codigo generado por IA sin ninguna revision?

```python
# Codigo generado por IA — sabes cuantas vulnerabilidades hay aqui?
app.config['SECRET_KEY'] = 'super-secret-key-123'
query = f"SELECT * FROM users WHERE id = '{user_input}'"
app.run(debug=True)
```

El codigo anterior contiene **3 vulnerabilidades de seguridad**: una clave secreta codificada en duro, inyeccion SQL y modo debug en produccion. El codigo generado por herramientas de IA como Cursor, Claude Code y Copilot se despliega cada dia con vulnerabilidades como estas.

**El problema es que la mayoria de los vibe coders ni siquiera lo saben, y dejan estas vulnerabilidades sin tratar.**

---

## Si operas en Corea, las directrices de KISA no son opcionales

La Agencia de Internet y Seguridad de Corea (KISA) publico la **Guia de Codificacion Segura en Python (revision 2023)**, que define 47 debilidades de seguridad y sus contramedidas. Si operas un servicio web en Corea o participas en proyectos del sector publico, seguir estas directrices es **practicamente una obligacion legal**.

- **Ley de Gobierno Electronico, Articulo 45**: aplicacion obligatoria de seguridad en el desarrollo de software para sistemas de informacion de organismos gubernamentales
- **Ley de Proteccion de Informacion Personal**: medidas de seguridad obligatorias al procesar informacion personal
- **Ley de Redes de Informacion y Comunicacion**: auditorias de vulnerabilidad de seguridad obligatorias para proveedores de servicios de informacion y comunicacion

> Aunque seas un desarrollador extranjero, si estas entrando al mercado coreano o trabajando con empresas coreanas, debes conocer las directrices de KISA.

---

## KKTV lo resuelve

KKTV es un plugin que convierte las 47 reglas de la guia de codificacion segura de KISA en skills de Claude Code. Con un solo comando, audita tu proyecto para verificar el cumplimiento de las directrices y corrige automaticamente las vulnerabilidades.

### Antes: Negligencia y exposicion

- Desplegar codigo generado por IA sin ninguna revision
- Ni siquiera saber que existen directrices de seguridad
- "Ya me ocupare despues" — y luego correr tras un incidente
- Sin experto en seguridad en el equipo, sin saber por donde empezar

### Despues: Con KKTV

- Un solo comando `/kktv.start` audita las 47 reglas
- Informes por categoria muestran exactamente donde estan las vulnerabilidades
- `/kktv.fix` corrige automaticamente las vulnerabilidades descubiertas
- `/kktv.guide` genera prompts para que la IA escriba codigo seguro desde el principio

---

## Inicio rapido

### 1. Instalacion

```bash
# Registro en el marketplace
/plugin marketplace add cdppcorp/KKTV

# Version en ingles
/plugin install kktv-en@kktv

# Version en coreano
/plugin install kktv-ko@kktv
```

### 2. Iniciar auditoria de seguridad

```bash
/kktv.start
```

En la primera ejecucion, aparece un cuestionario de entorno:
- Deteccion automatica del SO (Windows/Linux)
- Deteccion automatica del lenguaje y framework
- Confirmacion del destino de despliegue, base de datos y metodo de autenticacion
- Diagnostico automatico de compatibilidad de hooks del plugin en Windows

### 3. Revisar informes y corregir

```
reports/security/
├── summary.md              ← Resumen general
├── cat1-input-validation.md ← Detalle por categoria
├── cat2-security-features.md
├── ...
└── cat7-api-misuse.md
```

Cuando se encuentran vulnerabilidades:

```bash
/kktv.fix      # Correccion automatica
/kktv.check    # Verificacion final antes del despliegue
```

---

## Skills

| Skill | Comando | Descripcion |
|-------|---------|-------------|
| Start | `/kktv.start` | Auditoria de seguridad basada en las 47 reglas de KISA + generacion de informes por categoria |
| Fix | `/kktv.fix` | Correccion automatica de vulnerabilidades con patrones seguros |
| Check | `/kktv.check` | Lista de verificacion interactiva de 47 puntos antes del despliegue |
| Guide | `/kktv.guide` | Generacion de prompts para que las herramientas de IA escriban codigo seguro |

---

## 47 reglas de seguridad de KISA

KKTV se basa en las 47 debilidades de seguridad de la guia de codificacion segura en Python de KISA (revision 2023). Todas las reglas estan mapeadas al estandar internacional CWE (Common Weakness Enumeration).

| Categoria | Reglas | Elementos principales |
|-----------|--------|-----------------------|
| Validacion de datos de entrada y representacion | 18 | Inyeccion SQL, XSS, CSRF, SSRF, inyeccion de codigo, inyeccion de comandos |
| Funcionalidades de seguridad | 16 | Autenticacion, autorizacion, cifrado, secretos codificados en duro, politica de contrasenas |
| Tiempo y estado | 2 | Condicion de carrera TOCTOU, bucle infinito/recursion |
| Manejo de errores | 3 | Exposicion de mensajes de error, ausencia de respuesta, manejo inadecuado de excepciones |
| Errores de codigo | 3 | Desreferencia null, liberacion de recursos, deserializacion |
| Encapsulacion | 2 | Exposicion de datos de sesion, codigo de depuracion residual |
| Uso indebido de API | 3 | Decisiones de seguridad basadas en DNS, uso de API vulnerables |

---

## Quien necesita esto

| Publico | Situacion |
|---------|-----------|
| **Vibe coders** | Crean y despliegan sitios web con IA, pero nunca han realizado una revision de seguridad |
| **Desarrolladores de startups** | Necesitan lanzar rapido, pero no tienen personal dedicado a seguridad |
| **Participantes en proyectos gubernamentales/SI** | Proyectos donde la codificacion segura es obligatoria segun la Ley de Gobierno Electronico |
| **Desarrolladores extranjeros** | Entran al mercado coreano o colaboran con empresas coreanas y deben cumplir las directrices de KISA |
| **Freelancers** | Necesitan entregar informes de auditoria de seguridad a sus clientes |

---

## Manuscrito

El directorio `authorkit/manuscript/` proporciona la guia completa de codificacion segura en 3 versiones. Un manuscrito completo que cubre 17 capitulos, 6 PARTs y 47 tipos de vulnerabilidades.

| Version | Archivo | Publico objetivo |
|---------|---------|------------------|
| Django/Flask | `시큐어코딩_가이드라인_Skills_Django.md` | Usuarios de Django, Flask |
| FastAPI | `시큐어코딩_가이드라인_Skills_FastAPI.md` | Usuarios de FastAPI, SQLAlchemy, Pydantic |
| Pseudocode | `시큐어코딩_가이드라인_Skills_Pseudocode.md` | Usuarios de todos los lenguajes/frameworks |

---

## Referencias

- [KISA Guia de Codificacion Segura en Python (revision 2023)](https://www.kisa.or.kr)
- [CWE - Common Weakness Enumeration](https://cwe.mitre.org)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Ley de Gobierno Electronico, Articulo 45](https://www.law.go.kr)

---

## Licencia

MIT
