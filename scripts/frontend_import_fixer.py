
import asyncio
import os
import sys
import re
from pathlib import Path
from uuid import UUID, uuid5

# Add project root and dependencies
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "rae-core"))
sys.path.insert(0, str(PROJECT_ROOT / "rae_adapters"))

import asyncpg

# Standard RAE Tenant for Frontend
DREAMSOFT_NAMESPACE = UUID("550e8400-e29b-41d4-a716-446655440000")
DREAMSOFT_TENANT = uuid5(DREAMSOFT_NAMESPACE, "DREAMSOFT-FRONTEND-ASSEMBLY")

async def analyze_imports():
    print(f"🚀 Starting Dreamsoft Import-Fixer Analysis (Tenant: {DREAMSOFT_TENANT})...")
    
    db_url = os.getenv("DATABASE_URL", "postgresql://rae:rae_password@localhost:5432/rae")
    pool = await asyncpg.create_pool(db_url.replace("+asyncpg", ""))
    
    # 1. Get all components and their paths from RAE Graph
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT node_id, properties->>'path' as path, properties->>'human_label' as label
            FROM knowledge_graph_nodes 
            WHERE tenant_id = $1 AND label = 'FrontendComponent'
        """, DREAMSOFT_TENANT)
        
        # Map: ComponentName -> RelativePathInNext
        component_map = {}
        for r in rows:
            name = r['node_id'].replace("COMP-", "")
            # Convert legacy work_dir path to a guess of next-frontend path
            component_map[name] = r['path']

    # 2. Scan next-frontend services
    services_path = Path("/home/operator/dreamsoft_factory/next-frontend/src/services")
    ts_files = list(services_path.glob("*.ts"))
    print(f"   Analyzing {len(ts_files)} TypeScript services...")
    
    fix_report = []
    
    for ts_file in ts_files:
        with open(ts_file, 'r') as f:
            content = f.read()
        
        # Look for class usages that are NOT imported
        # Simple heuristic: find PascalCase words
        potential_deps = set(re.findall(r'\b[A-Z][a-zA-Z0-9]+\b', content))
        
        # Check which of these are known components in our RAE graph
        missing_imports = []
        for dep in potential_deps:
            if dep in component_map and f"import {{ {dep} }}" not in content and f"import {dep}" not in content:
                # Ignore self
                if dep != ts_file.stem:
                    missing_imports.append(dep)
        
        if missing_imports:
            fix_report.append({
                "file": ts_file.name,
                "missing": missing_imports
            })

    print("\n🏆 IMPORT FIX REPORT (Top 10):")
    for fix in fix_report[:10]:
        print(f"   - {fix['file']}: Missing {', '.join(fix['missing'])}")
    
    if len(fix_report) > 10:
        print(f"   ... and {len(fix_report)-10} more files.")

    # 3. Store result in RAE Reflective Layer
    storage_sql = "INSERT INTO memories (id, content, layer, tenant_id, agent_id, human_label, metadata, info_class) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)"
    import json
    from uuid import uuid4
    
    await pool.execute(
        storage_sql,
        uuid4(),
        f"Import Analysis: {len(fix_report)} services require import fixes.",
        "reflective",
        DREAMSOFT_TENANT,
        "Import-Fixer-Agent",
        "Dreamsoft-Import-Fix-Report",
        json.dumps({"fixes_required": fix_report}),
        "internal"
    )

    print(f"✅ Analysis Complete. Report saved to RAE Reflective Layer.")
    await pool.close()

if __name__ == "__main__":
    asyncio.run(analyze_imports())
