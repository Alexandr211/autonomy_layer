#!/usr/bin/env bash
set -euo pipefail

# S2-B9 demo runner:
# 1) Start Webots world (robotic arms example)
# 2) Start Webots ROS2 nodes (UR5e controller + spawners)
# 3) Send 3 mission-like steps: navigate_to_pick -> grasp -> place
#
# Run in two terminals is fine; this script attempts to automate it in one.

ROS_SETUP="${ROS_SETUP:-/opt/ros/jazzy/setup.bash}"
export WEBOTS_HOME="${WEBOTS_HOME:-/snap/webots/current/usr/share/webots}"

WORLD_FILE="${WORLD_FILE:-universal_robot.wbt}"

launch_world() {
  # `source /opt/ros/.../setup.bash` may reference unset variables.
  # With `set -u` enabled this would fail (AMENT_TRACE_SETUP_FILES unbound),
  # so temporarily disable nounset around `source`.
  set +u
  source "$ROS_SETUP"
  set -u
  export WEBOTS_HOME
  ros2 launch webots_ros2_universal_robot robot_world_launch.py "world:=$WORLD_FILE" >/tmp/webots_s2b9_world.log 2>&1 &
  echo $!
}

launch_nodes() {
  set +u
  source "$ROS_SETUP"
  set -u
  export WEBOTS_HOME
  ros2 launch webots_ros2_universal_robot robot_nodes_launch.py >/tmp/webots_s2b9_nodes.log 2>&1 &
  echo $!
}

kill_bg() {
  local pid="$1"
  if [[ -n "${pid}" ]] && kill -0 "$pid" 2>/dev/null; then
    kill "$pid" 2>/dev/null || true
  fi
}

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

WORLD_PID=""
NODES_PID=""
cleanup() {
  kill_bg "$NODES_PID"
  kill_bg "$WORLD_PID"
}
trap cleanup EXIT

WORLD_PID="$(launch_world)"
echo "Started world pid=$WORLD_PID"
sleep 10

NODES_PID="$(launch_nodes)"
echo "Started nodes pid=$NODES_PID"

export PYTHONPATH="$REPO_ROOT"
set +u
source "$ROS_SETUP"
set -u

python3 "$REPO_ROOT/scripts/webots_warehouse_pilot_demo.py"
echo "webots S2-B9 demo completed"

