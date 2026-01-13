import re
from datetime import datetime
from typing import List, Dict, Optional
from .models import LogEntry

class LogParser:
    @staticmethod
    def parse_line(line: str) -> Optional[LogEntry]:
        # Simple heuristics for demo purposes. In production, regex would be more robust.
        # Format: timestamp ip action ...
        
        try:
            parts = line.split()
            timestamp = datetime.now() # Default fallback
            
            # SSH Log Heuristic
            if "sshd" in line:
                # "2023-10-27T10:00:00 192.168.1.10 sshd: Failed password for root from 10.0.0.5 port 2222 ssh2"
                src_ip = "0.0.0.0"
                ip_match = re.search(r'from (\d+\.\d+\.\d+\.\d+)', line)
                if ip_match:
                    src_ip = ip_match.group(1)
                
                return LogEntry(
                    timestamp=timestamp,
                    source_ip=src_ip,
                    destination_ip="Server_SSH", 
                    protocol="SSH",
                    action="Failed Login" if "Failed" in line else "Login",
                    log_type="SSH",
                    details=line
                )

            # Web Log Heuristic (CLF)
            # 127.0.0.1 - - [10/Oct/2000:13:55:36 -0700] "GET /apa.html HTTP/1.0" 200 2326
            if "HTTP" in line:
                 ip_match = re.search(r'^(\d+\.\d+\.\d+\.\d+)', line)
                 src_ip = ip_match.group(1) if ip_match else "Unknown"
                 
                 return LogEntry(
                    timestamp=timestamp,
                    source_ip=src_ip,
                    destination_ip="WebServer",
                    protocol="HTTP",
                    action="GET" if "GET" in line else "POST",
                    log_type="WEB",
                    details=line
                 )
            
            return None

        except Exception as e:
            print(f"Error parsing line: {e}")
            return None

class DetectionEngine:
    def __init__(self):
        self.detections = []

    def analyze(self, logs: List[LogEntry]) -> List[Dict]:
        detected_events = []
        
        # 1. Brute Force Detection
        failed_logins = {}
        for log in logs:
            if log.protocol == "SSH" and "Failed" in log.action:
                failed_logins[log.source_ip] = failed_logins.get(log.source_ip, 0) + 1
        
        for ip, count in failed_logins.items():
            if count > 3: # Threshold
                detected_events.append({
                    "source": ip,
                    "target": "Server_SSH",
                    "type": "SSH_BRUTE_FORCE",
                    "details": f"Attempted {count} failed logins",
                    "mitre": "T1110"
                })

        # 2. Web Exploitation (SQLi check)
        for log in logs:
            if log.protocol == "HTTP":
                if "UNION SELECT" in log.details or "' OR '1'='1" in log.details:
                     detected_events.append({
                        "source": log.source_ip,
                        "target": "WebServer",
                        "type": "SQL_INJECTION",
                        "details": "SQL Injection Pattern Detected",
                        "mitre": "T1190"
                    })
        
        return detected_events
