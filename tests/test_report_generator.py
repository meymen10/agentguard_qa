import json
import tempfile
import unittest
from pathlib import Path

from checker.report_generator import generate_html_report, generate_json_report


class ReportGeneratorTests(unittest.TestCase):
    def test_generate_json_report_writes_payload(self):
        results = [{
            "test_id": "TC-001",
            "title": "Test title",
            "user_prompt": "Prompt",
            "status": "PASS",
            "called_tools": ["get_order_status"],
            "issues": [],
            "tool_sequence_validation": {"status": "SKIP"},
            "tool_executions": [],
        }]

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "report.json"
            generate_json_report(results, str(output_path))

            payload = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["summary"]["total"], 1)
            self.assertEqual(payload["results"][0]["test_id"], "TC-001")

    def test_generate_html_report_writes_html(self):
        results = [{
            "test_id": "TC-001",
            "title": "Test title",
            "user_prompt": "Prompt",
            "status": "PASS",
            "called_tools": ["get_order_status"],
            "issues": [],
            "tool_sequence_validation": {"status": "SKIP"},
            "tool_executions": [],
        }]

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "report.html"
            generate_html_report(results, str(output_path))

            content = output_path.read_text(encoding="utf-8")
            self.assertIn("<!DOCTYPE html>", content)
            self.assertIn("AgentGuard QA Test Report", content)


if __name__ == "__main__":
    unittest.main()
