from ..collectors.command import CommandResult
from ..models import ComplianceMapping, Finding

UNAVAILABLE_EXIT_CODES = {124, 127}


def unavailable_finding(
    check_name: str,
    result: CommandResult,
    compliance: tuple[ComplianceMapping, ...],
) -> Finding | None:
    if result.exit_code not in UNAVAILABLE_EXIT_CODES:
        return None
    command = " ".join(result.command)
    reason = result.stderr.strip() or "command unavailable"
    return Finding(
        check_name=check_name,
        status="WARN",
        severity="MEDIUM",
        output=f"Check unavailable: {command}",
        evidence=reason,
        compliance=compliance,
    )

