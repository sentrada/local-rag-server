export const ProjectCard = ({ project }: { project: { id: string; name: string; description: string; files: number } }) => {
	return (
		<div style={{ background: '#18181b', borderRadius: 6, padding: '10px 14px', color: '#e0e0e0', border: '1px solid #333', fontSize: 15 }}>
			<div style={{ fontWeight: 600 }}>{project.name}</div>
			<div style={{ fontSize: 13, color: '#a1a1aa' }}>{project.description}</div>
			<div style={{ fontSize: 12, color: '#818cf8', marginTop: 2 }}>Fájlok: {project.files}</div>
		</div>
	);
};
