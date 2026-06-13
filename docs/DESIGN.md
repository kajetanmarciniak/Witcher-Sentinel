# Witcher Sentinel v6: The Elder Blood

**Autonomous OSINT Intelligence Agent | AWS Lambda, Tavily, RAG & Discord**

Witcher Sentinel patrols the web for official DLCs, patches, and Project Polaris (Witcher 4) updates. v6 adds a cognitive layer: RAG-backed scoring validates signal authenticity before any alert fires.

---

## Key Features (v6)

* **Cognitive Engine:** Async remote API (`aiohttp`) scores each candidate 0–100 with verdict and reasoning. Heuristic fallback when API is unavailable.
* **RAG Vault:** S3-backed knowledge corpus and recent contracts injected into scoring context.
* **Stateful Memory (S3):** Master index deduplication (`O(1)` set lookup) before every hunt.
* **Passiflora Webhooks:** Rich Discord embeds with authenticity score, verdict, and color-coded severity.
* **Zero-Waste Architecture:** S3 writes and Discord triggers only on validated intelligence.
* **Modular Async Core:** `asyncio.gather` for parallel track scouting and concurrent candidate evaluation.
* **Silver Sword:** Noise filters from `targets.json` — no keywords hardcoded in Python.

---

## Technical Architecture

| Component | Implementation |
| :--- | :--- |
| **Search Engine** | Tavily (advanced depth + news routing) |
| **Cognitive Layer** | Chat-completions API via `aiohttp` |
| **RAG** | S3 knowledge base + token-overlap retrieval |
| **Compute** | AWS Lambda (Python 3.12, `asyncio`) |
| **Stateful Storage** | Amazon S3 (Bestiary Vault) |
| **Communication** | Discord Webhooks (`aiohttp`) |
| **Orchestration** | AWS EventBridge (24h cron) |
| **Security** | IAM Least Privilege, env vars / Secrets Manager |

### Module Layout

```
main.py               → orchestrator + lambda_handler
config.py             → Settings from .env + targets.json
targets.json          → hunt targets, filters, trusted domains
services/cognitive.py → scoring + hunt_track pipeline
services/s3_vault.py  → RagVault, index, archive
services/notifier.py  → Discord webhooks
lambda_function.py    → AWS handler alias
```

---

## Roadmap

| Version | Codename | Status |
| :--- | :--- | :--- |
| v1.0 | The Foundation | Done |
| v2.0 | The Trial of the Grasses | Done |
| v3.0 | The S3 Conjunction | Done |
| v4.0 | The Medallion's Resonance | Done |
| v5.0 | The Hunter's Mesh | Done |
| v6.0 | The Elder Blood | **Done** |
| v7.0 | The White Frost (Terraform IaC) | Planned |
| v8.0 | The Black Sun (GuardDuty / CloudWatch) | Planned |
| v9.0 | The Law of Surprise (CRR / DR) | Planned |
| v10.0 | The Witcher's Legacy (Microservice API) | Planned |

---

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # fill secrets locally
python main.py
```

**Lambda:** Handler `lambda_function.lambda_handler` | Timeout **60–90s** | IAM Role (no access keys in zip).

See [README.md](../README.md) for full deploy and security notes.
