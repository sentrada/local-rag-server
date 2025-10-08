import { useState } from 'react';
import './App.css';
import { SearchBar } from './features/search/components/SearchBar';
import { ResultsList } from './features/search/components/ResultsList';
import { ProjectSelector } from './features/projects/components/ProjectSelector';
import { IndexButton } from './features/indexing/components/IndexButton';
import { ModelSelector } from './features/settings/components/ModelSelector';
import { useSearch } from './features/search/hooks/useSearch';
import { useIndexing } from './features/indexing/hooks/useIndexing';
import { useProjects } from './features/projects/hooks/useProjects';

function App() {
  const { error: searchError } = useSearch();
  const { startIndexing, loading: indexing, error: indexError } = useIndexing();
  const { currentProject, refetch: refetchProjects } = useProjects();
  const [searchResult, setSearchResult] = useState<any>(null);

  const handleIndexStart = async (projectPath: string) => {
    try {
      await startIndexing({ project_path: projectPath });
      // Refresh projects list after indexing starts
      setTimeout(() => refetchProjects(), 1000);
    } catch (err) {
      console.error('Index error:', err);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: '#111',
      color: '#f1f5f9',
      padding: 24
    }}>
      <div style={{ maxWidth: 1200, margin: '0 auto' }}>
        <header style={{ marginBottom: 32 }}>
          <h1 style={{ fontSize: 32, marginBottom: 8, fontWeight: 700 }}>
            🔍 Local RAG Server
          </h1>
          <p style={{ color: '#a1a1aa', fontSize: 16 }}>
            AI-vezérelt kódkeresés és kontextus optimalizáció
          </p>
        </header>

        {/* Error messages */}
        {(searchError || indexError) && (
          <div style={{
            background: '#7f1d1d',
            border: '1px solid #991b1b',
            borderRadius: 8,
            padding: 16,
            marginBottom: 16,
            color: '#fca5a5'
          }}>
            {searchError || indexError}
          </div>
        )}

        {/* Indexing status */}
        {indexing && (
          <div style={{
            background: '#1e3a8a',
            border: '1px solid #2563eb',
            borderRadius: 8,
            padding: 16,
            marginBottom: 16,
            color: '#93c5fd'
          }}>
            Indexelés folyamatban...
          </div>
        )}

        {/* Top controls */}
        <div style={{
          background: '#1a1a1a',
          borderRadius: 12,
          padding: 20,
          marginBottom: 24,
          display: 'flex',
          flexDirection: 'column',
          gap: 16
        }}>
          <div style={{ display: 'flex', gap: 16, alignItems: 'center', flexWrap: 'wrap' }}>
            <ProjectSelector />
            <IndexButton onIndexStart={handleIndexStart} />
          </div>

          {currentProject && (
            <ModelSelector 
              projectPath={currentProject} 
              onModelChange={(model) => console.log('Model changed:', model)}
            />
          )}
        </div>

        {/* Search section */}
        <div style={{
          background: '#1a1a1a',
          borderRadius: 12,
          padding: 20,
          marginBottom: 24
        }}>
          <SearchBar onResult={setSearchResult} />
        </div>

        {/* Results */}
        {searchResult && (
          <ResultsList result={searchResult} />
        )}

        {!searchResult && !searchError && (
          <div style={{
            textAlign: 'center',
            padding: 48,
            color: '#6b7280',
            fontSize: 14
          }}>
            <p>Kezdj el gépelni a keresőmezőbe a kontextus lekérdezéséhez</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
