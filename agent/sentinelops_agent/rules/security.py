import re


def ssh_config_value(config_text: str, key: str) -> str | None:
    pattern = re.compile(rf"^\s*{re.escape(key)}\s+(\S+)", re.IGNORECASE | re.MULTILINE)
    matches = pattern.findall(config_text)
    return matches[-1].lower() if matches else None


def is_firewall_active(ufw_output: str) -> bool:
    return "status: active" in ufw_output.lower()


def has_pending_security_updates(update_output: str) -> bool:
    normalized = update_output.lower()
    return "security" in normalized and not normalized.startswith("0 ")


def shadow_permissions_are_safe(stat_output: str) -> bool:
    mode = stat_output.strip().split()[0] if stat_output.strip() else ""
    return mode in {"600", "640"}

