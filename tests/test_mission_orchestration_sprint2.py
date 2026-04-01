from __future__ import annotations

import unittest

from autonomy_layer.core.mission_runtime import MissionRuntime
from autonomy_layer.core.mission_trace import MissionEventKind
from autonomy_layer.core.models import Mission, MissionState, MissionStep
from autonomy_layer.core.recovery_policy import RecoveryPolicyV0, RecoveryPolicyV1
from autonomy_layer.sim.failure_injection import FailureInjector, FailureSpec, FailureType
from autonomy_layer.sim.simulation_adapter import SimulationExecutor
from autonomy_layer.telemetry.metrics import compute_snapshot


def _build_mission_with_fallback() -> Mission:
    return Mission(
        id="mission-fallback-001",
        scenario="orchestration_test",
        steps=[
            MissionStep(id="s1", action="navigate", params={}),
            MissionStep(
                id="s2",
                action="pick",
                params={},
                fallback_step_id="s3",
            ),
            MissionStep(id="s3", action="place", params={}),
        ],
    )


class MissionOrchestrationSprint2Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.runtime = MissionRuntime(recovery_policy=RecoveryPolicyV0(max_timeout_retries=1))

    def test_replay_id_and_events_on_happy_path(self) -> None:
        mission = _build_mission_with_fallback()
        executor = SimulationExecutor()

        result = self.runtime.run(mission=mission, executor=executor)

        self.assertEqual(result.state, MissionState.SUCCEEDED)
        self.assertTrue(result.replay_id)
        kinds = [e.kind for e in result.events]
        self.assertEqual(kinds[0], MissionEventKind.MISSION_STARTED)
        self.assertEqual(kinds[-1], MissionEventKind.MISSION_FINISHED)
        self.assertIn(MissionEventKind.STEP_SUCCEEDED, kinds)
        self.assertEqual(result.incidents, [])

    def test_fallback_on_action_failure_succeeds(self) -> None:
        mission = _build_mission_with_fallback()
        injector = FailureInjector(
            failures=[FailureSpec(step_id="s2", failure_type=FailureType.ACTION)]
        )
        executor = SimulationExecutor(failure_injector=injector)

        result = self.runtime.run(mission=mission, executor=executor)

        self.assertEqual(result.state, MissionState.SUCCEEDED)
        self.assertEqual(result.steps_executed, 2)
        fb = [e for e in result.events if e.kind == MissionEventKind.FALLBACK_TAKEN]
        self.assertEqual(len(fb), 1)
        self.assertEqual(fb[0].payload.get("to_step_id"), "s3")
        inc = [i for i in result.incidents if i.code == "fallback_invoked"]
        self.assertEqual(len(inc), 1)
        self.assertEqual(inc[0].replay_id, result.replay_id)

    def test_invalid_fallback_records_incident_and_fails(self) -> None:
        mission = Mission(
            id="mission-bad-fb",
            scenario="orchestration_test",
            steps=[
                MissionStep(id="a1", action="x", params={}, fallback_step_id="missing"),
            ],
        )
        executor = SimulationExecutor(fail_on_step_id="a1")

        result = self.runtime.run(mission=mission, executor=executor)

        self.assertEqual(result.state, MissionState.FAILED)
        self.assertTrue(any(i.code == "invalid_fallback" for i in result.incidents))

    def test_plain_failure_emits_incident(self) -> None:
        mission = Mission(
            id="mission-fail",
            scenario="orchestration_test",
            steps=[
                MissionStep(id="only", action="x", params={}),
            ],
        )
        executor = SimulationExecutor(fail_on_step_id="only")

        result = self.runtime.run(mission=mission, executor=executor)

        self.assertEqual(result.state, MissionState.FAILED)
        self.assertTrue(any(i.code == "step_execution_failed" for i in result.incidents))
        self.assertEqual(result.incidents[0].replay_id, result.replay_id)

    def test_recovery_policy_v1_safe_stop_on_action_failure(self) -> None:
        mission = Mission(
            id="mission-safe-stop",
            scenario="orchestration_test",
            steps=[MissionStep(id="s1", action="pick", params={})],
        )
        runtime = MissionRuntime(recovery_policy=RecoveryPolicyV1())
        injector = FailureInjector(
            failures=[FailureSpec(step_id="s1", failure_type=FailureType.ACTION)]
        )
        executor = SimulationExecutor(failure_injector=injector)

        result = runtime.run(mission=mission, executor=executor)

        self.assertEqual(result.state, MissionState.SAFE_STOPPED)
        self.assertTrue(any(i.code == "safe_stop" for i in result.incidents))

    def test_recovery_policy_v1_retries_action_then_safe_stop(self) -> None:
        mission = Mission(
            id="mission-action-retry",
            scenario="orchestration_test",
            steps=[MissionStep(id="s1", action="pick", params={})],
        )
        runtime = MissionRuntime(
            recovery_policy=RecoveryPolicyV1(max_timeout_retries=1, max_action_retries=1)
        )
        injector = FailureInjector(
            failures=[FailureSpec(step_id="s1", failure_type=FailureType.ACTION)]
        )
        executor = SimulationExecutor(failure_injector=injector)

        result = runtime.run(mission=mission, executor=executor)

        self.assertEqual(result.state, MissionState.SAFE_STOPPED)
        self.assertEqual(result.recovery_attempts, 1)
        retries = [e for e in result.events if e.kind == MissionEventKind.RECOVERY_RETRY]
        self.assertEqual(len(retries), 1)

    def test_telemetry_snapshot_includes_incident_breakdown_and_safe_stop_rate(self) -> None:
        mission_ok = _build_mission_with_fallback()
        result_ok = self.runtime.run(mission=mission_ok, executor=SimulationExecutor())

        mission_bad = Mission(
            id="mission-bad",
            scenario="orchestration_test",
            steps=[MissionStep(id="x1", action="pick", params={})],
        )
        runtime_v1 = MissionRuntime(recovery_policy=RecoveryPolicyV1())
        bad_exec = SimulationExecutor(
            failure_injector=FailureInjector(
                failures=[FailureSpec(step_id="x1", failure_type=FailureType.ACTION)]
            )
        )
        result_bad = runtime_v1.run(mission=mission_bad, executor=bad_exec)

        snapshot = compute_snapshot([result_ok, result_bad])

        self.assertEqual(snapshot.incidents_total, 1)
        self.assertEqual(snapshot.incidents_by_code.get("safe_stop"), 1)
        self.assertAlmostEqual(snapshot.safe_stop_rate, 0.5)
        self.assertGreaterEqual(snapshot.retries_per_mission_avg, 0.0)


if __name__ == "__main__":
    unittest.main()
