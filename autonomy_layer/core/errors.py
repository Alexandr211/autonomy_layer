from __future__ import annotations


class MissionExecutionError(RuntimeError):
    """Base class for mission step execution failures."""


class StepTimeoutError(MissionExecutionError):
    """Raised when a step exceeds its execution timeout."""


class StepActionError(MissionExecutionError):
    """Raised when a step action fails at runtime."""
