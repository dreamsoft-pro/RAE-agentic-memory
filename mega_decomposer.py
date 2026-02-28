# TIMESTAMP: 2026-02-23 13:20:00
import subprocess
import os
import json
import time
import re
import urllib.request

OUT_DIR = '/mnt/extra_storage/RAE-agentic-memory-agnostic-core/agent_hive/work_dir/components/'
API_URL = 'http://localhost:8001/v2/memories/'
HEADERS = {'X-API-Key': 'test-key', 'X-Tenant-Id': '00000000-0000-0000-0000-000000000000'}

def log_msg(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

def run_sql(query):
    # Use single quotes for the outer command to avoid f-string confusion
    full_query = query.replace('"', '\\"')
    cmd = ['docker', 'exec', 'rae-postgres', 'psql', '-U', 'rae', '-d', 'rae', '-t', '-c', full_query]
    return subprocess.check_output(cmd).decode('utf-8').strip()

def ask_gemini_mega(prompt):
    payload = {"content": prompt, "layer": "reflective", "tags": ["hive_call", "gemini-1.5-pro"]}
    req = urllib.request.Request(API_URL, data=json.dumps(payload).encode(), headers={'Content-Type': 'application/json', **HEADERS}, method='POST')
    with urllib.request.urlopen(req, timeout=600) as f:
        res = json.loads(f.read().decode())
        return res.get('message', '')

def decompose_file(filename):
    log_msg(f"🌟 Starting MEGA-DECOMPOSITION of {filename}...")
    try:
        sql = f"SELECT content FROM memories WHERE metadata->>'file' = '{filename}' ORDER BY (metadata->>'chunk_index')::int"
        full_source = run_sql(sql)
        log_msg(f"  -> Loaded {len(full_source)} characters.")

        arch_prompt = f"Break down this large AngularJS file into logical React sub-modules (hooks, utils, components). Return ONLY a JSON map of filename -> instruction. Module: {filename}. Snippet:\n{full_source[:100000]}"
        plan_json = ask_gemini_mega(arch_prompt)
        
        plan = json.loads(re.search(r'\{.*\}', plan_json, re.DOTALL).group(0))
        folder = filename.replace('.js', '').replace('.html', '')
        base_path = os.path.join(OUT_DIR, folder)
        if not os.path.exists(base_path): os.makedirs(base_path)
        
        for subfile, desc in plan.items():
            log_msg(f"  -> Building {subfile}...")
            # For implementation, we provide 100k context window
            code = ask_gemini_mega(f"Implement {subfile} for {filename}.\nLogic: {desc}\nContext:\n{full_source[:100000]}")
            if len(code) > 100:
                if '```' in code:
                    match = re.search(r'```(?:tsx|ts|html|javascript)?\n(.*?)\n```', code, re.DOTALL)
                    if match: code = match.group(1).strip()
                with open(os.path.join(base_path, subfile), 'w') as f: f.write(code)
                log_msg(f"  ✅ {subfile} saved.")
        
        log_msg(f"🚀 {filename} SUCCESS.")
    except Exception as e:
        log_msg(f"💥 Failed {filename}: {e}")

if __name__ == '__main__':
    decompose_file('CalcCtrl.js')
    decompose_file('calc.html')
