import httpx
import json
import time
import os

API_URL = 'http://localhost:8000/v2/memories' # internal docker port
OLLAMA_URL = 'http://ollama-dev:11434/api/generate' # internal docker host
TARGET_DIR = '/app/apps/memory_api/services/' # simple target inside container volume
MODEL = 'qwen2.5-coder:14b'

PROMPT = "TASK: Convert legacy JS to Next.js TypeScript class. RULES: 1. Use 'import api from @/lib/api;' 2. Use async/await. 3. NO Angular, NO RxJS. 4. Return ONLY code."

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
                # We save to a temp location first
                target_file = '/tmp/' + s_name.lower() + '.ts'
                with open(target_file, 'w') as f:
                    f.write(final)
                
                httpx.patch(API_URL + '/' + mid, json={'tags': ['modernization_v3', 'completed']})
                print('OK: ' + s_name + ' saved to ' + target_file)
    except Exception as e:
        print('Error in loop: ' + str(e))

if __name__ == "__main__":
    print('HIVE V4.9 (DOCKER STABLE) START')
    while True:
        process_hive()
        time.sleep(1)
