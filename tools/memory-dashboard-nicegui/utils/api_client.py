import logging
from typing import Any, Dict, List
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAEClient:
    def __init__(
        self,
        api_url: str,
        api_key: str,
        tenant_id: str = '00000000-0000-0000-0000-000000000000',
        project_id: str = 'screenwatcher_project',
    ):
        self.api_url = api_url.rstrip('/')
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'X-Tenant-Id': tenant_id,
            'X-Project-Id': project_id,
            'X-User-Id': '92b1f63ea74d16ec85da4b13f21ff0b2',
            'Content-Type': 'application/json',
        }
        self.timeout = 10.0

    async def check_connection(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                resp = await client.get(f'{self.api_url}/health')
                return resp.status_code == 200
        except Exception as e:
            logger.error(f'Connection check failed: {e}')
            return False

    async def get_tenants(self) -> List[Dict[str, str]]:
        return [{'id': '00000000-0000-0000-0000-000000000000', 'name': 'Default Tenant'}]

    async def get_projects(self) -> List[str]:
        return ['screenwatcher_project', 'rae_dev', 'default']

    async def update_context(self, tenant_id: str, project_id: str):
        self.headers['X-Tenant-Id'] = tenant_id
        self.headers['X-Project-Id'] = project_id

    async def get_stats(self) -> Dict[str, Any]:
        project = self.headers.get('X-Project-Id', 'default')
        tenant = self.headers.get('X-Tenant-Id', 'default')
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
                resp = await client.get(
                    f'{self.api_url}/v2/memories/?project={project}&tenant_id={tenant}&limit=1000'
                )
                
                counts = {'total': 0, 'episodic': 0, 'working': 0, 'semantic': 0, 'ltm': 0}

                if resp.status_code == 200:
                    data = resp.json()
                    results = data.get('results', [])
                    counts['total'] = data.get('total', len(results))
                    for m in results:
                        layer = m.get('layer', 'unknown').lower()
                        if layer in ['sensory', 'episodic']: counts['episodic'] += 1
                        elif layer == 'working': counts['working'] += 1
                        elif layer in ['longterm', 'semantic']: counts['semantic'] += 1
                        elif layer in ['reflective', 'ltm']: counts['ltm'] += 1
                    return counts
                return counts
        except Exception as e:
            logger.error(f'Stats fetch failed: {e}')
            return {'total': 0, 'episodic': 0, 'working': 0, 'semantic': 0, 'ltm': 0}

    async def get_recent_memories(self, limit: int = 50) -> List[Dict]:
        project = self.headers.get('X-Project-Id', 'default')
        tenant = self.headers.get('X-Tenant-Id', 'default')
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
                resp = await client.get(
                    f'{self.api_url}/v2/memories/?project={project}&tenant_id={tenant}&limit={limit}'
                )
                if resp.status_code == 200:
                    return resp.json().get('results', [])
                return []
        except Exception as e:
            logger.error(f'Failed to fetch memories: {e}')
            return []

    async def update_memory(self, memory_id: str, new_content: str, new_tags: List[str], reason: str, user: str) -> bool:
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
                audit_headers = self.headers.copy()
                audit_headers['X-Audit-Reason'] = reason
                await client.delete(f'{self.api_url}/v2/memories/{memory_id}', headers=audit_headers)
                payload = {
                    'content': new_content, 'tags': new_tags,
                    'project': self.headers.get('X-Project-Id', 'default'),
                    'source': 'dashboard-iso-edit', 'importance': 1.0,
                    'metadata': {'previous_version_id': memory_id, 'modification_reason': reason}
                }
                create_resp = await client.post(f'{self.api_url}/v2/memories/', json=payload, headers=audit_headers)
                return create_resp.status_code == 200
        except Exception: return False

    async def delete_memory(self, memory_id: str, reason: str, user: str) -> bool:
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
                audit_headers = self.headers.copy()
                audit_headers['X-Audit-Reason'] = reason
                resp = await client.delete(f'{self.api_url}/v2/memories/{memory_id}', headers=audit_headers)
                return resp.status_code == 200
        except Exception: return False
