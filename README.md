# 🐺 Witcher Sentinel v3: Serverless OSINT Intelligence Agent

**Autonomous Web Scouting for CD Projekt RED Ecosystem | Powered by Tavily AI, AWS Lambda & SNS**

Stop hunting for leaks and updates manually. Witcher Sentinel is a production-grade, event-driven intelligence agent that patrols the web for official DLCs, patches, and Project Polaris (Witcher 4) news. Following the **v3.1 "S3 Conjunction" mutation**, the Sentinel now possesses stateful cloud memory, zero-waste storage logic, and hardened IAM security policies to deliver flawless, zero-spam intelligence reports.

---

### 🛠️ Key Features (Upgraded in v3)

* 🧠 **Stateful Memory (S3 Deduplication):** The agent syncs with past S3 JSON archives (`O(1)` Set lookup) before hunting. It remembers past bounties and guarantees absolute zero duplication across wider timeframes.
* ♻️ **Zero-Waste Architecture:** "The Vault remains closed if no monsters are found." S3 storage is only utilized when genuine, filtered intelligence is gathered. Zero empty JSONs, zero clutter, optimized cloud costs.
* 🛡️ **Least Privilege IAM Security:** Cloud execution roles are strictly scoped. The Sentinel operates within a hardened AWS IAM policy, restricted to specific `s3:ListBucket` and `s3:PutObject` actions exclusively on the designated vault.
* 👁️ **AI-Powered Multi-Track Scouting:** Deep-web analysis via Tavily AI deploying multiple parallel queries (e.g., separating hardware specs from DLC news) for extreme precision.
* ⚔️ **The Silver Sword (Noise Reduction):** Hardened Python logic scans article titles, content, and URLs to instantly banish illusions (fanart, mods, NexusMods, Reddit rumors, and fan-casts).
* ⚡ **Serverless Compute:** Fully hosted on AWS Lambda (Python 3.12). Zero server maintenance, automated scaling, and execution times under 800ms.
* 📬 **Passiflora Relay (SNS):** Real-time AWS SNS integration delivers formatted "Witcher's Ledger" intelligence reports directly to your inbox.

---

### 📊 Technical Architecture

| Feature | Implementation |
| :--- | :--- |
| **Brain** | Tavily AI (Advanced Search Depth + News Topic Routing) |
| **Compute** | AWS Lambda (Python 3.12 Runtime) |
| **Storage** | Amazon S3 (Bronze Data Lake / Bestiary Vault) |
| **Alerting** | Amazon SNS (Simple Notification Service) |
| **Scheduling** | AWS EventBridge (Cron: 24h Cycles) |
| **Security** | IAM Scoped Policies & Environment Variables (`.env`) |

---

### 💡 Why this pipeline is different:

* **Cloud-Native & Stateful:** Built natively with `boto3`. It solves the problem of statefulness in stateless serverless environments by turning an S3 bucket into an active, readable memory module.
* **Hot Update Ready:** The separation of core logic from package dependencies allows for instant zero-downtime deployments via AWS Console without repacking `.zip` layers.
* **Clean Reporting:** Automatically formats raw JSON payloads into a readable, lore-friendly email template.

---

### 🚀 Roadmap

* ✅ **v1.0 (Foundation):** Core AWS Lambda logic, basic AWS SNS/S3 integration, and initial Tavily AI search.
* ✅ **v2.0 (The Trial of the Grasses):** Multi-query tracking, URL-level noise reduction, Date-Wall bypass, and 48-hour sliding window implementation. Pure Witcher focus.
* ✅ **v3.0 (The S3 Conjunction):** Deduplication memory module via `boto3` `list_objects_v2`, Zero-Waste storage optimization, and Least Privilege IAM policies.
* 📅 **v4.0 (The Medallion's Resonance - Rich Webhooks):** Transitioning from plain SNS emails to Discord/Telegram Webhook integrations, providing rich HTML/Markdown embeds with direct image links and categorized alert channels.
* 📅 **v5.0 (The Hunter's Mesh - Secure Architecture):** Implementation of a VPN mesh network layer to securely manage the cloud infrastructure and access S3 data lakes directly from the local development environment, eliminating any need for vulnerable port forwarding.

---

### 📁 Setup & Usage

#### 1. Requirements
Install the necessary dependencies locally for testing or packaging within your `.venv`:
~~~bash
pip install boto3 python-dotenv tavily-python
~~~

#### 2. Environment Variables (`.env` / AWS Config)
The Sentinel requires the following variables to be set within the AWS Lambda Environment Variables (or a local `.env` file for testing). **Never commit these to GitHub!**

~~~env
SEARCH_API_KEY=your_tavily_key
AWS_S3_BUCKET=your_witcher_vault
AWS_SNS_TOPIC_ARN=your_sns_arn
AWS_REGION=eu-central-1
~~~

#### 3. Deployment & Execution (The Hunt) ⚔️
* **Deploy:** Paste the `v3.0` Python code directly into your AWS Lambda function *(Zero-Downtime Deployment, no new layers required if v1.0 libraries are present)*.
* **Configuration:** Set the Lambda Timeout to **30s** in General Configuration *(Critical for deep AI search cycles via Tavily)*.
* **Automate:** Ensure **AWS EventBridge** is connected to trigger the function on your preferred schedule (e.g., daily at 12:00 UTC).
* **Verification:**
  * 📬 Check your SNS-linked email for the "Witcher's Ledger" report.
  * 🗄️ Navigate to your S3 Bucket to find the archived JSON in the `Bestiary/` folder.

---
*🛡️ Building the future of secure cloud engineering. Part of the 2026-2027 Development Journey.*
