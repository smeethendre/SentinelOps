import unittest

from agent.sentinelops_agent.checks.firewall import check_firewall_active
from agent.sentinelops_agent.collectors.command import CommandResult


class MissingCommandCollector:
    def run(self, command: tuple[str, ...], timeout_seconds: int = 10) -> CommandResult:
        return CommandResult(command, 127, "", "command not found")


class AgentUnavailableChecksTests(unittest.TestCase):
    def test_missing_linux_command_returns_warn_not_pass(self):
        finding = check_firewall_active(MissingCommandCollector())
        self.assertEqual(finding.status, "WARN")
        self.assertEqual(finding.output, "Check unavailable: ufw status")


if __name__ == "__main__":
    unittest.main()
