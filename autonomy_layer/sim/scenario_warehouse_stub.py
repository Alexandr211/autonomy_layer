from __future__ import annotations

from autonomy_layer.core.models import Mission, MissionStep


def build_warehouse_pilot_mission() -> Mission:
    """Sprint 2 target scenario: warehouse + manipulator (stub steps; same shape as hello mission)."""
    return Mission(
        id="warehouse-pilot-001",
        scenario="warehouse_pilot_v1",
        steps=[
            MissionStep(id="w1", action="navigate_to_pick", params={"zone": "A1"}),
            MissionStep(id="w2", action="grasp", params={"object_id": "box-1"}),
            MissionStep(id="w3", action="place", params={"zone": "B2"}),
        ],
    )
