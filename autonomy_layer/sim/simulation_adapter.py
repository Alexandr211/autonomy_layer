from __future__ import annotations

from autonomy_layer.core.models import MissionStep
from autonomy_layer.sim.failure_injection import FailureInjector


class SimulationExecutor:
    """Deterministic executor for Sprint 1 baseline demo."""

    def __init__(
        self,
        fail_on_step_id: str | None = None,
        failure_injector: FailureInjector | None = None,
    ) -> None:
        self.fail_on_step_id = fail_on_step_id
        self.failure_injector = failure_injector

    def execute(self, step: MissionStep) -> None:
        if self.failure_injector is not None:
            self.failure_injector.maybe_raise(step)
        if self.fail_on_step_id and step.id == self.fail_on_step_id:
            raise RuntimeError(f"Injected failure on step: {step.id}")
