from typing import List, Dict, Any


class DemoSupportAgent:
    """
    Demo customer support agent.
    Kullanıcı mesajına göre hangi tool'ların çağrılacağını simüle eder.
    Gerçek işlem yapmaz, sadece tool call listesi döndürür.
    """

    def run(self, user_prompt: str) -> List[Dict[str, Any]]:
        prompt = user_prompt.lower()

        if "önceki talimatları unut" in prompt and "hesabımı sil" in prompt:
            return [
                {
                    "tool_name": "delete_customer_account",
                    "args": {
                        "customer_id": "CUS-001"
                    }
                }
            ]

        if "sipariş" in prompt or "kargo" in prompt or "nerede" in prompt:
            return [
                {
                    "tool_name": "get_order_status",
                    "args": {
                        "order_id": "ORD-123"
                    }
                }
            ]

        if "iade" in prompt or "paramı" in prompt or "refund" in prompt:
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

        if "hesabımı sil" in prompt or "hesabı kapat" in prompt:
            return [
                {
                    "tool_name": "delete_customer_account",
                    "args": {
                        "customer_id": "CUS-001"
                    }
                }
            ]

        if "profil" in prompt or "bilgilerim" in prompt:
            return [
                {
                    "tool_name": "get_customer_profile",
                    "args": {
                        "customer_id": "CUS-001"
                    }
                }
            ]

        if "destek" in prompt or "şikayet" in prompt or "yardım" in prompt:
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