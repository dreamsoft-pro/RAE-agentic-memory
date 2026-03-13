from elasticsearch import Elasticsearch
import os

# Configuration for Elasticsearch client
# Host is 'elasticsearch' as defined in docker-compose.yml
# Use environment variables for production readiness
ES_HOST = os.getenv("ELASTICSEARCH_HOST", "localhost")
ES_PORT = os.getenv("ELASTICSEARCH_PORT", 9200)
ES_CLOUD_ID = os.getenv("ELASTIC_CLOUD_ID")
ES_API_KEY = os.getenv("ELASTIC_API_KEY") # Base64 encoded API key
ES_USERNAME = os.getenv("ELASTIC_USERNAME")
ES_PASSWORD = os.getenv("ELASTIC_PASSWORD")

# Initialize Elasticsearch client
# For local development with xpack.security.enabled=false
# just connect to the host and port.
# For a secured setup, use cloud_id and api_key or username/password
try:
    if ES_CLOUD_ID and ES_API_KEY:
        es_client = Elasticsearch(
            cloud_id=ES_CLOUD_ID,
            api_key=ES_API_KEY,
        )
    elif ES_USERNAME and ES_PASSWORD:
        es_client = Elasticsearch(
            hosts=[{"host": ES_HOST, "port": ES_PORT, "scheme": "http"}],
            basic_auth=(ES_USERNAME, ES_PASSWORD),
        )
    else:
        es_client = Elasticsearch(
            hosts=[{"host": ES_HOST, "port": ES_PORT, "scheme": "http"}],
            verify_certs=False,
            ssl_show_warn=False
        )
    
    # Test connection (temporarily commented out for debugging connection issues)
    # if not es_client.ping():
    #    raise ValueError("Connection to Elasticsearch failed!")
    print(f"Attempting to connect to Elasticsearch. Client info (if connected): {es_client.info()}")

except Exception as e:
    print(f"Failed to connect to Elasticsearch: {e}")
    es_client = None # Set to None if connection fails
