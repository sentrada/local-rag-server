import { useState } from 'react';

export const IndexButton = () => {
	const [running, setRunning] = useState(false);
	return (
		<button
			onClick={() => setRunning(r => !r)}
			style={{
				padding: '8px 18px',
				borderRadius: 6,
				background: running ? '#f59e42' : '#22c55e',
				color: '#fff',
				border: 'none',
				fontWeight: 600,
				fontSize: 16,
				cursor: 'pointer',
			}}
		>
			{running ? 'Indexelés leállítása' : 'Indexelés indítása'}
		</button>
	);
};
