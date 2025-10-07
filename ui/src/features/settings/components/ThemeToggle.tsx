import { useState } from 'react';

export const ThemeToggle = () => {
	const [dark, setDark] = useState(true);
	return (
		<button
			onClick={() => setDark(d => !d)}
			style={{
				background: dark ? '#18181b' : '#f1f5f9',
				color: dark ? '#fff' : '#18181b',
				border: '1px solid #6366f1',
				borderRadius: 20,
				padding: '6px 18px',
				fontWeight: 600,
				cursor: 'pointer',
			}}
			aria-label="Téma váltása"
		>
			{dark ? '🌙 Sötét' : '☀️ Világos'}
		</button>
	);
};
