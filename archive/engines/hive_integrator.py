import os
import json
import re

BASE_DIR = '/mnt/extra_storage/RAE-agentic-memory-agnostic-core/agent_hive/work_dir/components/'

def log_msg(msg):
    print(f'[*] {msg}', flush=True)

def clean_json(text):
    if '```json' in text:
        text = text.split('```json')[1].split('```')[0]
    elif '```' in text:
        text = text.split('```')[1].split('```')[0]
    return text.strip()

def integrate_service(folder_path, s_name):
    contract_path = os.path.join(folder_path, 'contract.json')
    symbols_path = os.path.join(folder_path, 'symbols.json')
    
    if not os.path.exists(contract_path) or not os.path.exists(symbols_path): return

    source_tsx = os.path.join(BASE_DIR, s_name + '.tsx')
    if not os.path.exists(source_tsx):
        source_tsx = os.path.join(folder_path, s_name + '.tsx')
    if not os.path.exists(source_tsx):
        tsxs = [f for f in os.listdir(folder_path) if f.endswith('.tsx') and f != '_integrated.tsx']
        if tsxs: source_tsx = os.path.join(folder_path, tsxs[0])
        else: return

    output_file = os.path.join(folder_path, '_integrated.tsx')
    if os.path.exists(output_file): return

    log_msg(f'Integrating Service: {s_name}')
    
    try:
        with open(source_tsx, 'r') as f: source_code = f.read()
    except: return

    header = "/**\n * Service: " + s_name + "\n * Integrated by RAE-Feniks v57.12\n */\n\n"
    header += 'import React from "react";\n'
    header += 'import { useCalculator } from "../Calculator/CalculatorContext";\n'
    header += 'import { useCart } from "../CartContext";\n\n'
    
    code = source_code.replace('$scope.', 'ctx.').replace('$scope', 'ctx')
    
    with open(output_file, 'w') as f:
        f.write(header + code)
    log_msg(f'  [SAVED] {output_file}')

if __name__ == "__main__":
    items = os.listdir(BASE_DIR)
    for item in items:
        path = os.path.join(BASE_DIR, item)
        if os.path.isdir(path):
            integrate_service(path, item)
