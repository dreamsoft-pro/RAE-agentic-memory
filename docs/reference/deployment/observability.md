# Observability in RAE

The RAE Agentic Memory Engine is designed with observability in mind, providing metrics and tools to monitor its performance and behavior.

## Prometheus Metrics

RAE exposes a wide range of metrics in the Prometheus format. These metrics can be scraped by a Prometheus server to provide a time-series database of the system's performance.

The metrics endpoint is available at `/metrics` on the Memory API.

## Grafana Dashboard

The project includes a pre-configured Grafana dashboard that visualizes the most important metrics from the RAE API. This dashboard is located at `infra/grafana/rae-dashboard.json`.

To use the dashboard, you will need to:
1. Set up a Grafana instance.
2. Add a Prometheus data source that points to your Prometheus server.
3. Import the `rae-dashboard.json` dashboard into Grafana.

## Key Metrics

Some of the key metrics exposed by RAE include:

-   `rae_request_latency_seconds`: The latency of API requests.
-   `rae_cache_hits_total`: The total number of cache hits.
-   `rae_cache_misses_total`: The total number of cache misses.
-   `rae_llm_token_usage_total`: The total number of LLM tokens used.
-   `rae_llm_cost_total`: The estimated cost of LLM usage.

More detailed documentation on the available metrics will be added here in the future.
