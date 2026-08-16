from __future__ import annotations


class PlannerError(Exception):
    pass


class ValidationError(PlannerError):
    pass


class RiskAnalysisError(PlannerError):
    pass


class DependencyError(PlannerError):
    pass


class VerificationError(PlannerError):
    pass


class UnsupportedCapabilityError(PlannerError):
    pass


class MalformedPlanError(PlannerError):
    pass
