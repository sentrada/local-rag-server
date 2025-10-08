import { useState } from 'react';
import { useSearch } from '../hooks/useSearch';

interface SearchBarProps {
	onResult?: (result: any) => void;
}

export const SearchBar: React.FC<SearchBarProps> = ({ onResult }) => {
	const [query, setQuery] = useState('');
	const { search, loading } = useSearch();

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		if (query.trim()) {
			try {
				const result = await search(query.trim());
				if (onResult) {
					onResult(result);
				}
			} catch (err) {
				console.error('Search error:', err);
			}
		}
	};

	return (
		<form onSubmit={handleSubmit} style={{ display: 'flex', gap: 8 }}>
			<input
				type="text"
				value={query}
				onChange={e => setQuery(e.target.value)}
				placeholder="Kód keresése..."
				disabled={loading}
				style={{ 
					flex: 1, 
					padding: 8, 
					borderRadius: 4, 
					border: '1px solid #333', 
					background: '#222', 
					color: '#fff',
					opacity: loading ? 0.6 : 1
				}}
			/>
			<button
				type="submit"
				style={{ 
					padding: '8px 16px', 
					borderRadius: 4, 
					border: 'none', 
					background: loading || !query.trim() ? '#4b5563' : '#6366f1', 
					color: '#fff', 
					fontWeight: 600,
					cursor: loading || !query.trim() ? 'not-allowed' : 'pointer'
				}}
				disabled={!query.trim() || loading}
			>
				{loading ? 'Keresés...' : 'Keresés'}
			</button>
		</form>
	);
};
