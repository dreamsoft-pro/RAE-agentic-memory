# Next Session Plan: Distributed Compute Integration

**Status**: 
- Iteration 1 (Abstraction): COMPLETED.
- Iteration 2 (Infrastructure Decoupling): COMPLETED (InfrastructureFactory implemented, Lite mode verified).

## 🎯 Primary Goal: Iteration 3 - Distributed Compute (Node1 Integration)
With `main.py` decoupled, we can now focus on offloading heavy computations (Embeddings, Graph Processing) to the GPU node (Kubus/Node1).

### Steps to Execute:
1.  **Remote Provider Check**: Verify `apps/memory_api/repositories/enhanced_graph_repository.py` and `apps/memory_api/services/rae_core_service.py` support remote execution configuration.
2.  **Node1 Configuration**: Ensure `RAE_PROFILE=standard` or a new `RAE_PROFILE=distributed` can point to Node1 for embeddings/reranking.
3.  **Smoke Test Node1**: Verify connection to Node1 services from the local RAE instance.

### 🚀 Secondary Goal: RAE-Lite Refinement
Ensure "Lite" mode is actually usable (e.g., provides meaningful mocks or in-memory fallbacks for critical services if they are None).

## 💡 Start Command
> `run-distributed-integration`