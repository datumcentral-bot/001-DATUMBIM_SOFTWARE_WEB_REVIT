from enum import Enum

from desktop_agent.models import CommandRequest


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class Permission:
    def __init__(self, action: str, risk_level: RiskLevel = RiskLevel.low, approval_required: bool = False) -> None:
        self.action = action
        self.risk_level = risk_level
        self.approval_required = approval_required

    def requires_approval(self) -> bool:
        return self.approval_required


class PermissionEngine:
    def __init__(self) -> None:
        self._permissions: dict[str, Permission] = {}

    def register(self, action: str, risk_level: RiskLevel = RiskLevel.low, approval_required: bool = False) -> None:
        self._permissions[action] = Permission(action=action, risk_level=risk_level, approval_required=approval_required)

    def check(self, request: CommandRequest) -> tuple[bool, str | None]:
        permission = self._permissions.get(request.action)
        if not permission:
            return False, f"Unknown action: {request.action}"
        if permission.requires_approval() and request.approval_required:
            return False, "Approval required"
        return True, None
