from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    stack_exchange_key: str | None = None
    stack_exchange_access_token: str | None = None
    site: str = "stackoverflow"
    pagesize: int = 30

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            stack_exchange_key=os.getenv("STACK_EXCHANGE_KEY") or None,
            stack_exchange_access_token=os.getenv("STACK_EXCHANGE_ACCESS_TOKEN") or None,
            site=os.getenv("STACK_OVERFLOW_SITE", "stackoverflow"),
            pagesize=int(os.getenv("STACK_OVERFLOW_PAGESIZE", "30")),
        )
