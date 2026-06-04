from ..compliance import mappings_for
from ..collectors.command import CommandCollector
from ..models import Finding
from .common import unavailable_finding


def check_admin_accounts(collector: CommandCollector) -> Finding:
    result = collector.run(("bash", "-lc", "getent group sudo || getent group wheel || true"))
    compliance = mappings_for("admin_accounts_review")
    if unavailable := unavailable_finding("admin_accounts_review", result, compliance):
        return unavailable
    accounts = result.stdout.strip().split(":")[-1].split(",") if result.stdout.strip() else []
    named_accounts = [account for account in accounts if account]
    passed = len(named_accounts) <= 3
    return Finding(
        check_name="admin_accounts_review",
        status="PASS" if passed else "WARN",
        severity="MEDIUM",
        output=f"{len(named_accounts)} admin account(s): {', '.join(named_accounts) or 'none found'}",
        evidence=result.stdout or result.stderr,
        compliance=compliance,
    )
