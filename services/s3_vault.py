import asyncio
import json
import logging
import re
from datetime import datetime, timedelta

import boto3

from config import settings

logger = logging.getLogger(__name__)


class RagVault:
    """Token-overlap retrieval over S3-backed historical corpus."""

    def __init__(self, s3_client, bucket: str):
        self._s3 = s3_client
        self._bucket = bucket
        self._entries: list[dict] = []

    @property
    def entries(self) -> list[dict]:
        return self._entries

    async def load(self) -> "RagVault":
        kb, contracts = await asyncio.gather(
            self._load_knowledge_base(),
            self._load_recent_contracts(),
        )
        self._entries = kb + contracts
        logger.info("Elder Blood corpus loaded: %d RAG entries.", len(self._entries))
        return self

    def retrieve(self, query_text: str, limit: int | None = None) -> list[dict]:
        limit = limit or settings.rag_context_limit
        tokens = set(re.findall(r"[a-z0-9]+", query_text.lower()))
        if not tokens:
            return []

        scored: list[tuple[int, dict]] = []
        for entry in self._entries:
            haystack = " ".join([
                entry.get("title", ""),
                entry.get("summary", ""),
                entry.get("url", ""),
                " ".join(entry.get("tags", [])),
            ]).lower()
            overlap = len(tokens & set(re.findall(r"[a-z0-9]+", haystack)))
            if overlap:
                scored.append((overlap, entry))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [entry for _, entry in scored[:limit]]

    async def _load_knowledge_base(self) -> list[dict]:
        try:
            raw = await self._get_object(settings.knowledge_key)
            return json.loads(raw).get("entries", [])
        except self._s3.exceptions.NoSuchKey:
            return list(settings.default_knowledge)
        except Exception as exc:
            logger.warning("RAG knowledge base unavailable: %s", exc)
            return list(settings.default_knowledge)

    async def _load_recent_contracts(self, days: int = 14) -> list[dict]:
        entries: list[dict] = []
        cutoff = datetime.now() - timedelta(days=days)
        try:
            keys = await self._list_contract_keys(cutoff)
            for key in keys:
                try:
                    body = json.loads(await self._get_object(key))
                    for alert in body.get("alerts", []):
                        cog = alert.get("cognitive", {})
                        entries.append({
                            "title": alert.get("title", ""),
                            "url": alert.get("url", ""),
                            "summary": (
                                f"{alert.get('game')} | {alert.get('type')} "
                                f"| score={cog.get('authenticity_score', 'N/A')}"
                            ),
                            "tags": [alert.get("game", ""), alert.get("type", "")],
                        })
                except Exception:
                    continue
        except Exception as exc:
            logger.warning("RAG contract scan failed: %s", exc)
        return entries

    async def _list_contract_keys(self, cutoff: datetime) -> list[str]:
        def _scan():
            keys = []
            paginator = self._s3.get_paginator("list_objects_v2")
            for page in paginator.paginate(Bucket=self._bucket, Prefix=settings.bestiary_prefix):
                for obj in page.get("Contents", []):
                    key = obj["Key"]
                    if not key.endswith(".json"):
                        continue
                    if key in (settings.index_key, settings.knowledge_key):
                        continue
                    if obj["LastModified"].replace(tzinfo=None) < cutoff:
                        continue
                    keys.append(key)
            return keys

        return await asyncio.to_thread(_scan)

    async def _get_object(self, key: str) -> str:
        def _read():
            obj = self._s3.get_object(Bucket=self._bucket, Key=key)
            return obj["Body"].read().decode("utf-8")

        return await asyncio.to_thread(_read)

    async def _put_object(self, key: str, body: str) -> None:
        await asyncio.to_thread(
            self._s3.put_object,
            Bucket=self._bucket,
            Key=key,
            Body=body,
            ContentType="application/json",
        )


class S3Vault:
    """Async facade over boto3 S3 operations."""

    def __init__(self):
        self._s3 = boto3.client("s3", region_name=settings.region)
        self.rag = RagVault(self._s3, settings.bucket_name)

    async def bootstrap(self) -> tuple[set[str], RagVault]:
        vaulted_urls, _ = await asyncio.gather(
            self.get_vaulted_urls(),
            self.rag.load(),
        )
        return vaulted_urls, self.rag

    async def get_vaulted_urls(self) -> set[str]:
        logger.info("Accessing Master Bestiary Index...")
        try:
            raw = await self.rag._get_object(settings.index_key)
            return set(json.loads(raw).get("urls", []))
        except self._s3.exceptions.NoSuchKey:
            logger.info("Master Index not found. Initiating new memory core.")
            return set()
        except Exception as exc:
            logger.error("S3 index read failed: %s", exc)
            return set()

    async def update_master_index(self, new_urls: set[str], current_vault: set[str]) -> None:
        payload = json.dumps({
            "urls": list(current_vault | new_urls),
            "updated_at": datetime.now().isoformat(),
            "version": settings.version,
        }, indent=4)
        try:
            await self.rag._put_object(settings.index_key, payload)
            logger.info("Master Index secured.")
        except Exception as exc:
            logger.error("Master Index write failed: %s", exc)

    async def archive_mission(self, mission_data: dict) -> str:
        folder = datetime.now().strftime("%Y-%m-%d")
        filename = f"Contract_Fulfilled_At_{datetime.now().strftime('%H%M')}.json"
        key = f"{settings.bestiary_prefix}{folder}/{filename}"
        await self.rag._put_object(key, json.dumps(mission_data, indent=4, ensure_ascii=False))
        logger.info("Mission archived: %s", key)
        return key

    async def update_knowledge_base(self, alerts: list[dict]) -> None:
        if not alerts:
            return
        try:
            try:
                raw = await self.rag._get_object(settings.knowledge_key)
                data = json.loads(raw)
            except self._s3.exceptions.NoSuchKey:
                data = {"entries": [], "version": settings.version}

            known = {e.get("url") for e in data.get("entries", [])}
            for alert in alerts:
                if alert["url"] in known:
                    continue
                cog = alert.get("cognitive", {})
                data["entries"].append({
                    "title": alert["title"],
                    "url": alert["url"],
                    "summary": f"Validated {alert['game']} — {cog.get('verdict', 'UNKNOWN')}",
                    "tags": [alert["game"], alert["type"], cog.get("verdict", "")],
                    "validated_at": datetime.now().isoformat(),
                })

            data["updated_at"] = datetime.now().isoformat()
            await self.rag._put_object(
                settings.knowledge_key,
                json.dumps(data, indent=4, ensure_ascii=False),
            )
            logger.info("Knowledge base enriched.")
        except Exception as exc:
            logger.error("Knowledge base update failed: %s", exc)

    async def persist_hunt(self, mission_data: dict, new_urls: set[str], vaulted_urls: set[str]) -> None:
        await asyncio.gather(
            self.archive_mission(mission_data),
            self.update_master_index(new_urls, vaulted_urls),
            self.update_knowledge_base(mission_data["alerts"]),
        )
