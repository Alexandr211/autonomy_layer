from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from autonomy_layer.core.errors import StepActionError, StepTimeoutError
from autonomy_layer.core.models import MissionStep


class FailureType(str, Enum):
    TIMEOUT = "timeout"
    ACTION = "action"


@dataclass(frozen=True)
class FailureSpec:
    step_id: str
    failure_type: FailureType
    message: str | None = None


class FailureInjector:
    """Injects deterministic failures for specific steps."""

    def __init__(self, failures: list[FailureSpec] | None = None) -> None:
        self._failures = failures or []

    def maybe_raise(self, step: MissionStep) -> None:
        for failure in self._failures:
            if failure.step_id != step.id:
                continue
            if failure.failure_type == FailureType.TIMEOUT:
                raise StepTimeoutError(
                    failure.message or f"Injected timeout on step: {step.id}"
                )
            raise StepActionError(
                failure.message or f"Injected action failure on step: {step.id}"
            )
