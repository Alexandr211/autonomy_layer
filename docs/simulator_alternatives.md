# Стек симуляции: Webots + PyBullet (baseline)

**Gazebo / OSRF в базовой линии проекта не используем** — вместо этого зафиксированы две роли:

| Слой | Инструмент | Назначение |
| --- | --- | --- |
| **3D-сим, демо, ROS 2** | **Webots** (+ `webots_ros2`) | Склад, манипулятор, **рендер для инвестора**, интеграционные прогоны с камерой и сценой. |
| **Быстрые тесты, CI, оркестрация** | **PyBullet** | Лёгкая физика, **детерминированные** сценарии без поднятия Webots; уже в Docker-образе `autonomy-layer:sim-humble`. |

Логический сим (`autonomy_layer/sim/`, `SimulationExecutor`) остаётся для минимальных сценариев и регрессов без физики.

---

## Webots

- Сайт: [Cyberbotics Webots](https://cyberbotics.com/)
- ROS 2: [webots_ros2](https://github.com/cyberbotics/webots_ros2)
- **Ставится на хост** (или отдельный образ позже); в текущий `Dockerfile` не включён из‑за размера и GUI.

Чеклист установки и проверки **`webots_ros2`** (S2-B8): [webots_host_s2b8.md](webots_host_s2b8.md). Проектные сцены: каталог [webots/](../webots/README.md).

Рекомендуемый рабочий процесс: одна машина с **достаточным GPU** (например RTX 3050 8 GB) для записи демо и интеграционных тестов с Webots.

---

## PyBullet

- **В Docker:** `pip install pybullet` (см. `docker/Dockerfile`).
- **На хосте:** `pip install pybullet` в venv при необходимости.

Использование: ускорение разработки **policy / recovery / failure injection** без полного 3D-контура; не обязан совпадать 1:1 с физикой Webots.

---

## Докер-образ `autonomy-layer:sim-humble`

- **ROS 2 Humble** + **PyBullet** — без Webots внутри образа.
- См. [docker/README.md](../docker/README.md).

---

## Другие движки (не в baseline)

- **NVIDIA Isaac Sim** — если позже понадобится максимальный фотореализм и есть ресурс на NVIDIA-стек.
- **MuJoCo** — при сильном уклоне в контроль/ML.
- **Gazebo** — только при явной необходимости и стабильном доступе к OSRF; не входит в текущий план Sprint 1–2.
