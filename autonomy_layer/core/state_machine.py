from __future__ import annotations

from autonomy_layer.core.models import MissionState


ALLOWED_TRANSITIONS: dict[MissionState, set[MissionState]] = {
    MissionState.QUEUED: {MissionState.RUNNING},
    MissionState.RUNNING: {
        MissionState.SUCCEEDED,
        MissionState.FAILED,
        MissionState.SAFE_STOPPED,
    },
    MissionState.FAILED: {MissionState.RUNNING, MissionState.SAFE_STOPPED},
    MissionState.SUCCEEDED: set(),
    MissionState.SAFE_STOPPED: set(),
}


def can_transition(current: MissionState, target: MissionState) -> bool:
    return target in ALLOWED_TRANSITIONS.get(current, set())
