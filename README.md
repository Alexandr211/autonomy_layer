# Universal Autonomy Layer

Early-stage project skeleton for Sprint 1 (Foundation) and Sprint 2 (Orchestration v1).

## Sprint 2 (завершен)

- Scope и приемка: [docs/sprint2_scope.md](docs/sprint2_scope.md)
- ROS 2 контракт (черновик): [docs/ros2_mission_contract_v1.md](docs/ros2_mission_contract_v1.md)
- Оркестрация (replay, события, fallback): `tests/test_mission_orchestration_sprint2.py`
- PyBullet acceptance: `tests/test_acceptance_sprint2_pybullet.py` (`pybullet` в Docker; без него тесты помечаются skipped)
- ROS 2 мост (S2-B7): пакеты в `ros2_ws/` — `autonomy_msgs`, `autonomy_mission_bridge`; smoke: `scripts/smoke_ros2_bridge.sh` (внутри контейнера). Подробнее: [docs/ros2_mission_contract_v1.md](docs/ros2_mission_contract_v1.md), [docker/README.md](docker/README.md)
- Webots на хосте (S2-B8): [docs/webots_host_s2b8.md](docs/webots_host_s2b8.md), проверка пакетов: `scripts/check_webots_ros2.sh` (после `source /opt/ros/humble/setup.bash`)
- Webots демо (S2-B9): [docs/webots_s2b9_warehouse_pilot_demo.md](docs/webots_s2b9_warehouse_pilot_demo.md)
- Sprint 2 report: [docs/reports/autonomy_layer_sprint2_orchestration_v1.md](docs/reports/autonomy_layer_sprint2_orchestration_v1.md)

## План спринтов (12 недель)

Связанные документы: [docs/simulator_alternatives.md](docs/simulator_alternatives.md), [docs/program/autonomy_layer_program_fixed_decision.md](docs/program/autonomy_layer_program_fixed_decision.md).

| Sprint | Недели | Документы |
| --- | --- | --- |
| 1 Foundation | 1-2 | [отчет](docs/reports/autonomy_layer_sprint1_foundation.md), [доска](docs/boards/autonomy_layer_sprint1_execution_board.md) |
| 2 Orchestration v1 | 3-4 | [спека](docs/sprints/sprint2_orchestration_v1.md), [доска](docs/boards/autonomy_layer_sprint2_execution_board.md), [отчет](docs/reports/autonomy_layer_sprint2_orchestration_v1.md) |
| 3 Reliability v1 | 5-6 | [docs/sprints/sprint3_reliability_v1.md](docs/sprints/sprint3_reliability_v1.md) |
| 4 Pilot packaging | 7-8 | [docs/sprints/sprint4_pilot_packaging.md](docs/sprints/sprint4_pilot_packaging.md) |
| 5 Pre-pilot hardening I | 9-10 | [docs/sprints/sprint5_prepilot_hardening.md](docs/sprints/sprint5_prepilot_hardening.md) |
| 6 Pre-pilot hardening II | 11-12 | [docs/sprints/sprint6_prepilot_hardening.md](docs/sprints/sprint6_prepilot_hardening.md) |

## Sprint 1 Goals

- establish runtime/module structure
- implement mission lifecycle state machine
- run a deterministic simulation "hello mission"
- collect KPI metrics v0

## Run Demo

```bash
python -m autonomy_layer.sim.scenario_hello_mission
```

## Run Acceptance Tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Docker (ROS 2 Humble + PyBullet)

Базовый стек симуляции: **Webots** (3D, демо) + **PyBullet** (быстрые тесты; в образе). См. [docker/README.md](docker/README.md) и [docs/simulator_alternatives.md](docs/simulator_alternatives.md).

```bash
docker compose build
docker compose run --rm autonomy-sim ros2 topic list
# Все тесты, включая PyBullet (образ содержит pybullet):
docker compose run --rm autonomy-sim python3 -m unittest discover -s tests -p "test_*.py"
# ROS 2 mission bridge smoke (после colcon в ros2_ws; см. docker/README):
docker compose run --rm autonomy-sim bash scripts/smoke_ros2_bridge.sh
```

## Recovery Policy v1

| Failure type | Source error | Policy action | Notes |
| --- | --- | --- | --- |
| Timeout during step execution | `StepTimeoutError` | `retry` until timeout budget is exhausted, then `abort` | Budget controlled by `max_timeout_retries` (default: 1). |
| Action execution failure | `StepActionError` | `retry` until action budget is exhausted, then `safe_stop` | Budget controlled by `max_action_retries` (default: 0). |
| Any unknown execution error | `Exception` | `abort` | Conservative default. |
