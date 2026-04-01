from __future__ import annotations

from dataclasses import dataclass, field
from time import monotonic
from uuid import uuid4

from autonomy_layer.core.mission_trace import (
    MissionEvent,
    MissionEventKind,
    Incident,
    new_incident,
    step_index_by_id,
)
from autonomy_layer.core.recovery_policy import (
    RecoveryContext,
    RecoveryDecision,
    RecoveryPolicyV0,
)
from autonomy_layer.core.models import Mission, MissionState
from autonomy_layer.core.state_machine import can_transition


@dataclass
class MissionResult:
    mission_id: str
    state: MissionState
    duration_seconds: float
    steps_executed: int
    recovery_attempts: int = 0
    error: str | None = None
    replay_id: str = ""
    events: list[MissionEvent] = field(default_factory=list)
    incidents: list[Incident] = field(default_factory=list)


class MissionRuntime:
    def __init__(self, recovery_policy: RecoveryPolicyV0 | None = None) -> None:
        self.recovery_policy = recovery_policy or RecoveryPolicyV0()

    def run(self, mission: Mission, executor) -> MissionResult:
        started = monotonic()
        replay_id = str(uuid4())
        events: list[MissionEvent] = []
        incidents: list[Incident] = []

        def emit(
            kind: MissionEventKind,
            step_id: str | None = None,
            message: str | None = None,
            payload: dict | None = None,
        ) -> None:
            events.append(
                MissionEvent(
                    replay_id=replay_id,
                    mission_id=mission.id,
                    kind=kind,
                    step_id=step_id,
                    message=message,
                    payload=payload or {},
                )
            )

        emit(MissionEventKind.MISSION_STARTED, payload={"scenario": mission.scenario})

        self._transition(mission, MissionState.RUNNING)
        steps_executed = 0
        recovery_attempts = 0
        index = 0

        while index < len(mission.steps):
            step = mission.steps[index]
            emit(MissionEventKind.STEP_STARTED, step_id=step.id)
            try:
                executor.execute(step)
                emit(MissionEventKind.STEP_SUCCEEDED, step_id=step.id)
                steps_executed += 1
                index += 1
            except Exception as exc:
                emit(
                    MissionEventKind.STEP_FAILED,
                    step_id=step.id,
                    message=str(exc),
                    payload={"error_type": type(exc).__name__},
                )
                decision = self.recovery_policy.decide(
                    RecoveryContext(
                        step_id=step.id,
                        error=exc,
                        retries_done=mission.retries,
                        max_timeout_retries=getattr(
                            self.recovery_policy, "max_timeout_retries", 0
                        ),
                        max_action_retries=getattr(
                            self.recovery_policy, "max_action_retries", 0
                        ),
                    )
                )
                if decision == RecoveryDecision.RETRY:
                    emit(MissionEventKind.RECOVERY_RETRY, step_id=step.id)
                    mission.retries += 1
                    recovery_attempts += 1
                    continue
                if decision == RecoveryDecision.SAFE_STOP:
                    incidents.append(
                        new_incident(
                            replay_id=replay_id,
                            mission_id=mission.id,
                            code="safe_stop",
                            detail=str(exc),
                            step_id=step.id,
                        )
                    )
                    self._transition(mission, MissionState.SAFE_STOPPED)
                    emit(
                        MissionEventKind.MISSION_FINISHED,
                        payload={"outcome": MissionState.SAFE_STOPPED.value},
                    )
                    return MissionResult(
                        mission_id=mission.id,
                        state=mission.state,
                        duration_seconds=monotonic() - started,
                        steps_executed=steps_executed,
                        recovery_attempts=recovery_attempts,
                        error=str(exc),
                        replay_id=replay_id,
                        events=events,
                        incidents=incidents,
                    )
                if step.fallback_step_id:
                    target = step_index_by_id(mission.steps, step.fallback_step_id)
                    if target is None:
                        detail = f"Unknown fallback_step_id: {step.fallback_step_id}"
                        incidents.append(
                            new_incident(
                                replay_id=replay_id,
                                mission_id=mission.id,
                                code="invalid_fallback",
                                detail=detail,
                                step_id=step.id,
                            )
                        )
                        self._transition(mission, MissionState.FAILED)
                        emit(
                            MissionEventKind.MISSION_FINISHED,
                            payload={"outcome": MissionState.FAILED.value},
                        )
                        return MissionResult(
                            mission_id=mission.id,
                            state=mission.state,
                            duration_seconds=monotonic() - started,
                            steps_executed=steps_executed,
                            recovery_attempts=recovery_attempts,
                            error=detail,
                            replay_id=replay_id,
                            events=events,
                            incidents=incidents,
                        )
                    incidents.append(
                        new_incident(
                            replay_id=replay_id,
                            mission_id=mission.id,
                            code="fallback_invoked",
                            detail=str(exc),
                            step_id=step.id,
                        )
                    )
                    emit(
                        MissionEventKind.FALLBACK_TAKEN,
                        step_id=step.id,
                        payload={"to_step_id": step.fallback_step_id},
                    )
                    mission.retries = 0
                    index = target
                    continue

                incidents.append(
                    new_incident(
                        replay_id=replay_id,
                        mission_id=mission.id,
                        code="step_execution_failed",
                        detail=str(exc),
                        step_id=step.id,
                    )
                )
                self._transition(mission, MissionState.FAILED)
                emit(
                    MissionEventKind.MISSION_FINISHED,
                    payload={"outcome": MissionState.FAILED.value},
                )
                return MissionResult(
                    mission_id=mission.id,
                    state=mission.state,
                    duration_seconds=monotonic() - started,
                    steps_executed=steps_executed,
                    recovery_attempts=recovery_attempts,
                    error=str(exc),
                    replay_id=replay_id,
                    events=events,
                    incidents=incidents,
                )

        self._transition(mission, MissionState.SUCCEEDED)
        emit(
            MissionEventKind.MISSION_FINISHED,
            payload={"outcome": MissionState.SUCCEEDED.value},
        )
        return MissionResult(
            mission_id=mission.id,
            state=mission.state,
            duration_seconds=monotonic() - started,
            steps_executed=steps_executed,
            recovery_attempts=recovery_attempts,
            replay_id=replay_id,
            events=events,
            incidents=incidents,
        )

    @staticmethod
    def _transition(mission: Mission, target: MissionState) -> None:
        if not can_transition(mission.state, target):
            raise ValueError(f"Invalid mission transition: {mission.state} -> {target}")
        mission.state = target
