from __future__ import annotations

from dataclasses import dataclass, field

from autonomy_layer.core.mission_runtime import MissionResult
from autonomy_layer.core.models import MissionState


@dataclass
class TelemetrySnapshot:
    mission_success_rate: float
    mttr_seconds: float
    auto_recovery_rate: float
    manual_interventions_count: int
    incidents_total: int = 0
    safe_stop_rate: float = 0.0
    retries_per_mission_avg: float = 0.0
    incidents_by_code: dict[str, int] = field(default_factory=dict)


def compute_snapshot(results: list[MissionResult]) -> TelemetrySnapshot:
    if not results:
        return TelemetrySnapshot(0.0, 0.0, 0.0, 0, 0, 0.0, 0.0, {})

    succeeded = sum(1 for r in results if r.state == MissionState.SUCCEEDED)
    failed = sum(1 for r in results if r.state == MissionState.FAILED)
    success_rate = succeeded / len(results)
    mttr = (
        sum(r.duration_seconds for r in results if r.state == MissionState.FAILED) / failed
        if failed
        else 0.0
    )

    missions_with_recovery = sum(1 for r in results if r.recovery_attempts > 0)
    recovered = sum(
        1
        for r in results
        if r.recovery_attempts > 0 and r.state == MissionState.SUCCEEDED
    )
    auto_recovery_rate = (
        recovered / missions_with_recovery if missions_with_recovery else 0.0
    )

    incidents_total = sum(len(r.incidents) for r in results)
    safe_stopped = sum(1 for r in results if r.state == MissionState.SAFE_STOPPED)
    safe_stop_rate = safe_stopped / len(results)
    retries_per_mission_avg = sum(r.recovery_attempts for r in results) / len(results)
    incidents_by_code: dict[str, int] = {}
    for r in results:
        for inc in r.incidents:
            incidents_by_code[inc.code] = incidents_by_code.get(inc.code, 0) + 1

    return TelemetrySnapshot(
        mission_success_rate=success_rate,
        mttr_seconds=mttr,
        auto_recovery_rate=auto_recovery_rate,
        manual_interventions_count=failed,
        incidents_total=incidents_total,
        safe_stop_rate=safe_stop_rate,
        retries_per_mission_avg=retries_per_mission_avg,
        incidents_by_code=incidents_by_code,
    )
