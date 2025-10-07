import { useState } from 'react';

export const IndexProgress = () => {
	// Dummy progress state
	const [progress] = useState({ percent: 42, file: 'src/main.py' });
	return (
		<div style={{ background: '#27272a', borderRadius: 6, padding: '6px 16px', color: '#a1a1aa', fontSize: 15, minWidth: 180 }}>
			<div>Indexelés: <b>{progress.percent}%</b></div>
			<div style={{ fontSize: 13 }}>Fájl: {progress.file}</div>
		</div>
	);
};
