from ..compliance import mappings_for
from ..collectors.command import CommandCollector
from ..models import Finding

EXPECTED_PORTS = {"22", "80", "443"}


def check_unexpected_exposed_services(collector: CommandCollector) -> Finding:
    result = collector.run(("bash", "-lc", "ss -tulpn"))
    unexpected = []
    for line in result.stdout.splitlines():
        if "LISTEN" not in line:
            continue
        local_address = line.split()[4] if len(line.split()) > 4 else ""
        port = local_address.rsplit(":", 1)[-1]
        if port.isdigit() and port not in EXPECTED_PORTS:
            unexpected.append(port)
    return Finding(
        check_name="unexpected_exposed_services",
        status="PASS" if not unexpected else "FAIL",
        severity="HIGH",
        output="Unexpected listening ports: " + ", ".join(sorted(set(unexpected))) if unexpected else "No unexpected listening ports",
        evidence=result.stdout or result.stderr,
        compliance=mappings_for("unexpected_exposed_services"),
    )

