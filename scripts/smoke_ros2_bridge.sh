#!/usr/bin/env bash
# Smoke: colcon build (if needed), run mission_bridge_node, send one MissionExecute goal.
# Usage (from repo root): docker compose run --rm autonomy-sim bash scripts/smoke_ros2_bridge.sh
set -eo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"
export PYTHONPATH="$REPO_ROOT"
set +u
source /opt/ros/humble/setup.bash
cd ros2_ws
if [[ ! -f install/setup.bash ]]; then
  colcon build --merge-install
fi
# shellcheck source=/dev/null
source install/setup.bash
set -u

ros2 run autonomy_mission_bridge mission_bridge_node &
PID=$!
sleep 4

ros2 action send_goal /autonomy/mission/execute autonomy_msgs/action/MissionExecute "{mission: {mission_id: 'smoke-1', scenario_id: 'hello', steps: [{id: 's1', action: 'navigate', params_json: '{}', fallback_step_id: ''}, {id: 's2', action: 'pick', params_json: '{}', fallback_step_id: ''}, {id: 's3', action: 'place', params_json: '{}', fallback_step_id: ''}]}}"

kill "$PID" 2>/dev/null || true
wait "$PID" 2>/dev/null || true
echo "smoke_ros2_bridge: ok"
