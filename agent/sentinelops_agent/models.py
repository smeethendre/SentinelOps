from dataclasses import dataclass, field
from typing import Literal

CheckStatus = Literal["PASS", "FAIL", "WARN"]
Severity = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]


@dataclass(frozen=True)
class ComplianceMapping:
    framework: str
    controls: tuple[str, ...]


@dataclass(frozen=True)
class Finding:
    check_name: str
    status: CheckStatus
    severity: Severity
    output: str
    evidence: str
    compliance: tuple[ComplianceMapping, ...] = field(default_factory=tuple)

