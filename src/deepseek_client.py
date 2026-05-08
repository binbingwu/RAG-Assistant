from __future__ import annotations

import requests


class DeepSeekClient:
    def __init__(self, *, api_key: str, api_base: str, model: str) -> None:
        if not api_key:
            raise ValueError("Missing DEEPSEEK_API_KEY. Add it to .env.")
        self.api_key = api_key
        self.api_base = api_base.rstrip("/")
        self.model = model

    def chat(self, messages: list[dict], *, temperature: float = 0.2) -> str:
        response = requests.post(
            f"{self.api_base}/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
            },
            timeout=120,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

