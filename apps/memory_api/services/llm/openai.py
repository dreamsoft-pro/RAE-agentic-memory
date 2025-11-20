from typing import Type
from pydantic import BaseModel
from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
import instructor

from .base import LLMProvider, LLMResult, LLMResultUsage
from ...config import settings


class OpenAIProvider(LLMProvider):
    """
    An LLM provider that uses the OpenAI API.
    """

    def __init__(self, api_key: str = None):
        key = api_key or settings.OPENAI_API_KEY
        if not key:
            raise ValueError("OPENAI_API_KEY is not set.")
        self.client = instructor.patch(AsyncOpenAI(api_key=key))

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
    async def generate(self, *, system: str, prompt: str, model: str) -> LLMResult:
        """
        Generates content using the OpenAI model.
        """
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
            )

            usage = LLMResultUsage(
                prompt_tokens=response.usage.prompt_tokens,
                candidates_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
            )

            return LLMResult(
                text=response.choices[0].message.content,
                usage=usage,
                model_name=model,
                finish_reason=response.choices[0].finish_reason,
            )
        except Exception as e:
            print(f"OpenAI API call failed: {e}")
            raise

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
    async def generate_structured(
        self, *, system: str, prompt: str, model: str, response_model: Type[BaseModel]
    ) -> BaseModel:
        """
        Generates structured content using the OpenAI model.
        """
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
                response_model=response_model,
            )
            return response
        except Exception as e:
            print(f"OpenAI API call failed: {e}")
            raise
