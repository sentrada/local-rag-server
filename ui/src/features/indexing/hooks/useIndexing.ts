import { useState } from 'react';
import { indexProject, reindexProject, type IndexRequest } from '../services/indexService';

export const useIndexing = () => {
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState<string | null>(null);
	const [status, setStatus] = useState<string | null>(null);

	const startIndexing = async (request: IndexRequest) => {
		try {
			setLoading(true);
			setError(null);
			const result = await indexProject(request);
			setStatus(result.message);
			return result;
		} catch (err: any) {
			const errorMsg = err.message || 'Indexing failed';
			setError(errorMsg);
			throw new Error(errorMsg);
		} finally {
			setLoading(false);
		}
	};

	const reindex = async (projectPath: string, model?: string) => {
		try {
			setLoading(true);
			setError(null);
			const result = await reindexProject(projectPath, model);
			setStatus(result.message);
			return result;
		} catch (err: any) {
			const errorMsg = err.message || 'Reindexing failed';
			setError(errorMsg);
			throw new Error(errorMsg);
		} finally {
			setLoading(false);
		}
	};

	return {
		loading,
		error,
		status,
		startIndexing,
		reindex,
	};
};
