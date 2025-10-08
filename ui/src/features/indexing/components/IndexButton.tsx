import { useState } from 'react';
import { Input } from '../../../shared/components';

interface IndexButtonProps {
	onIndexStart?: (projectPath: string) => void;
}

export const IndexButton: React.FC<IndexButtonProps> = ({ onIndexStart }) => {
	const [showInput, setShowInput] = useState(false);
	const [projectPath, setProjectPath] = useState('');

	const handleClick = () => {
		if (!showInput) {
			setShowInput(true);
		} else if (projectPath.trim()) {
			if (onIndexStart) {
				onIndexStart(projectPath.trim());
			}
			setShowInput(false);
			setProjectPath('');
		}
	};

	return (
		<div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
			{showInput && (
				<>
					<Input
						type="text"
						value={projectPath}
						onChange={(e) => setProjectPath(e.target.value)}
						placeholder="Projekt útvonal (pl. C:\Projects\myapp)"
						style={{ minWidth: 300 }}
					/>
					<button
						onClick={() => { setShowInput(false); setProjectPath(''); }}
						style={{
							padding: '8px 12px',
							borderRadius: 6,
							background: '#6b7280',
							color: '#fff',
							border: 'none',
							fontWeight: 600,
							cursor: 'pointer',
						}}
					>
						Mégse
					</button>
				</>
			)}
			<button
				onClick={handleClick}
				style={{
					padding: '8px 18px',
					borderRadius: 6,
					background: '#22c55e',
					color: '#fff',
					border: 'none',
					fontWeight: 600,
					fontSize: 16,
					cursor: 'pointer',
				}}
				disabled={showInput && !projectPath.trim()}
			>
				{showInput ? 'Indexelés indítása' : '+ Új projekt indexelése'}
			</button>
		</div>
	);
};
