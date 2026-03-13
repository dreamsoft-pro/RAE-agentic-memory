"""
Generates a Gold Standard Benchmark file.
"""
import yaml
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from benchmarking.scripts.industrial_factory import IndustrialFactory

def main(count: int, output_file: str):
    factory = IndustrialFactory()
    print(f"🏭 Generating Gold Standard with {count} memories...")
    data = factory.generate_benchmark_set(count)
    
    with open(output_file, "w") as f:
        yaml.dump(data, f, sort_keys=False)
    
    print(f"✨ Saved to {output_file}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=1000)
    parser.add_argument("--output", type=str, default="benchmarking/sets/gold_standard_1k.yaml")
    args = parser.parse_args()
    main(args.count, args.output)
