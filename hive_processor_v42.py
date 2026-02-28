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
        return 'ERROR: %s' % e

def process_hive():
    try:
        url = API_URL + '/?tag=modernization_v3&tag=pending&limit=1'
        response = httpx.get(url)
        memories = response.json().get('results', [])
        
        if not memories:
            return

        for mem in memories:
            mid = mem['id']
            source = mem['content']
            s_name = 'service_%s' % mid[:8]
            
            print('[WRITER] Modernizuje z DeepSeek (v4.2): %s' % s_name)
            
            # Use % formatting to avoid f-string issues with shell
            full_prompt = WRITER_PROMPT + "

SOURCE CODE:
" + source
            final = ask_ollama('deepseek-coder-v2:16b', full_prompt)
            
            if '```' in final:
                parts = final.split('```')
                for p in parts:
                    if 'export' in p or 'class' in p:
                        final = p.replace('typescript', '').replace('ts', '').strip()
                        break
            
            if 'class' in final or 'export' in final:
                target_file = os.path.join(TARGET_DIR, s_name.lower() + '.ts')
                with open(target_file, 'w') as f:
                    f.write(final)
                
                patch_url = API_URL + '/' + mid
                httpx.patch(patch_url, json={'tags': ['modernization_v3', 'completed']})
                print('[HIVE] SUKCES: %s' % target_file)
            else:
                print('[HIVE] Blad - wynik nie jest kodem')
                
    except Exception as e:
        print('[HIVE] Err: %s' % e)

if __name__ == "__main__":
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
    print('HIVE V4.2 START')
    while True:
        process_hive()
        time.sleep(5)
