
from desktop_agent.models import AuditLogEntry


class AuditLogger:
    def __init__(self) -> None:
        self._entries: list[AuditLogEntry] = []

    def log(self, entry: AuditLogEntry) -> None:
        self._entries.append(entry)

    def get_entries(self, agent_id: str | None = None) -> list[AuditLogEntry]:
        if not agent_id:
            return list(self._entries)
        return [e for e in self._entries if e.agent_id == agent_id]
