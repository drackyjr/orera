from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from .models import LogEntry, IngestResponse, GraphData
from .detection import LogParser, DetectionEngine
from .graph_engine import GraphEngine

app = FastAPI(title="Cyber Attack Visualization API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# State
log_storage: List[LogEntry] = []
graph_engine = GraphEngine()
detection_engine = DetectionEngine()

@app.get("/")
def health_check():
    return {"status": "ok", "service": "backend"}

@app.post("/api/ingest", response_model=IngestResponse)
async def ingest_logs(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")
    lines = text.split("\n")
    
    new_logs = []
    parser = LogParser()
    
    for line in lines:
        if not line.strip(): continue
        entry = parser.parse_line(line)
        if entry:
            new_logs.append(entry)
    
    log_storage.extend(new_logs)
    
    # Run Detection
    events = detection_engine.analyze(log_storage)
    
    # Update Graph
    # For now, we rebuild the graph from all detected events
    graph_engine.build_graph(events)
    
    return IngestResponse(
        message="Logs processed successfully",
        processed_count=len(new_logs),
        detections=len(events)
    )

@app.get("/api/graph", response_model=GraphData)
def get_graph():
    # In a real app, this might be cached or computed on demand
    events = detection_engine.analyze(log_storage)
    return graph_engine.build_graph(events)
