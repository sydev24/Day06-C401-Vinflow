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
        # Nhận diện API key và thiết lập giá trị mặc định cho từng provider
        gemini_key = os.getenv("GEMINI_API_KEY", "")
        mimo_key = os.getenv("MIMO_API_KEY", "")
        openai_key = os.getenv("OPENAI_API_KEY", "")

        if gemini_key:
            default_base = "https://generativelanguage.googleapis.com/v1beta/openai/"
            default_model = "gemini-1.5-flash"
            active_key = gemini_key
        elif mimo_key:
            default_base = "https://token-plan-sgp.xiaomimimo.com/v1"
            default_model = "mimo-v2.5-pro"
            active_key = mimo_key
        elif openai_key:
            default_base = "https://api.openai.com/v1"
            default_model = "gpt-4o-mini"
            active_key = openai_key
        else:
            active_key = ""
            default_base = "https://token-plan-sgp.xiaomimimo.com/v1"
            default_model = "mimo-v2.5-pro"

        self.api_key = api_key or active_key
        
        # Chọn base_url phù hợp (ưu tiên biến môi trường tương ứng)
        if gemini_key:
            self.api_base = api_base or os.getenv("GEMINI_API_BASE") or os.getenv("MIMO_API_BASE") or default_base
            self.model = model or os.getenv("GEMINI_MODEL") or os.getenv("MIMO_MODEL") or default_model
        else:
            self.api_base = api_base or os.getenv("MIMO_API_BASE") or os.getenv("OPENAI_API_BASE") or default_base
            self.model = model or os.getenv("MIMO_MODEL") or os.getenv("OPENAI_MODEL") or default_model

        self.timeout = timeout

        if not self.api_key:
            raise ValueError(
                "Không tìm thấy API Key. Vui lòng cấu hình GEMINI_API_KEY, MIMO_API_KEY, hoặc OPENAI_API_KEY trong file .env."
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
