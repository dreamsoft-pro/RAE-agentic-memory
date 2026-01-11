target_path = (
    "/home/grzegorz-lesniowski/cloud/screenwatcher_project/apps/dashboards/views.py"
)

with open(target_path, "r") as f:
    content = f.read()

# Replace the logic block for 'speed' extraction
old_logic = """            if metric == 'speed':
                metrics = pl.get('metrics', {})
                val = metrics.get('parts_delta', 0)"""

new_logic = """            if metric == 'speed':
                metrics = pl.get('metrics', {})
                # Prefer explicit speed metric, fallback to parts_delta * 60 (dummy calc)
                if 'speed' in metrics:
                    val = metrics['speed']
                else:
                    val = metrics.get('parts_delta', 0)"""

if old_logic in content:
    new_content = content.replace(old_logic, new_logic)
    with open(target_path, "w") as f:
        f.write(new_content)
    print("Fixed speed metric extraction logic in views.py")
else:
    print("Could not find exact logic block to replace. Check indentation or content.")
