import httpx
import json
import time
import os

API_URL = 'http://localhost:8000/v2/memories/'
OLLAMA_URL = 'http://ollama-dev:11434/api/generate'
TARGET_DIR = '/app/apps/memory_api/services/'
MODEL = 'qwen2.5:14b'
HEADERS = {
    'X-API-Key': 'test-key',
    'X-Tenant-Id': '00000000-0000-0000-0000-000000000000'
}

# V5.4 - DEBUGGING HANGS
PROMPT = """Convert legacy JS to Next.js TypeScript class. 
RULES: 
1. Use 'import api from @/lib/api;' (surowy axios jest zabroniony).
2. Use native async/await. 
3. NO Angular, NO RxJS. 
4. FORBIDDEN: Do NOT import 'bluebird' or use its Promise. Use native global Promise.
5. CRITICAL: Ensure all variables (like 'resource', 'url') are DEFINED before use. 
6. Return ONLY code."""

def ask_ollama(prompt):
    try:
        print(f"Asking Ollama (model: {MODEL})...")
        payload = {'model': MODEL, 'prompt': prompt, 'stream': False}
        resp = httpx.post(OLLAMA_URL, json=payload, timeout=600.0)
        return resp.json().get('response', '')
    except Exception as e:
        print('Ollama error: ' + str(e))
        return ''

def process_hive():
    try:
        print("Fetching pending memories...")
        resp = httpx.get(API_URL + '?tag=modernization_v3&tag=pending&limit=1', headers=HEADERS, timeout=30.0)
        print(f"API Response status: {resp.status_code}")
        
        mems = resp.json().get('results', [])
        if not mems: 
            print("No pending memories found.")
            return

        for mem in mems:
            mid = mem['id']
            source = mem['content']
            s_name = 'service_' + mid[:8]
            
            if "factory('" in source:
                s_name = source.split("factory('")[1].split("'")[0]
            elif 'factory("' in source:
                s_name = source.split('factory("')[1].split('"')[0]

            print('Modernizing (v5.4): ' + s_name)
            final = ask_ollama(PROMPT + chr(10) + source)
            
            if '```' in final:
                try:
                    final = final.split('```')[1]
                    if final.startswith('typescript'): final = final[10:]
                    if final.startswith('ts'): final = final[2:]
                except: pass

            final = final.strip()
            if len(final) > 10:
                target_file = '/app/apps/memory_api/services/' + s_name.lower() + '.ts'
                print(f"Saving to {target_file}")
                with open(target_file, 'w') as f:
                    f.write(final)
                
                print(f"Patching memory {mid} as completed...")
                resp_patch = httpx.patch(API_URL + mid, json={'tags': ['modernization_v3', 'completed']}, headers=HEADERS, timeout=30.0)
                print('OK: ' + s_name + ' (v5.4) | Status: ' + str(resp_patch.status_code))
            else:
                print('Empty result for ' + s_name)
    except Exception as e:
        print('Error in process_hive: ' + str(e))

if __name__ == "__main__":
    print('HIVE V5.4 (DEBUG HANGS) START')
    while True:
        process_hive()
        print("Sleeping 5s...")
        time.sleep(5)
