import os

DIR = 'dreamsoft_factory/next-frontend/src/legacy_modules/'

def fix_imports(filepath):
    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except Exception as e:
        return

    needs_react = 'React' in content or '<' in content or 'useState' in content or 'useEffect' in content
    
    react_imports = set()
    if 'useState' in content: react_imports.add('useState')
    if 'useEffect' in content: react_imports.add('useEffect')
    if 'useContext' in content: react_imports.add('useContext')
    if 'useMemo' in content: react_imports.add('useMemo')
    if 'useRef' in content: react_imports.add('useRef')
    
    new_imports = ""
    if needs_react and 'import React' not in content:
        if react_imports:
            imports_str = ', '.join(react_imports)
            new_imports = "import React, { " + imports_str + " } from 'react';\n"
        else:
            new_imports = "import React from 'react';\n"
    
    if new_imports:
        content = new_imports + content
        with open(filepath, 'w') as f:
            f.write(content)

if __name__ == '__main__':
    if os.path.exists(DIR):
        for root, dirs, files in os.walk(DIR):
            for file in files:
                if file.endswith('.tsx') or file.endswith('.ts'):
                    fix_imports(os.path.join(root, file))
        print("✅ Auto-Importer finished fixing React dependencies.")
    else:
        print("Directory not found")
