# 🐺 Witcher Sentinel v4: The Medallion's Resonance

**Autonomous OSINT Intelligence Agent | AWS Lambda, Tavily AI & Discord Integration**

Witcher Sentinel is a production-grade, serverless intelligence agent designed to patrol the web for official DLCs, patches, and Project Polaris (Witcher 4) updates. Following the **v4.0 "The Medallion's Resonance"** mutation, the agent has evolved from simple email alerts to sophisticated Discord Webhooks, delivering rich intelligence reports directly to dedicated secure channels.

---

### 🛠️ Key Features (Upgraded in v4)

* 🧠 **Stateful Memory (S3 Deduplication):** Syncs with historical S3 JSON archives (`O(1)` Set lookup) before every hunt. This prevents duplicate alerts and ensures that once a "monster" is caught, it never triggers the medallion again.
* 🛰️ **Passiflora Webhooks (Discord Integration):** Replaces legacy SNS emails with rich Markdown embeds. Alerts are color-coded (e.g., **IGNI Orange** for leaks/preorders) and include direct links, timestamps, and origin metadata.
* ♻️ **Zero-Waste Architecture:** "The path remains clear if no monsters are found." S3 storage and Discord triggers are only activated when genuine, filtered intelligence is gathered. Zero clutter, optimized cloud costs.
* 🛡️ **Hardened Cloud Security:** Operates under a strict **Least Privilege IAM Policy**. Environment variables (`.env`) secure all API keys, ensuring no sensitive data is ever exposed in the codebase.
* 👁️ **Multi-Track Scouting:** Simultaneously tracks multiple Witcher projects (Wild Hunt updates, Polaris/Witcher 4, Canis Majoris/Remake, and Project Sirius) using parallel AI search queries.
* ⚔️ **The Silver Sword (Noise Reduction):** Advanced Python logic filters out "illusions" such as fanart, mods, NexusMods, SEO-bait guides ("everything we know"), and Reddit rumors.

---

### 📊 Technical Architecture

| Component | Implementation |
| :--- | :--- |
| **Intelligence Engine** | Tavily AI (Advanced Search Depth + News Routing) |
| **Compute** | AWS Lambda (Python 3.12 Runtime) |
| **Stateful Storage** | Amazon S3 (Data Lake / Bestiary Vault) |
| **Communication** | Discord Webhooks (Rich Embeds via `requests`) |
| **Orchestration** | AWS EventBridge (Scheduled Cron: 24h Cycles) |
| **Security Layer** | Scoped IAM Roles & Encrypted Environment Vars |

---

### 💡 Why this pipeline is different:

* **Stateful Serverless:** It overcomes the "amnesia" of standard Lambda functions by using S3 as an active, readable memory module.
* **OSINT Precision:** This isn't a simple scraper. It's a context-aware agent that distinguishes between official studio updates and community-generated noise.
* **Cloud-First Engineering:** Built with scalability in mind, utilizing `boto3` to manage the entire lifecycle from discovery to archiving.

---

### 🚀 Roadmap

✅ v1.0 (The Foundation - Serverless Genesis): Core AWS Lambda event-driven logic, fundamental SNS/S3 integration, and initial deployment of the Tavily AI search heuristic engine.

---

✅ v2.0 (The Trial of the Grasses - Signal Extraction): Advanced multi-query tracking, URL-level cryptographic noise reduction, Date-Wall bypass protocols, and concurrent 48-hour sliding window implementation. Pure Witcher telemetry focus.

---

✅ v3.0 (The S3 Conjunction - Ephemeral State Memory): Deduplication memory module via `boto3 list_objects_v2`, Zero-Waste lifecycle storage optimization, and strict adherence to Least Privilege IAM architectures.

---

✅ v4.0 (The Medallion's Resonance - Event-Driven Telemetry): Transitioning from legacy SNS protocols to asynchronous Discord/Telegram Webhook integrations. Delivering rich HTML/Markdown payloads with direct media embedding and segmented incident-response channels.

---

📅 v5.0 (The Hunter's Mesh - Zero-Trust Architecture): Deployment of a cryptographically routed VPN mesh topology. Enabling secure, seamless VPC-to-Local tunneling for S3 data lake management, strictly deprecating any vulnerable port-forwarding vectors.

---

📅 v6.0 (The Elder Blood - Cognitive Intelligence): Integration of a Retrieval-Augmented Generation (RAG) pipeline. Deploying a local/API-driven LLM to autonomously ingest, synthesize, and heuristically score the authenticity of intercepted leaks, achieving zero-shot validation.

---

📅 v7.0 (The White Frost - Immutable Infrastructure): Complete migration to declarative Infrastructure as Code (IaC) via Terraform. Ensuring deterministic state recreation and ephemeral environment provisioning, allowing the entire Sentinel stack to be nuked and redeployed in minutes.

---

📅 v8.0 (The Black Sun - Active Cyber Defense): Implementation of AWS CloudWatch, GuardDuty telemetry streams, and real-time security logging. Automated incident triggers for unauthorized IAM calls or anomalous S3 access patterns, establishing a self-defending data perimeter.

---

📅 v9.0 (The Law of Surprise - Geo-Resilient Redundancy): Deployment of an Active-Passive Global Data Controller. Engineering cross-region S3 replication (CRR) and automated disaster recovery (DR) failover mechanisms to guarantee resilience during massive AWS regional outages.

---

📅 v10.0 (The Witcher’s Legacy - Apex Autonomous Core): Final architectural decoupling into a headless microservice API. Integration of a custom observability dashboard and self-healing orchestration scripts, securing a 99.99% SLA for the critical 2027-2028 deployment window.

---

### 📁 Setup & Usage

#### 1. Requirements
Install the necessary dependencies for local testing or Lambda packaging:
~~~bash
pip install boto3 python-dotenv tavily-python requests
~~~

#### 2. Environment Variables (`.env`)
Configure your secrets (keep them out of version control!):
~~~env
SEARCH_API_KEY=your_tavily_api_key
AWS_S3_BUCKET=your_s3_bucket_name
DISCORD_WEBHOOK_URL=your_discord_webhook_url
AWS_REGION=eu-central-1
~~~

#### 3. Execution (The Hunt) ⚔️
* **Lambda Config:** Set timeout to **30s** (required for deep AI search cycles).
* **Automation:** Connect **AWS EventBridge** to trigger the function daily.
* **Verification:** Check your Discord channel for the "Medallion Humming" alert.

---
*🛡️ Building the future of secure cloud engineering. Part of the 2026-2027 Development Journey.*
