# 🐺 Witcher Sentinel v2.0: Serverless OSINT Intelligence Agent

**Autonomous Web Scouting for CD Projekt RED Ecosystem | Powered by Tavily AI, AWS Lambda & SNS**

Stop hunting for leaks and updates manually. Witcher Sentinel is a production-grade, event-driven intelligence agent that patrols the web for official DLCs, patches, and Project Polaris (Witcher 4) news. Following the **v2.0 "Trial of the Grasses" mutation**, the Sentinel now possesses advanced noise-reduction capabilities, multi-track hunting, and time-boxed sliding windows to deliver zero-spam, high-value intelligence reports.

---

### 🛠️ Key Features (Upgraded in v2.0)

* 🧠 **AI-Powered Multi-Track Scouting:** Deep-web analysis via Tavily AI. Instead of a single broad search, v2.0 deploys multiple parallel queries (e.g., separating hardware specs from DLC news) for extreme precision.
* ⚔️ **The Silver Sword (Noise Reduction):** Hardened logic that scans article titles, content, and URLs to instantly banish illusions (fanart, mods, NexusMods, Reddit rumors, and fan-casts). You only get official "mutagens".
* ⏱️ **Sliding Window Filtering (Time-Box):** Forces the AI to only analyze the last 48 hours of global web data (`days=2`). Eliminates old forum posts and prevents duplicate alerts on consecutive days.
* 🛡️ **Date-Wall Fallback:** Intelligent metadata parsing. If target sites have broken schemas or missing publication dates, the Sentinel no longer crashes; it securely tags the anomaly with a live UTC detection timestamp.
* ⚡ **Serverless Architecture:** Fully hosted on AWS Lambda. Zero server maintenance, ultra-low cost, and scales automatically.
* 🏛️ **Vivaldi Bank Vault (S3):** Automated daily archiving. Every "Hunt" is logged as a structured JSON in Amazon S3, creating a historical data lake.
* 📬 **Passiflora Relay (SNS):** Real-time AWS SNS integration delivers formatted "Witcher's Ledger" intelligence reports directly to your inbox.

---

### 📊 Technical Architecture

| Feature | Implementation |
| :--- | :--- |
| **Brain** | Tavily AI (Advanced Search Depth + News Topic Routing) |
| **Compute** | AWS Lambda (Python 3.12 Runtime) |
| **Storage** | Amazon S3 (Data Lake Archiving) |
| **Alerting** | Amazon SNS (Simple Notification Service) |
| **Scheduling** | AWS EventBridge (Cron: 24h Cycles @ 12:00 UTC) |
| **Security** | IAM Role-based Access & Environment Variables (`.env`) |

---

### 💡 Why this pipeline is different:

* **Zero Noise:** The system doesn't just find "Witcher". It requires explicit contextual triggers ("rewards", "patch", "preorder") and survives the Silver Sword filter before alerting.
* **Cloud-Native:** Built natively with `boto3` and AWS SDK. The agent lives entirely in the cloud, utilizing a true Zero-Downtime deployment model.
* **Clean Reporting:** Automatically formats raw JSON payloads into a readable, lore-friendly "Witcher’s Ledger" email template.

---

### 🚀 Roadmap

* ✅ **v1.0 (Foundation):** Core AWS Lambda logic, basic AWS SNS/S3 integration, and initial Tavily AI search.
* ✅ **v2.0 (The Trial of the Grasses):** Multi-query tracking, URL-level noise reduction, Date-Wall bypass, and 48-hour sliding window implementation. Pure Witcher focus.
* 📅 **v3.0 (The S3 Conjunction - Deduplication):** Leveraging existing S3 JSON archives to cross-reference previously discovered URLs, ensuring absolute zero duplication across wider timeframes without adding new database costs.
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
* **Deploy:** Paste the `v2.0` Python code directly into your AWS Lambda function *(Zero-Downtime Deployment, no new layers required if v1.0 libraries are present)*.
* **Configuration:** Set the Lambda Timeout to **30s** in General Configuration *(Critical for deep AI search cycles via Tavily)*.
* **Automate:** Ensure **AWS EventBridge** is connected to trigger the function on your preferred schedule (e.g., daily at 12:00 UTC).
* **Verification:**
  * 📬 Check your SNS-linked email for the "Witcher's Ledger" report.
  * 🗄️ Navigate to your S3 Bucket to find the archived JSON in the `Bestiary/` folder.

---
*🛡️ Building the future of secure cloud engineering. Part of the 2026-2027 Development Journey.*
