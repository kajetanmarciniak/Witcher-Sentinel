🐺 Witcher Sentinel v1.0: Serverless OSINT Intelligence Agent

Autonomous Web Scouting for CD Projekt RED Ecosystem | Powered by Tavily AI, AWS Lambda & SNS

Stop hunting for leaks and updates manually. Witcher Sentinel is a production-grade, event-driven intelligence agent that patrols the web for official DLCs, patches, and Project Polaris (Witcher 4) news. It transforms raw search data into filtered, high-value email alerts and secure cloud archives.
🛠️ Key Features

    🧠 AI-Powered Scouting: Deep-web analysis via Tavily AI. Unlike standard scrapers, it uses advanced search depth to find buried "mutagens" (leaks and rewards).

    ⚡ Serverless Architecture: Fully hosted on AWS Lambda. Zero server maintenance, ultra-low cost, and scales automatically.

    🛡️ Smart "Date-or-Vault" Logic: Dual-stream data processing. Confirmed daily news triggers an immediate SNS Alert, while unverified data is stored in the S3 Archive.

    🏛️ Vivaldi Bank Vault (S3): Automated daily archiving. Every "Hunt" is logged as a structured JSON in Amazon S3, creating a historical database of CDPR developments.

    📬 Passiflora Relay (SNS): Real-time notification system. Integration with Amazon SNS delivers formatted intelligence reports directly to your inbox.

    ⚔️ Context-Aware Filtering: Hardened logic using must_have and trigger tokens to eliminate clickbait and irrelevant search results.

📊 Technical Architecture
Feature	Implementation
Brain	Tavily AI (Advanced Search Depth)
Compute	AWS Lambda (Python 3.12 Runtime)
Storage	Amazon S3 (Data Lake Archiving)
Alerting	Amazon SNS (Simple Notification Service)
Scheduling	AWS EventBridge (Cron: 12h Cycles)
Security	IAM Role-based Access & Environment Variables
💡 Why this pipeline is different:

    🚀 Zero Noise: The system doesn't just find "Witcher", it looks for specific triggers like "rewards", "patch", or "preorder".

    🔐 Cloud-Native: Built with boto3 and AWS SDK. No local resources required – the agent lives entirely in the cloud.

    🧹 Clean Reporting: Automatically formats raw JSON into a readable "Witcher’s Ledger" email template.

🚀 Roadmap

    ✅ v1.0 (Foundation): Core AWS Lambda logic & Tavily AI advanced search integration.

    📅 v1.1 (Automation): Event-driven architecture via AWS EventBridge (12h cycles) and SNS email relay.

    📅 v2.0 (The Night City Expansion):

        Implementation of Cyberpunk 2077 & Project Orion sectors.

        Advanced metadata filtering for "My Rewards" and UE5 development leaks.

    📅 v3.0 (Infrastructure as Code): Transition from manual AWS Console setup to Terraform for one-click environment deployment.

    📅 v4.0 (AI Watcher): Implementation of a local LLM "Watcher" for deeper semantic analysis of gathered intelligence.
    
📁 Setup & Usage
1. Requirements
Bash

pip install boto3 python-dotenv tavily-python

2. Environment Configuration

Create an AWS Lambda Environment Variable or a local .env file:
Fragment kodu

SEARCH_API_KEY=your_tavily_key
AWS_S3_BUCKET=your_witcher_vault
AWS_SNS_TOPIC_ARN=your_sns_arn
AWS_REGION=eu-central-1

3. Deployment

    Upload the script to AWS Lambda.

    Set Timeout to 30s (Critical for AI search depth).

    Add EventBridge Trigger with rate(12 hours).

    Check your S3 Bucket for the daily Bestiary/ reports.

Building the future of personal data engineering. Part of the 2026-2027 Development Journey.
