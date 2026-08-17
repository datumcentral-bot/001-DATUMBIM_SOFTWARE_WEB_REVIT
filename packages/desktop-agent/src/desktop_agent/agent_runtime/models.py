from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel


class AutonomyLevel(str, Enum):
    LEVEL_0 = "level_0"
    LEVEL_1 = "level_1"
    LEVEL_2 = "level_2"
    LEVEL_3 = "level_3"
    LEVEL_4 = "level_4"


class FailurePolicy(str, Enum):
    FAIL_FAST = "fail_fast"
    RETRY = "retry"
    REPLAN = "replan"
    FALLBACK_TOOL = "fallback_tool"
    ASK_USER = "ask_user"


class VerificationState(str, Enum):
    NOT_REQUIRED = "not_required"
    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"
    UNAVAILABLE = "unavailable"


class AgentRunStatus(str, Enum):
    QUEUED = "queued"
    PLANNING = "planning"
    WAITING_APPROVAL = "waiting_approval"
    RUNNING = "running"
    OBSERVING = "observing"
    VERIFYING = "verifying"
    REPLANNING = "replanning"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"
    MAX_STEPS_REACHED = "max_steps_reached"


class AgentStepStatus(str, Enum):
    QUEUED = "queued"
    PLANNING = "planning"
    WAITING_APPROVAL = "waiting_approval"
    RUNNING = "running"
    OBSERVING = "observing"
    VERIFYING = "verifying"
    REPLANNING = "replanning"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"
    SKIPPED = "skipped"


class AgentDefinition(BaseModel):
    agent_id: str
    name: str
    description: str
    version: str | None = None
    provider: str = "datumbim"
    model: str | None = None
    system_policy: str = "safe_default"
    tools: list[str] = []
    allowed_integrations: list[str] = []
    allowed_applications: list[str] = []
    permissions: list[str] = []
    approval_policy: str = "required"
    max_steps: int = 10
    max_execution_time: int = 300
    max_retries: int = 2
    max_tool_calls: int = 20
    enabled: bool = True
    memory_policy: str = "run_scoped"
    observation_policy: str = "after_relevant_actions"
    verification_policy: str = "explicit"
    failure_policy: FailurePolicy = FailurePolicy.REPLAN
    autonomy_level: AutonomyLevel = AutonomyLevel.LEVEL_2


class AgentRun(BaseModel):
    run_id: str
    agent_id: str
    goal: str
    status: AgentRunStatus = AgentRunStatus.QUEUED
    session_id: str | None = None
    application_id: str | None = None
    created_at: datetime | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    current_step: int = 0
    max_steps: int = 10
    steps: list[dict[str, Any]] = []
    result: Any = None
    error: str | None = None
    verification_state: VerificationState = VerificationState.NOT_REQUIRED
    metadata: dict[str, Any] = {}


class AgentStep(BaseModel):
    step_id: str
    run_id: str
    sequence: int
    goal: str
    thought_summary: str = ""
    tool_id: str | None = None
    parameters: dict[str, Any] = {}
    status: AgentStepStatus = AgentStepStatus.QUEUED
    approval_state: str = "pending"
    execution_id: str | None = None
    observation_id: str | None = None
    verification_state: VerificationState = VerificationState.NOT_REQUIRED
    result: Any = None
    error: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    metadata: dict[str, Any] = {}
