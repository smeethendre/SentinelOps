from ..compliance import mappings_for
from ..collectors.command import CommandCollector
from ..models import Finding
from ..rules.security import has_pending_security_updates


def check_pending_security_updates(collector: CommandCollector) -> Finding:
    result = collector.run(("bash", "-lc", "apt list --upgradable 2>/dev/null | grep -i security || true"))
    pending = has_pending_security_updates(result.stdout)
    return Finding(
        check_name="pending_security_updates",
        status="FAIL" if pending else "PASS",
        severity="MEDIUM",
        output=result.stdout.strip() or "No pending security updates detected",
        evidence=result.stdout or result.stderr,
        compliance=mappings_for("pending_security_updates"),
    )

