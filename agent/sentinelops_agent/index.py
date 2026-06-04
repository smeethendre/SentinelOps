from dataclasses import asdict
from socket import gethostname

from .checks import (
    check_admin_accounts,
    check_firewall_active,
    check_pending_security_updates,
    check_shadow_permissions,
    check_ssh_password_login,
    check_ssh_root_login,
    check_unexpected_exposed_services,
)
from .collectors.command import CommandCollector


def run_audit() -> dict:
    collector = CommandCollector()
    findings = [
        check_ssh_root_login(collector),
        check_ssh_password_login(collector),
        check_firewall_active(collector),
        check_pending_security_updates(collector),
        check_admin_accounts(collector),
        check_unexpected_exposed_services(collector),
        check_shadow_permissions(collector),
    ]
    return {
        "host": {
            "hostname": gethostname(),
            "os": "linux",
        },
        "findings": [asdict(finding) for finding in findings],
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run_audit(), indent=2))

