import os
import re

BASE_DIR = '/mnt/extra_storage/RAE-agentic-memory-agnostic-core/agent_hive/work_dir/components/'

def clean_file(path):
    try:
        with open(path, 'r') as f:
            lines = f.readlines()
        
        clean_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('//') or stripped.startswith('import ') or 'use' in stripped or 'const' in stripped:
                clean_lines.append(line)
                continue
            if '```' in line: continue
            if re.match(r'^#{1,6}\s', stripped): continue
            if re.match(r'^[\*\-]\s', stripped): continue
            if re.match(r'^[A-Z][^\{;\}]+[\.!\?]$', stripped) and not any(c in line for c in ['=', '(', ')', '{', '}', ':', '<', '>']):
                continue
            clean_lines.append(line)
            
        with open(path, 'w') as f:
            f.writelines(clean_lines)
        return True
    except: return False

if __name__ == '__main__':
    count = 0
    for root, dirs, files in os.walk(BASE_DIR):
        for f in files:
            if f.endswith('.tsx') or f.endswith('_stitched.tsx'):
                if clean_file(os.path.join(root, f)):
                    count += 1
    print(f'[*] Cleaned {count} files.')
