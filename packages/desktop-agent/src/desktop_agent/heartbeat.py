from datetime import UTC, datetime

from desktop_agent.models import Heartbeat


class HeartbeatManager:
    def __init__(self, agent_id: str) -> None:
        self.agent_id = agent_id
        self._last_heartbeat: Heartbeat | None = None

    def create_heartbeat(self, status: str = "online") -> Heartbeat:
        heartbeat = Heartbeat(
            agent_id=self.agent_id,
            timestamp=datetime.now(tz=UTC),
            status=status,
        )
        self._last_heartbeat = heartbeat
        return heartbeat

    def get_last_heartbeat(self) -> Heartbeat | None:
        return self._last_heartbeat
