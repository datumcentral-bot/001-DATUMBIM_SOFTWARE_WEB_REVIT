from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel


class PlanStatus(str, Enum):
    draft = "draft"
    validating = "validating"
    ready = "ready"
    awaiting_approval = "awaiting_approval"
    approved = "approved"
    executing = "executing"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"
    verification_failed = "verification_failed"


class ActionStatus(str, Enum):
    proposed = "proposed"
    validated = "validated"
    awaiting_approval = "awaiting_approval"
    approved = "approved"
    rejected = "rejected"
    executing = "executing"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"
    verification_failed = "verification_failed"


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class VerificationStrategyType(str, Enum):
    screen_changed = "screen_changed"
    window_changed = "window_changed"
    element_detected = "element_detected"
    text_detected = "text_detected"
    property_changed = "property_changed"
    file_created = "file_created"
    file_modified = "file_modified"
    application_state_changed = "application_state_changed"
    observation_match = "observation_match"
    custom = "custom"


class PlanningContext(BaseModel):
    application_id: str | None = None
    application_name: str | None = None
    session_id: str | None = None
    active_window: str | None = None
    active_document: str | None = None
    active_view: str | None = None
    selected_elements: list[str] = []
    observation_id: str | None = None
    available_capabilities: list[str] = []
    recent_actions: list[dict[str, Any]] = []
    recent_observations: list[str] = []
    project_id: str | None = None
    user_preferences: dict[str, Any] = {}


class GoalRequest(BaseModel):
    goal_id: str
    user_request: str
    session_id: str | None = None
    application_id: str | None = None
    requested_by: str = "system"
    context: PlanningContext | None = None
    constraints: list[str] = []
    preferred_provider: str | None = None
    preferred_model: str | None = None
    dry_run: bool = False
    timestamp: Any = None


class ActionProposal(BaseModel):
    action_id: str
    sequence: int
    action_type: str
    description: str
    application_id: str | None = None
    session_id: str | None = None
    parameters: dict[str, Any] = {}
    preconditions: list[str] = []
    expected_result: str | None = None
    verification_strategy: VerificationStrategyType | None = None
    verification_parameters: dict[str, Any] = {}
    risk_level: RiskLevel = RiskLevel.low
    approval_required: bool = False
    reversible: bool = True
    estimated_duration: float | None = None
    dependencies: list[str] = []
    confidence: float | None = None
    source: str = "mock"
    status: ActionStatus = ActionStatus.proposed


class ActionPlan(BaseModel):
    plan_id: str
    goal_id: str
    title: str
    objective: str
    summary: str
    application_id: str | None = None
    session_id: str | None = None
    context: PlanningContext | None = None
    actions: list[ActionProposal] = []
    dependencies: dict[str, list[str]] = {}
    risk_level: RiskLevel = RiskLevel.low
    approval_required: bool = False
    estimated_duration: float | None = None
    confidence: float | None = None
    expected_observations: list[str] = []
    success_criteria: list[str] = []
    rollback_strategy: str | None = None
    planner_provider: str | None = None
    planner_model: str | None = None
    created_at: Any = None
    status: PlanStatus = PlanStatus.draft


class ValidationResult(BaseModel):
    valid: bool
    errors: list[str] = []
    warnings: list[str] = []
    normalized_plan: ActionPlan | None = None


class RiskAssessment(BaseModel):
    level: RiskLevel
    reasons: list[str] = []
    approval_required: bool = False
    reversible: bool = True
    affected_resources: list[str] = []
    warnings: list[str] = []
