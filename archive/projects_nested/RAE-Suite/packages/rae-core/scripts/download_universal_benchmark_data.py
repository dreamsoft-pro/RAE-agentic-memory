import requests
import yaml
import os

def create_benchmark_set(name, source_texts):
    memories = []
    queries = []
    
    for i, (title, text) in enumerate(source_texts.items()):
        # Split text into chunks of ~500 chars
        chunks = [text[i:i+500] for i in range(0, len(text), 500)]
        for j, chunk in enumerate(chunks):
            mem_id = f"{name}_{i}_{j}"
            memories.append({
                "id": mem_id,
                "text": chunk,
                "metadata": {
                    "id": mem_id,  # IMPORTANT for mapping in run_benchmark.py
                    "source": title,
                    "importance": 0.7,
                    "layer": "semantic"
                }
            })
            
            # Create a query for every 5th chunk
            if j % 5 == 0:
                queries.append({
                    "query": f"Describe the details mentioned about {title} in the context of part {j}.",
                    "expected_source_ids": [mem_id] # Fixed key name
                })

    benchmark_set = {
        "name": name,
        "description": f"Universal benchmark set from {name}",
        "version": "1.0",
        "memories": memories,
        "queries": queries
    }
    
    output_path = f"benchmarking/sets/{name}.yaml"
    with open(output_path, 'w') as f:
        yaml.dump(benchmark_set, f)
    print(f"Created benchmark set: {output_path} with {len(memories)} memories.")

with open('docs/RAE-arxiv.txt', 'r') as f:
    rae_text = f.read()

source_texts = {
    "RAE_Technical_Paper": rae_text
}

if __name__ == "__main__":
    if not os.path.exists('benchmarking/sets'):
        os.makedirs('benchmarking/sets')
    create_benchmark_set("universal_rae_paper", source_texts)
