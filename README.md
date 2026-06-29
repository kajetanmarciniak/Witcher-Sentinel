# Witcher Sentinel v7 — The White Frost

[![Python](https://img.shields.io/badge/Python-3.12-blue)]()
[![AWS](https://img.shields.io/badge/AWS-Lambda%20%7C%20S3%20%7C%20EventBridge-orange)]()
[![Terraform](https://img.shields.io/badge/Terraform-IaC-844FBA)]()

Serverless OSINT agent for CD Projekt Red titles — Tavily search, S3 state, Discord alerts, async cognitive scoring, **fully declarative Terraform deployment**.

**Architecture & roadmap:** [`docs/DESIGN.md`](docs/DESIGN.md)

---

## What's new in v7

- **Immutable Infrastructure:** entire stack (Lambda, IAM, S3, EventBridge) defined in `infra/main.tf`
- **Deterministic redeploy:** `terraform apply` recreates the Sentinel in minutes
- **v6 fixes:** cognitive API concurrency semaphore + default `COGNITIVE_BASE_URL`

---

## Local development

```bash
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python main.py
```

---

## Terraform deploy

```bash
cd infra
copy terraform.tfvars.example terraform.tfvars   # fill secrets
terraform init
terraform plan
terraform apply
```

### Lambda dependencies

`archive_file` packages your source code. Third-party libs (`aiohttp`, `tavily-python`, etc.) must be installed into the project root **before** `terraform apply`:

```powershell
pip install -r requirements.txt -t . --platform manylinux2014_x86_64 --python-version 3.12 --only-binary=:all:
```

Or use a Linux/Docker build agent for production-quality Lambda layers.

### Required variables (`terraform.tfvars`)

| Variable | Description |
|----------|-------------|
| `s3_bucket_name` | Globally unique Bestiary Vault bucket |
| `cognitive_api_key` | Groq / OpenAI-compatible API key |
| `search_api_key` | Tavily API key |
| `discord_webhook_url` | Discord webhook URL |

---

## Lambda

| Handler | `lambda_function.lambda_handler` |
| Runtime | Python 3.12 |
| Timeout | 90s (configurable) |
| Auth | IAM Role only — no keys in zip |

---

*Portfolio project — The Witcher® belongs to CD Projekt Red.*
