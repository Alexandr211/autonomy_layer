from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from uuid import uuid4


class MissionEventKind(str, Enum):
    MISSION_STARTED = "mission_started"
    STEP_STARTED = "step_started"
    STEP_SUCCEEDED = "step_succeeded"
    STEP_FAILED = "step_failed"
    RECOVERY_RETRY = "recovery_retry"
    FALLBACK_TAKEN = "fallback_taken"
    MISSION_FINISHED = "mission_finished"


@dataclass(frozen=True)
class MissionEvent:
    replay_id: str
    mission_id: str
    kind: MissionEventKind
    step_id: str | None = None
    message: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Incident:
    incident_id: str
    replay_id: str
    mission_id: str
    code: str
    detail: str
    step_id: str | None = None


def new_incident(
    *,
    replay_id: str,
    mission_id: str,
    code: str,
    detail: str,
    step_id: str | None = None,
) -> Incident:
    return Incident(
        incident_id=str(uuid4()),
        replay_id=replay_id,
        mission_id=mission_id,
        code=code,
        detail=detail,
        step_id=step_id,
    )


def step_index_by_id(steps: list[Any], step_id: str) -> int | None:
    for i, s in enumerate(steps):
        if s.id == step_id:
            return i
    return None
