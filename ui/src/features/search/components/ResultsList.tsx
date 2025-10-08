import React from 'react';
import type { QueryResponse } from '../services/searchService';

interface ResultsListProps {
	result: QueryResponse | null;
}

export const ResultsList: React.FC<ResultsListProps> = ({ result }) => {
	if (!result) {
		return null;
	}

	return (
		<div style={{ marginTop: 24, width: '100%' }}>
			<div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
				<h2 style={{ fontSize: 20 }}>Találatok</h2>
				<div style={{ fontSize: 14, color: '#a1a1aa' }}>
					{result.context_chunks} chunk | {result.token_count} token
				</div>
			</div>

			{result.metadata && (
				<div style={{ background: '#27272a', borderRadius: 8, padding: 12, marginBottom: 16, fontSize: 13, color: '#a1a1aa' }}>
					<div><strong>Projekt:</strong> {result.metadata.project_root}</div>
					<div><strong>Indexelt fájlok:</strong> {result.metadata.indexed_files}</div>
					<div><strong>Model:</strong> {result.metadata.embedding_model}</div>
				</div>
			)}

			<div style={{ background: '#27272a', borderRadius: 8, padding: 16 }}>
				<div style={{ fontSize: 14, color: '#a1a1aa', marginBottom: 8 }}>Optimalizált prompt:</div>
				<pre style={{ 
					background: '#18181b', 
					color: '#f1f5f9', 
					padding: 12, 
					borderRadius: 4, 
					fontSize: 14, 
					overflowX: 'auto',
					whiteSpace: 'pre-wrap',
					wordWrap: 'break-word',
					maxHeight: 600,
					overflowY: 'auto'
				}}>
					{result.optimized_prompt}
				</pre>
			</div>
		</div>
	);
};
