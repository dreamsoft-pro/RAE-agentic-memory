from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
from .config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    """
    Dependency to validate the API key provided in the X-API-Key header.
    If settings.API_KEY is not set, authentication is effectively disabled.
    """
    if settings.API_KEY: # Only enforce if an API_KEY is configured
        if api_key and api_key == settings.API_KEY:
            return api_key
        raise HTTPException(
            status_code=403, detail="Could not validate credentials"
        )
    return None # Authentication disabled
