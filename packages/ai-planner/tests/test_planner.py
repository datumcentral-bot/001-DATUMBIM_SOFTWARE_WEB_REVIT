import pytest

from ai_planner.decomposer import PlanDecomposer
from ai_planner.dependencies import DependencyResolver
from ai_planner.models import ActionPlan, ActionProposal, GoalRequest, PlanningContext, PlanStatus, RiskLevel, ValidationResult, VerificationStrategyType
from ai_planner.planner import PlannerEngine
from ai_planner.planners.mock import MockPlannerProvider
from ai_planner.risk import RiskAnalyzer
from ai_planner.validator import PlanValidator
from ai_planner.verifier import VerificationStrategy


class TestDecomposer:
    def test_decompose_returns_plan(self) -> None:
        decomposer = PlanDecomposer()
        goal = GoalRequest(goal_id="goal-1", user_request="Open Revit")
        plan = decomposer.decompose(goal)
        assert plan.plan_id is not None
        assert plan.goal_id == "goal-1"
        assert len(plan.actions) >= 1

    def test_decompose_includes_detect_application(self) -> None:
        decomposer = PlanDecomposer()
        goal = GoalRequest(goal_id="goal-1", user_request="Open Revit", application_id="revit")
        plan = decomposer.decompose(goal)
        action_types = [action.action_type for action in plan.actions]
        assert "detect_application" in action_types


class TestValidator:
    def test_valid_plan_passes(self) -> None:
        validator = PlanValidator()
        plan = ActionPlan(plan_id="plan-1", goal_id="goal-1", title="Test", objective="Test", summary="Test", actions=[])
        result = validator.validate(plan)
        assert result.valid is False
        assert "no actions" in str(result.errors).lower()

    def test_plan_with_actions_passes(self) -> None:
        validator = PlanValidator()
        action = ActionProposal(action_id="a1", sequence=1, action_type="click", description="Click", verification_strategy=VerificationStrategyType.screen_changed)
        plan = ActionPlan(plan_id="plan-1", goal_id="goal-1", title="Test", objective="Test", summary="Test", actions=[action])
        result = validator.validate(plan)
        assert result.valid is True

    def test_missing_verification_warns(self) -> None:
        validator = PlanValidator()
        action = ActionProposal(action_id="a1", sequence=1, action_type="click", description="Click")
        plan = ActionPlan(plan_id="plan-1", goal_id="goal-1", title="Test", objective="Test", summary="Test", actions=[action])
        result = validator.validate(plan)
        assert any("verification" in str(w).lower() for w in result.warnings)


class TestRiskAnalyzer:
    def test_low_risk_plan(self) -> None:
        analyzer = RiskAnalyzer()
        action = ActionProposal(action_id="a1", sequence=1, action_type="view", description="View", risk_level=RiskLevel.low, reversible=True)
        plan = ActionPlan(plan_id="plan-1", goal_id="goal-1", title="Test", objective="Test", summary="Test", actions=[action])
        assessment = analyzer.analyze(plan)
        assert assessment.level == RiskLevel.low
        assert assessment.approval_required is False
        assert assessment.reversible is True

    def test_critical_risk_requires_approval(self) -> None:
        analyzer = RiskAnalyzer()
        action = ActionProposal(action_id="a1", sequence=1, action_type="delete", description="Delete", risk_level=RiskLevel.critical, reversible=False)
        plan = ActionPlan(plan_id="plan-1", goal_id="goal-1", title="Test", objective="Test", summary="Test", actions=[action])
        assessment = analyzer.analyze(plan)
        assert assessment.level == RiskLevel.critical
        assert assessment.approval_required is True
        assert assessment.reversible is False


class TestDependencyResolver:
    def test_valid_order(self) -> None:
        resolver = DependencyResolver()
        action1 = ActionProposal(action_id="a1", sequence=1, action_type="step1", description="Step 1")
        action2 = ActionProposal(action_id="a2", sequence=2, action_type="step2", description="Step 2", dependencies=["a1"])
        plan = ActionPlan(plan_id="plan-1", goal_id="goal-1", title="Test", objective="Test", summary="Test", actions=[action2, action1])
        resolved = resolver.resolve(plan)
        assert resolved.actions[0].action_id == "a1"
        assert resolved.actions[1].action_id == "a2"

    def test_cycle_detection(self) -> None:
        resolver = DependencyResolver()
        action1 = ActionProposal(action_id="a1", sequence=1, action_type="step1", description="Step 1", dependencies=["a2"])
        action2 = ActionProposal(action_id="a2", sequence=2, action_type="step2", description="Step 2", dependencies=["a1"])
        plan = ActionPlan(plan_id="plan-1", goal_id="goal-1", title="Test", objective="Test", summary="Test", actions=[action1, action2])
        with pytest.raises(Exception):
            resolver.resolve(plan)


class TestVerificationStrategy:
    def test_valid_screen_changed(self) -> None:
        action = ActionProposal(action_id="a1", sequence=1, action_type="click", description="Click", verification_strategy=VerificationStrategyType.screen_changed)
        assert VerificationStrategy.validate(action) is True

    def test_valid_text_detected_with_text(self) -> None:
        action = ActionProposal(action_id="a1", sequence=1, action_type="click", description="Click", verification_strategy=VerificationStrategyType.text_detected, verification_parameters={"text": "hello"})
        assert VerificationStrategy.validate(action) is True

    def test_invalid_text_detected_without_text(self) -> None:
        action = ActionProposal(action_id="a1", sequence=1, action_type="click", description="Click", verification_strategy=VerificationStrategyType.text_detected, verification_parameters={})
        assert VerificationStrategy.validate(action) is False


class TestMockPlanner:
    def test_plan_returns_deterministic_plan(self) -> None:
        provider = MockPlannerProvider()
        goal = GoalRequest(goal_id="goal-1", user_request="Open Revit", application_id="revit")
        plan = provider.plan(goal)
        assert plan.status == PlanStatus.draft
        assert len(plan.actions) >= 1
        assert plan.planner_provider == "mock"

    def test_explain_returns_text(self) -> None:
        provider = MockPlannerProvider()
        goal = GoalRequest(goal_id="goal-1", user_request="Open Revit", application_id="revit")
        plan = provider.plan(goal)
        explanation = provider.explain(plan)
        assert "PLAN:" in explanation
        assert "STEPS:" in explanation

    def test_estimate_risk_returns_dict(self) -> None:
        provider = MockPlannerProvider()
        goal = GoalRequest(goal_id="goal-1", user_request="Open Revit", application_id="revit")
        plan = provider.plan(goal)
        risk = provider.estimate_risk(plan)
        assert "level" in risk
        assert "approval_required" in risk


class TestPlannerEngine:
    def test_plan_without_provider_uses_decomposer(self) -> None:
        engine = PlannerEngine()
        goal = GoalRequest(goal_id="goal-1", user_request="Open Revit", application_id="revit")
        plan = engine.plan(goal)
        assert plan.status in (PlanStatus.ready, PlanStatus.awaiting_approval)
        assert len(plan.actions) >= 1

    def test_plan_with_mock_provider(self) -> None:
        engine = PlannerEngine(provider=MockPlannerProvider())
        goal = GoalRequest(goal_id="goal-1", user_request="Open Revit", application_id="revit")
        plan = engine.plan(goal)
        assert plan.planner_provider == "mock"
