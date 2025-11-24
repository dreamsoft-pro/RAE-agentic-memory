from fastapi import APIRouter, Depends

from apps.memory_api.dependencies import get_api_key
from apps.memory_api.tasks.background_tasks import rebuild_cache

router = APIRouter(prefix="/cache", tags=["cache"], dependencies=[Depends(get_api_key)])


@router.post("/rebuild", status_code=202)
async def trigger_rebuild():
    """
    Triggers a background task to rebuild the entire context cache.
    """
    rebuild_cache.delay()
    return {"message": "Cache rebuild task dispatched."}
