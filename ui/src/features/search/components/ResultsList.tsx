const dummyResults = [
	{
		id: 1,
		content: 'def hello_world():\n    print("Hello, world!")',
		filePath: 'src/hello.py',
		relevance: 0.98,
	},
	{
		id: 2,
		content: 'function greet() {\n  console.log("Hello, JS!");\n}',
		filePath: 'src/greet.js',
		relevance: 0.87,
	},
];

export const ResultsList = () => {
	return (
		<div style={{ marginTop: 24, width: '100%' }}>
			<h2 style={{ fontSize: 20, marginBottom: 12 }}>Találatok</h2>
			<ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: 16 }}>
				{dummyResults.map(result => (
					<li key={result.id} style={{ background: '#27272a', borderRadius: 8, padding: 16 }}>
						<div style={{ fontSize: 14, color: '#a1a1aa', marginBottom: 8 }}>{result.filePath} <span style={{ float: 'right', color: '#818cf8' }}>Relevancia: {result.relevance}</span></div>
						<pre style={{ background: '#18181b', color: '#f1f5f9', padding: 12, borderRadius: 4, fontSize: 15, overflowX: 'auto' }}>{result.content}</pre>
					</li>
				))}
			</ul>
		</div>
	);
};
