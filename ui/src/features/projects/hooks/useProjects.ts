import { useState, useEffect } from 'react';
import { listProjects, switchProject, type Project } from '../services/projectService';

export const useProjects = () => {
	const [projects, setProjects] = useState<Project[]>([]);
	const [currentProject, setCurrentProject] = useState<string | null>(null);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState<string | null>(null);

	const fetchProjects = async () => {
		try {
			setLoading(true);
			setError(null);
			const data = await listProjects();
			setProjects(data.projects);
			setCurrentProject(data.current_project);
		} catch (err: any) {
			setError(err.message || 'Failed to load projects');
		} finally {
			setLoading(false);
		}
	};

	const selectProject = async (projectPath: string) => {
		try {
			await switchProject(projectPath);
			setCurrentProject(projectPath);
			await fetchProjects(); // Refresh list
		} catch (err: any) {
			setError(err.message || 'Failed to switch project');
		}
	};

	useEffect(() => {
		fetchProjects();
	}, []);

	return {
		projects,
		currentProject,
		loading,
		error,
		refetch: fetchProjects,
		selectProject,
	};
};
