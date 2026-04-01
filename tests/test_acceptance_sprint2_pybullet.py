from __future__ import annotations

import importlib.util
import unittest

from autonomy_layer.core.mission_runtime import MissionRuntime
from autonomy_layer.core.models import MissionState
from autonomy_layer.core.recovery_policy import RecoveryPolicyV0
from autonomy_layer.sim.failure_injection import FailureInjector, FailureSpec, FailureType
from autonomy_layer.sim.pybullet_executor import PyBulletExecutor
from autonomy_layer.sim.scenario_warehouse_stub import build_warehouse_pilot_mission


@unittest.skipUnless(
    importlib.util.find_spec("pybullet") is not None,
    "pybullet not installed",
)
class Sprint2PyBulletAcceptanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runtime = MissionRuntime(recovery_policy=RecoveryPolicyV0(max_timeout_retries=1))

    def tearDown(self) -> None:
        # Executors created in tests should call close(); defensive noop if missing
        pass

    def test_happy_path_succeeds(self) -> None:
        mission = build_warehouse_pilot_mission()
        executor = PyBulletExecutor()
        self.addCleanup(executor.close)

        result = self.runtime.run(mission=mission, executor=executor)

        self.assertEqual(result.state, MissionState.SUCCEEDED)
        self.assertEqual(result.steps_executed, 3)
        self.assertEqual(result.recovery_attempts, 0)
        self.assertIsNone(result.error)

    def test_timeout_fail_after_single_retry(self) -> None:
        mission = build_warehouse_pilot_mission()
        injector = FailureInjector(
            failures=[FailureSpec(step_id="w2", failure_type=FailureType.TIMEOUT)]
        )
        executor = PyBulletExecutor(failure_injector=injector)
        self.addCleanup(executor.close)

        result = self.runtime.run(mission=mission, executor=executor)

        self.assertEqual(result.state, MissionState.FAILED)
        self.assertEqual(result.steps_executed, 1)
        self.assertEqual(result.recovery_attempts, 1)
        self.assertEqual(mission.retries, 1)
        self.assertIn("timeout", (result.error or "").lower())

    def test_action_fail_without_retry(self) -> None:
        mission = build_warehouse_pilot_mission()
        injector = FailureInjector(
            failures=[FailureSpec(step_id="w2", failure_type=FailureType.ACTION)]
        )
        executor = PyBulletExecutor(failure_injector=injector)
        self.addCleanup(executor.close)

        result = self.runtime.run(mission=mission, executor=executor)

        self.assertEqual(result.state, MissionState.FAILED)
        self.assertEqual(result.steps_executed, 1)
        self.assertEqual(result.recovery_attempts, 0)
        self.assertEqual(mission.retries, 0)
        self.assertIn("action", (result.error or "").lower())

    def test_generic_injected_failure_aborts(self) -> None:
        mission = build_warehouse_pilot_mission()
        executor = PyBulletExecutor(fail_on_step_id="w2")
        self.addCleanup(executor.close)

        result = self.runtime.run(mission=mission, executor=executor)

        self.assertEqual(result.state, MissionState.FAILED)
        self.assertEqual(result.steps_executed, 1)
        self.assertEqual(result.recovery_attempts, 0)


if __name__ == "__main__":
    unittest.main()
