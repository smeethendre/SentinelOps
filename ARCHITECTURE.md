# SentinelOps Architecture

## Product direction

SentinelOps is an agent-based infrastructure security platform, not a one-off Linux script. The MVP focuses on Linux security checks, compliance evidence, backend ingest, PostgreSQL persistence, and simple scoring.

## Phase 1 components

```text
Linux Host
  -> Sentinel Agent
  -> Backend API
  -> PostgreSQL
```

Dashboard and AI remediation are explicitly out of scope for Phase 1.

## Agent responsibilities

- Execute Linux security checks
- Collect command and file evidence
- Evaluate normalized rules
- Emit findings with compliance mappings
- Send audit payloads to the backend

## Backend responsibilities

- Receive audit submissions
- Validate host and finding payloads
- Require ISO 27001 and NIST mappings for every finding
- Calculate compliance score
- Persist host, audit, and finding records

## Security checks v1

| Check | Result rule | ISO 27001 | NIST |
| --- | --- | --- | --- |
| Root login disabled | `PermitRootLogin` is `no`, `prohibit-password`, or `forced-commands-only` | A.5.15, A.8.3, A.8.5 | AC-2, AC-6, IA-2 |
| Password login disabled | `PasswordAuthentication no` | A.5.17, A.8.5 | IA-2, IA-5 |
| Firewall active | `ufw status` reports active | A.8.20, A.8.22 | SC-7, CM-7 |
| Pending security updates | No security packages are listed as upgradable | A.8.8, A.8.32 | SI-2, RA-5 |
| Admin accounts review | Admin group size is within review threshold | A.5.15, A.8.2 | AC-2, AC-6 |
| Unexpected exposed services | Listening ports are limited to expected allowlist | A.8.20, A.8.22 | CM-7, SC-7 |
| `/etc/shadow` permissions | Mode is `600` or `640` | A.8.3, A.8.4 | AC-3, AC-6 |

## API contract

`POST /api/audits`

```json
{
  "host": {
    "hostname": "ubuntu-dev",
    "os": "linux"
  },
  "findings": [
    {
      "check_name": "firewall_active",
      "status": "FAIL",
      "severity": "HIGH",
      "output": "Status: inactive",
      "evidence": "Status: inactive",
      "compliance": [
        { "framework": "ISO27001", "controls": ["A.8.20", "A.8.22"] },
        { "framework": "NIST", "controls": ["SC-7", "CM-7"] }
      ]
    }
  ]
}
```

## Scoring

Score is intentionally simple in the MVP:

```text
score = PASS findings / total findings * 100
```

Only `PASS` increases the score. `FAIL` and `WARN` do not.

