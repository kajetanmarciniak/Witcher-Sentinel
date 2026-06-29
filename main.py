import asyncio
import json
import logging
from datetime import datetime

import aiohttp

from config import settings
from services.cognitive import CognitiveEngine, hunt_track
from services.notifier import DiscordNotifier
from services.s3_vault import S3Vault

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


async def run_mission() -> dict:
    logger.info("--- Witcher Sentinel v7.0: The White Frost Awakens ---")
    vault = S3Vault()
    vaulted, rag = await vault.bootstrap()
    mission = {
        "timestamp": datetime.now().isoformat(), "version": settings.version,
        "scoring_engine": settings.cognitive_model if settings.cognitive_api_key else "heuristic",
        "alerts": [], "filtered_out": [], "raw_results": {},
    }

    async with aiohttp.ClientSession() as session:
        cognitive = CognitiveEngine(session)
        notifier = DiscordNotifier(session, cognitive)
        if not cognitive.enabled:
            logger.warning("COGNITIVE_API_KEY or COGNITIVE_BASE_URL missing — heuristic fallback only.")

        outcomes = await asyncio.gather(*[
            hunt_track(g, c, q, cognitive, rag, vaulted)
            for g, c in settings.games.items() for q in c.get("queries", [])
        ])
        for game, results, alerts, rejected in outcomes:
            mission["raw_results"].setdefault(game, []).extend(results)
            mission["alerts"].extend(alerts)
            mission["filtered_out"].extend(rejected)

        if mission["alerts"]:
            logger.warning("Medallion humming: %d validated anomalies.", len(mission["alerts"]))
            await notifier.send(mission["alerts"])
            await vault.persist_hunt(mission, {a["url"] for a in mission["alerts"]}, vaulted)
        else:
            n = len(mission["filtered_out"])
            logger.info("Path clear.%s", f" {n} signals rejected." if n else "")
    return mission


def lambda_handler(event, context):
    try:
        asyncio.run(run_mission())
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Hunt successful: intelligence validated and vaulted.",
                "timestamp": datetime.now().isoformat(),
                "version": settings.version,
            }),
        }
    except Exception as exc:
        logger.error("Mission failed: %s", exc)
        return {"statusCode": 500, "body": json.dumps({"error": "Mission collapse"})}


if __name__ == "__main__":
    asyncio.run(run_mission())
