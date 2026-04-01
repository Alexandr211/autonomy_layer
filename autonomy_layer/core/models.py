from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class MissionState(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    SAFE_STOPPED = "safe_stopped"


@dataclass
class MissionStep:
    id: str
    action: str
    params: dict[str, Any] = field(default_factory=dict)
    # If set, after recovery policy yields ABORT, jump to this step id instead of failing the mission.
    fallback_step_id: str | None = None


@dataclass
class Mission:
    id: str
    scenario: str
    steps: list[MissionStep]
    state: MissionState = MissionState.QUEUED
    retries: int = 0
