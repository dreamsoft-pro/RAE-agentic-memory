import os
import re

DIR = '/mnt/extra_storage/RAE-agentic-memory-agnostic-core/agent_hive/work_dir/components/Calculator/Assembly/'

def clean_file(path):
    with open(path, 'r') as f:
        lines = f.readlines()
    
    clean_lines = []
    
    for line in lines:
        stripped = line.strip()
        # Keep imports, group headers, and core syntax
        if stripped.startswith('// --- chunk') or stripped.startswith('import ') or 'useCalculator' in stripped:
            clean_lines.append(line)
            continue
            
        # Remove markdown code tags
        if '```' in line:
            continue
        # Remove markdown headers
        if re.match(r'^#{1,6}\s', stripped):
            continue
        # Remove markdown bullet points
        if re.match(r'^[\*\-]\s', stripped):
            continue
        # Remove typical AI filler sentences (sentence-like but no code symbols)
        if re.match(r'^[A-Z][^\{;\}]+[\.!\?]$', stripped) and not any(c in line for c in ['=', '(', ')', '{', '}', ':']):
            continue
            
        clean_lines.append(line)
        
    with open(path, 'w') as f:
        f.writelines(clean_lines)
    print(f'[*] Cleaned: {path}')

if __name__ == '__main__':
    if not os.path.exists(DIR):
        print("Directory not found")
    else:
        for f in os.listdir(DIR):
            if f.endswith('.tsx'):
                clean_file(os.path.join(DIR, f))
