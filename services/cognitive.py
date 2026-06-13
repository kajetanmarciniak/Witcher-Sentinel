import asyncio
import json
import logging
import re
from datetime import datetime

import aiohttp
from tavily import TavilyClient

from config import settings

logger = logging.getLogger(__name__)
_tavily = TavilyClient(api_key=settings.tavily_key)


class CognitiveEngine:
    """Async authenticity scorer via remote API + RAG context."""

    VERDICT_COLORS = {
        "OFFICIAL": settings.color_mint,
        "CREDIBLE_LEAK": settings.color_igni,
        "RUMOR": settings.color_elder,
        "NOISE": settings.color_noise,
    }

    def __init__(self, session: aiohttp.ClientSession):
        self._session = session
        self._api_key = settings.cognitive_api_key
        self._model = settings.cognitive_model
        self._base_url = settings.cognitive_base_url.rstrip("/")
        self._threshold = settings.authenticity_threshold
        self.enabled = bool(self._api_key)

    async def evaluate(self, item: dict, game: str, trigger: str, rag_context: list[dict]) -> dict:
        if not self.enabled:
            return self._heuristic_fallback(item, trigger)

        domain = self._extract_domain(item.get("url", ""))
        trusted = domain in settings.trusted_domains
        user_prompt = self._build_prompt(item, game, trigger, trusted, rag_context)

        try:
            async with self._session.post(
                f"{self._base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self._model,
                    "temperature": 0.1,
                    "response_format": {"type": "json_object"},
                    "messages": [
                        {"role": "system", "content": self._system_prompt()},
                        {"role": "user", "content": user_prompt},
                    ],
                },
                timeout=aiohttp.ClientTimeout(total=settings.cognitive_timeout),
            ) as response:
                response.raise_for_status()
                payload = await response.json()
                result = json.loads(payload["choices"][0]["message"]["content"])
                result["source"] = "api"
                result["model"] = self._model
                logger.info(
                    "Cognitive verdict: %s (%s) — %s",
                    result.get("verdict"),
                    result.get("authenticity_score"),
                    item.get("title", "")[:40],
                )
                return result
        except Exception as exc:
            logger.error("Cognitive engine failure, heuristic fallback: %s", exc)
            return self._heuristic_fallback(item, trigger)

    def passes_threshold(self, result: dict) -> bool:
        if result.get("recommended_action") == "DISCARD":
            return False
        return result.get("authenticity_score", 0) >= self._threshold

    def embed_color(self, verdict: str) -> int:
        return self.VERDICT_COLORS.get(verdict, settings.color_mint)

    def _system_prompt(self) -> str:
        return (
            "Witcher Sentinel authenticity scoring module. Evaluate gaming news for the specified GAME TRACK only. "
            "CRITICAL DIRECTIVE 1: If the article covers a different title than the GAME TRACK, return verdict 'NOISE', score 0, action 'DISCARD'. "
            "CRITICAL DIRECTIVE 2: If the article is not in English or Polish, return 'NOISE', score 0. "
            "Return ONLY valid JSON with keys: authenticity_score (0-100), verdict (OFFICIAL|CREDIBLE_LEAK|RUMOR|NOISE), "
            "confidence (HIGH|MEDIUM|LOW), reasoning (max 2 sentences), recommended_action (ALERT|MONITOR|DISCARD)."
        )

    def _build_prompt(self, item: dict, game: str, trigger: str, trusted: bool, rag_context: list[dict]) -> str:
        context_block = self._format_rag_context(rag_context)
        return f"""Analyze this intercepted signal:

GAME TRACK: {game}
TRIGGER: {trigger}
TITLE: {item.get('title', '')}
URL: {item.get('url', '')}
DOMAIN TRUSTED: {trusted}
CONTENT SNIPPET: {item.get('content', '')[:800]}

RAG CONTEXT:
{context_block}

Scoring guide:
- 90-100: Official CDPR/studio source or major outlet citing primary source
- 70-89: Credible industry reporting, plausible leak with corroboration
- 40-69: Unverified rumor, single anonymous source
- 0-39: Fan content, SEO bait, mod, or clear misinformation"""

    def _format_rag_context(self, rag_context: list[dict]) -> str:
        if not rag_context:
            return "No historical context available."
        return "\n".join(
            f"{i}. [{e.get('title')}] {e.get('url')} — {e.get('summary', '')}"
            for i, e in enumerate(rag_context, 1)
        )

    def _extract_domain(self, url: str) -> str:
        match = re.search(r"https?://(?:www\.)?([^/]+)", url or "")
        return match.group(1).lower() if match else ""

    def _heuristic_fallback(self, item: dict, trigger: str) -> dict:
        domain = self._extract_domain(item.get("url", ""))
        content = (item.get("title", "") + item.get("content", "")).lower()
        boost_terms = settings.heuristic["boost_terms"]
        low_triggers = settings.heuristic["low_confidence_triggers"]

        score, verdict, action = 50, "RUMOR", "MONITOR"

        if domain in settings.trusted_domains:
            score, verdict, action = 85, "OFFICIAL", "ALERT"
        elif any(term in content for term in boost_terms):
            score, verdict, action = 72, "CREDIBLE_LEAK", "ALERT"
        elif trigger in low_triggers:
            score, verdict, action = 45, "RUMOR", "MONITOR"

        return {
            "authenticity_score": score,
            "verdict": verdict,
            "confidence": "LOW",
            "reasoning": "Heuristic fallback — scoring API unavailable or disabled.",
            "recommended_action": action,
            "source": "heuristic",
        }


async def hunt_track(game: str, config: dict, query: str, cognitive: CognitiveEngine, rag, vaulted: set[str]):
    """Run one Tavily query and evaluate all candidates concurrently."""
    def _search():
        return _tavily.search(query=query, search_depth="advanced", max_results=6, topic="news", days=2)["results"]

    results = await asyncio.to_thread(_search)
    pairs = await asyncio.gather(*[
        _analyze_item(item, game, config, cognitive, rag, vaulted) for item in results
    ])
    return game, results, [a for a, _ in pairs if a], [r for _, r in pairs if r]


async def _analyze_item(
    item: dict, game: str, config: dict, cognitive: CognitiveEngine, rag, vaulted: set[str]
) -> tuple[dict | None, dict | None]:
    url = item.get("url", "")
    if not url or url in vaulted:
        return None, None

    blob = (item.get("title", "") + item.get("content", "") + url).lower()
    if any(n in blob for n in config.get("noise_filters", [])):
        return None, None
    if not any(k in blob for k in config.get("must_have", [])):
        return None, None

    for trigger in config.get("triggers", []):
        if trigger not in blob:
            continue
        rag_ctx = rag.retrieve(item.get("title", "") + " " + item.get("content", ""))
        verdict = await cognitive.evaluate(item, game, trigger, rag_ctx)
        if not cognitive.passes_threshold(verdict):
            return None, {"url": url, "title": item.get("title"), "cognitive": verdict}

        published = item.get("published_date") or f"LIVE: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        return {
            "game": game, "type": trigger.upper(), "title": item["title"],
            "url": url, "published": published, "cognitive": verdict,
        }, None
    return None, None
