import httpx
import json
import time
import os
import re

# CONFIG
API_URL = 'http://localhost:8001/v2/memories'
OLLAMA_URL = 'http://localhost:11434/api/generate'
TARGET_DIR = '/home/operator/dreamsoft_factory/next-frontend/src/services/'
MODEL = 'qwen2.5-coder:14b' # Super fast on RTX 4080

PROMPT = "TASK: Convert legacy JS to Next.js TypeScript class. RULES: 1. Use 'import api from "@/lib/api";' 2. Use async/await. 3. NO Angular, NO RxJS. 4. Return ONLY code."

def ask_ollama(prompt):
    try:
        payload = {'model': MODEL, 'prompt': prompt, 'stream': False}
        resp = httpx.post(OLLAMA_URL, json=payload, timeout=600.0)
        return resp.json().get('response', '')
    except: return ''

def process_hive():
    try:
        resp = httpx.get(API_URL + '/?tag=modernization_v3&tag=pending&limit=1')
        mems = resp.json().get('results', [])
        if not mems: return

        for mem in mems:
            mid = mem['id']
            source = mem['content']
            s_name = 'service_' + mid[:8]
            
            # Simple name extraction
            match = re.search(r"factory\(['"](\w+)['"]", source)
            if not match: match = re.search(r"service\(['"](\w+)['"]", source)
            if match: s_name = match.group(1)

            print('Modernizing: ' + s_name)
            final = ask_ollama(PROMPT + chr(10) + source)
            
            # Extract code from markdown
            if '```' in final:
                try:
                    final = final.split('```')[1]
                    if final.startswith('typescript'): final = final[10:]
                    if final.startswith('ts'): final = final[2:]
                except: pass

            final = final.strip()
            if len(final) > 10:
                target_file = os.path.join(TARGET_DIR, s_name.lower() + '.ts')
                with open(target_file, 'w') as f:
                    f.write(final)
                
                httpx.patch(API_URL + '/' + mid, json={'tags': ['modernization_v3', 'completed']})
                print('OK: ' + s_name)
    except: pass

if __name__ == "__main__":
    print('HIVE V4.7 (GPU OPTIMIZED) START')
    while True:
        process_hive()
        time.sleep(1)
