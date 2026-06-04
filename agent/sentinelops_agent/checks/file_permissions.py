from ..compliance import mappings_for
from ..collectors.command import CommandCollector
from ..models import Finding
from ..rules.security import shadow_permissions_are_safe


def check_shadow_permissions(collector: CommandCollector) -> Finding:
    result = collector.run(("stat", "-c", "%a %U:%G", "/etc/shadow"))
    passed = shadow_permissions_are_safe(result.stdout)
    return Finding(
        check_name="etc_shadow_permissions",
        status="PASS" if passed else "FAIL",
        severity="CRITICAL",
        output=result.stdout.strip() or result.stderr.strip(),
        evidence=result.stdout or result.stderr,
        compliance=mappings_for("etc_shadow_permissions"),
    )

