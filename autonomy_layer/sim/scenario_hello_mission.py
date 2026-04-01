from __future__ import annotations

from autonomy_layer.core.mission_runtime import MissionRuntime
from autonomy_layer.core.models import Mission, MissionStep
from autonomy_layer.sim.simulation_adapter import SimulationExecutor
from autonomy_layer.telemetry.metrics import compute_snapshot


def build_hello_mission() -> Mission:
    return Mission(
        id="mission-hello-001",
        scenario="hello_mission",
        steps=[
            MissionStep(id="s1", action="navigate", params={"from": "A", "to": "B"}),
            MissionStep(id="s2", action="pick", params={"object": "sample_box"}),
            MissionStep(id="s3", action="place", params={"target": "station_B"}),
        ],
    )


def main() -> None:
    runtime = MissionRuntime()
    mission = build_hello_mission()
    executor = SimulationExecutor()

    result = runtime.run(mission=mission, executor=executor)
    snapshot = compute_snapshot([result])

    print("Mission result:")
    print(f"- mission_id: {result.mission_id}")
    print(f"- state: {result.state.value}")
    print(f"- duration_seconds: {result.duration_seconds:.3f}")
    print(f"- steps_executed: {result.steps_executed}")
    print(f"- error: {result.error}")
    print("KPI snapshot:")
    print(f"- mission_success_rate: {snapshot.mission_success_rate:.2f}")
    print(f"- mttr_seconds: {snapshot.mttr_seconds:.2f}")
    print(f"- auto_recovery_rate: {snapshot.auto_recovery_rate:.2f}")
    print(f"- manual_interventions_count: {snapshot.manual_interventions_count}")
    print(f"- incidents_total: {snapshot.incidents_total}")


if __name__ == "__main__":
    main()
