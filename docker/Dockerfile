# Simulation-first: ROS 2 Humble (Jammy) + PyBullet. Webots — на хосте; см. docs/simulator_alternatives.md
FROM ros:humble-ros-base-jammy

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3-pip \
        python3-colcon-common-extensions \
        build-essential \
        cmake \
    && pip3 install --no-cache-dir pybullet \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY ros2_ws /workspace/ros2_ws
ENV PYTHONPATH=/workspace
RUN bash -lc "source /opt/ros/humble/setup.bash && cd /workspace/ros2_ws && colcon build --merge-install"

COPY docker/entrypoint.bash /entrypoint.bash
RUN chmod +x /entrypoint.bash

RUN bash -lc "source /opt/ros/humble/setup.bash && source /workspace/ros2_ws/install/setup.bash && ros2 interface show autonomy_msgs/action/MissionExecute"

ENTRYPOINT ["/entrypoint.bash"]
CMD ["bash"]
