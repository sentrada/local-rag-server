import type { Project } from '../services/projectService';

interface ProjectCardProps {
	project: Project;
	onSelect?: (path: string) => void;
}

export const ProjectCard: React.FC<ProjectCardProps> = ({ project, onSelect }) => {
	return (
		<div 
			style={{ 
				background: project.is_current ? '#1e293b' : '#18181b', 
				borderRadius: 6, 
				padding: '10px 14px', 
				color: '#e0e0e0', 
				border: `1px solid ${project.is_current ? '#6366f1' : '#333'}`, 
				fontSize: 15,
				cursor: onSelect ? 'pointer' : 'default'
			}}
			onClick={() => onSelect && onSelect(project.path)}
		>
			<div style={{ fontWeight: 600, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
				<span>{project.name}</span>
				{project.is_current && (
					<span style={{ fontSize: 11, background: '#6366f1', padding: '2px 6px', borderRadius: 3 }}>
						Aktív
					</span>
				)}
			</div>
			<div style={{ fontSize: 12, color: '#a1a1aa', marginTop: 4 }}>{project.path}</div>
			<div style={{ fontSize: 12, color: '#818cf8', marginTop: 2 }}>
				Fájlok: {project.indexed_files} | Chunks: {project.total_chunks}
			</div>
		</div>
	);
};
