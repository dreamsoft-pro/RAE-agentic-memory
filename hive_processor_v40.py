import httpx
import json
import time
import os
import re

API_URL = 'http://localhost:8001/v2/memories'
OLLAMA_URL = 'http://localhost:11434/api/generate'
TARGET_DIR = '/home/operator/dreamsoft_factory/next-frontend/src/services/'

# DEEPSEEK CODING PROMPT
WRITER_PROMPT = """You are a Next.js Expert. Your task is to convert legacy JavaScript services to modern TypeScript classes for Next.js.

STRICT RULES:
- Use standard classes: 'export class Name { ... }'
- NO Angular decorators (no @Injectable, no @Component)
- NO RxJS (no Observable, no BehaviorSubject)
- NO HttpClient (use 'axios')
- Use async/await for all methods.
- Import axios from 'axios'.

EXAMPLE TRANSFORMATION:
Input: .factory('MySvc', function($http) { return { get: function() { return $http.get('/api'); } } })
Output:
import axios from 'axios';
export class MySvc {
  static async get() {
    const resp = await axios.get('/api');
    return resp.data;
  }
}

NOW CONVERT THIS SOURCE:
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
            source = mem['content']
            
            # Najprostszy mozliwy regex bez cudzyslowow w srodku klasy znakow
            s_name = f'Service_{mid[:8]}'
            # Szukamy .factory('Nazwa' lub .service('Nazwa'
            try:
                m = re.search(r"factory\(['"](\w+)['"]", source)
                if not m:
                    m = re.search(r"service\(['"](\w+)['"]", source)
                if m:
                    s_name = m.group(1)
            except:
                pass
            
            print(f'[WRITER] Modernizuje z DeepSeek (v4.0): {s_name} (ID: {mid})')
            final = ask_ollama('deepseek-coder-v2:16b', f'{WRITER_PROMPT}

{source}')
            
            if '```' in final:
                parts = final.split('```')
                for p in parts:
                    if 'export' in p or 'class' in p:
                        final = p.replace('typescript
', '').replace('ts
', '')
                        break
            
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
    print('HIVE V4.0 START')
    while True:
        process_hive()
        time.sleep(5)
