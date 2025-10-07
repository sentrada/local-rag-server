import { IndexButton } from '../features/indexing/components/IndexButton';
import { IndexProgress } from '../features/indexing/components/IndexProgress';

import { SearchBar } from '../features/search/components/SearchBar';
import { ProjectSelector } from '../features/projects/components/ProjectSelector';
import { ResultsList } from '../features/search/components/ResultsList';
import { ProjectDetails } from '../features/projects/components/ProjectDetails';
import { SettingsPanel } from '../features/settings/components/SettingsPanel';
import { ThemeToggle } from '../features/settings/components/ThemeToggle';

export const App = () => {
	return (
		<div style={{ minHeight: '100vh', width: '100vw', display: 'flex', background: '#18181b', color: '#fff' }}>
			{/* Sidebar */}
			<aside style={{ width: 320, background: '#23232b', padding: '32px 24px', display: 'flex', flexDirection: 'column', gap: 32, boxShadow: '2px 0 12px #0002' }}>
				<div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 16 }}>
					<h1 style={{ fontSize: 22, fontWeight: 700, letterSpacing: 1 }}>RAG Server UI</h1>
					<ThemeToggle />
				</div>
				<SearchBar />
					<ProjectSelector />
					<ProjectDetails />
				<div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
					<IndexButton />
					<IndexProgress />
				</div>
				<SettingsPanel />
			</aside>
			{/* Main content */}
			<main style={{ flex: 1, padding: '40px 32px', overflowY: 'auto', display: 'flex', flexDirection: 'column', alignItems: 'stretch' }}>
				<h2 style={{ fontSize: 26, fontWeight: 600, marginBottom: 24 }}>Találatok</h2>
				<ResultsList />
			</main>
		</div>
	);
};
