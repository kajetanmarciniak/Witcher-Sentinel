# Witcher Sentinel v6 — The Elder Blood

[![Python](https://img.shields.io/badge/Python-3.12-blue)]()
[![AWS](https://img.shields.io/badge/AWS-Lambda%20%7C%20S3%20%7C%20EventBridge-orange)]()

Serverless OSINT agent for CD Projekt Red titles — Tavily search, S3 state, Discord alerts, async authenticity scoring.

**Full architecture, features, and roadmap (v1–v10): [`docs/DESIGN.md`](docs/DESIGN.md)**

---

## Quick start

```bash
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python main.py
```

## Lambda

| Handler | `lambda_function.lambda_handler` |
| Runtime | Python 3.12 |
| Timeout | 60–90s |

Use env vars or Secrets Manager for credentials — never bundle `.env`. AWS access via IAM Role only.

---

*Portfolio project — The Witcher® belongs to CD Projekt Red.*
