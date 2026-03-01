import httpx
import json
import time
import os
import re

API_URL = 'http://localhost:8001/v2/memories'
OLLAMA_URL = 'http://localhost:11434/api/generate'
TARGET_DIR = '/home/operator/dreamsoft_factory/next-frontend/src/services/'

# V4.5 - API INTEGRATION VERSION
PROMPT = """Convert this legacy JS code to a modern TypeScript class for Next.js.
CRITICAL RULES:
1. USE our custom api instance: 'import api from "@/lib/api";'
2. DO NOT import axios directly.
3. USE 'api.get', 'api.post', etc. instead of '$http'.
4. NO Angular decorators, NO RxJS.
5. Use async/await.
6. RETURN ONLY CODE.
"""

def ask_ollama(model, prompt):
    try:
        payload = {'model': model, 'prompt': prompt, 'stream': False}
        resp = httpx.post(OLLAMA_URL, json=payload, timeout=600.0)
        return resp.json().get('response', '')
    except Exception: return ''

def process_hive():
    try:
        url = API_URL + '/?tag=modernization_v3&tag=pending&limit=1'
        response = httpx.get(url)
        memories = response.json().get('results', [])
        if not memories: return

        for mem in memories:
            mid = mem['id']
            source = mem['content']
            s_name = 'service_' + mid[:8]
            
            # Simple name extraction
            m = re.search(r"factory\(['"](\w+)['"]", source)
            if not m:
                m = re.search(r"service\(['"](\w+)['"]", source)
            if m: s_name = m.group(1)

            print('Modernizing ' + s_name + ' with @/lib/api')
            
            full_prompt = PROMPT + chr(10) + chr(10) + "SOURCE:" + chr(10) + source
            final = ask_ollama('qwen2.5-coder:14b', full_prompt)
            
            if '```' in final:
                try:
                    final = final.split('```')[1]
                    if final.startswith('typescript'): final = final[10:]
                    if final.startswith('ts'): final = final[2:]
                except: pass

            if len(final) > 10:
                target_file = os.path.join(TARGET_DIR, s_name.lower() + '.ts')
                with open(target_file, 'w') as f:
                    f.write(final)
                
                httpx.patch(API_URL + '/' + mid, json={'tags': ['modernization_v3', 'completed']})
                print('Saved ' + target_file)
    except Exception as e: print('Error in loop')

if __name__ == "__main__":
    print('HIVE V4.5 (API INTEGRATED) START')
    while True:
        process_hive()
        time.sleep(2)
