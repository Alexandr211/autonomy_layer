# S2-B8: Webots на хосте + `webots_ros2` (минимальная проверка)

Цель: на **хосте (GUI)** установить **Webots** и пакет **`webots_ros2`**, затем запустить штатный пример, чтобы проверить связку Webots ↔ ROS 2 ↔ драйвер. Полный паритет сценария `warehouse_pilot_v1` с PyBullet — задача **S2-B9**.

Подбираем ROS 2 под твою ОС:

- **Ubuntu 22.04 (jammy)** → ROS 2 **Humble**
- **Ubuntu 24.04 (noble)** → ROS 2 **Jazzy**

Официальный туториал ROS: [Installation (Ubuntu) — Webots](https://docs.ros.org/en/humble/Tutorials/Advanced/Simulators/Webots/Installation-Ubuntu.html).

## 1. Установить Webots

**С чего начать:** на **Ubuntu 22.04 (Jammy) amd64** с обычным рабочим столом (GUI). Достаточно **одного** из вариантов ниже. Полная матрица ОС и нюансы — в [официальной процедуре Cyberbotics](https://cyberbotics.com/doc/guide/installation-procedure).

### Вариант A — Snap (часто самый быстрый старт)

```bash
sudo snap install webots
```

Проверка в терминале:

```bash
webots --version
```

Если `webots` не в `PATH`, откройте приложение **Webots** из меню или используйте полный путь (у snap обычно есть обёртка после установки). Для интеграции с ROS 2 см. раздел про переменные ниже — snap-установка подхватывается по путям вроде `/snap/webots/current/usr/share/webots`.

### Вариант B — пакет `.deb` с GitHub

1. На странице [Releases · cyberbotics/webots](https://github.com/cyberbotics/webots/releases) скачайте **`.deb`** для Linux (например `webots_*_amd64.deb`).
2. В каталоге с файлом:

```bash
sudo apt-get install ./webots_*_amd64.deb
```

Подставьте **точное** имя скачанного файла. Частая установка в **`/usr/local/webots`**.

### Вариант C — репозиторий apt Cyberbotics

Подключение репозитория и ключей меняется от релиза к релизу; используйте только актуальные команды из [Installation Procedure](https://cyberbotics.com/doc/guide/installation-procedure), а не копипаст из сторонних блогов.

### Минимальная проверка «вручную»

Запустите симулятор (из меню или `webots`) и убедитесь, что открывается окно Webots без ошибки про драйверы OpenGL. При проблемах с GPU — обновите проприетарный драйвер NVIDIA/AMD по документации дистрибутива.

### Переменные окружения (если несколько установок)

- **`WEBOTS_HOME`** или **`ROS2_WEBOTS_HOME`** — корень **выбранной** установки Webots (как в [туториале ROS](https://docs.ros.org/en/humble/Tutorials/Advanced/Simulators/Webots/Installation-Ubuntu.html)).

Без переменных `webots_ros2` ищет Webots в типичных местах: **`/usr/local/webots`**, **`/snap/webots/current/usr/share/webots`**. Если симулятор не найден, при первом запуске примера может предложить **автоустановку** совместимой версии — для проекта надёжнее заранее поставить Webots одним из вариантов выше.

## 0. Установить ROS 2 на хост (если ещё не установлен)

Сейчас у тебя на хосте нет `/opt/ros/humble`, поэтому `source /opt/ros/humble/setup.bash` не работает. На **Ubuntu 24.04 (noble)** ставим **ROS 2 Jazzy** (official steps):

```bash
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

sudo apt install software-properties-common
sudo add-apt-repository universe

sudo apt update && sudo apt install curl -y
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb

sudo apt update
sudo apt upgrade
```

После этого переходи к установке `webots_ros2` из следующего раздела.

## 2. Установить `webots_ros2` из apt

После установки ROS 2 (см. ниже) установи пакет:

### Если ROS 2 Humble

```bash
sudo apt-get update
sudo apt-get install ros-humble-webots-ros2
```

### Если ROS 2 Jazzy (Ubuntu 24.04 / noble)

```bash
sudo apt-get update
sudo apt-get install ros-jazzy-webots-ros2
```

Пакет тянет зависимости (в т.ч. примеры вроде `*-universal-robot`).

## 3. Проверка пакетов и префикса

Выполни `source` для твоего ROS 2:

### Humble

```bash
source /opt/ros/humble/setup.bash
```

### Jazzy

```bash
source /opt/ros/jazzy/setup.bash
```

Дальше:

```bash
ros2 pkg list | grep webots_ros2
```

Локально в репозитории можно вызвать:

```bash
./scripts/check_webots_ros2.sh
```

 (ожидается, что `ros2` доступен после `source` твоего ROS 2 дистрибутива: `Humble` или `Jazzy`).

## 4. Минимальный «склад + манипулятор» на уровне S2-B8

В рамках S2-B8 **достаточно** поднять **официальный пример с манипулятором** — он подтверждает связку Webots ↔ ROS 2 ↔ драйвер:

### Терминал 1: запускаем Webots world

```bash
source /opt/ros/jazzy/setup.bash  # или /opt/ros/humble/setup.bash, если Humble
# при snap-установке Webots (как у тебя): укажи корректный корень
export WEBOTS_HOME=/snap/webots/current/usr/share/webots
ros2 launch webots_ros2_universal_robot robot_world_launch.py world:=universal_robot.wbt
```

### Терминал 2: запускаем ROS-ноды/контроллеры

```bash
source /opt/ros/jazzy/setup.bash  # или /opt/ros/humble/setup.bash, если Humble
export WEBOTS_HOME=/snap/webots/current/usr/share/webots
ros2 launch webots_ros2_universal_robot robot_nodes_launch.py
```

В терминале 2 должны появиться спавнеры контроллеров, а в логе увидеть строку вида `Successfully switched controllers!`.

Это зафиксированный **заменитель** «манипулятор в 3D» до отдельного мира склада.

> Примечание: `multirobot_launch.py` стартует сразу двух роботов (UR + ABB). В некоторых комбинациях версий/зависимостей ABB-контроллер может падать с ошибкой вида `no ros2_control tag`. Для S2-B8 используйте более надёжный `robot_nodes_launch.py`.

Отдельный визуальный контур **«склад»** (стеллажи, зона pick/place) — итерация дизайна сцены; базовая линия описана в [simulator_alternatives.md](simulator_alternatives.md). Для прототипа можно позже взять готовые миры из **File → Open Sample World** в Webots (логистика / промышленность) и перенести `.wbt` в каталог проекта `webots/worlds/` (см. [webots/README.md](../webots/README.md)).

## 5. Критерий готовности S2-B8

- [x] Webots установлен и запускается с хоста.
- [x] `*-webots-ros2` установлен (Humble: `ros-humble-webots-ros2`, Jazzy: `ros-jazzy-webots-ros2`), `ros2 pkg list` показывает пакеты `webots_ros2*`.
- [x] Пример `webots_ros2_universal_robot` успешно поднимает мир и контроллеры (`robot_world_launch.py` + `robot_nodes_launch.py`) — в логе `Successfully switched controllers!`.

Дальше: **S2-B9** — согласовать сцену с миссией `warehouse_pilot_v1` и при необходимости записать демо.
