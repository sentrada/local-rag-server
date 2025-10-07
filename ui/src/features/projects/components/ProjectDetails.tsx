import { useProjects } from '../hooks/useProjects';
import { useState } from 'react';

export const ProjectDetails = () => {
  const { projects } = useProjects();
  // For now, always show the first project as selected (sync with ProjectSelector logic)
  const [selected] = useState(projects[0]);
  if (!selected) return null;
  return (
    <div style={{ background: '#18181b', borderRadius: 6, padding: '10px 14px', color: '#e0e0e0', border: '1px solid #333', fontSize: 15, marginTop: 8 }}>
      <div style={{ fontWeight: 600 }}>{selected.name}</div>
      <div style={{ fontSize: 13, color: '#a1a1aa' }}>{selected.description}</div>
      <div style={{ fontSize: 12, color: '#818cf8', marginTop: 2 }}>Fájlok: {selected.files}</div>
    </div>
  );
};