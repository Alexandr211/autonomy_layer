from __future__ import annotations

from autonomy_layer.core.models import MissionStep
from autonomy_layer.sim.failure_injection import FailureInjector


class PyBulletExecutor:
    """Headless PyBullet stepping; same contract as SimulationExecutor for MissionRuntime."""

    def __init__(
        self,
        fail_on_step_id: str | None = None,
        failure_injector: FailureInjector | None = None,
        *,
        time_step: float = 1.0 / 240.0,
        steps_per_mission_step: int = 10,
    ) -> None:
        import pybullet as p

        self._p = p
        self.fail_on_step_id = fail_on_step_id
        self.failure_injector = failure_injector
        self._time_step = time_step
        self._steps_per_mission_step = steps_per_mission_step
        self._client: int | None = p.connect(p.DIRECT)
        p.setGravity(0, 0, -9.81, physicsClientId=self._client)
        p.setTimeStep(self._time_step, physicsClientId=self._client)

    def execute(self, step: MissionStep) -> None:
        if self._client is None:
            raise RuntimeError("PyBulletExecutor is closed")
        p = self._p
        if self.failure_injector is not None:
            self.failure_injector.maybe_raise(step)
        if self.fail_on_step_id and step.id == self.fail_on_step_id:
            raise RuntimeError(f"Injected failure on step: {step.id}")
        for _ in range(self._steps_per_mission_step):
            p.stepSimulation(physicsClientId=self._client)

    def close(self) -> None:
        p = self._p
        if self._client is not None:
            p.disconnect(self._client)
            self._client = None
