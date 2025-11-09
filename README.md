# RAG-MCP Knowledge Agent: Semantic Retrieval System

## Overview

This project implements a Retrieval-Augmented Generation (RAG) pipeline integrated with the Model Context Protocol (MCP), allowing an external Large Language Model (LLM) client (like Claude Desktop) to query a custom knowledge base of lecture materials (PDF slides) in real-time.

The architecture is built for traceability, speed, and modularity, using containerization (Docker) for state management and specialized Python libraries for high-performance vector search.

## Technologies and Tech-Stack

| Component | Technology | Rationale & Contribution |
| :--- | :--- | :--- |
| **Orchestration** | **Python (AsyncIO)** / `uv` | Manages the asynchronous data ingestion pipeline and serves the custom application logic. `uv` is used for ultra-fast dependency management. |
| **Vector Embedding** | **Qwen3-Embedding-0.6B** (`SentenceTransformer`) | Utilized a specialized, state-of-the-art embedding model to generate high-quality vector representations, ensuring superior semantic relevance over generic models. |
| **Vector Database** | **ChromaDB** (Dockerized) | Provides scalable, persistent storage for vector embeddings, original text chunks, and metadata (source tracing). Deployed in client-server mode for isolation. |
| **API/Tooling** | **FastMCP** (Model Context Protocol) | Implements a standardized interface, allowing any MCP-compliant LLM (e.g., Claude) to consume the custom RAG functionality as a callable tool (`get_documents_from_RAG`). |
| **Observability** | **OpenTelemetry (OTEL) & Zipkin** | Integrated tracing infrastructure to monitor request flow from the MCP proxy, through the Python server, to the ChromaDB database, aiding in performance analysis and debugging. |
| **Deployment** | **Docker Compose** | Used to manage and deploy the distributed service architecture (ChromaDB, OTEL Collector, Zipkin) within an isolated network. |

## Architecture Highlights

![System_diagram](https://github.com/NadmanFaisal/MCP_Server/blob/main/documentations/MCP_RAG_Server.drawio.png)

This project demonstrates proficiency in designing and implementing modern, distributed micro-architectures:

1. Robust RAG Pipeline Implementation

Custom Data Ingestion: Developed a dedicated ingestion script (main.py & data_extractor.py) that handles PDF extraction, robust text cleaning (merging line wraps, removing artifacts), and semantic chunking.

Traceability: Every document chunk stored in ChromaDB is indexed with a unique, traceable ID and metadata (source_file), allowing the LLM to cite the origin of the retrieved context.

Idempotency: Utilizes the ChromaDB .upsert() method to ensure the ingestion pipeline can be rerun safely without creating duplicate data entries, crucial for maintenance and data integrity.

2. Microservice and Interface Design

Protocol Implementation: Successfully implemented the Model Context Protocol (MCP) using FastMCP, showcasing ability to extend third-party LLMs with custom enterprise/domain logic.

Decoupled Services: Separated the core logic: The ChromaDB Server handles state (Docker) while the Embedding/RAG logic (server.py) runs on the host, achieving modularity and allowing independent scaling.

Complex Tool Execution: Resolved intricate execution path issues using the uvx mcpo proxy to correctly bridge the host Python environment with the Stdio/MCP standard on a Linux host.

3. Asynchronous Networking

The Python application uses asyncio and the chromadb.AsyncHttpClient (built on httpx) to handle vector database connections non-blockingly, demonstrating knowledge of high-concurrency network communication.

## Setup and Running the System

Prerequisites

- Docker and Docker Compose installed.
- Ollama installed and running locally on port 11434 (required for Open WebUI).
- Python 3.10+ and the uv package manager.

1. Start the Docker Infrastructure

This command launches the vector database (ChromaDB), the OTEL collector, and Zipkin.

```
docker compose up -d
```

2. Start the Virtual environment
```
python3 -m venv .venv
pip install -r requirements.txt
source ./venv/bin/activate
```

3. Run the Data Ingestion Pipeline

This loads, cleans, embeds (using Qwen3), and stores all PDF files in the datasets/ folder into ChromaDB.

```
python main.py
```

4. Run the MCP Server (The Tool)

This command starts the local MCP server, which listens for requests from the LLM client (or Open WebUI/FastAPI proxy).
```
uvx mcpo --port 8000 -- /home/nadman/Desktop/Personal_Projects/MCP_Server/.venv/bin/python server.py
```

5. Run the Open WebUI Client

This provides a UI for testing, connecting to your Ollama LLM and your running MCP server.

```
sudo docker run -d \
  -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```
6. Run the Open WebUI Client

This provides a UI for testing, connecting to your Ollama LLM and your running MCP server.
```
sudo docker run -d \
  -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data \
  -e OLLAMA_BASE_URL=[http://host.docker.internal:11434](http://host.docker.internal:11434) \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main

```
Access the client UI at http://localhost:3000.
