from __future__ import annotations

import platform
import socket
import uuid
from typing import Any

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


WINDOWS_AVAILABLE = platform.system() == "Windows"


class ApplicationDiscovery:
    def discover(self) -> list[ApplicationInfo]:
        if not WINDOWS_AVAILABLE:
            return []
        applications: list[ApplicationInfo] = []
        try:
            import psutil

            for proc in psutil.process_iter(["pid", "name", "exe", "status"]):
                try:
                    info = proc.info
                    if not info.get("name"):
                        continue
                    applications.append(
                        ApplicationInfo(
                            id=info["name"].lower().replace(".exe", "").replace(" ", "_"),
                            name=info["name"],
                            display_name=info["name"].replace(".exe", ""),
                            executable=info.get("exe"),
                            running=info.get("status") in ("running", "sleeping"),
                            process_id=info.get("pid"),
                            capabilities=[],
                        )
                    )
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except ImportError:
            return []
        return applications


class WindowDiscovery:
    def discover_windows(self) -> list[WindowInfo]:
        if not WINDOWS_AVAILABLE:
            return []
        windows: list[WindowInfo] = []
        try:
            import win32gui
            import win32process

            def callback(hwnd: int, extra: Any) -> bool:
                if not win32gui.IsWindowVisible(hwnd):
                    return True
                title = win32gui.GetWindowText(hwnd)
                if not title:
                    return True
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                class_name = win32gui.GetClassName(hwnd)
                rect = win32gui.GetWindowRect(hwnd)
                windows.append(
                    WindowInfo(
                        handle=hwnd,
                        title=title,
                        process_id=pid,
                        class_name=class_name,
                        bounds={
                            "left": rect[0],
                            "top": rect[1],
                            "right": rect[2],
                            "bottom": rect[3],
                        },
                        visible=True,
                    )
                )
                return True

            win32gui.EnumWindows(callback, None)
        except ImportError:
            return []
        return windows
