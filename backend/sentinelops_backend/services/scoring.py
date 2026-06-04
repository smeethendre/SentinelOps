PASSING_STATUSES = {"PASS"}


def calculate_score(findings: list[dict]) -> int:
    if not findings:
        return 0
    passed = sum(1 for finding in findings if finding.get("status") in PASSING_STATUSES)
    return round((passed / len(findings)) * 100)

