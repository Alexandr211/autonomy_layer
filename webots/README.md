# Webots: проектные сцены (хост)

Webots **не входит** в Docker-образ `autonomy-layer:sim-humble` (GUI, размер). Разработка 3D-сцен — на **хосте** с установленными Webots и `ros-humble-webots-ros2`.

## S2-B8 / S2-B9

- **S2-B8:** установка и проверка `webots_ros2` — см. [docs/webots_host_s2b8.md](../docs/webots_host_s2b8.md).
- **S2-B9:** перенос логики сценария `warehouse_pilot_v1` в Webots и при необходимости файлы миров сюда.

## Каталог `worlds/`

Сюда можно класть собственные `.wbt` и protos (например форк официального примера после **File → Save As**). Пока каталог может быть пустым — минимальная проверка идёт через launch-пакеты из apt.
