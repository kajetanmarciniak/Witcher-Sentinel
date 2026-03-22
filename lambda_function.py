import os
import json
import boto3
import logging
from datetime import datetime
from dotenv import load_dotenv
from tavily import TavilyClient

# --- INITIALIZATION & LOGGING ---
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Credentials
TAVILY_KEY = os.getenv('SEARCH_API_KEY')
BUCKET_NAME = os.getenv('AWS_S3_BUCKET')
SNS_ARN = os.getenv('AWS_SNS_TOPIC_ARN')
REGION = os.getenv('AWS_REGION', 'eu-central-1')

# Clients
tavily = TavilyClient(api_key=TAVILY_KEY)
s3 = boto3.client('s3', region_name=REGION)
sns = boto3.client('sns', region_name=REGION)

# --- THE MISSION CONFIGURATION ---
TARGET_GAMES = {
    "Witcher_3": {
        "query": "The Witcher 3 new free rewards DLC updates patches 2026",
        "must_have": ["witcher 3", "wild hunt", "w3", "cdpr"],
        "triggers": ["rewards", "dlc", "patch", "update", "bonus", "myrewards"]
    },
    "Witcher_4": {
        "query": "The Witcher 4 Project Polaris release date trailer preorder leaks news",
        "must_have": ["witcher 4", "project polaris", "w4", "cdpr"],
        "triggers": ["preorder", "trailer", "release date", "launch", "leak", "announcement", "rewards", "myrewards", "price"]
    }
}

# --- HELPER FUNCTIONS ---

def generate_email_body(alerts):
    header = "🐺 The Witcher’s Ledger ⚔️\n"
    divider = "=" * 45 + "\n"
    body = header + divider + f"Scent Picked Up {len(alerts)} Essential Mutagens Found At {datetime.now().strftime('%H:%M')}\n\n"

    for i, a in enumerate(alerts, 1):
        body += f"{i}. 🎯 TARGET: {a['game'].replace('_', ' ')}\n"
        body += f"   🚩 TYPE: {a['type']}\n"
        body += f"   📰 TITLE: {a['title']}\n"
        body += f"   📅 DATE: {a['published']}\n"
        body += f"   🔗 LINK: {a['url']}\n"
        body += "-" * 20 + "\n"

    footer = "\n🛡️ SYSTEM STATUS: ACTIVE\n"
    footer += "📍 INFRASTRUCTURE: AWS Cloud (eu-central-1)\n"
    footer += "🤖 GEN: Sentinel-v1\n"
    return body + footer

def send_sns_notification(alerts):
    """Sends the report to your email."""
    if not alerts:
        return
    
    try:
        subject = f"🐺 Witcher Alert: {len(alerts)} The Medallion Trembles: Items Detected"
        message = generate_email_body(alerts)
        
        sns.publish(
            TopicArn=SNS_ARN,
            Subject=subject,
            Message=message
        )
        logging.info("🌸 Intelligence Relayed To The Passiflora")
    except Exception as e:
        logging.error(f"❌ SNS Error: {str(e)}")

# --- THE CORE MISSION ---

def run_sentinel_mission():
    logging.info("--- 🐺 Witcher Sentinel v1.0: ON THE TRAIL ---")
    
    mission_data = {
        "timestamp": datetime.now().isoformat(),
        "alerts": [],
        "raw_results": {}
    }

    try:
        for game, config in TARGET_GAMES.items():
            logging.info(f"[*] Positioning Spyglass On  {game}...")
            # Advanced search for deeper links
            search_result = tavily.search(query=config["query"], search_depth="advanced", max_results=6)
            mission_data["raw_results"][game] = search_result['results']

            for item in search_result['results']:
                content_lower = (item.get('title', '') + item.get('content', '')).lower()
                
                # Context & Trigger
                if any(name in content_lower for name in config["must_have"]):
                    for trigger in config["triggers"]:
                        if trigger in content_lower:
                            mission_data["alerts"].append({
                                "game": game,
                                "type": trigger.upper(),
                                "title": item['title'],
                                "url": item.get('url'),
                                "published": item.get('published_date', 'Unknown')
                            })
                            break

        # Notice
        if mission_data["alerts"]:
            logging.warning(f"⚔️ Medallion Humming: {len(mission_data['alerts'])} Anomalies Detected!")
            send_sns_notification(mission_data["alerts"])
        else:
            logging.info("🕊️ The Path Is Clear: No Monsters Found.")

        # Archive to S3
        folder = datetime.now().strftime('%Y-%m-%d')
        filename = f"Contract_Fulfilled_At_{datetime.now().strftime('%H%M')}.json"
        s3_key = f"Bestiary/{folder}/{filename}"

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=json.dumps(mission_data, indent=4, ensure_ascii=False),
            ContentType='application/json'
        )
        logging.info(f"🏛️ Records Secured In The Vivaldi Bank Vault: {s3_key}")

    except Exception as e:
        logging.error(f"☄️ The Cataclysm: System Failed To Respond: {str(e)}")

# --- THE LAMBDA GATEWAY ---

def lambda_handler(event, context):
    logging.info("--- 🐺 Witcher Sentinel: The Medallion Awakens ---")
    
    try:
        # Startup
        run_sentinel_mission()
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': '⚔️ Hunt Succesful: Intelligence Gathered and Vaulted.',
                'timestamp': datetime.now().isoformat()
            })
        }
    except Exception as e:
        # Error Logs
        logging.error(f"❄️ The White Frost, All Processes Frozen: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': '🔥 Conjunction Of Spheres: Total System Collapse',
                'details': str(e)
            })
        }