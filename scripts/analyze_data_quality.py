import yaml
import os
from collections import Counter

def analyze_set(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        return

    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
    
    memories = data.get('memories', [])
    queries = data.get('queries', [])
    
    # Check both 'text' and 'content' keys
    contents = []
    for m in memories:
        c = m.get('text') or m.get('content') or ""
        contents.append(c)
        
    content_counts = Counter(contents)
    duplicates = {c: count for c, count in content_counts.items() if count > 1}
    
    print(f"--- Analysis for {file_path} ---")
    print(f"Total Memories: {len(memories)}")
    print(f"Unique Memories: {len(content_counts)}")
    print(f"Duplicates found: {len(duplicates)}")
    if duplicates:
        for c, count in list(duplicates.items())[:3]:
            print(f"  - '{c[:50]}...': {count} times")
    
    print(f"Total Queries: {len(queries)}")
    direct_matches = 0
    for q in queries:
        q_text = q.get('query', '')
        if q_text in contents:
            direct_matches += 1
    print(f"Direct Query-to-Memory exact matches: {direct_matches}")
    print("-----------------------------------")

sets = [
    'benchmarking/sets/industrial_small.yaml',
    'benchmarking/sets/industrial_1k_unique.yaml',
    'benchmarking/sets/industrial_10k_unique.yaml',
    'benchmarking/sets/industrial_100k_unique.yaml'
]

for s in sets:
    analyze_set(s)
