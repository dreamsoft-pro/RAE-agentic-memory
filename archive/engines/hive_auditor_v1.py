import httpx
import json
import time
import os

API_URL = 'http://localhost:8000/v2/memories/'
OLLAMA_URL = 'http://ollama-dev:11434/api/generate'
MODEL = 'deepseek-coder-v2:16b'
HEADERS = {'X-API-Key': 'test-key', 'X-Tenant-Id': '00000000-0000-0000-0000-000000000000'}

PROMPT = """You are an Elite Code Auditor. Compare Legacy AngularJS with New TypeScript.
CRITICAL RULES:
1. METHOD PARITY: Count methods in JS. If TS has fewer methods -> FAIL.
2. LOGIC INTEGRITY: Check if complex calculations are preserved.
3. NO TODOs: Any "// TODO" or "// Implement this" -> FAIL.
4. API: Must use '@/lib/api'.

Respond ONLY with:
PASS - if perfect.
FAIL: [reason] - if anything is missing."""

def process_audit():
    try:
        resp = httpx.get(API_URL + '?tag=modernization_v3&tag=review&limit=1', headers=HEADERS, timeout=60.0)
        mems = resp.json().get('results', [])
        if not mems: return

        for mem in mems:
            mid = mem['id']
            source_legacy = mem['content']
            s_name = mem.get('metadata', {}).get('service', 'unknown')
            
            ts_file = '/app/apps/memory_api/services/' + s_name.lower().replace('.js', '.ts')
            if not os.path.exists(ts_file):
                httpx.patch(API_URL + mid, json={'tags': ['modernization_v3', 'pending']}, headers=HEADERS)
                return

            with open(ts_file, 'r') as f:
                source_new = f.read()

            print(f'AUDITOR (DeepSeek 16B): Auditing {s_name}...')
            audit_prompt = f"{PROMPT}\n\nJS:\n{source_legacy}\n\nTS:\n{source_new}"
            payload = {
                'model': MODEL, 
                'prompt': audit_prompt, 
                'stream': False,
                'options': {'temperature': 0.0}
            }
            
            response = httpx.post(OLLAMA_URL, json=payload, timeout=600.0).json().get('response', '').strip()
            
            if 'PASS' in response.upper()[:10]:
                print(f'✅ PASS: {s_name}')
                httpx.patch(API_URL + mid, json={'tags': ['modernization_v3', 'completed']}, headers=HEADERS)
            else:
                print(f'❌ FAIL: {s_name} | Reason: {response[:100]}')
                httpx.patch(API_URL + mid, json={'tags': ['modernization_v3', 'pending']}, headers=HEADERS)

    except Exception as e:
        print(f'Auditor Error: {e}')

if __name__ == '__main__':
    print('HIVE AUDITOR v2.0 (DeepSeek 16B) START')
    while True:
        process_audit()
        time.sleep(5)
