import httpx
import os
import time
import re

API_URL = os.getenv('RAE_API_URL', 'http://localhost:8000/v2/memories/')
OLLAMA_URL = 'http://ollama-dev:11434/api/generate'
HEADERS = {'X-API-Key': 'test-key', 'X-Tenant-Id': '00000000-0000-0000-0000-000000000000'}
OUTPUT_DIR = '/app/apps/memory_api/services/components/'

TEMPLATES_CACHE = []

def log_msg(msg):
    try:
        ts = time.ctime()
        with open('/app/assembly.log', 'a') as f:
            f.write(f"{ts}: {msg}\n")
    except: pass
    print(msg, flush=True)

def ask_model(model, prompt, timeout=300.0):
    try:
        if any(x in model for x in ['gemini', 'claude', 'gpt']):
            payload = {"content": prompt, "layer": "reflective", "tags": ["visual_modernization", model]}
            r = httpx.post(API_URL, json=payload, headers=HEADERS, timeout=timeout)
            data = r.json()
            return data.get('message', data.get('content', '')).strip()
        else:
            payload = {'model': model, 'prompt': prompt, 'stream': False}
            r = httpx.post(OLLAMA_URL, json=payload, headers=HEADERS, timeout=timeout)
            return r.json().get('response', '').strip()
    except Exception as e:
        log_msg(f"  [TIMEOUT/ERROR] {model}")
        return ""

def get_template(service_name):
    global TEMPLATES_CACHE
    if not TEMPLATES_CACHE:
        try:
            resp = httpx.get(f"{API_URL}?tag=html_template&limit=1000", headers=HEADERS, timeout=60.0)
            TEMPLATES_CACHE = resp.json().get('results', [])
        except: pass
    
    clean = service_name.replace('.js', '').replace('Ctrl', '').replace('Controller', '').replace('Service', '').lower()
    for t in TEMPLATES_CACHE:
        t_file = t.get('metadata', {}).get('file', '').lower()
        if clean in t_file: return t['content'], t_file
    return None, None

def get_full_logic(service_name):
    try:
        resp = httpx.get(f"{API_URL}?tag=completed&limit=100", headers=HEADERS)
        results = resp.json().get('results', [])
        chunks = [m for m in results if m.get('metadata', {}).get('service') == service_name]
        chunks.sort(key=lambda x: int(x.get('metadata', {}).get('chunk_index', 0)))
        return "\n".join([c['content'] for c in chunks]), [c['id'] for c in chunks]
    except: return None, []

def assemble_cycle():
    try:
        resp = httpx.get(f"{API_URL}?tag=completed&tag=modernization_v3&limit=50", headers=HEADERS)
        mems = resp.json().get('results', [])
        for mem in mems:
            mid = mem['id']
            tags = mem['tags']
            if 'assembled' in tags or 'assembled_skip' in tags: continue
            
            s_name = mem.get('metadata', {}).get('service', 'unknown.js')
            template_code, t_file = get_template(s_name)
            
            full_logic, chunk_ids = get_full_logic(s_name)
            if not full_logic: continue

            if not template_code:
                log_msg(f"⏩ Skipping {s_name} - No HTML found.")
                for cid in chunk_ids:
                    httpx.patch(f"{API_URL}{cid}", json={'tags': tags + ['assembled_skip']}, headers=HEADERS)
                return

            log_msg(f"🎨 VISUAL CLEAN ASSEMBLY: {s_name}...")
            
            prompt = f\"\"\"
            TASK: Assemble a MODERN Next.js 14 Component.
            LOGIC (.ts): {full_logic}
            TEMPLATE (.html): {template_code}
            
            STRICT VISUAL RULES:
            1. 100% Tailwind CSS. 0% Bootstrap (ABSOLUTELY NO 'btn', 'panel', 'col-').
            2. Use modern layout patterns (flex, grid).
            3. Replace FontAwesome with clean SVG icons or comments for Lucide.
            4. Implement strict TypeScript interfaces for Props.
            5. Map ALL AngularJS directives to React state/hooks.
            6. Output ONLY the code block.
            \"\"\"
            
            code = ask_model("qwen2.5:14b", prompt)
            
            if len(code) > 100:
                if '```' in code:
                    try: code = code.split('```')[1].replace('tsx', '').replace('typescript', '').strip()
                    except: pass
                
                # High-Quality Visual Audit
                audit = ask_model("llama3.1:8b", f"Does this React code use ANY Bootstrap classes? Respond ONLY 'PASS' if purely Tailwind, or 'FAIL: classnames' if Bootstrap found:\n{code}")
                
                if "PASS" in audit.upper():
                    target_path = os.path.join(OUTPUT_DIR, s_name.replace('.js', '.tsx'))
                    with open(target_path, 'w') as f: f.write(code)
                    for cid in chunk_ids:
                        httpx.patch(f"{API_URL}{cid}", json={'tags': tags + ['assembled']}, headers=HEADERS)
                    log_msg(f"✅ VISUAL PASS: {s_name} (Pure Tailwind)")
                    return
                else:
                    log_msg(f"❌ VISUAL FAIL: {s_name} | Reason: {audit[:50]}")
                    # System will retry with even stricter prompt in next cycle
    except Exception as e: log_msg(f"❌ Error: {e}")

if __name__ == '__main__':
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    log_msg("VISUAL CLEAN ENGINE v57.1 START (TOTAL BOOTSTRAP PURGE)")
    while True:
        assemble_cycle()
        time.sleep(2)
