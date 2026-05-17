import os
import json
import boto3
import logging
import requests
from datetime import datetime
from dotenv import load_dotenv
from tavily import TavilyClient

# --- INITIALIZATION & LOGGING ---
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Credentials
TAVILY_KEY = os.getenv('SEARCH_API_KEY')
BUCKET_NAME = os.getenv('AWS_S3_BUCKET')
REGION = os.getenv('AWS_REGION', 'eu-central-1')
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

# Clients
tavily = TavilyClient(api_key=TAVILY_KEY)
s3 = boto3.client('s3', region_name=REGION)
INDEX_KEY = 'Bestiary/index.json'

# Colors
COLOR_MINT = 0x00FF96
COLOR_IGNI = 0xFF9900

# --- THE MISSION CONFIGURATION ---
TARGET_GAMES = {
    "Witcher_3": {
        "queries": [
            "The Witcher 3 wild hunt new patch update dlc 2026",
            "The Witcher 3 free rewards claim digital goodies 2026",
            "The Witcher 3 seasonal event bonus items"
        ],
        "must_have": ["witcher 3", "wild hunt", "w3", "cdpr", "next-gen"],
        "triggers": ["rewards", "dlc", "patch", "update", "bonus", "myrewards", "giveaway", "freebie", "hotfix", "claim", "redeem"],
        "noise_filters": ["mod", "nexus", "fanart", "cosplay", "reddit", "guide", "walkthrough", "build", "tutorial", "how to"]
    },
    "Witcher_4": {
        "queries": [
            "The Witcher 4 Project Polaris release date trailer news 2026",
            "The Witcher 4 CD Projekt Red investor report 2026",
            "Witcher Polaris production phase status update",
            "The Witcher 4 official announcement leak 2026"
        ],
        "must_have": ["witcher 4", "project polaris", "w4", "cdpr", "cd projekt"],
        "triggers": [
            "preorder", "trailer", "release date", "launch", "leak", "announcement", 
            "price", "hardware", "requirements", "specs", "bonus", "investor", 
            "financial", "shareholder", "casting", "teaser", "confirmed"
        ],
        "noise_filters": [
            "fan cast", "concept trailer", "fanart", "unreal engine 5 showcase", 
            "reddit", "rumor", "everything we know", "ai generated", "theory", "clickbait"
        ]
    },
    "Witcher_Remake_Sirius": {
        "queries": [
            "Witcher 1 Remake Canis Majoris news 2026",
            "Witcher Sirius project multiplayer update",
            "The Molasses Flood Witcher project news"
        ],
        "must_have": ["remake", "sirius", "canis majoris", "molasses flood", "witcher"],
        "triggers": ["unreal engine 5", "gameplay", "hiring", "delay", "reveal", "announcement", "teaser", "status"],
        "noise_filters": ["mod", "original", "2007", "fanart", "cosplay", "reddit"]
    }
}

# --- THE COMMUNICATOR ---
def send_discord_notification(alerts):
    """Sends rich markdown embeds to Discord via Webhook."""
    logging.info(f"🚀 Attempting to send {len(alerts)} alerts to Discord...")
    if not alerts:
        logging.info("ℹ️ No alerts to send (Empty List).")
        return
    embeds = []
    for alert in alerts[:10]: 
        color = COLOR_IGNI if alert['type'] in ["LEAK", "TRAILER", "PREORDER"] else COLOR_MINT
        embeds.append({
            "title": f"🎯 {alert['game'].replace('_', ' ')}: {alert['type']}",
            "description": f"**[{alert['title']}]({alert['url']})**", 
            "color": color,
            "fields": [
                {"name": "📅 Published", "value": alert['published'], "inline": True},
                {"name": "🔗 Origin", "value": "Tavily Deep Search", "inline": True}
            ],
            "footer": {
                "text": "🐺 Sentinel v5.0 | The Hunter's Mesh",
            }
        })

    payload = {
        "username": "Witcher Sentinel",
        "content": f"⚔️ **Medallion Humming:** {len(alerts)} Essential Mutagens Found!",
        "embeds": embeds
    }

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        logging.info("🌸 Intelligence Relayed To Discord Passiflora")
    except Exception as e:
        logging.error(f"❌ Webhook Error: {str(e)}")
        
# --- THE MEMORY MODULE ---
def get_vaulted_urls():
    logging.info("🧠 Accessing Master Bestiary Index...")
    try:
        file_obj = s3.get_object(Bucket=BUCKET_NAME, Key=INDEX_KEY)
        return set(json.loads(file_obj['Body'].read().decode('utf-8')).get("urls", []))
    except s3.exceptions.NoSuchKey:
        logging.info("ℹ️ Master Index not found. Initiating new memory core.")
        return set()
    except Exception as e:
        logging.error(f"🔮 Telepathic interference: Illusion blocked S3 Index access: {str(e)}")
        return set()

def update_master_index(new_urls, current_vault):
    try:
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=INDEX_KEY,
            Body=json.dumps({
                "urls": list(current_vault.union(new_urls)),
                "updated_at": datetime.now().isoformat(),
                "version": "5.0"
            }, indent=4),
            ContentType='application/json'
        )
        logging.info("🏛️ Chronicles synchronized. Master Index secured.")
    except Exception as e:
        logging.error(f"🔥 Archives on fire: Failed to save Master Index: {str(e)}")

# --- THE CORE MISSION ---
def run_sentinel_mission():
    logging.info("--- 🐺 Witcher Sentinel v5.0: The Hunter's Mesh Awakens ---")
    vaulted_urls = get_vaulted_urls()
    new_discovered_urls = set()
    mission_data = {
        "timestamp": datetime.now().isoformat(),
        "alerts": [],
        "raw_results": {}
    }
    
    try:
        for game, config in TARGET_GAMES.items():
            logging.info(f"🔭 Positioning Spyglass On {game}...")
            for current_track in config.get("queries", []):
                logging.info(f"🐾 Tracking scent: {current_track}")
                search_result = tavily.search(query=current_track, search_depth="advanced", max_results=6, topic="news", days=2)
                
                if game not in mission_data["raw_results"]:
                    mission_data["raw_results"][game] = []
                mission_data["raw_results"][game].extend(search_result['results'])

                for item in search_result['results']:
                    item_url = item.get('url', '')
                    if item_url in vaulted_urls:
                        logging.info(f"♻️ Trail already tracked in The Bestiary: {item_url}. Skipping.")
                        continue
                    content_lower = (item.get('title', '') + item.get('content', '') + item.get('url', '')).lower()
                    if any(noise in content_lower for noise in config.get("noise_filters", [])):
                        logging.info(f"🪞 Illusion detected in '{item['title'][:30]}...'. Skipping.")
                        continue 
                    
                    # Context & Trigger
                    if any(name in content_lower for name in config["must_have"]):
                        for trigger in config["triggers"]:
                            if trigger in content_lower:
                                raw_date = item.get('published_date')
                                final_date = raw_date if raw_date else f"LIVE: {datetime.now().strftime('%Y-%m-%d %H:%M')}"

                                mission_data["alerts"].append({
                                    "game": game,
                                    "type": trigger.upper(),
                                    "title": item['title'],
                                    "url": item_url,
                                    "published": final_date 
                                })
                                new_discovered_urls.add(item_url)
                                break

        # Notice & Archive
        if mission_data["alerts"]:
            logging.warning(f"⚔️ Medallion Humming: {len(mission_data['alerts'])} Anomalies Detected!")
            send_discord_notification(mission_data["alerts"])
            
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
            update_master_index(new_discovered_urls, vaulted_urls)
        else:
            logging.info("🕊️ The Path Is Clear: No Monsters Found. The Vault remains closed.")

    except Exception as e:
        logging.error(f"☄️ The Cataclysm: System Failed To Respond: {str(e)}")

# --- THE LAMBDA GATEWAY ---
def lambda_handler(event, context):
    logging.info("--- 🐺 Witcher Sentinel v5.0: The Medallion Awakens ---")
    
    try:
        # Startup
        run_sentinel_mission()
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': '⚔️ Hunt Successful: Intelligence Gathered and Vaulted.',
                'timestamp': datetime.now().isoformat()
            })
        }
    except Exception as e:
        # Error Logs
        logging.error(f"❄️ The White Frost, All Systems Frozen: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': '🔥 Conjunction Of Spheres: Total System Collapse',
                'details': str(e)
            })
        }
        
if __name__ == "__main__":
    run_sentinel_mission()
