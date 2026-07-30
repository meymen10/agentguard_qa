from typing import Any, Dict, List


class MockToolExecutor:
    """Executes mock tool calls and returns structured execution results."""

    def __init__(self):
        self.execution_log: List[Dict[str, Any]] = []

    def execute(self, tool_name: str, args: Dict[str, Any] | None = None) -> Dict[str, Any]:
        normalized_args = args or {}
        handler = self._handlers().get(tool_name)

        if handler is None:
            execution = {
                "tool_name": tool_name,
                "status": "error",
                "message": f"Unknown tool: {tool_name}",
                "args": normalized_args,
            }
            self.execution_log.append(execution)
            return execution

        execution = handler(normalized_args)
        execution["tool_name"] = tool_name
        execution["args"] = normalized_args
        execution.setdefault("status", "success")
        self.execution_log.append(execution)
        return execution

    def execute_many(self, tool_calls: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        executed_calls: List[Dict[str, Any]] = []

        for call in tool_calls:
            tool_name = call["tool_name"]
            args = call.get("args", {})
            execution = self.execute(tool_name, args)
            executed_calls.append({
                "tool_name": tool_name,
                "args": args,
                "execution": execution,
            })

        return executed_calls

    def _handlers(self) -> Dict[str, Any]:
        return {
            "search_knowledge_base": self._search_knowledge_base,
            "get_order_status": self._get_order_status,
            "check_refund_eligibility": self._check_refund_eligibility,
            "ask_user_confirmation": self._ask_user_confirmation,
            "get_customer_profile": self._get_customer_profile,
            "create_support_ticket": self._create_support_ticket,
            "refund_payment": self._refund_payment,
            "delete_customer_account": self._delete_customer_account,
        }

    def _search_knowledge_base(self, args: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "status": "success",
            "message": "Knowledge base search completed.",
            "query": args.get("query", ""),
            "result_count": 1,
        }

    def _get_order_status(self, args: Dict[str, Any]) -> Dict[str, Any]:
        order_id = args.get("order_id", "UNKNOWN")
        return {
            "status": "success",
            "message": "Order status retrieved.",
            "order_id": order_id,
            "state": "shipped",
        }

    def _check_refund_eligibility(self, args: Dict[str, Any]) -> Dict[str, Any]:
        order_id = args.get("order_id", "UNKNOWN")
        return {
            "status": "success",
            "message": "Refund eligibility checked.",
            "order_id": order_id,
            "eligible": True,
        }

    def _ask_user_confirmation(self, args: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "status": "success",
            "message": "User confirmation requested.",
            "prompt": args.get("message", "Please confirm the action."),
        }

    def _get_customer_profile(self, args: Dict[str, Any]) -> Dict[str, Any]:
        customer_id = args.get("customer_id", "UNKNOWN")
        return {
            "status": "success",
            "message": "Customer profile retrieved.",
            "customer_id": customer_id,
            "tier": "gold",
        }

    def _create_support_ticket(self, args: Dict[str, Any]) -> Dict[str, Any]:
        customer_id = args.get("customer_id", "UNKNOWN")
        return {
            "status": "success",
            "message": "Support ticket created.",
            "customer_id": customer_id,
            "ticket_id": "TK-1001",
        }

    def _refund_payment(self, args: Dict[str, Any]) -> Dict[str, Any]:
        amount = args.get("amount", 0)
        return {
            "status": "simulated",
            "message": "Refund payment simulated.",
            "order_id": args.get("order_id", "UNKNOWN"),
            "amount": amount,
        }

    def _delete_customer_account(self, args: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "status": "simulated",
            "message": "Customer account deletion simulated.",
            "customer_id": args.get("customer_id", "UNKNOWN"),
        }
