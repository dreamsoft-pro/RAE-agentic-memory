#!/usr/bin/env python3
"""
RAE Demo Data Seeding Script
Seeds RAE with sample memories for the fictional "Project Phoenix" scenario.

This script demonstrates RAE's multi-layer memory architecture and knowledge graph capabilities.

Usage:
    python3 scripts/seed_demo_data.py

Requirements:
    pip install httpx (or use system Python with httpx installed)
"""

import sys
import time
from typing import List, Dict, Any

try:
    import httpx
except ImportError:
    print("ERROR: httpx library not found")
    print("Install it with: pip install httpx")
    sys.exit(1)


# Configuration
RAE_API_URL = "http://localhost:8000"
TENANT_ID = "demo-tenant"
PROJECT_ID = "phoenix-project"

# Demo memories representing a software project lifecycle
DEMO_MEMORIES = [
    {
        "content": "Project Phoenix kickoff meeting held on 2024-01-15. Team decided to build a cloud-native microservices platform for real-time data processing. Key stakeholders: Alice (Tech Lead), Bob (Product Manager), Charlie (DevOps).",
        "layer": "em",  # Episodic Memory
        "tags": ["meeting", "kickoff", "planning"],
        "source": "meeting-notes",
        "importance": 0.9
    },
    {
        "content": "Alice proposed using Kafka for event streaming and PostgreSQL for persistent storage. The team agreed on this architecture after comparing it with Redis Streams and MongoDB alternatives.",
        "layer": "em",
        "tags": ["architecture", "decision", "kafka", "postgresql"],
        "source": "technical-discussion",
        "importance": 0.95
    },
    {
        "content": "Bug #PX-42 reported by QA team: Authentication service crashes when handling concurrent requests above 100 RPS. The issue is related to connection pool exhaustion in the database layer.",
        "layer": "em",
        "tags": ["bug", "authentication", "performance"],
        "source": "bug-tracker",
        "importance": 0.85
    },
    {
        "content": "Charlie implemented horizontal auto-scaling for the authentication service using Kubernetes HPA. The service now handles 500 RPS without issues. Bug #PX-42 resolved.",
        "layer": "em",
        "tags": ["fix", "kubernetes", "performance", "devops"],
        "source": "git-commit",
        "importance": 0.9
    },
    {
        "content": "The authentication service depends on the user-profile-service for JWT token validation. This dependency was added in release v2.3.0 to centralize user management.",
        "layer": "sm",  # Semantic Memory - Structured knowledge
        "tags": ["architecture", "dependencies", "authentication"],
        "source": "architecture-docs",
        "importance": 0.8
    },
    {
        "content": "Sprint retrospective insight: The team needs to improve test coverage for edge cases. Multiple bugs were found in production that could have been caught with better integration tests.",
        "layer": "rm",  # Reflective Memory - Insights and patterns
        "tags": ["retrospective", "testing", "quality"],
        "source": "team-reflection",
        "importance": 0.75
    },
    {
        "content": "Product roadmap Q2 2024: Priority features include OAuth2 integration, multi-tenant support, and advanced analytics dashboard. Bob estimates 8 weeks for completion.",
        "layer": "em",
        "tags": ["roadmap", "planning", "features"],
        "source": "product-planning",
        "importance": 0.7
    },
    {
        "content": "Best practice established: All microservices must implement structured logging with correlation IDs for distributed tracing. This pattern significantly improved debugging time during the last incident.",
        "layer": "sm",
        "tags": ["best-practice", "logging", "observability"],
        "source": "engineering-standards",
        "importance": 0.85
    },
    {
        "content": "Alice and Bob discussed the trade-offs between gRPC and REST for inter-service communication. They decided on REST for external APIs and gRPC for internal services to balance developer experience and performance.",
        "layer": "em",
        "tags": ["architecture", "discussion", "grpc", "rest"],
        "source": "technical-discussion",
        "importance": 0.8
    },
    {
        "content": "Meta-insight: When making architectural decisions, the team tends to prioritize developer experience over raw performance, unless performance becomes a proven bottleneck. This philosophy has led to faster iteration cycles.",
        "layer": "rm",
        "tags": ["meta-learning", "philosophy", "decision-making"],
        "source": "pattern-analysis",
        "importance": 0.9
    }
]


def check_rae_health() -> bool:
    """Check if RAE API is healthy and reachable."""
    try:
        response = httpx.get(f"{RAE_API_URL}/health", timeout=5.0)
        return response.status_code == 200
    except Exception as e:
        return False


def create_memory(client: httpx.Client, memory_data: Dict[str, Any]) -> bool:
    """Create a single memory in RAE."""
    try:
        # Add tenant_id and project to memory data
        payload = {
            "tenant_id": TENANT_ID,
            "project": PROJECT_ID,
            **memory_data
        }

        response = client.post(
            f"{RAE_API_URL}/v1/memories",
            json=payload,
            timeout=10.0
        )

        if response.status_code in [200, 201]:
            return True
        else:
            print(f"   WARNING: Failed to create memory (status {response.status_code})")
            print(f"   Response: {response.text[:200]}")
            return False

    except Exception as e:
        print(f"   ERROR: {str(e)}")
        return False


def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("  RAE Demo Data Seeding Script")
    print("  Project: Phoenix (Fictional Software Project)")
    print("="*60 + "\n")

    # Step 1: Check RAE health
    print(f"[1/3] Checking RAE API health at {RAE_API_URL}...")
    if not check_rae_health():
        print("❌ ERROR: RAE API is not reachable or unhealthy")
        print("\nPlease ensure RAE is running:")
        print("  docker-compose ps")
        print("  docker-compose logs rae-api")
        print("\nOr run: ./scripts/quickstart.sh")
        sys.exit(1)

    print("✅ RAE API is healthy\n")

    # Step 2: Seed memories
    print(f"[2/3] Seeding {len(DEMO_MEMORIES)} demo memories...")
    print(f"      Tenant: {TENANT_ID}")
    print(f"      Project: {PROJECT_ID}\n")

    success_count = 0
    failed_count = 0

    with httpx.Client() as client:
        for i, memory in enumerate(DEMO_MEMORIES, 1):
            layer_emoji = {
                "em": "📝",  # Episodic
                "sm": "📚",  # Semantic
                "rm": "💡"   # Reflective
            }.get(memory["layer"], "📄")

            print(f"{layer_emoji} [{i}/{len(DEMO_MEMORIES)}] {memory['layer'].upper()}: {memory['content'][:70]}...")

            if create_memory(client, memory):
                success_count += 1
                print("   ✅ Created")
            else:
                failed_count += 1
                print("   ❌ Failed")

            # Small delay to avoid overwhelming the API
            time.sleep(0.1)

    print()

    # Step 3: Summary
    print(f"[3/3] Summary:")
    print(f"      ✅ Successfully created: {success_count}/{len(DEMO_MEMORIES)} memories")

    if failed_count > 0:
        print(f"      ❌ Failed: {failed_count}/{len(DEMO_MEMORIES)} memories")

    # Step 4: Next steps
    print("\n" + "="*60)
    print("  Demo data seeded successfully! 🎉")
    print("="*60)
    print("\n💡 Try these queries to explore the data:\n")

    print("1. View all memories:")
    print(f"   curl http://localhost:8000/v1/memories?tenant_id={TENANT_ID}&project={PROJECT_ID}\n")

    print("2. Search for authentication-related memories:")
    print(f"   curl -X POST http://localhost:8000/v1/search \\")
    print(f'     -H "Content-Type: application/json" \\')
    print(f'     -d \'{{"query": "authentication bug", "tenant_id": "{TENANT_ID}", "project": "{PROJECT_ID}"}}\'\n')

    print("3. Explore the knowledge graph:")
    print(f"   curl http://localhost:8000/v1/graph/nodes?tenant_id={TENANT_ID}&project={PROJECT_ID}\n")

    print("4. Open the Dashboard:")
    print("   http://localhost:8501\n")

    print("5. Explore the API:")
    print("   http://localhost:8000/docs\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Seeding interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)
