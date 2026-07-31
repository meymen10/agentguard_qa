import json
import os
import re
from typing import Any, Dict, List

import requests

from agents.demo_support_agent import DemoSupportAgent


class LLMSupportAgent:
    """
    Optional LLM-backed support agent adapter.

    When an API key is not available, the adapter falls back to the safe demo agent.
    """

    DEFAULT_BASE_URL = "https://api.openai.com/v1/chat/completions"

    def __init__(
        self,
        model: str = "gpt-4.1-mini",
        api_key: str | None = None,
        base_url: str | None = None,
        fallback_mode: str = "safe",
        timeout: int = 15,
    ):
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL") or self.DEFAULT_BASE_URL
        self.timeout = timeout
        self.fallback_mode = fallback_mode
        self._fallback_agent = DemoSupportAgent(mode=self.fallback_mode)

    def run(self, user_prompt: str) -> List[Dict[str, Any]]:
        if not self.api_key:
            return self._fallback_agent.run(user_prompt)

        try:
            response = requests.post(
                self.base_url,
                headers=self._build_headers(),
                json=self._build_payload(user_prompt),
                timeout=self.timeout,
            )
            response.raise_for_status()
            tool_calls = self._parse_tool_calls(response.json())
            if tool_calls:
                return tool_calls
        except Exception:
            pass

        return self._fallback_agent.run(user_prompt)

    def _build_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def _build_payload(self, user_prompt: str) -> Dict[str, Any]:
        return {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a customer-support agent. Return a JSON array of tool calls "
                        "in the form [{\"tool_name\": \"tool_name\", \"args\": {}}]. "
                        "Do not include markdown fences."
                    ),
                },
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0,
        }

    @staticmethod
    def _parse_tool_calls(response_payload: Any) -> List[Dict[str, Any]] | None:
        content = ""

        if isinstance(response_payload, dict):
            choices = response_payload.get("choices") or []
            if choices:
                message = choices[0].get("message") or {}
                content = message.get("content", "") or ""
        elif isinstance(response_payload, str):
            content = response_payload

        if not isinstance(content, str) or not content.strip():
            return None

        cleaned_content = content.strip()
        if cleaned_content.startswith("```"):
            cleaned_content = re.sub(r"^```(?:json)?\s*", "", cleaned_content)
            cleaned_content = re.sub(r"\s*```$", "", cleaned_content)

        try:
            parsed = json.loads(cleaned_content)
        except json.JSONDecodeError:
            return None

        if isinstance(parsed, list):
            normalized_calls: List[Dict[str, Any]] = []
            for item in parsed:
                if not isinstance(item, dict):
                    continue
                tool_name = item.get("tool_name") or item.get("name")
                if not tool_name:
                    continue
                args = item.get("args") or item.get("arguments") or {}
                if not isinstance(args, dict):
                    try:
                        args = json.loads(args)
                    except (TypeError, json.JSONDecodeError):
                        args = {}
                normalized_calls.append({"tool_name": tool_name, "args": args})
            return normalized_calls or None

        return None
