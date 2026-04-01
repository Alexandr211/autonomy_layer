# Universal Autonomy Layer - Sprint 2 (Weeks 3-4) Orchestration v1

## Статус спринта

**Завершен** (задачи `S2-B1..S2-B11` выполнены).

## Результаты спринта

### 1) Оркестрация и восстановление
- Runtime-оркестрация расширена: `replay_id`, поток событий миссии, инциденты, fallback-переходы.
- Добавлена политика `RecoveryPolicyV1` (`autonomy_layer/core/recovery_policy.py`):
  - timeout: ограниченный retry, затем `abort`;
  - action failure: ограниченный retry, затем `safe_stop`;
  - прочие ошибки: `abort`.
- В `MissionRuntime` обновлена интеграция `RecoveryContext`: передаются лимиты `max_timeout_retries` и `max_action_retries`.

### 2) Обновление telemetry (S2-B10)
- Расширен KPI-снимок в `autonomy_layer/telemetry/metrics.py`:
  - `incidents_total`;
  - `incidents_by_code`;
  - `safe_stop_rate`;
  - `retries_per_mission_avg`.

### 3) Интеграция с ROS 2
- `mission_bridge_node` переведен на `RecoveryPolicyV1`:
  - `ros2_ws/src/autonomy_mission_bridge/autonomy_mission_bridge/mission_bridge_node.py`.
- Контракты action и публикация status/events сохранены в соответствии со Sprint 2.

### 4) Покрытие проверками
- Обновлены и расширены тесты в `tests/test_mission_orchestration_sprint2.py`:
  - `safe_stop` при action failure с v1-политикой;
  - retry для action failure с последующим `safe_stop` при исчерпании лимита;
  - проверки telemetry по `incidents_by_code` и `safe_stop_rate`.
- Существующее acceptance-покрытие для PyBullet и детерминированной инъекции сбоев сохранено.

### 5) Демо-контур и runbook (S2-B11)
- Runbook включен в этот же отчет (см. раздел `Runbook Sprint 2`).
- Для Webots поддержан сценарий с шагом release:
  - `navigate_to_pick -> grasp -> place -> release`.

## Проверка Definition of Done

- E2E-сценарий в PyBullet с детерминированными сбоями: **Done**
- Визуальный паритет сценария в Webots + ROS 2 bridge: **Done**
- Recovery policy v1 + telemetry по типам инцидентов: **Done**
- Воспроизводимый runbook и отчет по спринту: **Done**

## Runbook Sprint 2

Ниже приведен минимальный набор команд для запуска и проверки артефактов Sprint 2.

### 1) Локально (Python)

```bash
python3 -m unittest tests/test_mission_orchestration_sprint2.py
python3 -m unittest tests/test_acceptance_sprint2_pybullet.py
```

Примечание: `test_acceptance_sprint2_pybullet.py` будет `skipped`, если `pybullet` не установлен в текущем окружении.

### 2) Docker (рекомендуемый путь для acceptance)

```bash
docker compose build
docker compose run --rm autonomy-sim python3 -m unittest discover -s tests -p "test_*.py"
```

### 3) ROS 2 bridge smoke

```bash
docker compose run --rm autonomy-sim bash scripts/smoke_ros2_bridge.sh
```

Ожидаемый результат:
- стартует `mission_bridge_node`;
- action `/autonomy/mission/execute` принимает миссию;
- публикуются `/autonomy/mission/status` и `/autonomy/mission/events`.

### 4) Webots + ROS 2 на хосте

Проверка доступности пакетов:

```bash
source /opt/ros/jazzy/setup.bash
bash scripts/check_webots_ros2.sh
```

Запуск S2-B9 демо:

```bash
bash scripts/webots_run_s2b9_demo.sh
```

Ожидаемый результат:
- поднимаются world и nodes из `webots_ros2_universal_robot`;
- выполняются шаги `navigate_to_pick -> grasp -> place -> release`.

### 5) Политика восстановления v1

- `StepTimeoutError`: retry до `max_timeout_retries`, затем `abort`.
- `StepActionError`: retry до `max_action_retries`, затем `safe_stop`.
- Прочие ошибки: `abort`.

По умолчанию в ROS 2 bridge используется `RecoveryPolicyV1(max_timeout_retries=1, max_action_retries=0)`.

### 6) Telemetry (обновлено в S2-B10)

`autonomy_layer.telemetry.metrics.compute_snapshot` теперь включает:
- `incidents_total`;
- `incidents_by_code`;
- `safe_stop_rate`;
- `retries_per_mission_avg`.

### 7) Быстрый чек перед демо

- Убедиться, что `ros2_ws` собран (`colcon build --merge-install`).
- Для Webots запускать на хосте, где установлен `webots_ros2_universal_robot`.
- Для CI/автотестов использовать Docker-образ проекта.

## Примечания

- IDE может показывать нерезолвленные ROS-импорты вне окружения с `source`; рабочая проверка выполняется в sourced shell или в Docker.
- Для стабильных acceptance-прогонов использовать Docker-команды из runbook-раздела выше.
