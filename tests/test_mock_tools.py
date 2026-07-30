import unittest

from tools.mock_tools import MockToolExecutor


class MockToolExecutorTests(unittest.TestCase):
    def test_executes_known_tool_and_records_result(self):
        executor = MockToolExecutor()

        executed = executor.execute_many([
            {"tool_name": "get_order_status", "args": {"order_id": "ORD-123"}}
        ])

        self.assertEqual(len(executed), 1)
        self.assertEqual(executed[0]["tool_name"], "get_order_status")
        self.assertEqual(executed[0]["execution"]["status"], "success")
        self.assertEqual(executed[0]["execution"]["order_id"], "ORD-123")

    def test_returns_error_for_unknown_tool(self):
        executor = MockToolExecutor()

        execution = executor.execute("unknown_tool")

        self.assertEqual(execution["status"], "error")
        self.assertIn("Unknown tool", execution["message"])


if __name__ == "__main__":
    unittest.main()
