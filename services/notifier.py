import logging

import aiohttp

from config import settings
from services.cognitive import CognitiveEngine

logger = logging.getLogger(__name__)


class DiscordNotifier:
    """Async Discord webhook relay with cognitive metadata."""

    def __init__(self, session: aiohttp.ClientSession, cognitive: CognitiveEngine):
        self._session = session
        self._webhook_url = settings.discord_webhook_url
        self._cognitive = cognitive

    async def send(self, alerts: list[dict]) -> None:
        if not alerts:
            return

        logger.info("Sending %d alerts to Discord...", len(alerts))
        embeds = [self._build_embed(alert) for alert in alerts[:10]]
        payload = {
            "username": "Witcher Sentinel",
            "content": f"⚔️ **Medallion Humming:** {len(alerts)} Signals Validated By Elder Blood!",
            "embeds": embeds,
        }

        try:
            async with self._session.post(
                self._webhook_url,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=settings.discord_timeout),
            ) as response:
                response.raise_for_status()
                logger.info("Intelligence relayed to Discord.")
        except Exception as exc:
            logger.error("Discord webhook error: %s", exc)

    def _build_embed(self, alert: dict) -> dict:
        cog = alert.get("cognitive", {})
        verdict = cog.get("verdict", "UNKNOWN")
        return {
            "title": f"🎯 {alert['game'].replace('_', ' ')}: {alert['type']}",
            "description": f"**[{alert['title']}]({alert['url']})**",
            "color": self._cognitive.embed_color(verdict),
            "fields": [
                {"name": "📅 Published", "value": alert["published"], "inline": True},
                {"name": "🧬 Authenticity", "value": f"{cog.get('authenticity_score', '?')}/100", "inline": True},
                {"name": "⚖️ Verdict", "value": verdict, "inline": True},
                {"name": "🔮 Reasoning", "value": cog.get("reasoning", "N/A")[:1024], "inline": False},
                {"name": "🔗 Origin", "value": f"Tavily + {cog.get('source', 'scoring')}", "inline": True},
            ],
            "footer": {"text": "🐺 Sentinel v7.0 | The White Frost"},
        }
