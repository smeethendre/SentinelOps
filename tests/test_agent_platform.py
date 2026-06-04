import unittest
from unittest.mock import patch

from agent.sentinelops_agent.platform_info import current_os


class AgentPlatformTests(unittest.TestCase):
    def test_current_os_reports_windows(self):
        with patch("platform.system", return_value="Windows"):
            self.assertEqual(current_os(), "windows")

    def test_current_os_reports_linux(self):
        with patch("platform.system", return_value="Linux"):
            self.assertEqual(current_os(), "linux")

    def test_current_os_normalizes_macos(self):
        with patch("platform.system", return_value="Darwin"):
            self.assertEqual(current_os(), "macos")


if __name__ == "__main__":
    unittest.main()
