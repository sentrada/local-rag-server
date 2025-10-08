import { useState } from 'react';
import { queryRAG, type QueryRequest, type QueryResponse } from '../services/searchService';

export const useSearch = () => {
	const [result, setResult] = useState<QueryResponse | null>(null);
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState<string | null>(null);

	const search = async (query: string, options?: Partial<QueryRequest>) => {
		try {
			setLoading(true);
			setError(null);
			const data = await queryRAG({
				query,
				max_results: options?.max_results || 5,
				include_metadata: options?.include_metadata !== false,
				project_path: options?.project_path,
			});
			setResult(data);
			return data;
		} catch (err: any) {
			const errorMsg = err.message || 'Search failed';
			setError(errorMsg);
			throw new Error(errorMsg);
		} finally {
			setLoading(false);
		}
	};

	const clear = () => {
		setResult(null);
		setError(null);
	};

	return {
		result,
		loading,
		error,
		search,
		clear,
	};
};
