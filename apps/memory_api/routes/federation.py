from fastapi import APIRouter, Depends, Request
from apps.memory_api.models.federation_models import FederationQueryRequest, FederationQueryResponse, FederationResultItem
from apps.memory_api.services.hybrid_search_service import HybridSearchService

router = APIRouter(prefix="/v1/federation", tags=["Federation"])

async def get_pool(request: Request):
    return request.app.state.pool

@router.post("/query", response_model=FederationQueryResponse)
async def federation_query(request: FederationQueryRequest, req: Request, pool=Depends(get_pool)):
    """
    Federation endpoint to expose memories to other RAE instances.
    Returns candidates without embeddings.
    """
    # Use RAECoreService via app state
    rae_service = req.app.state.rae_service
    service = HybridSearchService(rae_service)
    
    # Execute fast hybrid search (no reranking)
    results = await service.search(
        tenant_id=request.tenant_id,
        project_id=request.project_id,
        query=request.query_text,
        k=request.limit,
        enable_reranking=False,
        enable_graph=False # Disable graph for speed/simplicity in federation for now?
    )
    
    fed_results = []
    for res in results.results:
        fed_results.append(FederationResultItem(
            memory_id=str(res.memory_id),
            content_snippet=res.content[:500],
            full_content=res.content,
            metadata=res.metadata or {}
        ))
        
    return FederationQueryResponse(results=fed_results)
