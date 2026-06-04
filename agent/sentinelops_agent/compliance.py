from .models import ComplianceMapping


COMPLIANCE_MAP: dict[str, tuple[ComplianceMapping, ...]] = {
    "ssh_root_login_disabled": (
        ComplianceMapping("ISO27001", ("A.5.15", "A.8.3", "A.8.5")),
        ComplianceMapping("NIST", ("AC-2", "AC-6", "IA-2")),
    ),
    "ssh_password_login_disabled": (
        ComplianceMapping("ISO27001", ("A.5.17", "A.8.5")),
        ComplianceMapping("NIST", ("IA-2", "IA-5")),
    ),
    "firewall_active": (
        ComplianceMapping("ISO27001", ("A.8.20", "A.8.22")),
        ComplianceMapping("NIST", ("SC-7", "CM-7")),
    ),
    "pending_security_updates": (
        ComplianceMapping("ISO27001", ("A.8.8", "A.8.32")),
        ComplianceMapping("NIST", ("SI-2", "RA-5")),
    ),
    "admin_accounts_review": (
        ComplianceMapping("ISO27001", ("A.5.15", "A.8.2")),
        ComplianceMapping("NIST", ("AC-2", "AC-6")),
    ),
    "unexpected_exposed_services": (
        ComplianceMapping("ISO27001", ("A.8.20", "A.8.22")),
        ComplianceMapping("NIST", ("CM-7", "SC-7")),
    ),
    "etc_shadow_permissions": (
        ComplianceMapping("ISO27001", ("A.8.3", "A.8.4")),
        ComplianceMapping("NIST", ("AC-3", "AC-6")),
    ),
}


def mappings_for(check_name: str) -> tuple[ComplianceMapping, ...]:
    return COMPLIANCE_MAP[check_name]

