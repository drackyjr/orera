import { useState, useEffect } from 'react';
import Scene from './components/Scene';
import Controls from './components/Controls';
import type { GraphData } from './types';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080/api';

function App() {
  const [data, setData] = useState<GraphData | null>(null);
  const [stats, setStats] = useState({ nodes: 0, edges: 0, detections: 0 });

  const fetchData = async () => {
    try {
      const res = await axios.get(`${API_URL}/graph`);
      if (res.data) {
        setData(res.data);
        setStats({
          nodes: res.data.nodes?.length || 0,
          edges: res.data.links?.length || 0,
          detections: res.data.attack_paths?.length || 0
        });
      }
    } catch (err) {
      console.error("Failed to fetch graph", err);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000); // Poll every 5s
    return () => clearInterval(interval);
  }, []);

  const handleUpload = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    try {
      await axios.post(`${API_URL}/ingest`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      fetchData(); // Refresh immediately
    } catch (err) {
      console.error("Upload failed", err);
      alert("Upload failed");
    }
  };

  return (
    <div className="w-screen h-screen relative bg-cyber-bg">
      <Scene data={data} />
      <Controls onUpload={handleUpload} stats={stats} />
    </div>
  );
}

export default App;
