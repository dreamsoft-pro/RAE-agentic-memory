import httpx
import json
import time
import os
import re

API_URL = 'http://localhost:8001/v2/memories'
OLLAMA_URL = 'http://localhost:11434/api/generate'
TARGET_DIR = '/home/operator/dreamsoft_factory/next-frontend/src/services/'

# DEEPSEEK 33B PROMPT - EXTREME DISCIPLINE
PROMPT = """You are a Senior TypeScript Developer. Convert legacy JavaScript to Next.js.
RULES:
1. USE: 'import api from "@/lib/api";'
2. USE: Plain TypeScript class with async/await.
3. FORBIDDEN: No Angular, No @Injectable, No RxJS, No Observable, No HttpClient.
4. Logic must use 'api.get', 'api.post', etc.
5. Return ONLY clean TypeScript code. No markdown, no comments.
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
            # SUPER SANITIZATION: hide 'angular' strings
            source = mem['content'].replace('angular.module', '/* mod */').replace('.factory', '.srv')
            
            s_name = 'service_%s' % mid[:8]
            m = re.search(r"srv\(['"](\w+)['"]", source)
            if m: s_name = m.group(1)

            print('Modernizing ' + s_name + ' with DeepSeek 33B')
            
            full_prompt = PROMPT + "

SOURCE:
" + source
            final = ask_ollama('deepseek-coder:33b', full_prompt)
            
            # Extract code if model still uses markdown
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
                print('Saved ' + target_file)
    except Exception: print('Error in loop')

if __name__ == "__main__":
    print('HIVE V4.6 (DEEPSEEK 33B) START')
    while True:
        process_hive()
        time.sleep(2)
