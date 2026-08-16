from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from revit_connector.models import RevitConnectionState, RevitOperationResult


class TransactionContext:
    def __init__(self, transaction_id: str, operation_id: str, dry_run: bool = False) -> None:
        self.transaction_id = transaction_id
        self.operation_id = operation_id
        self.dry_run = dry_run
        self.started_at = datetime.now(tz=UTC)
        self.committed = False
        self.rolled_back = False
        self.result: RevitOperationResult | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "transaction_id": self.transaction_id,
            "operation_id": self.operation_id,
            "dry_run": self.dry_run,
            "started_at": self.started_at.isoformat(),
            "committed": self.committed,
            "rolled_back": self.rolled_back,
        }


class TransactionManager:
    def __init__(self) -> None:
        self._transactions: dict[str, TransactionContext] = {}

    def begin(self, operation_id: str, dry_run: bool = False) -> TransactionContext:
        transaction_id = f"txn_{datetime.now(tz=UTC).strftime('%Y%m%d%H%M%S%f')}"
        context = TransactionContext(transaction_id=transaction_id, operation_id=operation_id, dry_run=dry_run)
        self._transactions[transaction_id] = context
        return context

    def commit(self, context: TransactionContext, result: RevitOperationResult) -> RevitOperationResult:
        context.committed = True
        context.result = result
        return result

    def rollback(self, context: TransactionContext, reason: str) -> RevitOperationResult:
        context.rolled_back = True
        context.result = RevitOperationResult(
            operation_id=context.operation_id,
            status="rolled_back",
            error=reason,
            transaction_id=context.transaction_id,
            rollback_available=False,
        )
        return context.result

    def get_transaction(self, transaction_id: str) -> TransactionContext | None:
        return self._transactions.get(transaction_id)
