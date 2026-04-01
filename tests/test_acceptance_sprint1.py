from __future__ import annotations

import unittest

from autonomy_layer.core.mission_runtime import MissionRuntime
from autonomy_layer.core.models import MissionState
from autonomy_layer.core.recovery_policy import RecoveryPolicyV0
from autonomy_layer.sim.failure_injection import FailureInjector, FailureSpec, FailureType
from autonomy_layer.sim.scenario_hello_mission import build_hello_mission
from autonomy_layer.sim.simulation_adapter import SimulationExecutor


class Sprint1AcceptanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runtime = MissionRuntime(recovery_policy=RecoveryPolicyV0(max_timeout_retries=1))

    def test_happy_path_succeeds(self) -> None:
        mission = build_hello_mission()
        executor = SimulationExecutor()

        result = self.runtime.run(mission=mission, executor=executor)

        self.assertEqual(result.state, MissionState.SUCCEEDED)
        self.assertEqual(result.steps_executed, 3)
        self.assertEqual(result.recovery_attempts, 0)
        self.assertIsNone(result.error)

    def test_timeout_fail_after_single_retry(self) -> None:
        mission = build_hello_mission()
        injector = FailureInjector(
            failures=[FailureSpec(step_id="s2", failure_type=FailureType.TIMEOUT)]
        )
        executor = SimulationExecutor(failure_injector=injector)

        result = self.runtime.run(mission=mission, executor=executor)

        self.assertEqual(result.state, MissionState.FAILED)
        self.assertEqual(result.steps_executed, 1)
        self.assertEqual(result.recovery_attempts, 1)
        self.assertEqual(mission.retries, 1)
        self.assertIn("timeout", (result.error or "").lower())

    def test_action_fail_without_retry(self) -> None:
        mission = build_hello_mission()
        injector = FailureInjector(
            failures=[FailureSpec(step_id="s2", failure_type=FailureType.ACTION)]
        )
        executor = SimulationExecutor(failure_injector=injector)

        result = self.runtime.run(mission=mission, executor=executor)

        self.assertEqual(result.state, MissionState.FAILED)
        self.assertEqual(result.steps_executed, 1)
        self.assertEqual(result.recovery_attempts, 0)
        self.assertEqual(mission.retries, 0)
        self.assertIn("action", (result.error or "").lower())


if __name__ == "__main__":
    unittest.main()
