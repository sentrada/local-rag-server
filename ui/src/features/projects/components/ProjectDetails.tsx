import { useProjects } from '../hooks/useProjects';
import { useEffect, useState } from 'react';
import { getProjectStats, type ProjectStats } from '../services/projectService';

export const ProjectDetails = () => {
  const { currentProject } = useProjects();
  const [stats, setStats] = useState<ProjectStats | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (currentProject) {
      setLoading(true);
      getProjectStats(currentProject)
        .then(setStats)
        .catch(err => console.error('Failed to load stats:', err))
        .finally(() => setLoading(false));
    }
  }, [currentProject]);

  if (!currentProject) {
    return (
      <div style={{ padding: 16, textAlign: 'center', color: '#a1a1aa' }}>
        Nincs kiválasztott projekt
      </div>
    );
  }

  if (loading) {
    return (
      <div style={{ padding: 16, textAlign: 'center', color: '#a1a1aa' }}>
        Statisztikák betöltése...
      </div>
    );
  }

  if (!stats) return null;

  return (
    <div style={{ background: '#18181b', borderRadius: 6, padding: '14px 16px', color: '#e0e0e0', border: '1px solid #333', fontSize: 15, marginTop: 8 }}>
      <div style={{ fontWeight: 600, marginBottom: 8 }}>Projekt részletek</div>
      <div style={{ fontSize: 13, color: '#a1a1aa', display: 'flex', flexDirection: 'column', gap: 4 }}>
        <div><strong>Útvonal:</strong> {stats.project_root}</div>
        <div><strong>Indexelt fájlok:</strong> {stats.indexed_files}</div>
        <div><strong>Chunks:</strong> {stats.total_chunks}</div>
        <div><strong>Vector DB méret:</strong> {stats.vector_db_size}</div>
        <div><strong>Embedding model:</strong> {stats.embedding_model}</div>
        {stats.is_current && (
          <div style={{ marginTop: 4, color: '#818cf8', fontWeight: 600 }}>
            ✓ Aktív projekt
          </div>
        )}
      </div>
    </div>
  );
};