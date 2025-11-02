import typer, requests, os, json

app = typer.Typer(help="Gemini CLI proxy for Agentic Memory API")


def _api_url() -> str:
    return os.environ.get("MEMORY_API_URL", "http://localhost:8000")

@app.command()
def health():
    r = requests.get(f"{_api_url()}/health")
    print(r.json())

@app.command()
def memory_add(tenant: str, agent: str, type: str, content: str):
    payload = {
        "tenant_id": tenant, "agent_id": agent,
        "memory_type": type, "content": content
    }
    r = requests.post(f"{_api_url()}/memory/add", json=payload, headers={"X-Tenant-Id": tenant})
    print(r.json())

@app.command()
def memory_query(tenant: str, query: str, k: int = 50, k_final: int = 5):
    payload = {"tenant_id": tenant, "query_text": query, "k": k, "k_final": k_final}
    r = requests.post(f"{_api_url()}/memory/query", json=payload, headers={"X-Tenant-Id": tenant})
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))

@app.command()
def agent_ask(tenant: str, prompt: str, budget: int = 20000):
    payload = {"tenant_id": tenant, "prompt": prompt, "budget_tokens": budget}
    r = requests.post(f"{_api_url()}/agent/execute", json=payload, headers={"X-Tenant-Id": tenant})
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    app()
