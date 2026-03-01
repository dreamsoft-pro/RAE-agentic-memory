import sys

target_path = '/app/apps/dashboards/services/widget_data.py'
new_code_path = '/app/new_provider_code.txt'

with open(target_path, 'r') as f:
    target_lines = f.readlines()

with open(new_code_path, 'r') as f:
    new_code = f.read()

# Find start and end of ProductionTrendProvider class
start_idx = -1
end_idx = -1

for i, line in enumerate(target_lines):
    if line.strip().startswith("class ProductionTrendProvider(BaseWidgetProvider):"):
        start_idx = i
        break

if start_idx == -1:
    print("Start not found")
    sys.exit(1)

# Find start of next class
for i in range(start_idx + 1, len(target_lines)):
    if line.strip().startswith("class ") and "(BaseWidgetProvider):" in target_lines[i]:
        end_idx = i
        break

if end_idx == -1:
    print("End not found")
    sys.exit(1)

print(f"Replacing lines {start_idx} to {end_idx}")

final_lines = target_lines[:start_idx] + [new_code + '
'] + target_lines[end_idx:]

with open(target_path, 'w') as f:
    f.writelines(final_lines)

print("SUCCESS")
