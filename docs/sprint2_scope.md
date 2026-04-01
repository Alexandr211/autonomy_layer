# Sprint 2 — цели и критерии приемки (v1)

Связанные документы: [sprints/sprint2_orchestration_v1.md](sprints/sprint2_orchestration_v1.md) · [ros2_mission_contract_v1.md](ros2_mission_contract_v1.md) · [simulator_alternatives.md](simulator_alternatives.md)

## Цели

- Один целевой сценарий **склад + манипулятор** (`warehouse_pilot_v1`) с оркестрацией через существующий `MissionRuntime`.
- **PyBullet** — быстрые автоматические acceptance-тесты (в т.ч. в Docker `autonomy-layer:sim-humble`).
- **Webots** — визуальный E2E и `webots_ros2` на хосте (не блокирует PyBullet-путь).

## Критерии приемки (минимум для закрытия спринта)

1. Миссия `warehouse_pilot_v1` выполняется end-to-end в **PyBullet** в штатном режиме (автотест happy path).
2. На **трёх сценариях сбоев** (timeout с retry, action failure, generic/step injection) реакция соответствует `RecoveryPolicyV0` и ожиданиям тестов Sprint 1.
3. Зафиксирован **черновик** ROS 2 контракта (`docs/ros2_mission_contract_v1.md`); реализация узлов — отдельная задача (S2-B7).
4. Границы модулей задокументированы ниже; оркестратор не импортирует PyBullet/Webots напрямую.

## Границы модулей (S2-B3)

| Модуль | Ответственность | Не должен |
| --- | --- | --- |
| `autonomy_layer.core` | Модель миссии, state machine, recovery policy, runtime loop | Знать про ROS 2, PyBullet, Webots |
| `autonomy_layer.sim` | Исполнители шагов для симуляции: `SimulationExecutor`, `PyBulletExecutor`, сценарии, инъекция сбоев | Публиковать ROS 2 топики |
| `autonomy_layer.adapters.ros2` (план) | Узлы/мост: команды миссии ↔ runtime, статус/события по контракту | Содержать физику или URDF |
| Интеграция Webots | Вне репозитория или тонкий слой: вызовы через ROS 2 / сценарий записи | Дублировать логику оркестрации в `.wbt` |

Протекание деталей симулятора в оркестратор запрещено: runtime получает только `executor` с методом `execute(step)`.

## Оркестрация v1 (S2-B6)

- Каждый прогон миссии получает **`replay_id`** (UUID); события и инциденты ссылаются на него.
- Поток **`MissionEvent`** (`mission_started`, шаги, `recovery_retry`, `fallback_taken`, `mission_finished`) возвращается в **`MissionResult.events`**.
- При финальном сбое и при вызове fallback пишутся **`Incident`** с кодами (`step_execution_failed`, `fallback_invoked`, `invalid_fallback`, …).
- **Ветвление:** опциональное поле шага **`fallback_step_id`** — после решения policy **ABORT** переход к шагу с данным `id` вместо `FAILED` (если целевой шаг не найден — `FAILED` + `invalid_fallback`).

## Webots на хосте (S2-B8)

- Установка Webots + **`ros-humble-webots-ros2`**, проверка примеров (минимум — launch с манипулятором из дистрибутива). См. [webots_host_s2b8.md](webots_host_s2b8.md), скрипт `scripts/check_webots_ros2.sh` · каталог [webots/](../webots/README.md).
