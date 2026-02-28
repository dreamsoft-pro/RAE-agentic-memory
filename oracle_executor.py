import httpx
import os
import time

API_URL = os.getenv('RAE_API_URL', 'http://localhost:8000/v2/memories/')
HEADERS = {'X-API-Key': 'test-key', 'X-Tenant-Id': '00000000-0000-0000-0000-000000000000'}
TARGET_DIR = '/app/apps/memory_api/services/'

MODELS = ['claude-opus-4-5', 'gpt-4o', 'gemini-1.5-pro']

def get_oracle_code(service_name, legacy_content):
    print(f"🚀 [ORACLE] Requesting full modernization for: {service_name}")
    
    prompt = f"TASK: Convert this legacy AngularJS/Node.js file to modern Next.js 14+ TypeScript.\nFILE: {service_name}\n\nREQUIREMENTS:\n1. Use TypeScript with strict typing.\n2. Follow the 'Thin Client' principle (logic in PHP, state management in React/Next).\n3. Use '@/lib/api' for HTTP calls.\n4. Replace AngularJS DI with standard imports.\n5. Output ONLY the code within markdown code blocks. NO conversation.\n\nLEGACY CODE:\n{legacy_content}"

    for model in MODELS:
        print(f"  -> Consulting {model}...")
        payload = {
            "content": prompt,
            "layer": "reflective",
            "tags": ["oracle_direct_execution", model, "modernization_v3"],
            "metadata": {"service": service_name, "priority": "CRITICAL", "direct_exec": True}
        }
        try:
            r = httpx.post(API_URL, json=payload, headers=HEADERS, timeout=300.0)
            data = r.json()
            code = data.get('message', data.get('content', data.get('response', '')))
            
            if len(code) > 50:
                print(f"  ✅ SUCCESS: {model} delivered {len(code)} chars of code.")
                return code
            else:
                print(f"  ⚠️  Empty response from {model}")
        except Exception as e:
            print(f"  ❌ Error with {model}: {e}")
            time.sleep(2)
    
    return None

def main():
    print("🎯 STAGE 1: Infrastructure (Proxy & Routes)")
    resp = httpx.get(f"{API_URL}?tag=ORACLE_WAITING&limit=50", headers=HEADERS)
    mems = resp.json().get('results', [])
    
    processed_services = set()
    
    for m in mems:
        s_name = m.get('metadata', {}).get('service', 'unknown.js')
        if s_name not in ['proxy.js', 'routes.js']:
            continue
        if s_name in processed_services:
            continue
            
        mid = m['id']
        print(f"\n--- Processing {s_name} ({mid}) ---")
        code = get_oracle_code(s_name, m['content'])
        
        if code:
            if '```' in code:
                try: 
                    parts = code.split('```')
                    code = parts[1] if len(parts) >= 2 else code
                except: pass
                
            if code.startswith('typescript'): code = code[10:]
            if code.startswith('ts'): code = code[2:]
            if code.startswith('javascript'): code = code[10:]
            code = code.strip()

            target_path = os.path.join(TARGET_DIR, s_name.replace('.js', '.ts'))
            with open(target_path, 'w') as f:
                f.write(code)
            
            httpx.patch(f"{API_URL}{mid}", json={"tags": ["modernization_v3", "completed", "oracle_pass"]}, headers=HEADERS)
            processed_services.add(s_name)
            print(f"🎉 SAVED: {target_path}")
        else:
            print(f"🚨 FAILED: Could not get code for {s_name}")

if __name__ == '__main__':
    main()
