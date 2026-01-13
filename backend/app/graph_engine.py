import networkx as nx
from typing import List, Dict
from .models import Node, Edge, AttackPath, GraphData

class GraphEngine:
    def __init__(self):
        self.graph = nx.DiGraph()

    def build_graph(self, events: List[Dict]) -> GraphData:
        # Clear previous state or keep it? For now, we rebuild per request or append.
        # Let's rebuild for simplicity of this request context, or we can make it stateful.
        
        nodes_dict = {}
        edges_list = []

        for event in events:
            src_ip = event["source"]
            target_ip = event["target"]
            
            # Create Source Node
            if src_ip not in nodes_dict:
                nodes_dict[src_ip] = Node(
                    id=src_ip,
                    type="Attacker" if "BRUTE" in event["type"] or "INJECTION" in event["type"] else "User",
                    label=f"IP: {src_ip}",
                    ip=src_ip,
                    val=2 if "BRUTE" in event["type"] else 1
                )
            
            # Create Target Node
            if target_ip not in nodes_dict:
                nodes_dict[target_ip] = Node(
                    id=target_ip,
                    type="Server",
                    label=target_ip,
                    ip=target_ip,
                    compromised=True if "INJECTION" in event["type"] else False
                )

            # Add Edge
            self.graph.add_edge(src_ip, target_ip, type=event["type"])
            edges_list.append(Edge(
                source=src_ip,
                target=target_ip,
                type=event["type"],
                timestamp=datetime.now(), # Placeholder
                details=event["details"]
            ))

        # Reconstruct Paths (Simple connectivity check)
        attack_paths = []
        for src in nodes_dict:
            for tgt in nodes_dict:
                if src != tgt and nodes_dict[src].type == "Attacker" and nodes_dict[tgt].compromised:
                     try:
                        path_nodes = nx.shortest_path(self.graph, src, tgt)
                        attack_paths.append(AttackPath(
                            nodes=path_nodes,
                            description=f"Attack path from {src} to {tgt}"
                        ))
                     except nx.NetworkXNoPath:
                         pass

        return GraphData(
            nodes=list(nodes_dict.values()),
            links=edges_list,
            attack_paths=attack_paths
        )
from datetime import datetime
