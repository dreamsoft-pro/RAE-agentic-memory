
import json
import re

file_path = "docs/offline_data_19-01-2026.jsonl"

def inspect_file():
    print("Inspecting first 10 lines of", file_path)
    with open(file_path, 'r') as f:
        for i, line in enumerate(f):
            if i >= 10: break
            try:
                data = json.loads(line)
                metrics = data.get('metrics', {})
                pole_1 = metrics.get('pole_1', '')
                status = metrics.get('status', 'UNKNOWN')
                
                print(f"\n--- Line {i+1} (Status: {status}) ---")
                print(repr(pole_1))
                
                # Test Extraction Logic
                # Looking for: "193.69m)/h" or similar
                # Regex hypothesis: (\d+\.\d+)m)/h
                
                speed_match = re.search(r"(\d+\.\d+)\s*m)/h", pole_1)
                speed = float(speed_match.group(1)) if speed_match else None
                print(f" -> Extracted Speed: {speed}")

            except Exception as e:
                print(f"Error parsing line {i}: {e}")

if __name__ == "__main__":
    inspect_file()

