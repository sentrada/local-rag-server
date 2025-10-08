import { ProjectCard } from './ProjectCard';
import { useProjects } from '../hooks/useProjects';

export const ProjectList = () => {
	const { projects, selectProject, loading } = useProjects();

	if (loading) {
		return <div style={{ padding: 16, textAlign: 'center', color: '#a1a1aa' }}>Projektek betöltése...</div>;
	}

	if (projects.length === 0) {
		return (
			<div style={{ padding: 16, textAlign: 'center', color: '#a1a1aa' }}>
				Nincs indexelt projekt. Adj hozzá egyet az Indexelés gombbal.
			</div>
		);
	}

	return (
		<div style={{ marginTop: 8, display: 'flex', flexDirection: 'column', gap: 10 }}>
			{projects.map(p => (
				<ProjectCard 
					key={p.path} 
					project={p} 
					onSelect={selectProject}
				/>
			))}
		</div>
	);
};
