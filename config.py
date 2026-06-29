import json
import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent
TARGETS_PATH = ROOT_DIR / "targets.json"


def _load_targets() -> dict:
    with TARGETS_PATH.open(encoding="utf-8") as f:
        return json.load(f)


_targets = _load_targets()


@dataclass(frozen=True)
class Settings:
    """Runtime configuration sourced from .env and targets.json."""

    tavily_key: str = field(default_factory=lambda: os.getenv("SEARCH_API_KEY", ""))
    bucket_name: str = field(default_factory=lambda: os.getenv("AWS_S3_BUCKET", ""))
    region: str = field(default_factory=lambda: os.getenv("AWS_REGION", "eu-central-1"))
    discord_webhook_url: str = field(default_factory=lambda: os.getenv("DISCORD_WEBHOOK_URL", ""))
    cognitive_api_key: str = field(default_factory=lambda: os.getenv("COGNITIVE_API_KEY", ""))
    cognitive_model: str = field(default_factory=lambda: os.getenv("COGNITIVE_MODEL", "llama-3.3-70b-versatile"))
    cognitive_base_url: str = field(
        default_factory=lambda: os.getenv("COGNITIVE_BASE_URL", "https://api.groq.com/openai/v1")
    )
    authenticity_threshold: int = field(default_factory=lambda: int(os.getenv("AUTHENTICITY_THRESHOLD", "60")))
    rag_context_limit: int = field(default_factory=lambda: int(os.getenv("RAG_CONTEXT_LIMIT", "5")))
    cognitive_timeout: int = field(default_factory=lambda: int(os.getenv("COGNITIVE_TIMEOUT", "20")))
    cognitive_max_concurrency: int = field(default_factory=lambda: int(os.getenv("COGNITIVE_MAX_CONCURRENCY", "8")))
    discord_timeout: int = field(default_factory=lambda: int(os.getenv("DISCORD_TIMEOUT", "10")))

    index_key: str = "Bestiary/index.json"
    knowledge_key: str = "Bestiary/knowledge_base.json"
    bestiary_prefix: str = "Bestiary/"
    version: str = "7.0"

    color_mint: int = 0x00FF96
    color_igni: int = 0xFF9900
    color_elder: int = 0x9B59B6
    color_noise: int = 0x555555

    targets: dict = field(default_factory=lambda: _targets)
    games: dict = field(default_factory=lambda: _targets["games"])
    trusted_domains: set = field(default_factory=lambda: set(_targets["trusted_domains"]))
    heuristic: dict = field(default_factory=lambda: _targets["heuristic"])
    default_knowledge: list = field(default_factory=lambda: _targets["default_knowledge"])


settings = Settings()
