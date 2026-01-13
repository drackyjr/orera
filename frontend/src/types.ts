export interface Node {
    id: string;
    type: 'Attacker' | 'Server' | 'Database' | 'Firewall' | 'User';
    label: string;
    ip: string;
    compromised: boolean;
    val: number;
    x?: number;
    y?: number;
    z?: number;
}

export interface Link {
    source: string | Node;
    target: string | Node;
    type: string;
    description?: string;
}

export interface GraphData {
    nodes: Node[];
    links: Link[];
    attack_paths: Array<{
        nodes: string[];
        description: string;
    }>;
}
