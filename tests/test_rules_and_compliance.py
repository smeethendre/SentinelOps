import unittest

from agent.sentinelops_agent.compliance import COMPLIANCE_MAP
from agent.sentinelops_agent.rules.security import (
    is_firewall_active,
    shadow_permissions_are_safe,
    ssh_config_value,
)


class RulesAndComplianceTests(unittest.TestCase):
    def test_ssh_root_login_rule_reads_last_config_value(self):
        config = "PermitRootLogin yes\nPermitRootLogin no\n"
        self.assertEqual(ssh_config_value(config, "PermitRootLogin"), "no")

    def test_firewall_active_rule(self):
        self.assertTrue(is_firewall_active("Status: active\n"))
        self.assertFalse(is_firewall_active("Status: inactive\n"))

    def test_shadow_permission_rule(self):
        self.assertTrue(shadow_permissions_are_safe("640 root:shadow"))
        self.assertFalse(shadow_permissions_are_safe("644 root:root"))

    def test_every_check_maps_to_iso27001_and_nist(self):
        for check_name, mappings in COMPLIANCE_MAP.items():
            frameworks = {mapping.framework for mapping in mappings}
            self.assertIn("ISO27001", frameworks, check_name)
            self.assertIn("NIST", frameworks, check_name)


if __name__ == "__main__":
    unittest.main()

