import httpx
import os
import time
import json
import re

# Configuration
API_URL = os.getenv('RAE_API_URL', 'http://localhost:8000/v2/memories/')
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://ollama-dev:11434/api/generate')
HEADERS = {'X-API-Key': 'test-key', 'X-Tenant-Id': '00000000-0000-0000-0000-000000000000'}
OUTPUT_DIR = '/app/apps/memory_api/services/components/'

# Models for 3x3 Protocol
MODEL_EXTRACTOR = "qwen2.5:14b"
MODEL_ARCHITECT = "deepseek-coder:16b"
MODEL_VALIDATOR = "llama3.1:8b"

TEMPLATES_CACHE = []

def log_msg(msg):
    # Log to file and console
    try:
        ts = time.ctime()
        with open('/app/assembly_v57.log', 'a') as f:
            f.write(f"{ts}: {msg}
")
    except: pass
    print(msg, flush=True)

def ask_model(model, prompt, system_prompt="", timeout=600.0):
    try:
        payload = {
            'model': model, 
            'prompt': prompt, 
            'system': system_prompt,
            'stream': False,
            'options': {'num_ctx': 32768, 'temperature': 0.1}
        }
        r = httpx.post(OLLAMA_URL, json=payload, headers=HEADERS, timeout=timeout)
        if r.status_code != 200:
            log_msg(f"  [HTTP {r.status_code}] {model}")
            return ""
        return r.json().get('response', '').strip()
    except Exception as e:
        log_msg(f"  [ERROR] {model}: {e}")
        return ""

def get_template(service_name):
    global TEMPLATES_CACHE
    if not TEMPLATES_CACHE:
        try:
            resp = httpx.get(f"{API_URL}?tag=html_template&limit=1000", headers=HEADERS, timeout=60.0)
            TEMPLATES_CACHE = resp.json().get('results', [])
        except Exception as e:
            log_msg(f"  [ERROR] Failed to fetch templates: {e}")
    
    clean = service_name.replace('.js', '').replace('Ctrl', '').replace('Controller', '').replace('Service', '').lower()
    for t in TEMPLATES_CACHE:
        t_file = t.get('metadata', {}).get('file', '').lower()
        if clean in t_file: return t['content'], t_file
    return None, None

def get_full_logic(service_name):
    try:
        resp = httpx.get(f"{API_URL}?tag=completed&tag=modernization_v3&limit=100", headers=HEADERS)
        results = resp.json().get('results', [])
        chunks = [m for m in results if m.get('metadata', {}).get('service') == service_name]
        chunks.sort(key=lambda x: int(x.get('metadata', {}).get('chunk_index', 0)))
        return "
".join([c['content'] for c in chunks]), [c['id'] for c in chunks]
    except Exception as e:
        log_msg(f"  [ERROR] Failed to fetch logic for {service_name}: {e}")
        return None, []

def extract_symbols(logic, template):
    log_msg("  [1/3] THE EXTRACTOR: Building Symbol Table...")
    prompt = f"""
    ANALYSIS TASK: Create a Symbol Table for AngularJS to Next.js migration.
    
    LOGIC:
    {logic}
    
    TEMPLATE:
    {template}
    
    OUTPUT JSON FORMAT:
    {{
      "state": {{ "$scope.var": "useState equivalent", ... }},
      "functions": {{ "functionName": "React handler equivalent", ... }},
      "directives": {{ "ng-repeat": "map", "ng-if": "conditional", ... }},
      "dependencies": [ "services to be imported via axios/hooks" ]
    }}
    Output ONLY valid JSON.
    """
    resp = ask_model(MODEL_EXTRACTOR, prompt, "You are a specialized Symbol Extractor for AngularJS.")
    # Extract JSON from markdown if needed
    if "```json" in resp:
        resp = resp.split("```json")[1].split("```")[0].strip()
    elif "```" in resp:
        resp = resp.split("```")[1].split("```")[0].strip()
    return resp

def architect_component(logic, template, symbols):
    log_msg("  [2/3] THE ARCHITECT: Reconstructing .tsx...")
    prompt = f"""
    CONSTRUCTION TASK: Build a Modern Next.js 14 Component.
    
    SYMBOL TABLE:
    {symbols}
    
    LOGIC:
    {logic}
    
    TEMPLATE:
    {template}
    
    STRICT RULES:
    1. 100% Tailwind CSS.
    2. Zero Bootstrap.
    3. Pure TypeScript.
    4. Use hooks (useState, useEffect) as defined in Symbol Table.
    5. Clean layouts (Flexbox/Grid).
    6. Lucide icons or SVG placeholders.
    """
    return ask_model(MODEL_ARCHITECT, prompt, "You are a Senior Next.js Architect.")

def validate_component(code, logic, template):
    log_msg("  [3/3] THE VALIDATOR: Auditing for Parity & Quality...")
    prompt = f"""
    AUDIT TASK: Verify React code against Legacy Parity and Tailwind Standards.
    
    REACT CODE:
    {code}
    
    ORIGINAL LOGIC:
    {logic}
    
    ORIGINAL TEMPLATE:
    {template}
    
    CHECKLIST:
    - [ ] No Bootstrap classes (btn, col-, panel-)?
    - [ ] Functional parity with original logic?
    - [ ] Correct TypeScript types?
    - [ ] No AngularJS artifacts?
    
    Respond ONLY with:
    PASS
    or
    FAIL: [Reason]
    """
    return ask_model(MODEL_VALIDATOR, prompt, "You are a Strict Code Auditor.")

def protocol_3x3_cycle():
    try:
        resp = httpx.get(f"{API_URL}?tag=completed&tag=modernization_v3&limit=20", headers=HEADERS)
        mems = resp.json().get('results', [])
        for mem in mems:
            mid = mem['id']
            tags = mem['tags']
            if 'v57_processed' in tags: continue
            
            s_name = mem.get('metadata', {}).get('service', 'unknown.js')
            template_code, t_file = get_template(s_name)
            full_logic, chunk_ids = get_full_logic(s_name)
            
            if not full_logic or not template_code:
                # Mark as processed but skipped to avoid re-checking every time
                httpx.patch(f"{API_URL}{mid}", json={'tags': tags + ['v57_processed', 'v57_skip']}, headers=HEADERS)
                continue

            log_msg(f"🚀 3x3 PROTOCOL START: {s_name}")
            
            # 1. Extractor
            symbols = extract_symbols(full_logic, template_code)
            if not symbols:
                log_msg(f"  [ABORT] Extractor failed for {s_name}")
                continue
            
            # 2. Architect
            code = architect_component(full_logic, template_code, symbols)
            if not code:
                log_msg(f"  [ABORT] Architect failed for {s_name}")
                continue
            
            # Clean code
            if '```' in code:
                try: code = code.split('```')[1].replace('tsx', '').replace('typescript', '').strip()
                except: pass

            # 3. Validator
            audit = validate_component(code, full_logic, template_code)
            
            if "PASS" in audit.upper():
                target_path = os.path.join(OUTPUT_DIR, s_name.replace('.js', '.tsx'))
                with open(target_path, 'w') as f: f.write(code)
                # Save symbols for reference
                try:
                    with open(target_path + '.symbols.json', 'w') as f: f.write(symbols)
                except: pass
                
                for cid in chunk_ids:
                    # Update all chunks for this service
                    httpx.patch(f"{API_URL}{cid}", json={'tags': tags + ['v57_processed', 'v57_pass']}, headers=HEADERS)
                log_msg(f"✅ 3x3 SUCCESS: {s_name}")
            else:
                log_msg(f"❌ 3x3 FAIL: {s_name} | {audit[:100]}")
                # Log failure to RAE Reflective layer
                httpx.post(API_URL, json={
                    "content": f"3x3 Audit Failure for {s_name}: {audit}",
                    "layer": "reflective",
                    "tags": ["audit_failure", "v57"],
                    "metadata": {"service": s_name, "audit": audit}
                }, headers=HEADERS)
                # Mark chunks as failed
                for cid in chunk_ids:
                    httpx.patch(f"{API_URL}{cid}", json={'tags': tags + ['v57_processed', 'v57_fail']}, headers=HEADERS)

    except Exception as e:
        log_msg(f"💥 Fatal Error in cycle: {e}")

if __name__ == '__main__':
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    log_msg("=== HIVE ENGINE v57 (MISSION FENIKS) START ===")
    while True:
        protocol_3x3_cycle()
        time.sleep(5)
