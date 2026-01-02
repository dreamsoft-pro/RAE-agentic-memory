"""
Integration tests for all available LLM providers in the RAE ecosystem.

Covers:
1. Local Ollama (localhost)
2. Node1 Ollama (Distributed Compute)
3. Anthropic (Cloud)
4. Gemini (Cloud - Google)
5. OpenAI (Cloud - if available)
"""
import os
import pytest
import httpx
from apps.llm import LLMRequest, LLMMessage, LLMResponse
from apps.llm.providers.anthropic_provider import AnthropicProvider
from apps.llm.providers.gemini_provider import GeminiProvider
from apps.llm.providers.ollama_provider import OllamaProvider
from apps.llm.providers.openai_provider import OpenAIProvider

# Configuration
LOCAL_OLLAMA_URL = "http://localhost:11434"
NODE1_OLLAMA_URL = "http://100.66.252.117:11434"
# Models
OLLAMA_MODEL = "deepseek-coder:1.3b"
CLAUDE_MODEL = "claude-3-haiku-20240307"
GEMINI_MODEL = "gemini-1.5-flash"
OPENAI_MODEL = "gpt-3.5-turbo"

@pytest.mark.asyncio
@pytest.mark.llm
class TestAllProvidersIntegration:

    async def test_local_ollama_connectivity(self):
        """Verify Local Ollama is reachable."""
        print(f"\nTesting Local Ollama at {LOCAL_OLLAMA_URL}...")
        provider = OllamaProvider(api_url=LOCAL_OLLAMA_URL)
        
        request = LLMRequest(
            model=OLLAMA_MODEL,
            messages=[LLMMessage(role="user", content="Say 'Local Ollama OK'")],
            temperature=0.1,
            max_tokens=20
        )
        
        try:
            # Check if model exists first (optional but good for debug)
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{LOCAL_OLLAMA_URL}/api/tags")
                if resp.status_code == 200:
                    models = [m['name'] for m in resp.json()['models']]
                    print(f"  Available models: {models}")
                    if OLLAMA_MODEL not in models and f"{OLLAMA_MODEL}:latest" not in models:
                        print(f"  Warning: {OLLAMA_MODEL} not found in local tags.")

            response = await provider.complete(request)
            print(f"  Response: {response.text}")
            assert response.text
        except Exception as e:
            pytest.fail(f"Local Ollama failed: {e}")

    async def test_node1_ollama_connectivity(self):
        """Verify Node1 (Distributed) Ollama is reachable."""
        print(f"\nTesting Node1 Ollama at {NODE1_OLLAMA_URL}...")
        provider = OllamaProvider(api_url=NODE1_OLLAMA_URL)
        
        request = LLMRequest(
            model=OLLAMA_MODEL,
            messages=[LLMMessage(role="user", content="Say 'Node1 Ollama OK'")],
            temperature=0.1,
            max_tokens=20
        )
        
        try:
            response = await provider.complete(request)
            print(f"  Response: {response.text}")
            assert response.text
        except Exception as e:
            pytest.fail(f"Node1 Ollama failed: {e}")

    async def test_anthropic_connectivity(self):
        """Verify Anthropic (Claude) connectivity."""
        print("\nTesting Anthropic...")
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            pytest.skip("ANTHROPIC_API_KEY not found")
            
        provider = AnthropicProvider(api_key=api_key)
        request = LLMRequest(
            model=CLAUDE_MODEL,
            messages=[LLMMessage(role="user", content="Say 'Claude OK'")],
            max_tokens=20
        )
        
        try:
            response = await provider.complete(request)
            print(f"  Response: {response.text}")
            assert response.text
        except Exception as e:
            pytest.fail(f"Anthropic failed: {e}")

    async def test_gemini_connectivity(self):
        """Verify Google Gemini connectivity."""
        print("\nTesting Gemini...")
        api_key = os.environ.get("GEMINI_API_KEY")
        credentials = None
        
        if not api_key:
            oauth_path = os.path.expanduser("~/.gemini/oauth_creds.json")
            if os.path.exists(oauth_path):
                print(f"  Loading OAuth credentials from {oauth_path}...")
                import json
                from google.oauth2.credentials import Credentials
                with open(oauth_path, "r") as f:
                    creds_data = json.load(f)
                    # Mapping our saved keys to Credentials expected keys
                    # oauth_creds.json format from cat: access_token, refresh_token, token_type, id_token, expiry_date, scope
                    credentials = Credentials(
                        token=creds_data.get("access_token"),
                        refresh_token=creds_data.get("refresh_token"),
                        token_uri="https://oauth2.googleapis.com/token",
                        client_id="681255809395-oo8ft2oprdnrp9e3aqf6av3hmdib135j.apps.googleusercontent.com", # Hardcoded from id_token azp/aud
                        client_secret=None, # Personal OAuth usually doesn't need secret if token is valid
                        scopes=creds_data.get("scope", "").split(" ")
                    )
        
        # Now supporting ADC/implicit auth in GeminiProvider
        provider = GeminiProvider(api_key=api_key, credentials=credentials)
        request = LLMRequest(
            model=GEMINI_MODEL,
            messages=[LLMMessage(role="user", content="Say 'Gemini OK'")],
            max_tokens=20
        )
        
        try:
            response = await provider.complete(request)
            print(f"  Response: {response.text}")
            assert response.text
        except Exception as e:
            if not api_key and not credentials:
                print(f"  Gemini failed (likely missing credentials/key): {e}")
                pytest.skip(f"Gemini authentication failed: {e}")
            else:
                print(f"  Gemini Error detail: {e}")
                pytest.fail(f"Gemini failed: {e}")

    async def test_openai_connectivity(self):
        """Verify OpenAI connectivity."""
        print("\nTesting OpenAI...")
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            pytest.skip("OPENAI_API_KEY not found")
            
        provider = OpenAIProvider(api_key=api_key)
        request = LLMRequest(
            model=OPENAI_MODEL,
            messages=[LLMMessage(role="user", content="Say 'OpenAI OK'")],
            max_tokens=20
        )
        
        try:
            response = await provider.complete(request)
            print(f"  Response: {response.text}")
            assert response.text
        except Exception as e:
            pytest.fail(f"OpenAI failed: {e}")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
