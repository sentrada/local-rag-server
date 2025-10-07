import { useState } from 'react';
import { useProjects } from '../hooks/useProjects';

export const ProjectSelector = () => {
	const { projects } = useProjects();
	const [selected, setSelected] = useState(projects[0]?.id ?? '');

	return (
		<div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
			<label htmlFor="project-select" style={{ fontWeight: 500 }}>Projekt:</label>
			<select
				id="project-select"
				value={selected}
				onChange={e => setSelected(e.target.value)}
				style={{ padding: 8, borderRadius: 4, border: '1px solid #333', background: '#222', color: '#fff' }}
			>
				{projects.map(p => (
					<option key={p.id} value={p.id}>{p.name}</option>
				))}
			</select>
		</div>
	);
};
