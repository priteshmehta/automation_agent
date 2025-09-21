from abc import ABC, abstractmethod
import time
from logger import JsonLogger

class LlmClient(ABC):
    @abstractmethod
    async def chat(self, messages, **kwargs):
        pass

class OpenAiClient(LlmClient):
    def __init__(self, api_key=None, base_url=None):
        from openai import AsyncOpenAI
        self.logger = JsonLogger("llm_client")
        if base_url:
            self.client = AsyncOpenAI(base_url=base_url, api_key=api_key)
        else:
            self.client = AsyncOpenAI()

    async def chat(self, messages, **kwargs):
        # Instrument LLM query time
        start = time.time()
        response = await self.client.chat.completions.create(
            messages=messages,
            **kwargs
        )
        duration = time.time() - start
        self.logger.log(f"{duration:.2f}s", "[chatGPT TIMING]")
        return response

class LocalModelClient(LlmClient):
    def __init__(self, endpoint):
        self.endpoint = endpoint

    async def chat(self, messages, **kwargs):
        # Implement local model API call here
        start = time.time()
        duration = time.time() - start
        self.logger(f"Local Model: {duration:.2f} seconds",  "[LLM TIMING]")
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

