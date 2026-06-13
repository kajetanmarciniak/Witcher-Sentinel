# Witcher Sentinel v6 — The Elder Blood

[![Python](https://img.shields.io/badge/Python-3.12-blue)]()
[![AWS](https://img.shields.io/badge/AWS-Lambda%20%7C%20S3%20%7C%20EventBridge-orange)]()
[![License](https://img.shields.io/badge/License-Portfolio-lightgrey)]()

Autonomous OSINT agent for CD Projekt Red titles. Serverless on **AWS Lambda** with Tavily search, **S3 state**, **Discord** alerts, and async **authenticity scoring** (RAG + cognitive filter).

> Architecture and full roadmap: [`docs/DESIGN.md`](docs/DESIGN.md)

---

## What it does

1. Scouts multiple Witcher tracks in parallel (W3, W4/Polaris, Sirius remake)
2. Filters noise (mods, fanart, Reddit bait) via `targets.json`
3. Scores each signal against S3-backed context before alerting
4. Sends Discord notifications only when authenticity passes threshold
5. Archives validated hunts to the S3 Bestiary vault

---

## Project structure

```
├── lambda_function.py   # AWS entrypoint → main.lambda_handler
├── main.py              # async orchestrator (asyncio.gather)
├── config.py            # .env + targets.json loader
├── targets.json         # hunt config (no secrets in code)
├── services/
│   ├── cognitive.py     # authenticity scoring + parallel hunt (aiohttp)
│   ├── s3_vault.py      # S3 memory + RAG corpus (boto3)
│   └── notifier.py      # Discord webhooks (aiohttp)
├── docs/DESIGN.md       # architecture & roadmap
├── .env.example         # secret template (commit this, not .env)
└── requirements.txt
```

---

## Quick start (local)

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env          # fill in your keys
python main.py
```

---

## Lambda deploy

| Setting | Value |
|---|---|
| Handler | `lambda_function.lambda_handler` |
| Runtime | Python 3.12 |
| Timeout | 60–90s |
| Secrets | Lambda env vars or Secrets Manager |

**IAM (minimum):** `s3:GetObject`, `s3:PutObject`, `s3:ListBucket` on Bestiary bucket.

Package: `main.py`, `config.py`, `targets.json`, `lambda_function.py`, `services/`, dependencies — **never** include `.env`.

---

## Environment variables

Copy from [`.env.example`](.env.example). Required:

| Variable | Purpose |
|---|---|
| `SEARCH_API_KEY` | Tavily search |
| `AWS_S3_BUCKET` | Bestiary vault |
| `DISCORD_WEBHOOK_URL` | Alert channel |
| `COGNITIVE_API_KEY` | Authenticity scoring API (optional — heuristic fallback) |

On Lambda use **IAM Role** for AWS access — do not deploy `AWS_ACCESS_KEY_ID` to production.

---

## Security

- `.env` is gitignored — only `.env.example` goes to repo
- No API keys, webhooks, or credentials in source code
- Rotate keys if ever exposed in logs

---

*Portfolio project — The Witcher universe belongs to CD Projekt Red.*
