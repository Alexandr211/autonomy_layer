# ROS 2 mission interface contract (draft v1)

Статус: **черновик** — имена и типы могут быть уточнены до freeze перед S2-B7.

Цель: описать минимальный набор интерфейсов между **внешним оператором/планировщиком** и **autonomy layer** (узлы в `autonomy_layer.adapters.ros2`).

## Принципы

- Одна миссия за раз на инстанс узла оркестрации (v1).
- Статус и события — **поток событий** (topics); команда старта — **action** (отмена и обратная связь из коробки).

## Packages / сообщения

Рекомендуется отдельный пакет `autonomy_msgs` (или префикс проекта). До генерации из `.msg` допустимы эквиваленты из `std_msgs` + JSON в строке (только для прототипа).

| Имя (предложение) | Поля (логика) |
| --- | --- |
| `MissionStep.msg` | `string id`, `string action`, `string params_json` |
| `Mission.msg` | `string mission_id`, `string scenario_id`, `MissionStep[] steps` |
| `MissionStatus.msg` | `string mission_id`, `string state`, `string last_error`, `int32 steps_done`, `int32 retries` |
| `MissionEvent.msg` | `builtin_interfaces/Time stamp`, `string mission_id`, `string event_type`, `string step_id`, `string payload_json` |

`event_type` (строковый enum): `mission_started`, `step_started`, `step_succeeded`, `step_failed`, `recovery_retry`, `mission_finished`, `incident`.

## Topics

| Topic | Direction | Тип | Описание |
| --- | --- | --- | --- |
| `/autonomy/mission/status` | out | `MissionStatus` | Текущее состояние (периодически и по изменению). |
| `/autonomy/mission/events` | out | `MissionEvent` | События для логов, replay, инцидентов. |

## Actions

| Action | Goal | Result | Cancel |
| --- | --- | --- | --- |
| `/autonomy/mission/execute` | `Mission` | `MissionStatus` (финальный) + success flag | Остановка после текущего шага / safe stop (политика v1) |

## Services (опционально v1)

| Service | Request | Response |
| --- | --- | --- |
| `/autonomy/mission/get_status` | `mission_id` | `MissionStatus` |

Можно не вводить, если статус полностью покрыт topic + action result.

## Соответствие коду Python

- `Mission` / `MissionStep` в `autonomy_layer.core.models` маппятся на сообщения: `params` ↔ JSON в `params_json`.
- Расширения контракта (incident id, replay id) — в `MissionEvent.payload_json` до появления отдельных полей в `autonomy_msgs`.

## Реализация (S2-B7)

- Пакет интерфейсов: **`ros2_ws/src/autonomy_msgs`** (`Mission`, `MissionStep`, `MissionStatus`, `MissionEvent`, action **`MissionExecute`**).
- Узел моста: **`ros2_ws/src/autonomy_mission_bridge`**, исполняемое имя **`mission_bridge_node`** — action `/autonomy/mission/execute`, публикаторы `/autonomy/mission/status` и `/autonomy/mission/events`; исполнитель шагов по умолчанию — `SimulationExecutor` (детерминированный сим).
- Сборка: `colcon build --merge-install` в `ros2_ws` (в образе Docker выполняется при `docker compose build`). При монтировании `.:/workspace` при первом запуске выполнить сборку внутри контейнера, если каталога `ros2_ws/install` нет.
- Smoke: `scripts/smoke_ros2_bridge.sh` или вручную `ros2 run autonomy_mission_bridge mission_bridge_node` + `ros2 action send_goal ...` (см. [docker/README.md](../docker/README.md)).
