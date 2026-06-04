from ..compliance import mappings_for
from ..collectors.command import CommandCollector
from ..models import Finding
from ..rules.security import is_firewall_active
from .common import unavailable_finding


def check_firewall_active(collector: CommandCollector) -> Finding:
    result = collector.run(("ufw", "status"))
    compliance = mappings_for("firewall_active")
    if unavailable := unavailable_finding("firewall_active", result, compliance):
        return unavailable
    passed = is_firewall_active(result.stdout)
    return Finding(
        check_name="firewall_active",
        status="PASS" if passed else "FAIL",
        severity="HIGH",
        output=result.stdout.strip() or result.stderr.strip(),
        evidence=result.stdout or result.stderr,
        compliance=compliance,
    )
