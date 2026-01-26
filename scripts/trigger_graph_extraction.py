import asyncio
import structlog
from apps.memory_api.tasks.background_tasks import rae_context

# Configure logger to see what's happening
structlog.configure()

async def main():
    print("Manually triggering graph extraction queue...")
    
    async with rae_context() as rae_service:
        records = await rae_service.list_memories_for_graph_extraction(limit=10)
        print(f"Found {len(records)} tenants with pending memories.")
        
        for record in records:
            tenant_id = record["tenant_id"]
            memory_ids = record["memory_ids"]
            print(f"Processing {len(memory_ids)} memories for tenant {tenant_id}...")
            
            from apps.memory_api.repositories.graph_repository import GraphRepository
            from apps.memory_api.services.graph_extraction import GraphExtractionService
            
            graph_repo = GraphRepository(rae_service.postgres_pool)
            service = GraphExtractionService(rae_service=rae_service, graph_repo=graph_repo)
            
            try:
                # Use a smaller limit for manual run
                result = await service.extract_knowledge_graph(
                    project_id="default",
                    tenant_id=tenant_id,
                    min_confidence=0.5,
                    limit=10
                )
                
                if result.triples:
                    stats = await service.store_graph_triples(result.triples, "default", tenant_id)
                    print(f"Stored {stats['nodes_created']} nodes and {stats['edges_created']} edges.")
                else:
                    print("No triples extracted.")
            except Exception as e:
                print(f"Failed to process tenant {tenant_id}: {e}")

if __name__ == "__main__":
    asyncio.run(main())