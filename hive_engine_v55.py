import httpx
import json
import time
import os

API_URL = 'http://localhost:8000/v2/memories/'
OLLAMA_URL = 'http://ollama-dev:11434/api/generate'
MODEL = 'qwen2.5:14b'
HEADERS = {'X-API-Key': 'test-key', 'X-Tenant-Id': '00000000-0000-0000-0000-000000000000'}

def get_rae_context(query):
    """RAE-FIRST: Query RAE for existing patterns or Feniks recipes."""
    try:
        resp = httpx.get(f"{API_URL}search?q={query}&limit=2", headers=HEADERS, timeout=10.0)
        results = resp.json().get('results', [])
        if results:
            return "\n".join([r['content'] for r in results])
    except: pass
    return "No historical context found."

PROMPT_TEMPLATE = """You are a Lead Software Architect operating in a HARD FRAME. 
Use RAE-FIRST protocol to integrate historical context and Feniks recipes.

HISTORICAL CONTEXT FROM RAE:
{context}

MANDATORY RULES:
1. LEAN DESIGN: 100-150 lines per file.
2. BACKEND-FIRST: Add // [BACKEND_ADVICE] for heavy logic.
3. API: Use '@/lib/api'.
4. COMPLETENESS: 1:1 parity with legacy methods.

Convert the following code:
{source}

Return ONLY code."""

def process_hive():
    try:
        resp = httpx.get(API_URL + '?tag=modernization_v3&tag=pending&limit=1', headers=HEADERS, timeout=60.0)
        mems = resp.json().get('results', [])
        if not mems: return

        for mem in mems:
            mid = mem['id']
            source = mem['content']
            s_name = mem.get('metadata', {}).get('service', 'unknown_service')
            
            # RAE-FIRST: Get context before writing
            context = get_rae_context(f"angular service {s_name} modernization pattern")
            
            print(f'PISARZ (v7.0 RAE-FIRST): Modernizacja {s_name}...')
            
            prompt = PROMPT_TEMPLATE.format(context=context, source=source)
            payload = {'model': MODEL, 'prompt': prompt, 'stream': False}
            final = httpx.post(OLLAMA_URL, json=payload, timeout=600.0).json().get('response', '').strip()
            
            if '```' in final:
                try:
                    final = final.split('```')[1]
                    if final.startswith('typescript'): final = final[10:]
                    if final.startswith('ts'): final = final[2:]
                except: pass

            target_file = '/app/apps/memory_api/services/' + s_name.lower().replace('.js', '.ts')
            with open(target_file, 'w') as f:
                f.write(final)
            
            httpx.patch(API_URL + mid, json={'tags': ['modernization_v3', 'review']}, headers=HEADERS, timeout=30.0)
            print(f'OK: {s_name} sent to review.')
    except Exception as e:
        print(f'Writer Error: {e}')

if __name__ == '__main__':
    print('HIVE PISARZ v7.0 (RAE-FIRST & HARD FRAMES) START')
    while True:
        process_hive()
        time.sleep(5)
