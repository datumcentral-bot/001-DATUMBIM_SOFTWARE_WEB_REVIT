import platform
import socket
import uuid

from desktop_agent.models import ApplicationInfo, WindowInfo


def get_machine_name() -> str:
    return platform.node()


def get_os_info() -> tuple[str, str]:
    return platform.system(), platform.version()


def get_python_version() -> str:
    return platform.python_version()


def get_hostname() -> str:
    return socket.gethostname()


def get_ip_addresses() -> list[str]:
    try:
        hostname = socket.gethostname()
        return [str(ip[4][0]) for ip in socket.getaddrinfo(hostname, None)]
    except OSError:
        return []


def generate_agent_id() -> str:
    return str(uuid.uuid4())


class ApplicationDiscovery:
    def discover(self) -> list[ApplicationInfo]:
        return []


class WindowDiscovery:
    def discover_windows(self) -> list[WindowInfo]:
        return []
