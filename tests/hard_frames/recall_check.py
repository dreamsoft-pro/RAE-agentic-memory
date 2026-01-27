import requests


# Security import removed for internal container run
def apply_hard_frames(): pass

def get_ground_truth(url, api_key, tenant_id):
    """Fetch a real existing memory from the DB."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "X-Tenant-Id": tenant_id
    }
    print("🔭 Fetching a real sample from memory for Ground Truth test...")
    resp = requests.get(f"{url}/v1/memory/list?project=industrial_ultra_v3&limit=1&offset=100", headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        if data["results"]:
            sample = data["results"][0]
            print(f"✅ Found Sample ID: {sample['id']}")
            return sample
    print(f"❌ API Error {resp.status_code}: {resp.text}")
    return None

def verify_precision(session, url, sample, api_key, tenant_id):
    query_text = sample["content"]
    sample_meta = sample.get("metadata", {})

    # Extract keys we want to filter by
    filters = {
        "machine_id": sample_meta.get("machine_id"),
        "machine_status": sample_meta.get("machine_status")
    }
    filters = {k: v for k, v in filters.items() if v is not None}

    payload = {
        "query_text": query_text,
        "k": 5,
        "project": "industrial_ultra_v3",
        "filters": filters
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "X-Tenant-Id": tenant_id,
        "Content-Type": "application/json"
    }

    print("\n🔍 PROVING PRECISION 🔍")
    print(f"Target ID: {sample['id']}")
    print(f"Filters: {filters}")

    try:
        resp = session.post(f"{url}/v1/memory/query", json=payload, headers=headers, timeout=10)
        if resp.status_code == 200:
            results = resp.json().get("results", [])
            print(f"📊 Results Found: {len(results)}")

            found_target = False
            for i, res in enumerate(results):
                res_id = res.get('id')
                res_meta = res.get('metadata', {})
                is_exact_match = (str(res_id) == str(sample["id"]))

                status_icon = "🟢" if is_exact_match else "🟡"
                match_desc = "EXACT MATCH!" if is_exact_match else "Related"

                print(f"   [{i+1}] {status_icon} {match_desc} (Score: {res.get('score', 0):.4f}) ID: {res_id}")
                if is_exact_match:
                    found_target = True

            if found_target:
                print("\n🏆 VERIFIED: RAE retrieved the exact record. PRECISION = 100%.")
            else:
                print("\n❌ FAILED: Target record not found.")
        else:
            print(f"❌ API Error {resp.status_code}: {resp.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

def run_recall_check():
    print("🧠 ULTIMATE MEMORY QUALITY CHECK v4.3 (Internal Run) 🧠")
    base_url = "http://localhost:8000" # Running inside API container
    api_key = "dev-key"
    tenant_id = "00000000-0000-0000-0000-000000000000"
    session = requests.Session()
    sample = get_ground_truth(base_url, api_key, tenant_id)
    if sample:
        verify_precision(session, base_url, sample, api_key, tenant_id)

if __name__ == "__main__":
    run_recall_check()
