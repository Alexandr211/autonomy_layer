# Docker: ROS 2 Humble + PyBullet

Образ **`autonomy-layer:sim-humble`**:

- база **`ros:humble-ros-base-jammy`**;
- **`python3-pip`** и **`pybullet`** — для быстрых тестов и симуляции без Webots.

**Webots** в этот образ **не входит** (GUI, размер, установка на хост или отдельный образ позже). Роль Webots vs PyBullet — в **[docs/simulator_alternatives.md](../docs/simulator_alternatives.md)**.

## Требования

- Docker + Docker Compose v2

## Сборка

```bash
cd /path/to/autonomy_layer
docker compose build
```

## Запуск

```bash
docker compose run --rm autonomy-sim ros2 topic list
docker compose run --rm autonomy-sim python3 -c "import pybullet; print('pybullet API', pybullet.getAPIVersion())"
docker compose run --rm autonomy-sim bash
```

Внутри контейнера выполнен `source /opt/ros/humble/setup.bash` (см. `docker/entrypoint.bash`). Если смонтирован репозиторий (`.:/workspace`), дополнительно подключается `ros2_ws/install/setup.bash` при наличии сборки и задаётся `PYTHONPATH=/workspace` для импорта `autonomy_layer`.

## ROS 2 mission bridge (S2-B7)

Интерфейсы и узел: `ros2_ws/src/autonomy_msgs`, `ros2_ws/src/autonomy_mission_bridge`. В образе выполняется `colcon build` при `docker compose build`. При **volume** на весь репозиторий каталог `ros2_ws/install` на хосте может отсутствовать — тогда один раз:

```bash
docker compose run --rm autonomy-sim bash -lc 'cd /workspace/ros2_ws && source /opt/ros/humble/setup.bash && colcon build --merge-install'
```

Smoke (узел + один goal action `MissionExecute`):

```bash
docker compose run --rm autonomy-sim bash scripts/smoke_ros2_bridge.sh
```

Ручной запуск узла: `ros2 run autonomy_mission_bridge mission_bridge_node` (после `source .../ros2_ws/install/setup.bash`).

**Webots** в этот образ не входит; установка на хосте и проверка `webots_ros2`: [../docs/webots_host_s2b8.md](../docs/webots_host_s2b8.md).

## Сеть ROS 2

По умолчанию bridge-сеть Compose. На Linux при необходимости можно включить `network_mode: host` в `docker-compose.yml`.
