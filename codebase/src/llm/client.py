import os
from typing import List, Dict, Any, Optional
from openai import OpenAI


class LLMClient:
    def __init__(
        self,
        api_base: Optional[str] = None,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        timeout: int = 60,
    ):
        self.api_base = api_base or os.getenv("MIMO_API_BASE", "https://token-plan-sgp.xiaomimimo.com/v1")
        self.api_key = api_key or os.getenv("MIMO_API_KEY", "")
        self.model = model or os.getenv("MIMO_MODEL", "mimo-v2.5-pro")
        self.timeout = timeout

        if not self.api_key:
            raise ValueError(
                "MIMO_API_KEY is not set. "
                "Create a .env file based on .env.example or set the environment variable."
            )

        self.client = OpenAI(
            base_url=self.api_base,
            api_key=self.api_key,
            timeout=self.timeout,
        )

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 1024,
    ) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content


_client_instance: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    global _client_instance
    if _client_instance is None:
        _client_instance = LLMClient()
    return _client_instance
