import { useState } from 'react';

export const SearchBar = () => {
	const [query, setQuery] = useState('');

	const handleSubmit = (e: React.FormEvent) => {
		e.preventDefault();
		// For now, just alert the query
		if (query.trim()) {
			alert(`Keresés: ${query}`);
		}
	};

	return (
		<form onSubmit={handleSubmit} style={{ display: 'flex', gap: 8 }}>
			<input
				type="text"
				value={query}
				onChange={e => setQuery(e.target.value)}
				placeholder="Kód keresése..."
				style={{ flex: 1, padding: 8, borderRadius: 4, border: '1px solid #333', background: '#222', color: '#fff' }}
			/>
			<button
				type="submit"
				style={{ padding: '8px 16px', borderRadius: 4, border: 'none', background: '#6366f1', color: '#fff', fontWeight: 600 }}
				disabled={!query.trim()}
			>
				Keresés
			</button>
		</form>
	);
};
