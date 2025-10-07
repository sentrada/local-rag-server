//
import { ProjectCard } from './ProjectCard';
import { useProjects } from '../hooks/useProjects';

export const ProjectList = () => {
	const { projects } = useProjects();
	return (
		<div style={{ marginTop: 8, display: 'flex', flexDirection: 'column', gap: 10 }}>
			{projects.map(p => (
				<ProjectCard key={p.id} project={p} />
			))}
		</div>
	);
};
