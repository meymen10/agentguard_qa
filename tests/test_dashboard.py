import json
import tempfile
import unittest
from pathlib import Path

from dashboard import build_dashboard_data, load_report_payload


class DashboardTests(unittest.TestCase):
    def test_load_report_payload_reads_json(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            report_path = Path(tmp_dir) / "report.json"
            report_path.write_text(
                json.dumps({"summary": {"total": 1}, "results": []}),
                encoding="utf-8",
            )

            payload = load_report_payload(report_path)
            self.assertEqual(payload["summary"]["total"], 1)

    def test_build_dashboard_data_summarizes_results(self):
        payload = {
            "summary": {"total": 2, "passed": 1, "failed": 1},
            "mode_summary": {
                "safe": {"total": 1, "passed": 1, "failed": 0},
                "unsafe": {"total": 1, "passed": 0, "failed": 1},
            },
            "severity_summary": {"HIGH": 1, "MEDIUM": 0, "LOW": 0},
            "results": [
                {
                    "test_id": "TC-001",
                    "title": "Safe flow",
                    "status": "PASS",
                    "called_tools": ["get_order_status"],
                    "issues": [],
                    "agent_mode": "safe",
                },
                {
                    "test_id": "TC-002",
                    "title": "Unsafe flow",
                    "status": "FAIL",
                    "called_tools": ["delete_customer_account"],
                    "issues": [{"type": "FORBIDDEN_TOOL_USED", "severity": "HIGH"}],
                    "agent_mode": "unsafe",
                },
            ],
        }

        dashboard_data = build_dashboard_data(payload)

        self.assertEqual(dashboard_data["summary"]["failed"], 1)
        self.assertEqual(dashboard_data["tool_usage_counts"]["delete_customer_account"], 1)
        self.assertEqual(dashboard_data["issue_types"]["FORBIDDEN_TOOL_USED"], 1)
        self.assertEqual(len(dashboard_data["failed_results"]), 1)
        self.assertEqual(dashboard_data["failed_results"][0]["test_id"], "TC-002")


if __name__ == "__main__":
    unittest.main()
