import { useProjects } from '../hooks/useProjects';

export const ProjectSelector = () => {
	const { projects, currentProject, loading, error, selectProject } = useProjects();

	const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
		const projectPath = e.target.value;
		if (projectPath) {
			selectProject(projectPath);
		}
	};

	if (loading) {
		return <div>Projektek betöltése...</div>;
	}

	if (error) {
		return <div style={{ color: '#ef4444' }}>Hiba: {error}</div>;
	}

	if (projects.length === 0) {
		return <div style={{ color: '#6b7280' }}>Nincs indexelt projekt</div>;
	}

	return (
		<div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
			<label htmlFor="project-select" style={{ fontWeight: 500 }}>Projekt:</label>
			<select
				id="project-select"
				value={currentProject || ''}
				onChange={handleChange}
				style={{ padding: 8, borderRadius: 4, border: '1px solid #333', background: '#222', color: '#fff' }}
			>
				{projects.map(p => (
					<option key={p.path} value={p.path}>
						{p.name} ({p.indexed_files} fájl)
					</option>
				))}
			</select>
		</div>
	);
};
