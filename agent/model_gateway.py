"""Provider abstraction used by v5.8 Agent Core."""
from __future__ import annotations

from dataclasses import dataclass
from .model_manager import LocalRuntime


@dataclass
class ModelEndpoint:
    provider: str
    base_url: str
    model: str
    api_key: str = "no-key"
    local: bool = False


class ModelGateway:
    def __init__(self, local_runtime: LocalRuntime | None = None):
        self.local_runtime = local_runtime or LocalRuntime()
        self.endpoint: ModelEndpoint | None = None

    def use_provider(self, base_url: str, model: str, api_key: str = "no-key", provider="OpenAI-compatible"):
        self.endpoint = ModelEndpoint(provider, base_url.rstrip("/"), model, api_key or "no-key", False)
        return self.endpoint

    def use_local(self, model: str | None = None):
        if not self.local_runtime.running:
            raise RuntimeError("Локальный runtime не запущен.")
        self.endpoint = ModelEndpoint("llama.cpp", self.local_runtime.base_url, model or "", "no-key", True)
        return self.endpoint

    def status(self):
        return {
            "endpoint": self.endpoint.__dict__ if self.endpoint else None,
            "local_runtime": self.local_runtime.status(),
        }
