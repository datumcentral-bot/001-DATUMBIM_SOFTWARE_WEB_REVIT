from __future__ import annotations

import os
from datetime import UTC, datetime
from typing import Any

from desktop_agent.observation.models import ObservationResult, ObservationStoreEntry


class ObservationStore:
    def __init__(self, base_path: str | None = None) -> None:
        self.base_path = base_path or os.path.join(os.getcwd(), "observations")
        self._entries: dict[str, ObservationStoreEntry] = {}

    def save(self, result: ObservationResult) -> ObservationStoreEntry:
        if result.image_reference and "://" in result.image_reference:
            reference = result.image_reference
        else:
            filename = f"{result.observation_id}.{result.image_format}"
            reference = f"mock://observations/{filename}"
        entry = ObservationStoreEntry(
            observation_id=result.observation_id,
            session_id=result.session_id,
            application_id=result.application_id,
            target_type=result.target_type,
            target_id=result.target_id,
            image_reference=reference,
            image_format=result.image_format,
            width=result.width,
            height=result.height,
            timestamp=result.timestamp,
            duration=result.duration,
            provider=result.provider,
            metadata=result.metadata,
            error=result.error,
        )
        self._entries[result.observation_id] = entry
        return entry

    def get(self, observation_id: str) -> ObservationStoreEntry | None:
        return self._entries.get(observation_id)

    def list_by_session(self, session_id: str) -> list[ObservationStoreEntry]:
        return [entry for entry in self._entries.values() if entry.session_id == session_id]

    def delete(self, observation_id: str) -> bool:
        entry = self._entries.pop(observation_id, None)
        return entry is not None
