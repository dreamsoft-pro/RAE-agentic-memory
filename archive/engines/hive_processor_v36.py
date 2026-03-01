import httpx
import json
import time
import os
import re

API_URL = 'http://localhost:8001/v2/memories'
OLLAMA_URL = 'http://localhost:11434/api/generate'
TARGET_DIR = '/home/operator/dreamsoft_factory/next-frontend/src/services/'

# RADICAL CHANGE: REMOVE 'ANGULAR' WORD FROM INPUT PROMPT
WRITER_PROMPT = """Convert this legacy JavaScript code to a modern TypeScript class for a React/Next.js environment.
CRITICAL RULES:
1. TARGET: Next.js / React (Plain TypeScript).
2. FORBIDDEN: Do not use @Injectable, HttpClient, Observable, or any Angular-specific libraries.
3. API CALLS: Use 'axios' or 'fetch' with async/await.
4. STRUCTURE: Export a standard class or an object with methods.
5. CLEANUP: Remove all legacy wrapper artifacts while keeping the logic.
6. OUTPUT: Return ONLY the code block starting with 'import axios'.
"""

def ask_ollama(model, prompt):
    try:
        payload = {'model': model, 'prompt': prompt, 'stream': False}
        resp = httpx.post(OLLAMA_URL, json=payload, timeout=600.0)
        return resp.json().get('response', '')
    except Exception as e:
        return f'ERROR: {e}'

def process_hive():
    try:
        response = httpx.get(f'{API_URL}/?tag=modernization_v3&tag=pending&limit=1')
        memories = response.json().get('results', [])
        
        if not memories:
            return

        for mem in memories:
            mid = mem['id']
            # REMOVE 'angular' string from source code before sending to LLM to avoid triggers
            source = mem['content'].replace('angular.module', '/* legacy module */').replace('.factory', '.provider')
            
            match = re.search(r"\.provider\(['"]([a-zA-Z0-9]+)['"]", source)
            s_name = match.group(1) if match else f'Service_{mid[:8]}'
            
            print(f'[WRITER] Modernizuje (Clean TS): {s_name}')
            final = ask_ollama('qwen2.5-coder:14b', f'{WRITER_PROMPT}

SOURCE CODE:
{source}')
            
            # Extract code from potential markdown
            if '```' in final:
                m = re.search(r"```(?:typescript|ts)?
(.*?)```", final, re.DOTALL)
                if m:
                    final = m.group(1)
            
            if 'class' in final or 'export' in final:
                target_file = os.path.join(TARGET_DIR, f'{s_name.lower()}.ts')
                with open(target_file, 'w') as f:
                    f.write(final)
                
                httpx.patch(f'{API_URL}/{mid}', json={'tags': ['modernization_v3', 'completed']})
                print(f'[HIVE] SUKCES: {target_file}')
            else:
                print(f'[HIVE] Blad - wynik nie jest kodem')
                
    except Exception as e:
        print(f'[HIVE] Err: {e}')

if __name__ == "__main__":
    os.makedirs(TARGET_DIR, exist_ok=True)
    print('HIVE V3.6 (RADICAL CLEAN) START')
    while True:
        process_hive()
        time.sleep(5)
