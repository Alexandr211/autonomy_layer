#!/usr/bin/env bash
# Проверка наличия пакетов webots_ros2 в ROS 2 Humble (хост).
# Перед запуском: source /opt/ros/humble/setup.bash
set -eo pipefail
if ! command -v ros2 >/dev/null 2>&1; then
  echo "ros2 не найден в PATH. Выполните: source /opt/ros/humble/setup.bash"
  exit 1
fi
if ! ros2 pkg list 2>/dev/null | grep -q '^webots_ros2'; then
  echo "Пакеты webots_ros2 не найдены. Установите: sudo apt-get install ros-humble-webots-ros2"
  exit 1
fi
echo "OK: найдены пакеты webots_ros2:"
ros2 pkg list | grep '^webots_ros2' || true
echo "Дальше: запуск примера см. docs/webots_host_s2b8.md"
exit 0
