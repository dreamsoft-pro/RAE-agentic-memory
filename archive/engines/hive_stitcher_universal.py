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

def process_directory(dir_path, s_name):
    contract_path = os.path.join(dir_path, 'contract.json')
    if not os.path.exists(contract_path): return
    
    # Check if we have chunks
    chunks = [f for f in os.listdir(dir_path) if f.startswith('chunk_') and f.endswith('.tsx')]
    if not chunks: return
    
    output_file = os.path.join(dir_path, '_stitched.tsx')
    if os.path.exists(output_file): return

    log_msg(f'Assembling: {s_name}')
    
    try:
        with open(contract_path, 'r') as f:
            contract = json.loads(clean_json(f.read()))
    except:
        log_msg(f'  [ERROR] Bad contract in {s_name}')
        return

    stitched_content = "/**\n * Module: " + s_name + "\n * Auto-assembled by RAE-Feniks Universal Stitcher\n */\n\n"
    stitched_content += 'import React from "react";\n'
    # Flexible context hooks based on name
    if 'Calc' in s_name:
        stitched_content += 'import { useCalculator } from "../Calculator/CalculatorContext";\n'
    if 'Cart' in s_name:
        stitched_content += 'import { useCart } from "../CartContext";\n'
    
    for group in contract.get('componentGroups', []):
        group_name = group.get('groupName', 'Group').replace(' ', '_')
        stitched_content += "\n// --- GROUP: " + group_name + " ---\n"
        
        for chunk_file in group.get('components', []):
            chunk_path = os.path.join(dir_path, chunk_file)
            if os.path.exists(chunk_path):
                with open(chunk_path, 'r') as cf:
                    content = cf.read()
                    content = re.sub(r'import.*?;', '', content)
                    content = re.sub(r'export const.*?=>.*?{', '', content)
                    content = re.sub(r'};?\s*$', '', content.strip())
                    stitched_content += "\n// " + chunk_file + "\n" + content
        
    # Standard cleanup
    stitched_content = stitched_content.replace('$scope.', 'ctx.')
    stitched_content = stitched_content.replace('$scope', 'ctx')
    
    with open(output_file, 'w') as f:
        f.write(stitched_content)
    log_msg(f'  [SAVED] {output_file}')

if __name__ == "__main__":
    items = os.listdir(BASE_DIR)
    for item in items:
        path = os.path.join(BASE_DIR, item)
        if os.path.isdir(path):
            process_directory(path, item)
