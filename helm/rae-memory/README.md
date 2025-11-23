# RAE Memory Engine - Helm Chart

Enterprise-grade Kubernetes deployment for RAE (Reflective Agentic Memory Engine).

## Prerequisites

- Kubernetes 1.23+
- Helm 3.8+
- PersistentVolume provisioner support in the underlying infrastructure
- LoadBalancer support (or Ingress controller)

## Installing the Chart

```bash
# Add Helm repository (if published)
helm repo add rae https://charts.rae.memory

# Create namespace
kubectl create namespace rae-memory

# Create secrets
kubectl create secret generic rae-secrets \
  --from-literal=database-url='postgresql://user:pass@postgres:5432/rae' \
  --from-literal=redis-url='redis://:pass@redis:6379/0' \
  --from-literal=openai-api-key='sk-...' \
  --from-literal=anthropic-api-key='sk-ant-...' \
  -n rae-memory

# Install chart
helm install rae-memory ./helm/rae-memory \
  --namespace rae-memory \
  --values custom-values.yaml
```

## Configuration

### Core Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `memoryApi.replicaCount` | Number of API replicas | `2` |
| `memoryApi.resources.requests.memory` | API memory request | `1Gi` |
| `memoryApi.resources.requests.cpu` | API CPU request | `500m` |
| `memoryApi.autoscaling.enabled` | Enable HPA | `true` |
| `memoryApi.autoscaling.minReplicas` | Min replicas | `2` |
| `memoryApi.autoscaling.maxReplicas` | Max replicas | `10` |

### ML Service Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `mlService.replicaCount` | Number of ML service replicas | `2` |
| `mlService.resources.requests.memory` | ML memory request | `2Gi` |
| `mlService.resources.requests.cpu` | ML CPU request | `1000m` |

### Database Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `postgresql.enabled` | Deploy PostgreSQL | `true` |
| `postgresql.auth.username` | PostgreSQL username | `rae` |
| `postgresql.primary.persistence.size` | PostgreSQL volume size | `20Gi` |

### Redis Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `redis.enabled` | Deploy Redis | `true` |
| `redis.auth.enabled` | Enable Redis auth | `true` |
| `redis.master.persistence.size` | Redis volume size | `8Gi` |

### Qdrant Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `qdrant.enabled` | Deploy Qdrant | `true` |
| `qdrant.persistence.size` | Qdrant volume size | `50Gi` |

### Ingress Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `ingress.enabled` | Enable ingress | `true` |
| `ingress.className` | Ingress class | `nginx` |
| `ingress.hosts[0].host` | API hostname | `rae-api.example.com` |

## Example Values Files

### Production Configuration

```yaml
# production-values.yaml
memoryApi:
  replicaCount: 5
  resources:
    limits:
      cpu: 2000m
      memory: 4Gi
    requests:
      cpu: 1000m
      memory: 2Gi
  autoscaling:
    enabled: true
    minReplicas: 5
    maxReplicas: 20
    targetCPUUtilizationPercentage: 60

mlService:
  replicaCount: 3
  resources:
    limits:
      cpu: 4000m
      memory: 8Gi
    requests:
      cpu: 2000m
      memory: 4Gi

postgresql:
  primary:
    persistence:
      size: 100Gi
    resources:
      limits:
        memory: 4Gi
        cpu: 2000m

qdrant:
  persistence:
    size: 200Gi
  resources:
    limits:
      memory: 8Gi
      cpu: 4000m

ingress:
  enabled: true
  className: "nginx"
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/rate-limit: "1000"
  hosts:
    - host: api.rae.prod.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: rae-prod-tls
      hosts:
        - api.rae.prod.example.com
```

### Development Configuration

```yaml
# dev-values.yaml
memoryApi:
  replicaCount: 1
  resources:
    limits:
      cpu: 500m
      memory: 1Gi
    requests:
      cpu: 250m
      memory: 512Mi
  autoscaling:
    enabled: false

mlService:
  replicaCount: 1

postgresql:
  primary:
    persistence:
      size: 10Gi

redis:
  master:
    persistence:
      size: 2Gi

qdrant:
  persistence:
    size: 10Gi

ingress:
  enabled: true
  className: "nginx"
  hosts:
    - host: rae-dev.local
      paths:
        - path: /
          pathType: Prefix
  tls: []
```

## Upgrading

```bash
# Upgrade to new version
helm upgrade rae-memory ./helm/rae-memory \
  --namespace rae-memory \
  --values custom-values.yaml

# Rollback if needed
helm rollback rae-memory 1 -n rae-memory
```

## Uninstalling

```bash
# Uninstall release
helm uninstall rae-memory -n rae-memory

# Delete namespace
kubectl delete namespace rae-memory
```

## Monitoring

The chart includes ServiceMonitor for Prometheus:

```bash
# Enable monitoring
helm install rae-memory ./helm/rae-memory \
  --set monitoring.enabled=true \
  --set monitoring.serviceMonitor.enabled=true
```

## Security

### Network Policies

Enable network policies to restrict traffic:

```yaml
networkPolicy:
  enabled: true
```

### Pod Security

The chart enforces:
- Non-root user (UID 1000)
- Read-only root filesystem
- No privilege escalation
- Dropped capabilities

## Troubleshooting

### Check Pod Status

```bash
kubectl get pods -n rae-memory
kubectl logs -f deployment/rae-memory-api -n rae-memory
```

### Check Service Connectivity

```bash
kubectl port-forward svc/rae-memory-api 8000:8000 -n rae-memory
curl http://localhost:8000/health
```

### Database Issues

```bash
# Check PostgreSQL
kubectl exec -it deployment/rae-memory-postgresql -n rae-memory -- psql -U rae -d rae_memory

# Check Redis
kubectl exec -it deployment/rae-memory-redis-master -n rae-memory -- redis-cli ping
```

## Support

- Documentation: https://github.com/dreamsoft-pro/RAE-agentic-memory/docs
- Issues: https://github.com/dreamsoft-pro/RAE-agentic-memory/issues
