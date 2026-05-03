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

* ✅ **v1.0 (Foundation):** Core AWS Lambda logic, basic AWS SNS/S3 integration, and initial Tavily AI search.
* ✅ **v2.0 (The Trial of the Grasses):** Multi-query tracking, URL-level noise reduction, Date-Wall bypass, and 48-hour sliding window implementation. Pure Witcher focus.
* ✅ **v3.0 (The S3 Conjunction):** Deduplication memory module via `boto3` `list_objects_v2`, Zero-Waste storage optimization, and Least Privilege IAM policies.
* ✅ **v4.0 (The Medallion's Resonance - Rich Webhooks):** Transitioning from plain SNS emails to Discord/Telegram Webhook integrations, providing rich HTML/Markdown embeds with direct image links and categorized alert channels.
* 📅 **v5.0 (The Hunter's Mesh - Secure Architecture):** Implementation of a VPN mesh network layer to securely manage the cloud infrastructure and access S3 data lakes directly from the local development environment, eliminating any need for vulnerable port forwarding.
* 📅 **v6.0 (The Elder Blood - Predictive Synthesis):** Integration of a cognitive LLM layer to autonomously read, summarize, and score the authenticity of intercepted leaks, transforming the agent into an intelligent analyst and eliminating the need to manually verify false positives.

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
