import sys

path = '/app/apps/dashboards/services/widget_data.py'
with open(path, 'r') as f:
    lines = f.readlines()

start_marker = "            # 2. Filter (RUNNING & > 0)"

# Find start index
start_idx = -1
for i, line in enumerate(lines):
    if start_marker in line:
        start_idx = i
        break

if start_idx == -1:
    print("Start marker not found")
    sys.exit(1)

# Find end index (looking for 'else:' aligned with 'if is_truejet:')
end_idx = -1
for i in range(start_idx, len(lines)):
    if "        else:" in lines[i]: # Standard indent for class method else
        end_idx = i
        break

if end_idx == -1:
    print("End marker not found")
    sys.exit(1)

print(f"Replacing lines {start_idx} to {end_idx}")

new_code = '''            # 2. Clean, Sort & Deduplicate
            # We must keep ALL points (even STOPPED) to correctly calculate duration of states.
            # Removing STOPPED points caused "bridging" of gaps, leading to inflated production.
            valid_data = []
            seen_ts = set()
            
            # Filter out complete garbage first
            clean_raw = []
            for d in raw_data:
                if d['status'] or d['speed'] is not None:
                    clean_raw.append(d)

            # Sort by TS first
            clean_raw.sort(key=lambda x: x['ts'])
            
            for d in clean_raw:
                # Skip exact timestamp duplicates
                if d['ts'] in seen_ts:
                    continue
                seen_ts.add(d['ts'])
                
                # Normalize
                d['status'] = str(d['status']).upper() if d['status'] else 'UNKNOWN'
                d['speed'] = d['speed'] or 0.0
                valid_data.append(d)
            
            sys.stderr.write(f"DEBUG: Valid data (timeline): {len(valid_data)}\n")
            
            if valid_data:
                # 3. Hampel Filter & Smoothing (Apply only to speeds, preserving 0s)
                speeds = [d['speed'] for d in valid_data]
                
                # Simple cleaning: if speed is crazy high (>2000), cap it or set to 0
                cleaned_speeds = []
                for s in speeds:
                    if s > 2000: cleaned_speeds.append(0) # Safety cap
                    else: cleaned_speeds.append(s)

                # 4. EMA Smoothing (light)
                smoothed_speeds = []
                alpha = 0.3
                ema = cleaned_speeds[0]
                for val in cleaned_speeds:
                    ema = alpha * val + (1 - alpha) * ema
                    smoothed_speeds.append(ema)

                # 5. Integration
                # Area = Speed (m2/h) * dt (h)
                # Logic: Production occurs ONLY during the interval starting with RUNNING
                
                MAX_GAP_SECONDS = 300.0 # Increased to 5 min

                for i in range(len(valid_data) - 1):
                    t1 = valid_data[i]['ts']
                    t2 = valid_data[i+1]['ts']
                    status = valid_data[i]['status']
                    
                    dt_seconds = (t2 - t1).total_seconds()
                    
                    # SAFETY CHECK
                    if dt_seconds > MAX_GAP_SECONDS:
                        continue 

                    # Only integrate if machine was RUNNING
                    if status == 'RUNNING':
                        dt_hours = dt_seconds / 3600.0
                        
                        speed_to_use = smoothed_speeds[i]
                        if speed_to_use < 0: speed_to_use = 0
                        
                        m2_inc = speed_to_use * dt_hours
                        total_production += m2_inc
                        
                        # Bucketing
                        ts_bucket = t1.replace(second=0, microsecond=0)
                        if bucket_minutes == 60:
                            ts_bucket = ts_bucket.replace(minute=0)
                        elif bucket_minutes == 1440:
                            ts_bucket = ts_bucket.replace(hour=0, minute=0)
                        
                        ts_str = ts_bucket.isoformat()
                        buckets[ts_str] = buckets.get(ts_str, 0.0) + m2_inc

'''

# Insert new code (with trailing newline)
new_lines = [l + '
' for l in new_code.split('
')]
final_lines = lines[:start_idx] + new_lines + lines[end_idx:]

with open(path, 'w') as f:
    f.writelines(final_lines)

print("SUCCESS: Patched logic")
