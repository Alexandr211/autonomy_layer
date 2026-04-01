# Описание спринтов (12 недель)

Связанные документы: **[simulator_alternatives.md](../simulator_alternatives.md)** (стек **Webots + PyBullet**), **[program](../program/autonomy_layer_program_fixed_decision.md)**.

| Sprint | Недели | Файл |
| --- | --- | --- |
| 1 Foundation | 1–2 | [отчёт](../reports/autonomy_layer_sprint1_foundation.md), [доска](../boards/autonomy_layer_sprint1_execution_board.md) |
| 2 Orchestration v1 | 3–4 | [sprint2_orchestration_v1.md](sprint2_orchestration_v1.md) |
| 3 Reliability v1 | 5–6 | [sprint3_reliability_v1.md](sprint3_reliability_v1.md) |
| 4 Pilot packaging | 7–8 | [sprint4_pilot_packaging.md](sprint4_pilot_packaging.md) |
| 5 Pre-pilot hardening I | 9–10 | [sprint5_prepilot_hardening.md](sprint5_prepilot_hardening.md) |
| 6 Pre-pilot hardening II | 11–12 | [sprint6_prepilot_hardening.md](sprint6_prepilot_hardening.md) |
| Sprint 2 execution (доска) | — | [../boards/autonomy_layer_sprint2_execution_board.md](../boards/autonomy_layer_sprint2_execution_board.md) |

## Линия развития по стеку

- **Sprint 1:** Foundation + **ROS 2 в Docker** + **PyBullet**; **Webots** на хосте для 3D демо (документировано).
- **Sprint 2:** **ROS 2** как транспорт (`topic/service/action`) + оркестрация; **PyBullet** = автоматические E2E/acceptance; **Webots** = визуальный E2E и `webots_ros2`.
- **Sprint 3:** Reliability на тех же двух контурах (массовые прогоны на PyBullet, выборочно Webots).
- **Sprint 4:** API + пилотный пакет; демо-артефакт может включать **запись Webots**.
- **Sprint 5–6:** Hardening, observability, **sim → real** адаптер с учётом выбранного сим-контура.
