const dummyProjects = [
	{ id: 'proj1', name: 'Projekt 1', description: 'Demo projekt 1', files: 12 },
	{ id: 'proj2', name: 'Projekt 2', description: 'Demo projekt 2', files: 8 },
];

export const useProjects = () => {
	// In real app, this would fetch from API
	return {
		projects: dummyProjects,
		loading: false,
		error: null,
	};
};
