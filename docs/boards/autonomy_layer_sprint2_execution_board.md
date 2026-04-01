# Доска выполнения Sprint 2 (Orchestration v1)

Спека спринта: [../sprints/sprint2_orchestration_v1.md](../sprints/sprint2_orchestration_v1.md) · стек симуляции: [../simulator_alternatives.md](../simulator_alternatives.md)

## Статус спринта

- Спринт: **Sprint 2**
- Этап: **В работе**
- Итог: _(заполнить по завершении)_

## Backlog

### Планирование и контракты

- [x] **S2-B1:** Зафиксировать цели Sprint 2 и **критерии приемки** (1 сценарий: склад + манипулятор; PyBullet = автотесты, Webots = визуальный E2E) → [../sprint2_scope.md](../sprint2_scope.md)
- [x] **S2-B2:** Зафиксировать **ROS 2 interface contract** для миссии: перечень `topic` / `service` / `action`, имена, типы сообщений (черновик → freeze) → [../ros2_mission_contract_v1.md](../ros2_mission_contract_v1.md)
- [x] **S2-B3:** Согласовать **границы модулей**: `core` vs `adapters/ros2` vs `sim/pybullet` vs интеграция `webots_ros2` (без протекания деталей симулятора в оркестратор) → таблица в [../sprint2_scope.md](../sprint2_scope.md)

### PyBullet + CI (критический путь первым)

- [x] **S2-B4:** Реализовать **sim-адаптер PyBullet**: минимальная сцена или заглушка физики + вызов шагов миссии через существующий runtime → `autonomy_layer/sim/pybullet_executor.py`, сценарий `scenario_warehouse_stub.py`
- [x] **S2-B5:** Поднять **acceptance-тесты** на PyBullet: happy path + **3 типа сбоев** (детерминированная инъекция); запуск в **Docker** (`autonomy-layer:sim-humble`) → `tests/test_acceptance_sprint2_pybullet.py`; см. [README](../../README.md)

### ROS 2

- [x] **S2-B7:** Реализовать **ROS 2 мост/узлы**: приём команд миссии и публикация статуса/событий согласно S2-B2; smoke в контейнере → `ros2_ws/src/autonomy_msgs`, `ros2_ws/src/autonomy_mission_bridge`, `scripts/smoke_ros2_bridge.sh`

### Webots (параллельно после или с частичным PyBullet)

- [x] **S2-B8:** **Webots:** установка на хосте, минимальный мир (склад/манипулятор), проверка **`webots_ros2`** → [../webots_host_s2b8.md](../webots_host_s2b8.md), [../../webots/README.md](../../webots/README.md), `scripts/check_webots_ros2.sh`
- [x] **S2-B9:** Воспроизвести **тот же сценарий**, что и на PyBullet, в Webots (ручной или скриптованный прогон); подготовить **запись для демо** (видео готово)

### Надёжность и закрытие спринта

- [x] **S2-B10:** **Recovery policy v1** + обновление **telemetry** под новые сценарии и типы инцидентов → `autonomy_layer/core/recovery_policy.py`, `autonomy_layer/telemetry/metrics.py`, `tests/test_mission_orchestration_sprint2.py`
- [x] **S2-B11:** **Runbook** Sprint 2 (как запустить тесты, Docker, Webots, ROS 2) + **отчёт по спринту** → [../reports/autonomy_layer_sprint2_orchestration_v1.md](../reports/autonomy_layer_sprint2_orchestration_v1.md)

## In Progress

## Done

- [x] Инициализация Sprint 2 (доска создана)
- [x] Доска детализирована: PyBullet / Webots / ROS 2 / оркестрация
- [x] S2-B1–B3: scope, ROS 2 contract draft, границы модулей
- [x] S2-B4–B5: PyBullet executor + warehouse stub + acceptance-тесты
- [x] **S2-B6:** `replay_id`, цепочка `MissionEvent`, инциденты (`Incident`), fallback по `MissionStep.fallback_step_id` после ABORT; telemetry `incidents_total` → `core/mission_trace.py`, `tests/test_mission_orchestration_sprint2.py`
- [x] **S2-B7:** ROS 2 `autonomy_msgs` + `mission_bridge_node`, smoke
- [x] **S2-B8:** Webots на хосте: документация, `check_webots_ros2.sh`, официальный пример = минимальный «манипулятор»; склад — итерация в S2-B9
- [x] **S2-B9:** Webots паритет `warehouse_pilot_v1`: прогон (`webots_run_s2b9_demo.sh`) + запись для демо (видео готово)
- [x] **S2-B10:** Recovery policy v1 + telemetry v1 (incidents_by_code, safe_stop_rate, retries_per_mission_avg)
- [x] **S2-B11:** Runbook Sprint 2 + отчёт по спринту

## Блокеры и риски

- **Сеть/время на Webots** — не блокировать PyBullet-путь; Webots вести параллельно
- **Сложность ROS 2 контракта** — начать с минимального набора (1 action или 2 topic)

## Примечания

- Формат: задача в работе → `In Progress`; завершена → `[x]` и `Done`
- Изменения scope — отдельной строкой здесь
- Критический путь: **S2-B4 → S2-B5 → S2-B6 → S2-B7**, затем **S2-B8–S2-B9** для паритета с Webots
