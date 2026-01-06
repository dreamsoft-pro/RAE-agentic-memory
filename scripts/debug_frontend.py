target_path = "/home/grzegorz-lesniowski/cloud/screenwatcher_project/templates/dashboards/builder.html"

# I will inject a console.log into the fetch success handler to help debug in browser console
# and handle the case where data might be null more gracefully.

with open(target_path, "r") as f:
    content = f.read()

# Locate the fetch success block
fetch_block = ".then(res => {"
debug_block = """.then(res => {
                    console.log("API Response for " + type, res);
                    // DEBUG: If no data, alert once
                    if ((!res.data || res.data.length === 0) && !window.alerted_no_data) {
                        console.warn("No data for " + type + ". Meta:", res.meta);
                        // window.alerted_no_data = true; // Uncomment to spam alerts
                    }"""

if fetch_block in content:
    new_content = content.replace(fetch_block, debug_block)

    # Also fix potential issue with ECharts and ISO dates with microseconds
    # ECharts < 5.0 might struggle, but we included 5.4.3.
    # Let's explicitly parse date to timestamp in JS to be safe.

    map_fix_old = "data.map(d => [d.t, d.v])"
    map_fix_new = "data.map(d => [new Date(d.t).getTime(), d.v])"

    new_content = new_content.replace(map_fix_old, map_fix_new)

    with open(target_path, "w") as f:
        f.write(new_content)
    print("Injected JS debugging and date parsing fix to builder.html")
else:
    print("Could not find JS block to inject debug.")
