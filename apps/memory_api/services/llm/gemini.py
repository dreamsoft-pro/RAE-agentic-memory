from typing import Type
from pydantic import BaseModel
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential
import instructor

from .base import LLMProvider, LLMResult, LLMResultUsage
from ...config import settings


class GeminiProvider(LLMProvider):
    """
    An LLM provider that uses the Google Gemini API.
    """

    def __init__(self, api_key: str = None):
        key = api_key or settings.GEMINI_API_KEY
        if not key:
            raise ValueError("GEMINI_API_KEY is not set.")
        genai.configure(api_key=key)
        self.client = instructor.patch(genai.GenerativeModel)

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
    async def generate(self, *, system: str, prompt: str, model: str) -> LLMResult:
        """
        Generates content using the Gemini model.
        """
        try:
            generative_model = self.client(
                model_name=model,
                system_instruction=system,
            )
            response = await generative_model.generate_content(prompt)

            usage = LLMResultUsage(
                prompt_tokens=response.usage_metadata.prompt_token_count,
                candidates_tokens=response.usage_metadata.candidates_token_count,
                total_tokens=response.usage_metadata.total_token_count,
            )

            return LLMResult(
                text=response.text,
                usage=usage,
                model_name=model,
                finish_reason=str(response.candidates[0].finish_reason),
            )
        except Exception as e:
            print(f"Gemini API call failed: {e}")
            raise  # Re-raise after logging/handling, tenacity will handle retries

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
    async def generate_structured(
        self, *, system: str, prompt: str, model: str, response_model: Type[BaseModel]
    ) -> BaseModel:
        """
        Generates structured content using the Gemini model.
        """
        try:
            generative_model = self.client(
                model_name=model,
                system_instruction=system,
            )
            response = await generative_model.generate_content(
                prompt, response_model=response_model
            )
            return response
        except Exception as e:
            print(f"Gemini API call failed: {e}")
            raise
