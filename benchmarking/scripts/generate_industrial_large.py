#!/usr/bin/env python3
"""
Generator for industrial_large.yaml benchmark dataset

Generates 1000-5000 memories with real-world patterns:
- Time-series data (logs, events, metrics)
- Duplicate/near-duplicate entries
- Evolving concepts
- Multi-domain knowledge

Usage:
    python generate_industrial_large.py --size 1000 --output ../sets/industrial_large.yaml
"""

import argparse
import random
from datetime import datetime, timedelta
from typing import Dict, List

import yaml


class IndustrialDataGenerator:
    """Generate realistic industrial benchmark data"""

    def __init__(self, seed: int = 42):
        random.seed(seed)
        self.domains = self._init_domains()
        self.base_date = datetime(2024, 1, 1)

    def _init_domains(self) -> Dict[str, Dict]:
        """Initialize domain-specific templates"""
        return {
            "logs": {
                "levels": ["INFO", "WARN", "ERROR", "CRITICAL", "DEBUG"],
                "services": [
                    "api-gateway",
                    "auth-service",
                    "db-cluster",
                    "cache-layer",
                    "ml-inference",
                ],
                "templates": [
                    "{service} - {level}: Request processed in {latency}ms",
                    "{service} - {level}: Connection pool size: {count}",
                    "{service} - {level}: Cache hit rate: {percent}%",
                    "{service} - {level}: Memory usage: {size}MB",
                    "{service} - {level}: Queue depth: {count} messages",
                ],
            },
            "tickets": {
                "types": ["bug", "feature", "improvement", "question"],
                "priorities": ["low", "medium", "high", "critical"],
                "statuses": ["open", "in_progress", "resolved", "closed"],
                "templates": [
                    "User reports {issue_type} with {component}: {description}",
                    "{issue_type} - {component} performance degradation: {metric}",
                    "Request for {feature} in {component} - priority: {priority}",
                ],
            },
            "metrics": {
                "types": ["cpu_usage", "memory", "disk_io", "network", "requests"],
                "templates": [
                    "Server {server_id}: {metric_type} at {value}% - timestamp {time}",
                    "Alert: {metric_type} exceeded threshold ({threshold}%) on {server_id}",
                ],
            },
            "documentation": {
                "types": ["api", "architecture", "deployment", "troubleshooting"],
                "templates": [
                    "API endpoint /{path} accepts {method} requests with {params} parameters",
                    "Architecture: {component} communicates with {other_component} via {protocol}",
                    "Deployment procedure for {service}: {steps}",
                    "Troubleshooting guide: {problem} - solution: {solution}",
                ],
            },
            "incidents": {
                "severities": ["sev1", "sev2", "sev3", "sev4"],
                "templates": [
                    "Incident {id}: {service} outage - duration: {duration} mins",
                    "{severity} incident: {description} - affected users: {count}",
                    "Post-mortem: {incident_type} caused by {root_cause}",
                ],
            },
        }

    def generate_log_entry(self, idx: int) -> Dict:
        """Generate a log entry memory"""
        domain = self.domains["logs"]
        level = random.choice(domain["levels"])
        service = random.choice(domain["services"])
        template = random.choice(domain["templates"])

        text = template.format(
            service=service,
            level=level,
            latency=random.randint(10, 500),
            count=random.randint(1, 100),
            percent=random.randint(50, 99),
            size=random.randint(100, 4000),
        )

        timestamp = self.base_date + timedelta(hours=idx)

        return {
            "id": f"log_{idx:04d}",
            "text": text,
            "tags": ["log", level.lower(), service],
            "metadata": {
                "source": "System Logs",
                "importance": 0.3
                if level == "INFO"
                else 0.6
                if level == "WARN"
                else 0.9,
                "timestamp": timestamp.isoformat(),
                "service": service,
                "level": level,
            },
        }

    def generate_ticket_entry(self, idx: int) -> Dict:
        """Generate a support ticket memory"""
        domain = self.domains["tickets"]
        ticket_type = random.choice(domain["types"])
        priority = random.choice(domain["priorities"])
        status = random.choice(domain["statuses"])

        components = ["dashboard", "api", "database", "authentication", "reporting"]
        component = random.choice(components)

        descriptions = [
            "slow response times",
            "intermittent failures",
            "incorrect data displayed",
            "timeout errors",
            "unable to access feature",
        ]

        text = f"[{ticket_type.upper()}] {component}: {random.choice(descriptions)} - Priority: {priority}, Status: {status}"

        timestamp = self.base_date + timedelta(hours=idx * 2)

        return {
            "id": f"ticket_{idx:04d}",
            "text": text,
            "tags": ["ticket", ticket_type, priority],
            "metadata": {
                "source": "Support System",
                "importance": {
                    "low": 0.3,
                    "medium": 0.5,
                    "high": 0.8,
                    "critical": 0.95,
                }[priority],
                "timestamp": timestamp.isoformat(),
                "type": ticket_type,
                "priority": priority,
                "component": component,
            },
        }

    def generate_metric_entry(self, idx: int) -> Dict:
        """Generate a metrics memory"""
        domain = self.domains["metrics"]
        metric_type = random.choice(domain["types"])
        server_id = f"srv-{random.randint(1, 50):02d}"

        value = random.randint(20, 95)
        timestamp = self.base_date + timedelta(minutes=idx * 5)

        text = f"Metric {metric_type} on {server_id}: {value}% at {timestamp.strftime('%H:%M')}"

        return {
            "id": f"metric_{idx:04d}",
            "text": text,
            "tags": ["metric", metric_type, server_id],
            "metadata": {
                "source": "Monitoring System",
                "importance": 0.5 if value < 70 else 0.8 if value < 90 else 0.95,
                "timestamp": timestamp.isoformat(),
                "server_id": server_id,
                "metric_type": metric_type,
                "value": value,
            },
        }

    def generate_doc_entry(self, idx: int) -> Dict:
        """Generate documentation memory"""
        domain = self.domains["documentation"]
        doc_type = random.choice(domain["types"])

        paths = ["users", "posts", "comments", "auth", "metrics"]
        methods = ["GET", "POST", "PUT", "DELETE"]

        text = f"Documentation ({doc_type}): API endpoint /{random.choice(paths)} - {random.choice(methods)} method"

        return {
            "id": f"doc_{idx:04d}",
            "text": text,
            "tags": ["documentation", doc_type, "api"],
            "metadata": {
                "source": "Technical Documentation",
                "importance": 0.7,
                "type": doc_type,
            },
        }

    def generate_incident_entry(self, idx: int) -> Dict:
        """Generate incident memory"""
        domain = self.domains["incidents"]
        severity = random.choice(domain["severities"])

        services = ["payment-gateway", "authentication", "database", "api-server"]
        service = random.choice(services)

        duration = random.randint(5, 240)
        affected_users = random.randint(10, 10000)

        text = f"[{severity.upper()}] Incident #{idx:04d}: {service} outage for {duration} minutes, {affected_users} users affected"

        timestamp = self.base_date + timedelta(days=idx // 10)

        return {
            "id": f"incident_{idx:04d}",
            "text": text,
            "tags": ["incident", severity, service],
            "metadata": {
                "source": "Incident Management",
                "importance": {"sev4": 0.4, "sev3": 0.6, "sev2": 0.85, "sev1": 0.99}[
                    severity
                ],
                "timestamp": timestamp.isoformat(),
                "severity": severity,
                "duration_minutes": duration,
                "affected_users": affected_users,
            },
        }

    def generate_memories(self, count: int) -> List[Dict]:
        """Generate mixed collection of memories"""
        memories = []

        # Distribution: 40% logs, 25% tickets, 20% metrics, 10% docs, 5% incidents
        distributions = [
            (0.40, self.generate_log_entry),
            (0.25, self.generate_ticket_entry),
            (0.20, self.generate_metric_entry),
            (0.10, self.generate_doc_entry),
            (0.05, self.generate_incident_entry),
        ]

        for idx in range(count):
            rand = random.random()
            cumulative = 0
            for threshold, generator in distributions:
                cumulative += threshold
                if rand < cumulative:
                    memories.append(generator(idx))
                    break

        return memories

    def generate_queries(self, num_queries: int, memories: List[Dict]) -> List[Dict]:
        """Generate queries based on memories"""
        queries = []

        # Sample different types of queries
        query_templates = [
            {
                "template": "What {service} issues occurred?",
                "filter_tag": "log",
                "category": "service_issues",
            },
            {
                "template": "Show critical incidents",
                "filter_tag": "incident",
                "category": "incidents",
            },
            {
                "template": "What are high priority tickets?",
                "filter_tag": "ticket",
                "category": "tickets",
            },
            {
                "template": "What servers have high {metric}?",
                "filter_tag": "metric",
                "category": "metrics",
            },
            {
                "template": "Find documentation about {component}",
                "filter_tag": "documentation",
                "category": "documentation",
            },
        ]

        for idx in range(num_queries):
            template_info = random.choice(query_templates)
            template = template_info["template"]

            # Generate query text
            query_text = template.format(
                service=random.choice(["api-gateway", "auth-service", "database"]),
                metric=random.choice(["cpu_usage", "memory", "disk_io"]),
                component=random.choice(["API", "authentication", "database"]),
            )

            # Find relevant memories
            filter_tag = template_info["filter_tag"]
            relevant_memories = [m for m in memories if filter_tag in m["tags"]]

            # Sample some as expected results
            num_expected = min(random.randint(1, 3), len(relevant_memories))
            expected = (
                random.sample(relevant_memories, num_expected)
                if relevant_memories
                else []
            )
            expected_ids = [m["id"] for m in expected]

            difficulty = (
                "easy"
                if num_expected <= 1
                else "medium"
                if num_expected <= 2
                else "hard"
            )

            queries.append(
                {
                    "query": query_text,
                    "expected_source_ids": expected_ids,
                    "difficulty": difficulty,
                    "category": template_info["category"],
                }
            )

        return queries


def main():
    parser = argparse.ArgumentParser(
        description="Generate industrial_large.yaml benchmark"
    )
    parser.add_argument(
        "--size", type=int, default=1000, help="Number of memories to generate"
    )
    parser.add_argument(
        "--queries", type=int, default=100, help="Number of queries to generate"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="../sets/industrial_large.yaml",
        help="Output file path",
    )
    parser.add_argument(
        "--seed", type=int, default=42, help="Random seed for reproducibility"
    )

    args = parser.parse_args()

    print("🏭 Generating Industrial Large Benchmark")
    print(f"   Memories: {args.size}")
    print(f"   Queries: {args.queries}")
    print(f"   Output: {args.output}")

    generator = IndustrialDataGenerator(seed=args.seed)

    print("\n📝 Generating memories...")
    memories = generator.generate_memories(args.size)

    print("🔍 Generating queries...")
    queries = generator.generate_queries(args.queries, memories)

    # Create benchmark structure
    benchmark = {
        "name": "industrial_large",
        "description": f"Large-scale industrial benchmark with {args.size} memories simulating real-world production data",
        "version": "1.0",
        "memories": memories,
        "queries": queries,
        "config": {
            "top_k": 10,
            "min_relevance_score": 0.25,
            "enable_reranking": True,
            "enable_reflection": True,
            "enable_graph": True,
            "test_scale": True,
            "test_performance": True,
        },
    }

    # Write to YAML
    print(f"\n💾 Writing to {args.output}...")
    with open(args.output, "w") as f:
        yaml.dump(
            benchmark, f, default_flow_style=False, allow_unicode=True, sort_keys=False
        )

    print("\n✅ Generated successfully!")
    print(f"   Total memories: {len(memories)}")
    print(f"   Total queries: {len(queries)}")
    print(f"   File size: {len(yaml.dump(benchmark)) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
