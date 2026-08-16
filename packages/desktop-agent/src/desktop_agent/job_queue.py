from datetime import UTC, datetime

from desktop_agent.models import CommandRequest, CommandResult


class Job:
    def __init__(self, request: CommandRequest) -> None:
        self.request = request
        self.result: CommandResult | None = None
        self.started_at: datetime | None = None
        self.finished_at: datetime | None = None

    def start(self) -> None:
        self.started_at = datetime.now(tz=UTC)

    def finish(self, result: CommandResult) -> None:
        self.result = result
        self.finished_at = datetime.now(tz=UTC)


class JobQueue:
    def __init__(self) -> None:
        self._jobs: list[Job] = []

    def enqueue(self, request: CommandRequest) -> Job:
        job = Job(request=request)
        self._jobs.append(job)
        return job

    def dequeue(self) -> Job | None:
        for job in self._jobs:
            if job.result is None:
                return job
        return None

    def get_pending(self) -> list[Job]:
        return [job for job in self._jobs if job.result is None]
