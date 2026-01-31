import yaml
import random
import argparse
from datetime import datetime, timedelta

def generate_benchmark(count, output_file):
    name = f"industrial_{count // 1000}k"
    description = f"Large-scale industrial benchmark with {count} memories simulating real-world production data"
    
    memories = []
    
    # Templates for generation
    types = ["bug", "feature", "question", "improvement"]
    priorities = ["low", "medium", "high", "critical"]
    statuses = ["open", "in_progress", "resolved", "closed"]
    components = ["api", "authentication", "database", "reporting", "dashboard", "deployment", "monitoring"]
    sources = ["Support System", "Monitoring System", "System Logs", "Incident Management", "Technical Documentation"]
    services = ["auth-service", "api-gateway", "db-cluster", "ml-inference", "cache-layer", "payment-gateway"]
    levels = ["INFO", "DEBUG", "WARN", "ERROR", "CRITICAL"]
    
    start_date = datetime(2024, 1, 1)
    
    # Store some specific IDs for queries
    critical_incidents = []
    high_disk_io_metrics = []
    documentation_ids = []
    
    for i in range(count):
        m_type = random.choice(["ticket", "metric", "log", "incident", "doc"])
        timestamp = (start_date + timedelta(minutes=i*5)).isoformat()
        
        m_id = f"{m_type}_{i:06d}"
        
        if m_type == "ticket":
            t_type = random.choice(types)
            prio = random.choice(priorities)
            comp = random.choice(components)
            status = random.choice(statuses)
            text = f"[{t_type.upper()}] {comp}: {random.choice(['intermittent failures', 'unable to access feature', 'slow response times', 'incorrect data displayed', 'timeout errors'])} - Priority: {prio}, Status: {status}"
            
            memory = {
                "id": m_id,
                "text": text,
                "tags": ["ticket", t_type, prio],
                "metadata": {
                    "source": "Support System",
                    "importance": 0.3 if prio == "low" else 0.5 if prio == "medium" else 0.8 if prio == "high" else 0.95,
                    "timestamp": timestamp,
                    "type": t_type,
                    "priority": prio,
                    "component": comp
                }
            }
        elif m_type == "metric":
            metric_type = random.choice(["requests", "cpu_usage", "memory", "network", "disk_io"])
            val = random.randint(10, 99)
            srv = f"srv-{random.randint(1, 99):02d}"
            text = f"Metric {metric_type} on {srv}: {val}% at {timestamp[11:16]}"
            
            if metric_type == "disk_io" and val > 80:
                high_disk_io_metrics.append(m_id)
                
            memory = {
                "id": m_id,
                "text": text,
                "tags": ["metric", metric_type, srv],
                "metadata": {
                    "source": "Monitoring System",
                    "importance": 0.5 if val < 80 else 0.95,
                    "timestamp": timestamp,
                    "server_id": srv,
                    "metric_type": metric_type,
                    "value": val
                }
            }
        elif m_type == "log":
            svc = random.choice(services)
            lvl = random.choice(levels)
            text = f"{svc} - {lvl}: {random.choice(['Memory usage: 981MB', 'Cache hit rate: 96%', 'Request processed in 473ms', 'Queue depth: 71 messages', 'Connection pool size: 31'])}"
            
            memory = {
                "id": m_id,
                "text": text,
                "tags": ["log", lvl.lower(), svc],
                "metadata": {
                    "source": "System Logs",
                    "importance": 0.3 if lvl == "INFO" else 0.9,
                    "timestamp": timestamp,
                    "service": svc,
                    "level": lvl
                }
            }
        elif m_type == "incident":
            sev = random.choice(["sev1", "sev2", "sev3", "sev4"])
            comp = random.choice(components + services)
            users = random.randint(100, 10000)
            dur = random.randint(10, 300)
            text = f"[{sev.upper()}] Incident #{i}: {comp} outage for {dur} minutes, {users} users affected"
            
            if sev in ["sev1", "sev2"]:
                critical_incidents.append(m_id)
                
            memory = {
                "id": m_id,
                "text": text,
                "tags": ["incident", sev, comp],
                "metadata": {
                    "source": "Incident Management",
                    "importance": 0.4 if sev == "sev4" else 0.6 if sev == "sev3" else 0.85 if sev == "sev2" else 0.99,
                    "timestamp": timestamp,
                    "severity": sev,
                    "duration_minutes": dur,
                    "affected_users": users
                }
            }
        else: # doc
            comp = random.choice(components + ["architecture", "deployment", "troubleshooting"])
            method = random.choice(["GET", "POST", "PUT", "DELETE"])
            text = f"Documentation ({comp}): API endpoint /{random.choice(['auth', 'users', 'posts', 'comments', 'metrics', 'database'])} - {method} method"
            
            documentation_ids.append(m_id)
            
            memory = {
                "id": m_id,
                "text": text,
                "tags": ["documentation", comp, "api"],
                "metadata": {
                    "source": "Technical Documentation",
                    "importance": 0.7,
                    "type": comp
                }
            }
        
        memories.append(memory)

    # Select limited number of expected IDs for queries to keep YAML readable
    queries = [
        {
            "query": "Find all API documentation",
            "expected_source_ids": random.sample(documentation_ids, min(50, len(documentation_ids))),
            "difficulty": "hard",
            "category": "documentation"
        },
        {
            "query": "Show critical incidents",
            "expected_source_ids": random.sample(critical_incidents, min(10, len(critical_incidents))) if critical_incidents else [],
            "difficulty": "medium",
            "category": "incidents"
        },
        {
            "query": "What servers have high disk_io?",
            "expected_source_ids": random.sample(high_disk_io_metrics, min(40, len(high_disk_io_metrics))) if high_disk_io_metrics else [],
            "difficulty": "hard",
            "category": "metrics"
        }
    ]
    
    config = {
        "top_k": 10,
        "min_relevance_score": 0.25,
        "enable_reranking": True,
        "enable_reflection": True,
        "enable_graph": True,
        "test_scale": True,
        "test_performance": True
    }
    
    benchmark = {
        "name": name,
        "description": description,
        "version": "1.0",
        "memories": memories,
        "queries": queries,
        "config": config
    }
    
    with open(output_file, 'w') as f:
        yaml.dump(benchmark, f, sort_keys=False)
    
    print(f"✅ Generated {count} memories to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate large-scale industrial benchmark")
    parser.add_argument("--count", type=int, required=True, help="Number of memories to generate")
    parser.add_argument("--output", type=str, required=True, help="Output YAML file")
    args = parser.parse_args()
    generate_benchmark(args.count, args.output)
