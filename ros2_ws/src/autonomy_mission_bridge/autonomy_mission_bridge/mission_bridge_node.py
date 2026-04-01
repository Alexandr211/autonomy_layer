from __future__ import annotations

import json

import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.node import Node

from autonomy_msgs.action import MissionExecute
from autonomy_msgs.msg import MissionEvent as RosMissionEvent
from autonomy_msgs.msg import MissionStatus as RosMissionStatus
from autonomy_layer.core.mission_runtime import MissionResult, MissionRuntime
from autonomy_layer.core.mission_trace import MissionEvent
from autonomy_layer.core.models import Mission, MissionState, MissionStep
from autonomy_layer.core.recovery_policy import RecoveryPolicyV1
from autonomy_layer.sim.simulation_adapter import SimulationExecutor


class MissionBridgeNode(Node):
    """Action server + publishers for mission status and events (Sprint 2 / S2-B7)."""

    def __init__(self) -> None:
        super().__init__("mission_bridge")
        self._runtime = MissionRuntime(recovery_policy=RecoveryPolicyV1())
        self._busy = False
        self._status_pub = self.create_publisher(RosMissionStatus, "/autonomy/mission/status", 10)
        self._events_pub = self.create_publisher(RosMissionEvent, "/autonomy/mission/events", 10)
        self._action = ActionServer(
            self,
            MissionExecute,
            "/autonomy/mission/execute",
            self._execute_callback,
            goal_callback=self._goal_callback,
            cancel_callback=self._cancel_callback,
        )

    def _goal_callback(self, _goal_request: MissionExecute.Goal) -> GoalResponse:
        if self._busy:
            self.get_logger().warn("Rejecting goal: mission already running")
            return GoalResponse.REJECT
        self._busy = True
        return GoalResponse.ACCEPT

    def _cancel_callback(self, _goal_handle) -> CancelResponse:
        return CancelResponse.ACCEPT

    def _execute_callback(self, goal_handle) -> MissionExecute.Result:
        try:
            mission = self._ros_to_core_mission(goal_handle.request.mission)
            executor = SimulationExecutor()
            result = self._runtime.run(mission, executor)
            for ev in result.events:
                self._events_pub.publish(self._core_event_to_ros(ev))
            status = self._core_to_ros_status(result, mission)
            self._status_pub.publish(status)
            res = MissionExecute.Result()
            res.status = status
            res.success = result.state == MissionState.SUCCEEDED
            res.replay_id = result.replay_id
            res.last_error = result.error or ""
            goal_handle.succeed()
            return res
        except Exception as exc:  # noqa: BLE001 — surface any executor/runtime failure to action client
            self.get_logger().error(f"Mission failed: {exc}")
            err = MissionExecute.Result()
            err.success = False
            err.last_error = str(exc)
            goal_handle.abort()
            return err
        finally:
            self._busy = False

    @staticmethod
    def _ros_to_core_mission(m) -> Mission:
        steps: list[MissionStep] = []
        for s in m.steps:
            params: dict = {}
            if s.params_json:
                try:
                    params = json.loads(s.params_json)
                except json.JSONDecodeError:
                    params = {}
            fb = (s.fallback_step_id or "").strip() or None
            steps.append(
                MissionStep(id=s.id, action=s.action, params=params, fallback_step_id=fb)
            )
        return Mission(id=m.mission_id, scenario=m.scenario_id, steps=steps)

    def _core_event_to_ros(self, ev: MissionEvent) -> RosMissionEvent:
        out = RosMissionEvent()
        out.stamp = self.get_clock().now().to_msg()
        out.mission_id = ev.mission_id
        out.event_type = ev.kind.value
        out.step_id = ev.step_id or ""
        out.message = ev.message or ""
        out.payload_json = json.dumps(ev.payload) if ev.payload else ""
        out.replay_id = ev.replay_id
        return out

    @staticmethod
    def _core_to_ros_status(result: MissionResult, mission: Mission) -> RosMissionStatus:
        s = RosMissionStatus()
        s.mission_id = result.mission_id
        s.state = result.state.value
        s.last_error = result.error or ""
        s.steps_done = result.steps_executed
        s.retries = mission.retries
        s.replay_id = result.replay_id
        return s


def main() -> None:
    rclpy.init()
    node = MissionBridgeNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        try:
            rclpy.shutdown()
        except Exception:
            pass


if __name__ == "__main__":
    main()
