from pathlib import Path
from typing import Any, Protocol, runtime_checkable
from abc import ABC, abstractmethod
from datetime import datetime, timezone


@runtime_checkable
class StorageProvider(Protocol):
    name: str

    def write(self, path: str, data: bytes) -> str:
        ...

    def read(self, path: str) -> bytes:
        ...

    def delete(self, path: str) -> bool:
        ...

    def exists(self, path: str) -> bool:
        ...

    def list(self, prefix: str = "") -> list[str]:
        ...

    def stat(self, path: str) -> dict[str, Any]:
        ...


class LocalStorageProvider:
    name = "local"

    def __init__(self, base_path: Path):
        self.base_path = Path(base_path).resolve()

    def _resolve(self, path: str) -> Path:
        target = (self.base_path / path).resolve()
        if not str(target).startswith(str(self.base_path)):
            raise ValueError(f"Path traversal detected: {path}")
        return target

    def write(self, path: str, data: bytes) -> str:
        target = self._resolve(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        return str(target)

    def read(self, path: str) -> bytes:
        target = self._resolve(path)
        return target.read_bytes()

    def delete(self, path: str) -> bool:
        target = self._resolve(path)
        if target.exists():
            target.unlink()
            return True
        return False

    def exists(self, path: str) -> bool:
        return self._resolve(path).exists()

    def list(self, prefix: str = "") -> list[str]:
        prefix_path = self._resolve(prefix)
        if not prefix_path.exists() or not prefix_path.is_dir():
            return []
        return [str(p.relative_to(self.base_path)) for p in prefix_path.rglob("*") if p.is_file()]

    def stat(self, path: str) -> dict[str, Any]:
        target = self._resolve(path)
        if not target.exists():
            return {}
        stat = target.stat()
        return {
            "size": stat.st_size,
            "created_at": datetime.fromtimestamp(stat.st_ctime, tz=timezone.utc).isoformat(),
            "modified_at": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
            "is_dir": target.is_dir(),
        }


class NetworkStorageProvider:
    name = "network"

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def write(self, path: str, data: bytes) -> str:
        raise NotImplementedError("Network storage write not implemented")

    def read(self, path: str) -> bytes:
        raise NotImplementedError("Network storage read not implemented")

    def delete(self, path: str) -> bool:
        raise NotImplementedError("Network storage delete not implemented")

    def exists(self, path: str) -> bool:
        raise NotImplementedError("Network storage exists not implemented")

    def list(self, prefix: str = "") -> list[str]:
        raise NotImplementedError("Network storage list not implemented")

    def stat(self, path: str) -> dict[str, Any]:
        raise NotImplementedError("Network storage stat not implemented")


class CloudStorageProvider:
    name = "cloud"

    def write(self, path: str, data: bytes) -> str:
        raise NotImplementedError("Cloud storage write not implemented")

    def read(self, path: str) -> bytes:
        raise NotImplementedError("Cloud storage read not implemented")

    def delete(self, path: str) -> bool:
        raise NotImplementedError("Cloud storage delete not implemented")

    def exists(self, path: str) -> bool:
        raise NotImplementedError("Cloud storage exists not implemented")

    def list(self, prefix: str = "") -> list[str]:
        raise NotImplementedError("Cloud storage list not implemented")

    def stat(self, path: str) -> dict[str, Any]:
        raise NotImplementedError("Cloud storage stat not implemented")


class StorageService:
    def __init__(self, default_provider: StorageProvider):
        self.default_provider = default_provider
        self._providers: dict[str, StorageProvider] = {"local": default_provider, "network": NetworkStorageProvider(""), "cloud": CloudStorageProvider()}

    def provider(self, name: str = "local") -> StorageProvider:
        return self._providers.get(name, self.default_provider)

    def register_provider(self, name: str, provider: StorageProvider) -> None:
        self._providers[name] = provider
