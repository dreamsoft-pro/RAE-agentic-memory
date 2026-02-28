import os
import json
import re

BASE_DIR = '/mnt/extra_storage/RAE-agentic-memory-agnostic-core/agent_hive/work_dir/components/CalcCtrl_Atomic/'
OUTPUT_DIR = '/mnt/extra_storage/RAE-agentic-memory-agnostic-core/agent_hive/work_dir/components/Calculator/Assembly/'

def log_msg(msg):
    print(f'[*] {msg}', flush=True)

def clean_json(text):
    if '```json' in text:
        text = text.split('```json')[1].split('```')[0]
    elif '```' in text:
        text = text.split('```')[1].split('```')[0]
    return text.strip()

def stitch_groups():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    
    with open(os.path.join(BASE_DIR, 'contract.json'), 'r') as f:
        raw_content = f.read()
        try:
            contract = json.loads(clean_json(raw_content))
        except Exception as e:
            log_msg(f"Failed to parse JSON: {e}")
            return
    
    for group in contract.get('componentGroups', []):
        group_name = group['groupName'].replace(' ', '_').replace('/', '_')
        log_msg(f'Assembling group: {group_name}')
        
        stitched_content = f"/**\n * Group: {group_name}\n * Auto-assembled by RAE-Feniks\n */\n\n"
        stitched_content += 'import React from "react";\n'
        stitched_content += 'import { useCalculator } from "../CalculatorContext";\n\n'
        stitched_content += f'export const {group_name} = () => {{\n'
        stitched_content += '  const calc = useCalculator();\n\n'
        
        group_body = ""
        for chunk_file in group['components']:
            chunk_path = os.path.join(BASE_DIR, chunk_file)
            if os.path.exists(chunk_path):
                with open(chunk_path, 'r') as cf:
                    content = cf.read()
                    content = re.sub(r'import.*?;', '', content)
                    content = re.sub(r'export const.*?=>.*?{', '', content)
                    content = re.sub(r'};?\s*$', '', content.strip())
                    group_body += f'\n  // --- {chunk_file} ---\n' + content
            else:
                log_msg(f'  [MISSING] {chunk_file}')
        
        group_body = group_body.replace('$scope.', 'calc.')
        group_body = group_body.replace('$scope', 'calc')
        
        stitched_content += group_body + '\n};\n'
        
        target_file = os.path.join(OUTPUT_DIR, f'{group_name}.tsx')
        with open(target_file, 'w') as f:
            f.write(stitched_content)
        log_msg(f'  [SAVED] {target_file}')

if __name__ == "__main__":
    stitch_groups()
