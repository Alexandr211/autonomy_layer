#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from typing import Sequence

import rclpy
from builtin_interfaces.msg import Duration
from control_msgs.action import FollowJointTrajectory
from rclpy.action import ActionClient
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint


JOINT_NAMES: list[str] = [
    # Keep ordering consistent with webots_ros2_universal_robot/resource/ros2_control_config.yaml
    "shoulder_pan_joint",
    "shoulder_lift_joint",
    "elbow_joint",
    "wrist_1_joint",
    "wrist_2_joint",
    "wrist_3_joint",
    "finger_1_joint_1",
    "finger_2_joint_1",
    "finger_middle_joint_1",
]


def _dur_from_sec(seconds: float) -> Duration:
    sec = int(seconds)
    nanosec = int(round((seconds - sec) * 1_000_000_000))
    return Duration(sec=sec, nanosec=nanosec)


@dataclass(frozen=True)
class Step:
    name: str
    positions: Sequence[float]
    seconds: float


DEFAULT_STEPS: list[Step] = [
    Step(
        name="navigate_to_pick",
        # Rough poses for UR5e; used only for demo visualization parity.
        positions=[
            -1.57,
            -1.20,
            1.35,
            -1.10,
            1.00,
            0.50,
            0.05,
            0.05,
            0.05,
        ],
        seconds=3.5,
    ),
    Step(
        name="grasp",
        # Close gripper (finger joints) while keeping arm pose close to pick.
        positions=[
            -1.55,
            -1.18,
            1.33,
            -1.08,
            1.00,
            0.50,
            0.80,
            0.80,
            0.80,
        ],
        seconds=2.5,
    ),
    Step(
        name="place",
        # Move to a different arm pose and close gripper (finger joints).
        positions=[
            1.20,
            -1.10,
            1.05,
            -0.90,
            0.90,
            -0.60,
            0.80,
            0.80,
            0.80,
        ],
        seconds=3.5,
    ),
    Step(
        name="release",
        # Keep place pose and open gripper to release the object.
        positions=[
            1.20,
            -1.10,
            1.05,
            -0.90,
            0.90,
            -0.60,
            0.05,
            0.05,
            0.05,
        ],
        seconds=2.0,
    ),
]


class WarehousePilotWebotsDemo(Node):
    def __init__(self, action_name: str, steps: list[Step]) -> None:
        super().__init__("warehouse_pilot_webots_demo")
        self._steps = steps
        self._client = ActionClient(self, FollowJointTrajectory, action_name)

    def run(self) -> None:
        self.get_logger().info(f"Waiting for action server...")
        if not self._client.wait_for_server(timeout_sec=60.0):
            raise RuntimeError("FollowJointTrajectory action server not available")

        for step in self._steps:
            self._send_step(step)

    def _send_step(self, step: Step) -> None:
        if len(step.positions) != len(JOINT_NAMES):
            raise ValueError(
                f"positions length mismatch for {step.name}: "
                f"{len(step.positions)} != {len(JOINT_NAMES)}"
            )

        traj = JointTrajectory()
        traj.joint_names = list(JOINT_NAMES)
        point = JointTrajectoryPoint()
        point.positions = list(step.positions)
        point.time_from_start = _dur_from_sec(step.seconds)
        traj.points = [point]

        goal_msg = FollowJointTrajectory.Goal()
        goal_msg.trajectory = traj

        self.get_logger().info(f"Step: {step.name} (t={step.seconds}s)")
        future = self._client.send_goal_async(goal_msg)
        rclpy.spin_until_future_complete(self, future)
        goal_handle = future.result()
        if goal_handle is None:
            raise RuntimeError(f"send_goal failed for step {step.name}")
        if not goal_handle.accepted:
            raise RuntimeError(f"goal rejected for step {step.name}")

        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)
        result = result_future.result()
        if result is None or result.result is None:
            raise RuntimeError(f"missing result for step {step.name}")
        if result.result.error_code != 0:
            raise RuntimeError(
                f"step {step.name} failed with error_code="
                f"{result.result.error_code}: {result.result.error_string}"
            )

        self.get_logger().info(f"Completed: {step.name}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--action-name",
        default="/ur5e/ur_joint_trajectory_controller/follow_joint_trajectory",
        help="FollowJointTrajectory action name",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    argv = argv if argv is not None else sys.argv[1:]
    args = parse_args(argv)

    rclpy.init(args=None)
    demo: WarehousePilotWebotsDemo | None = None
    try:
        demo = WarehousePilotWebotsDemo(action_name=args.action_name, steps=DEFAULT_STEPS)
        demo.run()
    finally:
        if demo is not None:
            demo.destroy_node()
        rclpy.try_shutdown()


if __name__ == "__main__":
    main()

