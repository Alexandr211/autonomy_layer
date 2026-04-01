# Доска выполнения Sprint 1 (Foundation)

## Статус спринта

- Спринт: **В работе**
- Этап: **Weeks 1-2 Foundation**
- Итог: базовый Python-контур реализован; Sprint 1 не закрыт до фиксации sim/ROS2 baseline.

## Backlog

- [x] B1: Подтвердить use-case v1 и базовые KPI для Foundation
- [x] B2: Создать структуру модулей (`core/sim/telemetry/tests/docs`)
- [x] B3: Реализовать state machine жизненного цикла миссии
- [x] B4: Реализовать runtime loop и модель результата выполнения
- [x] B5: Реализовать simulation adapter и сценарий hello mission
- [x] B6: Добавить KPI telemetry v0
- [x] B7: Добавить failure injection + recovery policy v0
- [x] B8: Добавить acceptance-тесты и отчет/runbook по этапу
- [x] B9: Зафиксировать стек симуляции: **Webots** (3D/демо) + **PyBullet** (CI/быстрые тесты; см. `docs/simulator_alternatives.md`)
- [x] B10: Выполнить базовую установку/проверку `ROS2` (workspace + минимальный контур запуска)

## In Progress

- [ ] Нет активных задач Sprint 1

## Done

- [x] Инициализирован проект и пакетная структура
- [x] Добавлены core-модули (`models`, `state_machine`, `mission_runtime`)
- [x] Добавлены sim-модули (`simulation_adapter`, `scenario_hello_mission`)
- [x] Добавлен telemetry-модуль (`metrics`)
- [x] Реализованы ошибки исполнения (`StepTimeoutError`, `StepActionError`)
- [x] Реализован `failure_injection` с детерминированными отказами
- [x] Реализован `recovery_policy v0` (timeout -> retry один раз, иначе abort)
- [x] Добавлены 3 acceptance-теста: happy path, timeout fail, action fail
- [x] Обновлен `README.md` (запуск демо, запуск тестов, таблица policy v0)
- [x] Проверено выполнение демо и прохождение тестов
- [x] Сформирован итоговый отчет в `docs/reports/autonomy_layer_sprint1_foundation.md`
- [x] Зафиксирован baseline: **ROS2 Docker + PyBullet**; **Webots** — для 3D и инвесторского демо на хосте; см. `docs/simulator_alternatives.md`
- [x] Проверен ROS2 baseline в изолированной среде Docker (`ros2 topic list`; образ `autonomy-layer:sim-humble`)
