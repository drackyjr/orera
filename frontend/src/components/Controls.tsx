import { Upload, Server, Shield, Activity } from 'lucide-react';

interface ControlsProps {
    onUpload: (file: File) => void;
    stats: { nodes: number; edges: number; detections: number };
}

const Controls = ({ onUpload, stats }: ControlsProps) => {
    return (
        <div className="absolute top-0 left-0 w-full h-full pointer-events-none p-6 flex flex-col justify-between">
            {/* Header */}
            <div className="flex justify-between items-start pointer-events-auto">
                <div>
                    <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyber-primary to-cyber-secondary font-mono tracking-tighter">
                        NET_SENTRY_3D
                    </h1>
                    <p className="text-cyber-dim text-sm font-mono mt-1">
                        LIVE THREAT VISUALIZATION
                    </p>
                </div>

                <div className="cyber-panel p-4 flex gap-4">
                    <label className="cyber-button cursor-pointer flex items-center gap-2">
                        <Upload size={14} />
                        Ingest Logs
                        <input
                            type="file"
                            className="hidden"
                            onChange={(e) => e.target.files && onUpload(e.target.files[0])}
                        />
                    </label>
                </div>
            </div>

            {/* Stats */}
            <div className="flex gap-4 pointer-events-auto w-fit">
                <StatCard icon={<Server />} label="NODES" value={stats.nodes} />
                <StatCard icon={<Activity />} label="EDGES" value={stats.edges} />
                <StatCard icon={<Shield />} label="THREATS" value={stats.detections} isAlert />
            </div>
        </div>
    );
};

const StatCard = ({ icon, label, value, isAlert = false }: any) => (
    <div className={`cyber-panel p-4 min-w-[120px] ${isAlert ? 'border-cyber-alert/50' : ''}`}>
        <div className={`flex items-center gap-2 mb-2 ${isAlert ? 'text-cyber-alert' : 'text-cyber-primary'}`}>
            {icon}
            <span className="text-xs font-bold">{label}</span>
        </div>
        <div className="text-2xl font-mono font-bold text-white">
            {value}
        </div>
    </div>
);

export default Controls;
