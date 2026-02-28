import httpx
import os
import time
import json
import re

# Configuration (Paths inside container, mapped to /mnt/extra_storage/... on Node 1)
OUTPUT_DIR = '/app/work_dir/components/'
API_URL = 'http://rae-api-dev:8000/v2/memories/'
OLLAMA_URL = 'http://ollama-dev:11434/api/generate'
HEADERS = {'X-API-Key': 'test-key', 'X-Tenant-Id': '00000000-0000-0000-0000-000000000000'}

MODEL_EXTRACTOR = os.getenv('MODEL_EXTRACTOR', 'qwen2.5:14b')

def log_msg(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

def ask_model(model, prompt, system_prompt="", timeout=600.0):
    try:
        payload = {
            'model': model, 'prompt': prompt, 'system': system_prompt,
            'stream': False, 'options': {'num_ctx': 32768, 'temperature': 0.1}
        }
        r = httpx.post(OLLAMA_URL, json=payload, timeout=timeout)
        return r.json().get('response', '').strip()
    except Exception as e:
        log_msg(f'  [ERROR] {model}: {e}')
        return ""

def get_full_logic(service_name):
    try:
        resp = httpx.get(f'{API_URL}?q={service_name}&limit=200', headers=HEADERS)
        results = resp.json().get('results', [])
        chunks = [m for m in results if service_name in (m.get('metadata', {}).get('file') or m.get('metadata', {}).get('service') or '')]
        if not chunks: chunks = [m for m in results if m.get('metadata', {}).get('is_chunk')]
        if not chunks: return None
        chunks.sort(key=lambda x: int(x.get('metadata', {}).get('chunk_index', 0)))
        return "\n".join([c['content'] for c in chunks])
    except: return None

def process_item(item_name, full_path):
    # Determine directory name (e.g. "AddressService" for "AddressService.tsx")
    s_name = item_name.replace('.tsx', '').replace('.js', '').replace('.html', '')
    if not s_name: return
    
    target_dir = os.path.join(OUTPUT_DIR, s_name)
    
    # Skip if contract already exists
    if os.path.exists(os.path.join(target_dir, 'contract.json')):
        return

    log_msg(f"📝 Creating Contract for: {s_name}")
    
    # Try to get logic from API or local source
    logic = get_full_logic(s_name)
    if not logic:
        if os.path.isfile(full_path):
            with open(full_path, 'r') as f: logic = f.read()
        elif os.path.isdir(full_path):
            chunks = [f for f in os.listdir(full_path) if f.endswith('.tsx')]
            if chunks:
                logic = ""
                for c in sorted(chunks):
                    with open(os.path.join(full_path, c), 'r') as f: logic += f.read() + "\n"
    
    if not logic or len(logic) < 50:
        log_msg(f"  [SKIP] No source for {s_name}")
        return

    # EXTRACT SYMBOLS & CONTRACT
    prompt = f"""
    TASK: Generate Symbol Table and Integration Contract for this component.
    SOURCE:
    {logic[:25000]}
    
    OUTPUT JSON FORMAT:
    {{
      "symbols": {{ "state": {{}}, "functions": {{}}, "dependencies": [] }},
      "contract": {{
        "component_group": "Main/UI/Logic/Service",
        "props_mapping": {{}},
        "global_state_keys": [],
        "legacy_parity_notes": ""
      }}
    }}
    Output valid JSON ONLY.
    """
    res = ask_model(MODEL_EXTRACTOR, prompt, "You are a Senior System Architect.")
    if '```' in res:
        try: res = re.search(r'```(?:json)?\n(.*?)\n```', res, re.DOTALL).group(1).strip()
        except: pass
    
    try:
        data = json.loads(res)
        if not os.path.exists(target_dir): os.makedirs(target_dir)
        with open(os.path.join(target_dir, 'symbols.json'), 'w') as f:
            json.dump(data.get('symbols', {}), f, indent=2)
        with open(os.path.join(target_dir, 'contract.json'), 'w') as f:
            json.dump(data.get('contract', {}), f, indent=2)
        log_msg(f"✅ Contract & Symbols saved in {target_dir}")
    except Exception as e:
        log_msg(f"❌ JSON Error for {s_name}: {e}")

if __name__ == '__main__':
    log_msg("=== HIVE ENGINE v57.9 (IN-PLACE CONTRACTOR) START ===")
    
    while True:
        items = os.listdir(OUTPUT_DIR)
        log_msg(f"Scanning {len(items)} items in {OUTPUT_DIR}")
        for item in items:
            process_item(item, os.path.join(OUTPUT_DIR, item))
        log_msg("--- Cycle complete. Sleeping... ---")
        time.sleep(300)
