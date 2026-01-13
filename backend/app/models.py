from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Literal
from datetime import datetime

class LogEntry(BaseModel):
    timestamp: datetime
    source_ip: str
    destination_ip: str
    protocol: str
    action: str
    user: Optional[str] = None
    details: Optional[str] = None
    log_type: Literal['SSH', 'WEB', 'FIREWALL', 'AUDIT']

class Node(BaseModel):
    id: str
    type: Literal['Attacker', 'Server', 'Database', 'Firewall', 'User']
    label: str
    ip: str
    compromised: bool = False
    details: Dict[str, str] = {}
    val: int = 1  # For visualization sizing

class Edge(BaseModel):
    source: str
    target: str
    type: str # e.g., "SSH_BRUTE_FORCE", "SQL_INJECTION"
    timestamp: datetime
    details: str

class AttackPath(BaseModel):
    nodes: List[str]
    description: str

class GraphData(BaseModel):
    nodes: List[Node]
    links: List[Edge]
    attack_paths: List[AttackPath]

class IngestResponse(BaseModel):
    message: str
    processed_count: int
    detections: int
