import urllib.request
import json
import os
import time
import re
import traceback
from typing import List, Dict, Tuple, Optional

IN_DOCKER = os.path.exists('/.dockerenv')
BASE_API = os.getenv('RAE_API_URL', 'http://rae-api-dev:8000' if IN_DOCKER else 'http://localhost:8001')
if not BASE_API.endswith('/'): BASE_API += '/'
API_URL = BASE_API + "v2/memories/"
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://host.docker.internal:11435/api/generate' if IN_DOCKER else 'http://localhost:11435/api/generate')
OUT_DIR = '/app/work_dir/components/' if IN_DOCKER else '/mnt/extra_storage/factory/RAE-Feniks/modernized/components/'
HEADERS = {'X-API-Key': 'test-key', 'X-Tenant-Id': '00000000-0000-0000-0000-000000000000'}

MODEL_ARCHITECT = "gemini-2.5-pro"
MODEL_L1_WRITER = "qwen2.5:14b"
MODEL_L1_AUDITOR = "gemini-2.5-flash"
MODEL_L2_CONSENSUS = ["gemini-2.5-pro", "gpt-4o-mini", "deepseek-coder:14b"]

def log_msg(msg, reflective=False):
    ts = time.strftime("%H:%M:%S")
    formatted = f"[{ts}] {msg}"
    print(formatted, flush=True)
    if reflective:
        try:
            http_req(API_URL, {"content": formatted, "layer": "reflective", "tags": ["v62_log"]}, 'POST')
        except: pass

def http_req(url, data=None, method='GET'):
    body = json.dumps(data).encode('utf-8') if data else None
    headers = {'Content-Type': 'application/json', **HEADERS} if data else HEADERS
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=120) as f:
        return json.loads(f.read().decode('utf-8'))

def ask_saas(model, prompt, system=""):
    try:
        content = f"SYSTEM: {system}\nUSER: {prompt}"
        payload = {"content": content, "layer": "reflective", "tags": ["hive_call", model], "metadata": {"target_model": model}}
        data = http_req(API_URL, payload, 'POST')
        return data.get('message', data.get('content', ''))
    except Exception as e:
        log_msg(f"SaaS Error: {e}")
        return ""

def ask_ollama(model, prompt, system=""):
    try:
        data = {"model": model, "prompt": prompt, "system": system, "stream": False, "options": {"num_ctx": 16384}}
        res = http_req(OLLAMA_URL, data, 'POST')
        return res.get('response', '')
    except Exception as e:
        log_msg(f"Ollama Error: {e}")
        return ""

def get_template(service_name):
    try:
        data = http_req(API_URL + "?tag=html_template&limit=500")
        mems = data.get('results', [])
        clean = service_name.replace('.js', '').replace('Ctrl', '').replace('Controller', '').replace('Service', '').lower()
        for t in mems:
            meta = t.get('metadata', {})
            t_file = meta.get('file') or meta.get('filename') or ""
            if not t_file:
                match = re.search(r'FILE:\s*(\S+)', t['content'])
                if match: t_file = match.group(1)
            if t_file and clean in t_file.lower(): return t['content'], t_file
    except: pass
    return None, None

def process_one(mem):
    mid = mem['id']
    content = mem['content']
    tags = mem['tags']
    match = re.search(r'FILE:\s*(\S+)', content)
    s_name = match.group(1) if match else f"unknown_{mid[:8]}.js"
    if "routes.js" in s_name or "proxy.js" in s_name:
        log_msg(f"Blacklisted: {s_name}")
        http_req(f"{API_URL}{mid}/", {"tags": list(set(tags + ['v62_processed']))}, 'PATCH')
        return
    log_msg(f"PROCESSING: {s_name}")
    template_code, t_file = get_template(s_name)
    if not template_code:
        log_msg(f"No template: {s_name}")
        http_req(f"{API_URL}{mid}/", {"tags": list(set(tags + ['v62_processed', 'v62_no_template']))}, 'PATCH')
        return
    plan = ask_saas(MODEL_ARCHITECT, f"Blueprint for {s_name}. JSON ONLY. Source: {content[:2000]}")
    code = ask_ollama(MODEL_L1_WRITER, f"Plan: {plan}\nLogic: {content[:2000]}\nTemplate: {template_code[:2000]}")
    if '```' in code:
        try: code = re.search(r'```(?:tsx|typescript|js|javascript)?\n(.*?)\n```', code, re.DOTALL).group(1).strip()
        except: pass
    v1 = ask_saas(MODEL_L2_CONSENSUS[0], f"Vote PASS/FAIL. Plan: {plan}. Code: {code[:1000]}")
    if "PASS" in v1.upper():
        target_path = os.path.join(OUT_DIR, s_name.replace('.js', '.tsx'))
        with open(target_path, 'w') as f: f.write(code)
        log_msg(f"SUCCESS: {s_name}")
        http_req(f"{API_URL}{mid}/", {"tags": list(set(tags + ['v62_processed', 'v62_pass']))}, 'PATCH')
    else:
        log_msg(f"FAIL: {s_name}")
        http_req(f"{API_URL}{mid}/", {"tags": list(set(tags + ['v62_processed', 'v62_fail']))}, 'PATCH')

if __name__ == '__main__':
    if not os.path.exists(OUT_DIR): os.makedirs(OUT_DIR)
    while True:
        try:
            data = http_req(API_URL + "?tag=modernization_v3&exclude_tags=v62_processed&limit=1")
            mems = data.get('results', [])
            if mems: process_one(mems[0])
            else: time.sleep(20)
        except Exception as e:
            log_msg(f"Error: {e}")
            time.sleep(10)
