# Witcher Sentinel v7: The White Frost

**Autonomous OSINT Intelligence Agent | Terraform IaC, AWS Lambda, Tavily, RAG & Discord**

Witcher Sentinel patrols the web for official DLCs, patches, and Project Polaris (Witcher 4) updates. v7 migrates the entire stack to declarative Infrastructure as Code — redeployable in minutes.

---

## Key Features (v7)

* **Immutable Infrastructure:** Terraform manages Lambda, IAM, S3 Bestiary Vault, and EventBridge schedule.
* **Deterministic State:** `terraform apply` / `destroy` recreates or tears down the full Sentinel stack.
* **Cognitive Engine (v6 carry-over):** Async remote API scores each candidate 0–100 with verdict and reasoning. Concurrency capped via semaphore.
* **RAG Vault:** S3-backed knowledge corpus and recent contracts injected into scoring context.
* **Zero-Waste Architecture:** S3 writes and Discord triggers only on validated intelligence.
* **Modular Async Core:** `asyncio.gather` for parallel track scouting and concurrent candidate evaluation.

---

## Technical Architecture

| Component | Implementation |
| :--- | :--- |
| **Infrastructure** | Terraform (`infra/main.tf`) |
| **Search Engine** | Tavily (advanced depth + news routing) |
| **Cognitive Layer** | Chat-completions API via `aiohttp` |
| **RAG** | S3 knowledge base + token-overlap retrieval |
| **Compute** | AWS Lambda (Python 3.12, `asyncio`) |
| **Stateful Storage** | Amazon S3 (Bestiary Vault) |
| **Communication** | Discord Webhooks (`aiohttp`) |
| **Orchestration** | AWS EventBridge (configurable schedule) |
| **Security** | IAM Least Privilege, Terraform-managed secrets via variables |

### Module Layout

```
main.py               → orchestrator + lambda_handler
config.py             → Settings from .env + targets.json
targets.json          → hunt targets, filters, trusted domains
services/cognitive.py → scoring + hunt_track pipeline
services/s3_vault.py  → RagVault, index, archive
services/notifier.py  → Discord webhooks
lambda_function.py    → AWS handler alias
infra/main.tf         → Terraform — Lambda, IAM, S3, EventBridge
```

---

## Roadmap

✅ **v1.0 — The Foundation (Serverless Genesis):** Core AWS Lambda event-driven logic, fundamental SNS/S3 integration, and initial deployment of the Tavily search heuristic engine.

✅ **v2.0 — The Trial of the Grasses (Signal Extraction):** Advanced multi-query tracking, URL-level noise reduction, Date-Wall bypass protocols, and concurrent 48-hour sliding window implementation.

✅ **v3.0 — The S3 Conjunction (Ephemeral State Memory):** Deduplication memory module via `boto3 list_objects_v2`, Zero-Waste lifecycle storage optimization, and strict adherence to Least Privilege IAM architectures.

✅ **v4.0 — The Medallion's Resonance (Event-Driven Telemetry):** Transition from legacy SNS protocols to asynchronous Discord Webhook integrations.

✅ **v5.0 — The Hunter's Mesh (Zero-Trust Evolution):** High-speed indexed memory architecture for S3 Data Lake management.

✅ **v6.0 — The Elder Blood (Cognitive Intelligence):** Modular async architecture with RAG pipeline and API-driven authenticity scoring.

✅ **v7.0 — The White Frost (Immutable Infrastructure):** Complete migration to declarative Infrastructure as Code (IaC) via Terraform. Deterministic state recreation and ephemeral environment provisioning — entire Sentinel stack redeployable in minutes.

📅 **v8.0 — The Black Sun (Active Cyber Defense):** AWS CloudWatch, GuardDuty telemetry streams, and real-time security logging.

📅 **v9.0 — The Law of Surprise (Geo-Resilient Redundancy):** Cross-region S3 replication (CRR) and automated disaster recovery failover.

📅 **v10.0 — The Witcher's Legacy (Apex Autonomous Core):** Headless microservice API with custom observability dashboard.

---

## Setup

**Local:**
```bash
pip install -r requirements.txt
cp .env.example .env
python main.py
```

**Deploy:**
```bash
cd infra && terraform init && terraform apply
```

See [README.md](../README.md) for full deploy instructions.
