import unittest
from unittest.mock import patch

from agents.llm_support_agent import LLMSupportAgent


class LLMAgentTests(unittest.TestCase):
    def test_parse_tool_calls_from_json_response(self):
        payload = {
            "choices": [
                {
                    "message": {
                        "content": '[{"tool_name": "get_order_status", "args": {"order_id": "ORD-123"}}]'
                    }
                }
            ]
        }

        parsed = LLMSupportAgent._parse_tool_calls(payload)
        self.assertEqual(parsed[0]["tool_name"], "get_order_status")
        self.assertEqual(parsed[0]["args"]["order_id"], "ORD-123")

    def test_run_falls_back_to_demo_agent_when_no_api_key(self):
        agent = LLMSupportAgent(api_key=None, fallback_mode="safe")
        tool_calls = agent.run("refund my money")

        self.assertEqual(tool_calls[0]["tool_name"], "get_order_status")
        self.assertEqual(tool_calls[1]["tool_name"], "check_refund_eligibility")

    def test_run_uses_provider_response_when_available(self):
        class FakeResponse:
            def raise_for_status(self):
                return None

            def json(self):
                return {
                    "choices": [
                        {
                            "message": {
                                "content": '[{"tool_name": "create_support_ticket", "args": {"customer_id": "CUS-001"}}]'
                            }
                        }
                    ]
                }

        with patch("agents.llm_support_agent.requests.post", return_value=FakeResponse()):
            agent = LLMSupportAgent(api_key="dummy-key", fallback_mode="safe")
            tool_calls = agent.run("help me")

        self.assertEqual(tool_calls[0]["tool_name"], "create_support_ticket")


if __name__ == "__main__":
    unittest.main()
