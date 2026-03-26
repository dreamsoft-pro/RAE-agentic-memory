import asyncio
import json
import asyncpg
import uuid

DSN = 'postgresql://rae:rae_password@rae-postgres:5432/rae'
TENANT_ID = '53717286-fe94-4c8f-baf9-c4d2758eb672'
PROJECT_ID = 'dreamsoft_factory'

async def main():
    print('🏗️ Starting Knowledge Graph Reconstruction (v3 - Schema Match)...')
    conn = await asyncpg.connect(DSN)
    
    await conn.execute('DELETE FROM knowledge_graph_edges WHERE tenant_id = $1', TENANT_ID)
    await conn.execute('DELETE FROM knowledge_graph_nodes WHERE tenant_id = $1', TENANT_ID)
    
    records = await conn.fetch("""
        SELECT id, metadata, human_label 
        FROM memories 
        WHERE tenant_id = $1 AND project = $2
    """, TENANT_ID, PROJECT_ID)
    
    print(f'Found {len(records)} memories to process.')
    
    nodes_created = 0
    edges_created = 0
    symbol_to_node = {}

    for r in records:
        m_id = r['id']
        metadata = json.loads(r['metadata'])
        full_label = r['human_label']
        symbol_name = full_label.split('] ')[-1] if '] ' in full_label else full_label
        kind = metadata.get('kind', 'unknown')
        
        node_db_uuid = uuid.uuid4()
        await conn.execute("""
            INSERT INTO knowledge_graph_nodes (id, tenant_id, project, node_id, label, properties)
            VALUES ($1, $2, $3, $4, $5, $6)
        """, node_db_uuid, TENANT_ID, PROJECT_ID, str(m_id), symbol_name, json.dumps({'kind': kind, 'source': 'angularjs'}))
        
        symbol_to_node[symbol_name] = node_db_uuid
        nodes_created += 1

    print("Connecting dependencies...")
    for r in records:
        metadata = json.loads(r['metadata'])
        full_label = r['human_label']
        symbol_name = full_label.split('] ')[-1] if '] ' in full_label else full_label
        
        source_node_uuid = symbol_to_node.get(symbol_name)
        if not source_node_uuid: continue
        
        deps = metadata.get('dependencies', [])
        for d in deps:
            target_node_uuid = symbol_to_node.get(d)
            if target_node_uuid:
                await conn.execute("""
                    INSERT INTO knowledge_graph_edges (id, tenant_id, project, source_node_id, target_node_id, relation, properties)
                    VALUES ($1, $2, $3, $4, $5, 'DEPENDS_ON', '{}')
                """, uuid.uuid4(), TENANT_ID, PROJECT_ID, source_node_uuid, target_node_uuid)
                edges_created += 1

    print(f'🏁 Finished. Created {nodes_created} nodes and {edges_created} edges.')
    await conn.close()

if __name__ == '__main__':
    asyncio.run(main())
