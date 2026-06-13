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

✅ **v1.0 — The Foundation (Serverless Genesis):** Core AWS Lambda event-driven logic, fundamental SNS/S3 integration, and initial deployment of the Tavily search heuristic engine.

---

✅ **v2.0 — The Trial of the Grasses (Signal Extraction):** Advanced multi-query tracking, URL-level noise reduction, Date-Wall bypass protocols, and concurrent 48-hour sliding window implementation. Pure Witcher telemetry focus.

---

✅ **v3.0 — The S3 Conjunction (Ephemeral State Memory):** Deduplication memory module via `boto3 list_objects_v2`, Zero-Waste lifecycle storage optimization, and strict adherence to Least Privilege IAM architectures.

---

✅ **v4.0 — The Medallion's Resonance (Event-Driven Telemetry):** Transition from legacy SNS protocols to asynchronous Discord Webhook integrations. Rich Markdown payloads with direct links, timestamps, and origin metadata.

---

✅ **v5.0 — The Hunter's Mesh (Zero-Trust Evolution):** High-speed indexed memory architecture for S3 Data Lake management. Intelligence flow secured via IAM-bound contracts, deprecating linear search patterns and vulnerable access vectors.

---

✅ **v6.0 — The Elder Blood (Cognitive Intelligence):** Modular async architecture with RAG pipeline and API-driven authenticity scoring. Parallel hunt tracks, S3-backed knowledge corpus, and heuristic fallback — signals validated before any Discord alert fires.

---

📅 **v7.0 — The White Frost (Immutable Infrastructure):** Complete migration to declarative Infrastructure as Code (IaC) via Terraform. Deterministic state recreation and ephemeral environment provisioning — entire Sentinel stack redeployable in minutes.

---

📅 **v8.0 — The Black Sun (Active Cyber Defense):** AWS CloudWatch, GuardDuty telemetry streams, and real-time security logging. Automated incident triggers for unauthorized IAM calls or anomalous S3 access patterns.

---

📅 **v9.0 — The Law of Surprise (Geo-Resilient Redundancy):** Active-Passive Global Data Controller with cross-region S3 replication (CRR) and automated disaster recovery failover for AWS regional outages.

---

📅 **v10.0 — The Witcher's Legacy (Apex Autonomous Core):** Final decoupling into a headless microservice API. Custom observability dashboard and self-healing orchestration scripts, targeting 99.99% SLA for the 2027–2028 deployment window.

---

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # fill secrets locally
python main.py
```

**Lambda:** Handler `lambda_function.lambda_handler` | Timeout **60–90s** | IAM Role (no access keys in zip).

See [README.md](../README.md) for quick start.
