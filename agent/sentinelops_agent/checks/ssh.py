from ..compliance import mappings_for
from ..collectors.command import CommandCollector
from ..models import Finding
from ..rules.security import ssh_config_value


SSHD_CONFIG = "/etc/ssh/sshd_config"


def check_ssh_root_login(collector: CommandCollector) -> Finding:
    result = collector.run(("cat", SSHD_CONFIG))
    value = ssh_config_value(result.stdout, "PermitRootLogin")
    passed = value in {"no", "prohibit-password", "forced-commands-only"}
    return Finding(
        check_name="ssh_root_login_disabled",
        status="PASS" if passed else "FAIL",
        severity="HIGH",
        output=f"PermitRootLogin {value or 'not configured'}",
        evidence=result.stdout or result.stderr,
        compliance=mappings_for("ssh_root_login_disabled"),
    )


def check_ssh_password_login(collector: CommandCollector) -> Finding:
    result = collector.run(("cat", SSHD_CONFIG))
    value = ssh_config_value(result.stdout, "PasswordAuthentication")
    passed = value == "no"
    return Finding(
        check_name="ssh_password_login_disabled",
        status="PASS" if passed else "FAIL",
        severity="HIGH",
        output=f"PasswordAuthentication {value or 'not configured'}",
        evidence=result.stdout or result.stderr,
        compliance=mappings_for("ssh_password_login_disabled"),
    )

