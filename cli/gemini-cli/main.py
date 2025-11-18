import typer, requests, os, json

app = typer.Typer(help="Gemini CLI proxy for Agentic Memory API")


def _api_url() -> str:
    return os.environ.get("MEMORY_API_URL", "http://localhost:8000")

@app.command()
def health():
    r = requests.get(f"{_api_url()}/health")
    print(r.json())

import sys

@app.command()
def memory_add(tenant: str, agent: str, type: str, content: str = typer.Option(None), file: typer.Optional[str] = None):
    if file:
        with open(file, "r") as f:
            payload = json.load(f)
    elif content:
        payload = {
            "tenant_id": tenant, "agent_id": agent,
            "memory_type": type, "content": content
        }
    else:
        payload = json.load(sys.stdin)

    r = requests.post(f"{_api_url()}/memory/add", json=payload, headers={"X-Tenant-Id": tenant})
    print(r.json())

@app.command()
def memory_query(tenant: str, query: str, k: int = 50, k_final: int = 5):
    payload = {"tenant_id": tenant, "query_text": query, "k": k, "k_final": k_final}
    r = requests.post(f"{_api_url()}/memory/query", json=payload, headers={"X-Tenant-Id": tenant})
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))

@app.command()
def agent_ask(tenant: str, prompt: str = typer.Option(None), file: typer.Optional[str] = None, budget: int = 20000):
    if file:
        with open(file, "r") as f:
            prompt_text = f.read()
    elif prompt:
        prompt_text = prompt
    else:
        prompt_text = sys.stdin.read()

    payload = {"tenant_id": tenant, "prompt": prompt_text, "budget_tokens": budget}
    r = requests.post(f"{_api_url()}/agent/execute", json=payload, headers={"X-Tenant-Id": tenant})
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    app()
