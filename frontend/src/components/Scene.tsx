import { useRef, useMemo } from 'react';
import ForceGraph3D from 'react-force-graph-3d';
import * as THREE from 'three';
import type { GraphData } from '../types';

interface SceneProps {
    data: GraphData | null;
}

const Scene = ({ data }: SceneProps) => {
    const fgRef = useRef<any>(null);

    const nodes = useMemo(() => data?.nodes || [], [data]);
    const links = useMemo(() => data?.links || [], [data]);

    return (
        <div className="w-full h-full bg-cyber-bg">
            <ForceGraph3D
                ref={fgRef}
                graphData={{ nodes, links }}
                nodeLabel="label"
                nodeColor={(node: any) => {
                    if (node.compromised) return '#ff003c'; // Red
                    if (node.type === 'Attacker') return '#7000ff'; // Purple
                    return '#00f3ff'; // Cyan
                }}
                nodeVal="val"
                linkColor={() => '#ffffff30'}
                linkDirectionalParticles={2}
                linkDirectionalParticleSpeed={0.005}
                linkDirectionalParticleWidth={2}
                backgroundColor="#050510"
                nodeThreeObject={(node: any) => {
                    const color = node.compromised ? 0xff003c : (node.type === 'Attacker' ? 0x7000ff : 0x00f3ff);
                    const geometry = new THREE.SphereGeometry(node.val * 3);
                    const material = new THREE.MeshLambertMaterial({
                        color,
                        transparent: true,
                        opacity: 0.8,
                        emissive: color,
                        emissiveIntensity: 0.5
                    });
                    return new THREE.Mesh(geometry, material);
                }}
            />
        </div>
    );
};

export default Scene;
