from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from autonomy_layer.core.errors import StepActionError, StepTimeoutError


class RecoveryDecision(str, Enum):
    RETRY = "retry"
    ABORT = "abort"
    SAFE_STOP = "safe_stop"


@dataclass(frozen=True)
class RecoveryContext:
    step_id: str
    error: Exception
    retries_done: int
    max_timeout_retries: int
    max_action_retries: int = 0


class RecoveryPolicyV0:
    """Sprint 1 policy: retry timeout once, abort otherwise."""

    def __init__(self, max_timeout_retries: int = 1) -> None:
        self.max_timeout_retries = max_timeout_retries

    def decide(self, context: RecoveryContext) -> RecoveryDecision:
        if (
            isinstance(context.error, StepTimeoutError)
            and context.retries_done < context.max_timeout_retries
        ):
            return RecoveryDecision.RETRY
        return RecoveryDecision.ABORT


class RecoveryPolicyV1:
    """Sprint 2 policy: bounded retries + safe stop on action failures."""

    def __init__(self, max_timeout_retries: int = 1, max_action_retries: int = 0) -> None:
        self.max_timeout_retries = max_timeout_retries
        self.max_action_retries = max_action_retries

    def decide(self, context: RecoveryContext) -> RecoveryDecision:
        if isinstance(context.error, StepTimeoutError):
            if context.retries_done < context.max_timeout_retries:
                return RecoveryDecision.RETRY
            return RecoveryDecision.ABORT

        if isinstance(context.error, StepActionError):
            if context.retries_done < context.max_action_retries:
                return RecoveryDecision.RETRY
            return RecoveryDecision.SAFE_STOP

        return RecoveryDecision.ABORT
