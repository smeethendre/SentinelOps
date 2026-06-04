import unittest

from backend.sentinelops_backend.services.audit_ingest import build_audit_record
from backend.sentinelops_backend.services.scoring import calculate_score


def finding(status: str) -> dict:
    return {
        "check_name": "firewall_active",
        "status": status,
        "severity": "HIGH",
        "output": "Status: active",
        "evidence": "Status: active",
        "compliance": [
            {"framework": "ISO27001", "controls": ["A.8.20"]},
            {"framework": "NIST", "controls": ["SC-7"]},
        ],
    }


class BackendScoringTests(unittest.TestCase):
    def test_score_counts_pass_only(self):
        self.assertEqual(calculate_score([finding("PASS"), finding("FAIL"), finding("WARN")]), 33)

    def test_audit_payload_requires_framework_mapping_for_pass_and_fail(self):
        record = build_audit_record(
            {
                "host": {"hostname": "ubuntu-dev", "os": "linux"},
                "findings": [finding("PASS"), finding("FAIL")],
            }
        )
        self.assertEqual(record["score"], 50)

    def test_missing_nist_mapping_fails_validation(self):
        bad = finding("FAIL")
        bad["compliance"] = [{"framework": "ISO27001", "controls": ["A.8.20"]}]
        with self.assertRaises(ValueError):
            build_audit_record({"host": {"hostname": "ubuntu-dev"}, "findings": [bad]})


if __name__ == "__main__":
    unittest.main()

