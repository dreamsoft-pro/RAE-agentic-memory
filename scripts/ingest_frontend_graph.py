
import asyncio
import os
import sys
import json
from pathlib import Path
from uuid import UUID, uuid5

# Add project root and dependencies
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "rae-core"))
sys.path.insert(0, str(PROJECT_ROOT / "rae_adapters"))

import asyncpg
from rae_adapters.postgres import PostgreSQLGraphStore, PostgreSQLStorage

# RAE Identity Contract for Dreamsoft Frontend
DREAMSOFT_NAMESPACE = UUID("550e8400-e29b-41d4-a716-446655440000")
DREAMSOFT_TENANT = uuid5(DREAMSOFT_NAMESPACE, "DREAMSOFT-FRONTEND-ASSEMBLY")

async def ingest_assembly_plan():
    print(f"🚀 Starting Dreamsoft Frontend Assembly Ingest (Tenant: {DREAMSOFT_TENANT})...")
    
    db_url = os.getenv("DATABASE_URL", "postgresql://rae:rae_password@localhost:5432/rae")
    pool = await asyncpg.create_pool(db_url.replace("+asyncpg", ""))
    
    graph_store = PostgreSQLGraphStore(pool=pool)
    storage = PostgreSQLStorage(pool=pool)
    
    # 1. Component Search Path
    base_path = Path("/mnt/extra_storage/RAE-Suite-Modular/packages/rae-hive/work_dir")
    symbol_files = list(base_path.glob("**/symbols.json"))
    print(f"   Found {len(symbol_files)} component symbol files.")
    
    # 2. Status Analysis (What is done vs missing)
    # We define the master assembly state as a reflective memory
    assembly_status = {
        "total_components_identified": len(symbol_files),
        "status": "PHASE_ASSEMBLY_READY",
        "missing_elements": [
            "Final Layout Integration",
            "Visual Mirroring of AngularJS Styles",
            "Full Editor Widget Assembly",
            "Cross-Service State Sync (Zustand)"
        ],
        "inventory_location": str(base_path.absolute())
    }
    
    await storage.store_memory(
        content=f"Frontend Assembly Plan: {len(symbol_files)} components ready for stitching.",
        layer="reflective",
        tenant_id=DREAMSOFT_TENANT,
        agent_id="Lumina-Architect",
        human_label="Dreamsoft-Frontend-Assembly-Master-Plan",
        metadata={
            "type": "assembly_plan",
            "status": assembly_status
        },
        info_class="internal"
    )

    # 3. Build the Graph
    ingested_count = 0
    edge_count = 0
    for sym_file in symbol_files:
        try:
            with open(sym_file, 'r') as f:
                symbols = json.load(f)
            
            comp_name = sym_file.parent.name
            
            # Extract all possible symbols
            all_symbols = []
            for key in ["methods", "functions", "properties", "state"]:
                val = symbols.get(key, [])
                if isinstance(val, list):
                    all_symbols.extend(val)
                elif isinstance(val, dict):
                    all_symbols.extend(list(val.keys()))

            # Add Component Node
            await graph_store.add_node(
                tenant_id=DREAMSOFT_TENANT,
                project_id="dreamsoft_v2",
                node_id=f"COMP-{comp_name}",
                label="FrontendComponent",
                properties={
                    "path": str(sym_file),
                    "symbols": all_symbols,
                    "human_label": f"Component: {comp_name}",
                    "raw_data": symbols
                }
            )
            
            # 4. Extract and Link Dependencies
            deps = symbols.get("dependencies", [])
            for dep in deps:
                # Ensure dependency node exists (placeholder)
                await graph_store.add_node(
                    tenant_id=DREAMSOFT_TENANT,
                    project_id="dreamsoft_v2",
                    node_id=f"COMP-{dep}",
                    label="FrontendComponent",
                    properties={"human_label": f"Dependency: {dep}", "is_placeholder": True}
                )
                # Create Edge
                await graph_store.add_edge(
                    tenant_id=DREAMSOFT_TENANT,
                    project_id="dreamsoft_v2",
                    source_node_id=f"COMP-{comp_name}",
                    target_node_id=f"COMP-{dep}",
                    label="DEPENDS_ON"
                )
                edge_count += 1
            
            ingested_count += 1
            if ingested_count % 50 == 0:
                print(f"   Ingested {ingested_count}/{len(symbol_files)} components and {edge_count} edges.")
                
        except Exception as e:
            print(f"   ❌ Error processing {sym_file}: {e}")

    print(f"✅ Assembly Ingest Complete. Components: {ingested_count}, Dependencies linked: {edge_count}")
    await pool.close()

if __name__ == "__main__":
    asyncio.run(ingest_assembly_plan())
