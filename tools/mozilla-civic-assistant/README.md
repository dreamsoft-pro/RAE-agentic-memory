# 🛡️ Mozilla Civic Assistant (RAE Module)

A specialized AI assistant designed for civil society organizations and local watchdogs to analyze public documents with high transparency and auditability.

## 🚀 Key Features
- **Evidence Ingestion**: Upload PDF/TXT public records (budget reports, meeting minutes).
- **Procedural Audit**: Uses RAE's multi-stage flow (`Draft -> Reflection -> Human`).
- **Provenance Tracking**: Every claim is mapped back to the source document.
- **Reflection**: Synthesize long-term semantic knowledge from uploaded evidence.

## 🛠️ Installation & Run

1. Ensure the RAE API is running (port 8001).
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the app:
```bash
export RAE_API_URL=http://localhost:8001
python app.py
```

## 🧠 System Architecture
- **Writer**: Qwen 3.5 9B (Drafting)
- **Auditor**: DeepSeek R1 8B (Critical Audit)
- **Storage**: RAE-Core V2 (PostgreSQL + Qdrant)

*Part of the RAE (Robotic Agent Emulation) Suite.*
