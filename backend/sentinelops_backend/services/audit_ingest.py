from .scoring import calculate_score


REQUIRED_FRAMEWORKS = {"ISO27001", "NIST"}


def validate_audit_payload(payload: dict) -> None:
    if not payload.get("host", {}).get("hostname"):
        raise ValueError("host.hostname is required")
    findings = payload.get("findings")
    if not isinstance(findings, list) or not findings:
        raise ValueError("findings must be a non-empty list")
    for finding in findings:
        frameworks = {item.get("framework") for item in finding.get("compliance", [])}
        missing = REQUIRED_FRAMEWORKS - frameworks
        if missing:
            raise ValueError(f"{finding.get('check_name')} missing compliance mappings: {', '.join(sorted(missing))}")


def build_audit_record(payload: dict) -> dict:
    validate_audit_payload(payload)
    findings = payload["findings"]
    return {
        "host": payload["host"],
        "score": calculate_score(findings),
        "findings": findings,
    }

