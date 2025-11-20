# API Reference

The RAE Agentic Memory API is built using FastAPI, which provides automatic, interactive API documentation. This is the best way to explore the available endpoints, their parameters, and their responses.

## Interactive Documentation

Once you have the Memory API running, you can access the interactive documentation in your browser at one of the following URLs:

-   **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
-   **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Swagger UI

Swagger UI provides a rich, interactive interface where you can not only browse the API but also make live requests to the endpoints. You can fill in parameters, specify headers (like `X-Tenant-Id`), and see the actual responses from the running server.

![Swagger UI Example](httpsimage.png)  <!-- Placeholder for an image of the Swagger UI -->

### ReDoc

ReDoc offers a clean, three-panel view of the API documentation. It's less interactive than Swagger but is often preferred for its clear and readable layout.

## OpenAPI Specification

The underlying OpenAPI 3.0 specification is available at `/openapi.json`. You can use this JSON file to generate clients in various programming languages or import it into other API tools.

-   **OpenAPI Spec**: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)