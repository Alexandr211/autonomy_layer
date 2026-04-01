# S2-B9: Webots паритет `warehouse_pilot_v1` (демо/запись)

Задача S2-B9: воспроизвести тот же сценарий, что и в PyBullet (`navigate_to_pick` → `grasp` → `place`), но в **Webots**, и подготовить запись для демо.

Базовая идея для v1:
- Webots поднимаем на готовом универсальном мире `universal_robot.wbt` (параллельно со S2-B8 мы подтвердили связку Webots ↔ ROS 2 ↔ драйвер).
- “warehouse” часть в v1 имитируем **движениями UR5e** (и закрытием/открытием пальцев грейпера), соответствующими шагам миссии.
- Склад/манипулятор в полном виде — это S2-B9.2 (следующая итерация мира `.wbt`), но для паритета интерфейса и демо этого уже достаточно.

## Предусловия

1. S2-B8 пройден: `webots_ros2_universal_robot` запускается, `robot_world_launch.py` + `robot_nodes_launch.py` работают.
2. На хосте: ROS 2 **Jazzy** или **Humble** и пакет `webots_ros2` установлен.
3. У тебя в системе есть `python3` и зависимости `rclpy`/`control_msgs`/`trajectory_msgs` (они идут с ROS 2).

## Скрипт демо (скриптованный прогон)

1. Открой терминал и запусти:

```bash
cd /workspace/autonomy_layer
chmod +x scripts/webots_run_s2b9_demo.sh scripts/webots_warehouse_pilot_demo.py
./scripts/webots_run_s2b9_demo.sh
```

2. Скрипт поднимает:
   - `webots_ros2_universal_robot/robot_world_launch.py` (мир `universal_robot.wbt`)
   - `webots_ros2_universal_robot/robot_nodes_launch.py` (контроллеры UR5e)
   - затем выполняет 3 шага через `FollowJointTrajectory` (см. `scripts/webots_warehouse_pilot_demo.py`)

Успешность: в консоли должны появляться `Step: navigate_to_pick / grasp / place` и `Completed: ...`.
Проверено на хосте: `webots_run_s2b9_demo.sh` завершился с `webots S2-B9 demo completed`.
Видео для демо подготовлено: запись сгенерирована/закодирована в Webots (ошибка `ffmpeg: not found` устранена).

## Где делать запись для демо

В v1 записи самый простой вариант:
- запускаем Webots в GUI (а не `--batch`),
- и делаем запись экрана на время прогона (например `ffmpeg` или запись через системный тул).

Если хочешь, скажи как ты обычно записываешь (OBS / ffmpeg / встроенный рекордер) — добавлю точную команду под твою схему.

## Что “считать паритетом”

Для Sprint 2 (v1) паритет — это совпадение **формы реакции**:
- шаги миссии выполняются в правильном порядке,
- “grasp” визуально меняет состояние грейпера,
- “place” переводит робота в другую позу и возвращает грейпер в открытое состояние.

Точный визуальный контур склада (.wbt со стеллажами) — следующий подэтап после того, как интерфейс и fallback-тракт синхронизированы между PyBullet и Webots.

