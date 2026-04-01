#!/usr/bin/env bash
set -eo pipefail
# ROS setup scripts reference unset vars (e.g. AMENT_TRACE_SETUP_FILES); disable nounset while sourcing.
set +u
# shellcheck source=/dev/null
source /opt/ros/humble/setup.bash

if [[ -f /workspace/ros2_ws/install/setup.bash ]]; then
  # shellcheck source=/dev/null
  source /workspace/ros2_ws/install/setup.bash
fi
export PYTHONPATH=/workspace
set -u

exec "$@"
