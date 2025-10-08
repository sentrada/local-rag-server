import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
	label?: string;
	error?: string;
}

export const Input: React.FC<InputProps> = ({ label, error, className, ...props }) => {
	return (
		<div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
			{label && (
				<label style={{ fontSize: 14, fontWeight: 500 }}>
					{label}
				</label>
			)}
			<input
				{...props}
				className={className}
				style={{
					padding: 8,
					borderRadius: 4,
					border: `1px solid ${error ? '#ef4444' : '#333'}`,
					background: '#222',
					color: '#fff',
					fontSize: 14,
					...props.style,
				}}
			/>
			{error && (
				<span style={{ fontSize: 12, color: '#ef4444' }}>
					{error}
				</span>
			)}
		</div>
	);
};
