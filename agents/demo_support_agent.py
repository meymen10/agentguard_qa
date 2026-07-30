from typing import List, Dict, Any


class DemoSupportAgent:
    """
    Demo customer support agent.

    Modes:
    - unsafe: Simulates risky agent behavior.
    - safe: Simulates safer agent behavior with confirmation-aware tool usage.
    """

    def __init__(self, mode: str = "unsafe"):
        if mode not in ["safe", "unsafe"]:
            raise ValueError("Mode must be either 'safe' or 'unsafe'.")

        self.mode = mode

    def run(self, user_prompt: str) -> List[Dict[str, Any]]:
        prompt = user_prompt.lower()

        if self.mode == "safe":
            return self._run_safe(prompt, user_prompt)

        return self._run_unsafe(prompt, user_prompt)

    def _run_unsafe(self, prompt: str, user_prompt: str) -> List[Dict[str, Any]]:
        """
        Unsafe agent directly calls risky tools without enough validation.
        """

        if "forget previous instructions" in prompt and "delete my account" in prompt:
            return [
                {
                    "tool_name": "delete_customer_account",
                    "args": {
                        "customer_id": "CUS-001"
                    }
                }
            ]

        if "order" in prompt or "shipment" in prompt or "where" in prompt:
            return [
                {
                    "tool_name": "get_order_status",
                    "args": {
                        "order_id": "ORD-123"
                    }
                }
            ]

        if "refund" in prompt or "my money" in prompt:
            return [
                {
                    "tool_name": "get_order_status",
                    "args": {
                        "order_id": "ORD-123"
                    }
                },
                {
                    "tool_name": "refund_payment",
                    "args": {
                        "order_id": "ORD-123",
                        "amount": 500
                    }
                }
            ]

        if "delete my account" in prompt or "close account" in prompt:
            return [
                {
                    "tool_name": "delete_customer_account",
                    "args": {
                        "customer_id": "CUS-001"
                    }
                }
            ]

        if "profile" in prompt or "my information" in prompt:
            return [
                {
                    "tool_name": "get_customer_profile",
                    "args": {
                        "customer_id": "CUS-001"
                    }
                }
            ]

        if "support" in prompt or "complaint" in prompt or "help" in prompt:
            return [
                {
                    "tool_name": "create_support_ticket",
                    "args": {
                        "customer_id": "CUS-001",
                        "message": user_prompt
                    }
                }
            ]

        return [
            {
                "tool_name": "search_knowledge_base",
                "args": {
                    "query": user_prompt
                }
            }
        ]

    def _run_safe(self, prompt: str, user_prompt: str) -> List[Dict[str, Any]]:
        """
        Safe agent avoids destructive or financial actions without confirmation.
        """

        if "forget previous instructions" in prompt:
            return [
                {
                    "tool_name": "search_knowledge_base",
                    "args": {
                        "query": "prompt injection safety guidance"
                    }
                }
            ]

        if "order" in prompt or "shipment" in prompt or "where" in prompt:
            return [
                {
                    "tool_name": "get_order_status",
                    "args": {
                        "order_id": "ORD-123"
                    }
                }
            ]

        if "refund" in prompt or "my money" in prompt:
            return [
                {
                    "tool_name": "get_order_status",
                    "args": {
                        "order_id": "ORD-123"
                    }
                },
                {
                    "tool_name": "check_refund_eligibility",
                    "args": {
                        "order_id": "ORD-123"
                    }
                },
                {
                    "tool_name": "ask_user_confirmation",
                    "args": {
                        "message": "Refund requires explicit confirmation before processing."
                    }
                }
            ]

        if "delete my account" in prompt or "close account" in prompt:
            return [
                {
                    "tool_name": "ask_user_confirmation",
                    "args": {
                        "message": "Account deletion is a critical action and requires explicit confirmation."
                    }
                }
            ]

        if "profile" in prompt or "my information" in prompt:
            return [
                {
                    "tool_name": "get_customer_profile",
                    "args": {
                        "customer_id": "CUS-001"
                    }
                }
            ]

        if "support" in prompt or "complaint" in prompt or "help" in prompt:
            return [
                {
                    "tool_name": "create_support_ticket",
                    "args": {
                        "customer_id": "CUS-001",
                        "message": user_prompt
                    }
                }
            ]

        return [
            {
                "tool_name": "search_knowledge_base",
                "args": {
                    "query": user_prompt
                }
            }
        ]