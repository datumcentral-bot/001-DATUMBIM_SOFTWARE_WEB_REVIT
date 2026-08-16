import platform
import secrets
import socket
from datetime import UTC, datetime

from desktop_agent.models import AgentRegistration


class PairingManager:
    def __init__(self) -> None:
        self._paired_agent: AgentRegistration | None = None

    def generate_token(self) -> str:
        return secrets.token_urlsafe(32)

    def register(self, machine_name: str, token: str | None = None) -> AgentRegistration:
        registration = AgentRegistration(
            agent_id=secrets.token_urlsafe(16),
            machine_name=machine_name,
            os=platform.system(),
            os_version=platform.version(),
            python_version=platform.python_version(),
            hostname=socket.gethostname(),
            ip_addresses=[],
            paired_at=datetime.now(tz=UTC),
            token=token or self.generate_token(),
            status="paired",
        )
        self._paired_agent = registration
        return registration

    def get_registration(self) -> AgentRegistration | None:
        return self._paired_agent

    def is_paired(self) -> bool:
        return self._paired_agent is not None and self._paired_agent.status == "paired"
