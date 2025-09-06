from abc import ABC, abstractmethod

class LlmClient(ABC):
    @abstractmethod
    async def chat(self, messages, **kwargs):
        pass

class OpenAiClient(LlmClient):
    def __init__(self, api_key=None, base_url=None):
        from openai import AsyncOpenAI
        if base_url:
            self.client = AsyncOpenAI(base_url=base_url, api_key=api_key)
        else:
            self.client = AsyncOpenAI()

    async def chat(self, messages, **kwargs):
        response = await self.client.chat.completions.create(
            messages=messages,
            **kwargs
        )
        return response

class LocalModelClient(LlmClient):
    def __init__(self, endpoint):
        self.endpoint = endpoint

    async def chat(self, messages, **kwargs):
        # Implement local model API call here
        raise NotImplementedError("Local model integration not implemented.")

class LlmClientFactory:
    @staticmethod
    def create(config):
        provider = getattr(config, "LLM_PROVIDER", "openai").lower()
        if provider == "openai":
            api_key = getattr(config, "OPENAI_API_KEY", None)
            base_url = getattr(config, "BASE_URL", None)
            return OpenAiClient(api_key=api_key, base_url=base_url)
        elif provider == "local":
            endpoint = getattr(config, "LOCAL_MODEL_ENDPOINT", None)
            return LocalModelClient(endpoint=endpoint)
        else:
            raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")

# Usage in main.py:
# from llm_client import LlmClientFactory
# import config
# client = LlmClientFactory.create(config)