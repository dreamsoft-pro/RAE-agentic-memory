
import json
import requests
import sys

def import_dashboard(file_path):
    grafana_url = "http://localhost:3000/api/dashboards/db"
    
    with open(file_path, 'r') as f:
        dashboard_data = json.load(f)
    
    # Wrap in the required structure
    payload = {
        "dashboard": dashboard_data,
        "overwrite": True
    }
    
    response = requests.post(grafana_url, json=payload)
    
    if response.status_code == 200:
        print(f"Successfully imported dashboard: {dashboard_data.get('title')}")
        print(response.json())
    else:
        print(f"Failed to import dashboard. Status: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    import_dashboard("docs/grafana_dashboard_tj02_v6.json")
