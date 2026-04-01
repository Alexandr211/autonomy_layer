# Universal Autonomy Layer - Sprint 1 (Weeks 1-2) Foundation

## Sprint Status

**Completed** (Foundation scope delivered, including sim/ROS2 baseline).

## Delivered Results

### 1) Repository and module foundation
- Created package structure with core modules:
  - `autonomy_layer/core/models.py`
  - `autonomy_layer/core/state_machine.py`
  - `autonomy_layer/core/mission_runtime.py`
- Created simulation modules:
  - `autonomy_layer/sim/simulation_adapter.py`
  - `autonomy_layer/sim/scenario_hello_mission.py`
- Created telemetry module:
  - `autonomy_layer/telemetry/metrics.py`
- Added package init files for root and subpackages.

### 2) Mission lifecycle and runtime
- Implemented mission states and transition validation:
  - `queued -> running -> succeeded|failed|safe_stopped`
  - controlled retry path from `failed -> running` supported by state machine.
- Implemented deterministic runtime execution and result model.

### 3) Failure handling (v0)
- Added failure injection framework:
  - `autonomy_layer/sim/failure_injection.py`
  - failure types: timeout, action.
- Added execution errors:
  - `autonomy_layer/core/errors.py`
  - `StepTimeoutError`, `StepActionError`.
- Added recovery policy v0:
  - `autonomy_layer/core/recovery_policy.py`
  - timeout: retry once (configurable via `max_timeout_retries`)
  - action/unknown error: abort.

### 4) Telemetry and docs
- Implemented KPI snapshot output:
  - `mission_success_rate`
  - `mttr_seconds`
  - `auto_recovery_rate`
  - `manual_interventions_count`
- Updated `README.md`:
  - demo run command
  - acceptance test command
  - failure-to-policy behavior table for v0.

### 5) Acceptance tests
- Added `tests/test_acceptance_sprint1.py` with 3 deterministic scenarios:
  - happy path -> mission succeeded
  - timeout fail -> single retry then fail
  - action fail -> fail without retry.

## Verification Evidence

- Demo executed successfully:
  - `python3 -m autonomy_layer.sim.scenario_hello_mission`
  - final mission state: `succeeded`.
- Acceptance tests passed:
  - `python3 -m unittest discover -s tests -p "test_*.py"`
  - result: `Ran 3 tests ... OK`.
- Linter diagnostics for changed files: no issues.

## Definition of Done Check

- Deterministic "hello mission" demo works end-to-end: **Done**
- States implemented (`queued`, `running`, `succeeded`, `failed`, `safe_stopped`): **Done**
- Metrics emitted (`mission_success_rate`, `mttr_seconds`, `auto_recovery_rate`, `manual_interventions_count`): **Done**
- Sprint runbook/report available for another engineer: **Done**
- Simulation stack documented (`docs/simulator_alternatives.md`): **Webots** (3D/демо) + **PyBullet** (Docker image `autonomy-layer:sim-humble`): **Done**
- ROS2 baseline smoke-validated in isolated Docker environment: **Done**

## Notes for Sprint 2 Handoff

- ROS2 baseline (minimal): `docker run --rm ros:humble-ros-base ...` or project image `docker compose run --rm autonomy-sim ros2 topic list`
- Smoke output in baseline run:
  - `/parameter_events`
  - `/rosout`
- Recovery policy is intentionally minimal (v0) and ready for extension in v1.
- Clear next evolution points:
  - richer error taxonomy
  - per-step retry strategies
  - safe-stop workflows
  - expanded acceptance matrix for mixed failure sequences.
