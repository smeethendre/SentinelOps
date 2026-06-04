import platform


def current_os() -> str:
    system_name = platform.system().lower()
    if system_name == "darwin":
        return "macos"
    return system_name or "unknown"

