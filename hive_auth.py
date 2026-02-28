import httpx
import json
import time
import os

API_URL = 'http://localhost:8000/v2/memories'
OLLAMA_URL = 'http://ollama-dev:11434/api/generate'
TARGET_DIR = '/app/apps/memory_api/services/'
MODEL = 'qwen2.5-coder:14b'
HEADERS = {
    'X-API-Key': 'test-key',
    'X-Tenant-Id': '00000000-0000-0000-0000-000000000000'
}

PROMPT = "TASK: Convert legacy JS to Next.js TypeScript class. RULES: 1. Use 'import api from @/lib/api;' 2. Use async/await. 3. NO Angular, NO RxJS. 4. Return ONLY code."

def ask_ollama(prompt):
    try:
        payload = {'model': MODEL, 'prompt': prompt, 'stream': False}
        resp = httpx.post(OLLAMA_URL, json=payload, timeout=600.0)
        return resp.json().get('response', '')
    except: return ''

def process_hive():
    try:
        resp = httpx.get(API_URL + '/?tag=modernization_v3&tag=pending&limit=1', headers=HEADERS)
        mems = resp.json().get('results', [])
        if not mems: return

        for mem in mems:
            mid = mem['id']
            source = mem['content']
            s_name = 'service_' + mid[:8]
            
            # Simple name extraction
            if "factory('" in source:
                s_name = source.split("factory('")[1].split("'")[0]
            elif 'factory("' in source:
                s_name = source.split('factory("')[1].split('"')[0]

            print('Modernizing: ' + s_name)
            final = ask_ollama(PROMPT + chr(10) + source)
            
            if '```' in final:
                try:
                    final = final.split('```')[1]
                    if final.startswith('typescript'): final = final[10:]
                    if final.startswith('ts'): final = final[2:]
                except: pass

            final = final.strip()
            if len(final) > 10:
                # Save directly to the mounted volume for persistence
                target_file = '/app/apps/memory_api/services/' + s_name.lower() + '.ts'
                with open(target_file, 'w') as f:
                    f.write(final)
                
                resp_patch = httpx.patch(API_URL + '/' + mid, json={'tags': ['modernization_v3', 'completed']}, headers=HEADERS)
                print('OK: ' + s_name + ' PATCH: ' + str(resp_patch.status_code))
    except Exception as e:
        print('Error: ' + str(e))

if __name__ == "__main__":
    print('HIVE V5.0 (AUTH ENABLED) START')
    while True:
        process_hive()
        time.sleep(1)
