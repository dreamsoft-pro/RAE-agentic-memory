openapi: 3.0.3
info:
  title: Agentic Memory API
  version: "0.1"
paths:
  /health:
    get:
      responses: { "200": { "description": "ok" } }

  /memory/add:
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AddMemoryRequest'
      responses:
        "200": { description: "added", content: { application/json: { schema: { $ref: '#/components/schemas/AddMemoryResponse' } } } }

  /memory/query:
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: '#/components/schemas/QueryRequest' }
      responses:
        "200": { description: "results", content: { application/json: { schema: { $ref: '#/components/schemas/QueryResponse' } } } }

  /agent/execute:
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: '#/components/schemas/AgentExecuteRequest' }
      responses:
        "200": { description: "answer", content: { application/json: { schema: { $ref: '#/components/schemas/AgentExecuteResponse' } } } }

  /memory/timeline:
    get:
      parameters:
        - in: query
          name: start_date
          schema: { type: string }
        - in: query
          name: end_date
          schema: { type: string }
        - in: query
          name: limit
          schema: { type: integer, default: 100 }
      responses:
        "200": { description: "timeline", content: { application/json: { schema: { $ref: '#/components/schemas/TimelineResponse' } } } }

components:
  schemas:
    MemoryType:
      type: string
      enum: [episodic, semantic, procedural]

    AddMemoryRequest:
      type: object
      required: [tenant_id, agent_id, memory_type, content]
      properties:
        tenant_id: { type: string }
        agent_id: { type: string }
        memory_type: { $ref: '#/components/schemas/MemoryType' }
        content: { type: string }
        source_id: { type: string }
        created_at: { type: string, format: date-time }
        metadata: { type: object, additionalProperties: true }

    AddMemoryResponse:
      type: object
      properties:
        memory_id: { type: string, format: uuid }

    QueryRequest:
      type: object
      required: [tenant_id, query_text]
      properties:
        tenant_id: { type: string }
        query_text: { type: string }
        k: { type: integer, default: 50 }
        k_final: { type: integer, default: 5 }
        filters:
          type: object
          properties:
            memory_type: { $ref: '#/components/schemas/MemoryType' }
            min_saliency: { type: number }
            since: { type: string, format: date-time }

    QueryResponse:
      type: object
      properties:
        results:
          type: array
          items:
            type: object
            properties:
              memory_id: { type: string, format: uuid }
              score: { type: number }
              content: { type: string }
              source_id: { type: string }
              memory_type: { $ref: '#/components/schemas/MemoryType' }
              provenance: { type: object, additionalProperties: true }

    AgentExecuteRequest:
      type: object
      required: [tenant_id, prompt]
      properties:
        tenant_id: { type: string }
        prompt: { type: string }
        tools_allowed: { type: array, items: { type: string } }
        budget_tokens: { type: integer, default: 20000 }

    AgentExecuteResponse:
      type: object
      properties:
        answer: { type: string }
        used_memories: { $ref: '#/components/schemas/QueryResponse' }
        cost:
          type: object
          properties:
            input_tokens: { type: integer }
            output_tokens: { type: integer }
            total_estimate: { type: number }

    TimelineResponse:
      type: object
      properties:
        items:
          type: array
          items:
            type: object
            properties:
              memory_id: { type: string, format: uuid }
              created_at: { type: string, format: date-time }
              content: { type: string }
              memory_type: { $ref: '#/components/schemas/MemoryType' }
              saliency_score: { type: number }
