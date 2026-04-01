# Universal Autonomy Layer

Early-stage project skeleton for Sprint 1 (Foundation) and Sprint 2 (Orchestration v1).

## Sprint 2 (в работе)

- Scope и приемка: [docs/sprint2_scope.md](docs/sprint2_scope.md)
- ROS 2 контракт (черновик): [docs/ros2_mission_contract_v1.md](docs/ros2_mission_contract_v1.md)
- Оркестрация (replay, события, fallback): `tests/test_mission_orchestration_sprint2.py`
- PyBullet acceptance: `tests/test_acceptance_sprint2_pybullet.py` (`pybullet` в Docker; без него тесты помечаются skipped)
- ROS 2 мост (S2-B7): пакеты в `ros2_ws/` — `autonomy_msgs`, `autonomy_mission_bridge`; smoke: `scripts/smoke_ros2_bridge.sh` (внутри контейнера). Подробнее: [docs/ros2_mission_contract_v1.md](docs/ros2_mission_contract_v1.md), [docker/README.md](docker/README.md)
- Webots на хосте (S2-B8): [docs/webots_host_s2b8.md](docs/webots_host_s2b8.md), проверка пакетов: `scripts/check_webots_ros2.sh` (после `source /opt/ros/humble/setup.bash`)
- Webots демо (S2-B9): [docs/webots_s2b9_warehouse_pilot_demo.md](docs/webots_s2b9_warehouse_pilot_demo.md)
- Sprint 2 report: [docs/reports/autonomy_layer_sprint2_orchestration_v1.md](docs/reports/autonomy_layer_sprint2_orchestration_v1.md)

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
