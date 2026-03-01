import os

DIR = 'dreamsoft_factory/next-frontend/src/legacy_modules/'

def inject_bridge(filepath):
    if 'httpBridge' in filepath: return
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except: return

    uses_http = '$http' in content
    uses_q = '$q' in content or 'defer()' in content
    
    if uses_http or uses_q:
        imports = []
        if uses_http: imports.append('$http')
        if uses_q: imports.append('$q')
        
        joined_imports = ', '.join(imports)
        import_stmt = "import { " + joined_imports + " } from './httpBridge';\n"
        
        if import_stmt not in content:
            content = import_stmt + content
            with open(filepath, 'w') as f:
                f.write(content)

if __name__ == '__main__':
    count = 0
    if os.path.exists(DIR):
        for root, dirs, files in os.walk(DIR):
            for file in files:
                if file.endswith('.tsx') or file.endswith('.ts'):
                    inject_bridge(os.path.join(root, file))
                    count += 1
        print(f"✅ Bridge injected into {count} modules.")
