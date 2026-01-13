# Production-Grade 3D Cyber Attack Route Analysis & Visualization Platform

## System Overview
This platform ingests real security logs (SSH, Web, Firewall, Audit), reconstructs attack paths using a graph-based detection engine, and visualizes them in an interactive 3D environment.

### Core Stack
- **Backend**: Python 3.11, FastAPI, NetworkX (Graph Analysis), Pydantic
- **Frontend**: React 19, TypeScript, Three.js (3D Rendering), TailwindCSS
- **Infrastructure**: Docker, Google Cloud Run

## Quick Start (Local)

1. **Backend**:
    ```bash
    cd backend
    pip install -r requirements.txt
    uvicorn app.main:app --reload --port 8080
    ```

2. **Frontend**:
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

3. **Usage**:
    - Open `http://localhost:5173`
    - Upload `test_logs.txt` (located in root)
    - Observe 3D attack graph and threats.

## Deployment (Google Cloud)

**Prerequisites**: `gcloud` CLI authenticated.

1. **Run Deployment Script**:
    ```bash
    chmod +x deploy.sh
    ./deploy.sh
    ```
    This script will:
    - Enable required GCP services.
    - Create an Artifact Registry repo.
    - Build Docker images for Backend and Frontend.
    - Deploy to Cloud Run (Backend on port 8080, Frontend on port 80).

## Architecture

- **Ingestion**: Uploaded logs are parsed for IP, timestamp, and attack signatures.
- **Detection**:
    - SSH Brute Force (T1110)
    - SQL Injection (T1190)
    - Lateral Movement
- **Graph Construction**: Nodes (IPs) and Edges (Traffic/Attacks) are mapped in NetworkX.
- **Visualization**: React Force Graph 3D renders the topology with glowing nodes indicating compromise status.

## Security
- Containerized services.
- Validation using Pydantic.
- Scalable Serverless architecture (Cloud Run).
