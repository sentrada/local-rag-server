# 🌐 RAG Server Web UI - Tervezési Dokumentáció

## 📋 Áttekintés

Egy modern, letisztult webes felület a RAG szerver számára, amely lehetővé teszi a kódban való keresést, kérdezést és releváns kódrészletek megtalálását böngészőből.

---

## 🎯 Célkitűzések

1. **Egyszerű használat** - Intuitív, nem igényel technikai tudást
2. **Gyors keresés** - Real-time válaszok a RAG rendszerből
3. **Kód kontextus** - Syntax highlighting, relevancia kiemelés
4. **Multi-project** - Több projekt kezelése egyidejűleg
5. **Modern UX** - Dark mode, responsive design, accessibility

---

## 🏗️ Architektúra

### High-Level Architektúra

```
┌─────────────────────────────────────────────────────────┐
│                    Browser (Client)                     │
│                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Search    │  │   Projects   │  │   Settings   │  │
│  │    View     │  │   Dashboard  │  │     View     │  │
│  └─────────────┘  └──────────────┘  └──────────────┘  │
│           │              │                  │           │
│           └──────────────┴──────────────────┘           │
│                          │                              │
│                   ┌──────▼──────┐                       │
│                   │  API Client │                       │
│                   └──────┬──────┘                       │
└──────────────────────────┼──────────────────────────────┘
                           │ HTTP/WebSocket
                           │
┌──────────────────────────▼──────────────────────────────┐
│              FastAPI Backend (Python)                   │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Web API     │  │  RAG System  │  │  WebSocket   │  │
│  │  Endpoints   │  │   Service    │  │   Handler    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│           │              │                  │           │
│           └──────────────┴──────────────────┘           │
│                          │                              │
└──────────────────────────┼──────────────────────────────┘
                           │
                ┌──────────┴──────────┐
                │                     │
        ┌───────▼────────┐    ┌──────▼──────┐
        │   ChromaDB     │    │    Redis    │
        │  Vector Store  │    │    Cache    │
        └────────────────┘    └─────────────┘
```

---

## 🎨 Frontend Architektúra

### Technológia Stack

**Framework:** React 18+ (TypeScript)
- Modern, jól dokumentált, nagy közösség
- Component-based architektúra
- Hooks API → tiszta, funkcionális kód

**State Management:** Zustand vagy Redux Toolkit
- Zustand: Egyszerűbb, kisebb bundle size
- Redux Toolkit: Ha komplex state logika

**UI Library:** Tailwind CSS + shadcn/ui
- Tailwind: Utility-first, gyors fejlesztés
- shadcn/ui: Előre elkészített, testreszabható komponensek

**HTTP Client:** Axios vagy TanStack Query (React Query)
- TanStack Query: Automatikus cache, retry, stale-while-revalidate

**Code Highlighting:** Prism.js vagy Monaco Editor
- Prism.js: Egyszerű syntax highlighting
- Monaco: Full-featured editor (VS Code alapú)

**WebSocket:** Socket.io-client vagy native WebSocket
- Real-time indexelés státusz

---

### SOLID Elvek Alkalmazása

#### 1. Single Responsibility Principle (SRP)

Minden komponens és modul egy felelősségért felel.

```typescript
// ❌ BAD: Túl sok felelősség egy komponensben
const SearchPage = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [projects, setProjects] = useState([]);
  // API hívások, state management, rendering - mindent egyben
};

// ✅ GOOD: Szeparált felelősségek
const SearchPage = () => {
  return (
    <div>
      <SearchBar />
      <ProjectSelector />
      <ResultsList />
    </div>
  );
};

// Külön komponensek:
// - SearchBar: csak a keresési input kezelése
// - ProjectSelector: csak a projekt választás
// - ResultsList: csak az eredmények megjelenítése
```

#### 2. Open/Closed Principle (OCP)

A kód nyitott a bővítésre, de zárt a módosításra.

```typescript
// ✅ Plugin-based query processors
interface QueryProcessor {
  process(query: string): Promise<QueryResult>;
}

class SemanticQueryProcessor implements QueryProcessor {
  async process(query: string): Promise<QueryResult> {
    // Szemantikus keresés
  }
}

class ExactMatchQueryProcessor implements QueryProcessor {
  async process(query: string): Promise<QueryResult> {
    // Pontos egyezés keresés
  }
}

// Új processor hozzáadása nem módosítja a meglévőt
class FuzzyQueryProcessor implements QueryProcessor {
  async process(query: string): Promise<QueryResult> {
    // Fuzzy keresés
  }
}
```

#### 3. Liskov Substitution Principle (LSP)

Az alosztályok helyettesíthetők a szülő osztállyal.

```typescript
// ✅ Consistent interface
interface ResultRenderer {
  render(result: SearchResult): JSX.Element;
}

class CodeSnippetRenderer implements ResultRenderer {
  render(result: SearchResult): JSX.Element {
    return <CodeSnippet code={result.content} />;
  }
}

class MarkdownRenderer implements ResultRenderer {
  render(result: SearchResult): JSX.Element {
    return <MarkdownView markdown={result.content} />;
  }
}

// Mindkettő ugyanúgy használható
const renderer: ResultRenderer = new CodeSnippetRenderer();
```

#### 4. Interface Segregation Principle (ISP)

Ne kényszeríts klienst olyan metódusokra, amiket nem használ.

```typescript
// ❌ BAD: Túl nagy interface
interface DataService {
  search(query: string): Promise<Result[]>;
  index(project: string): Promise<void>;
  clearCache(): Promise<void>;
  exportData(): Promise<Blob>;
  importData(data: Blob): Promise<void>;
}

// ✅ GOOD: Szeparált interfészek
interface SearchService {
  search(query: string): Promise<Result[]>;
}

interface IndexService {
  index(project: string): Promise<void>;
}

interface CacheService {
  clear(): Promise<void>;
}

interface DataExportService {
  export(): Promise<Blob>;
  import(data: Blob): Promise<void>;
}
```

#### 5. Dependency Inversion Principle (DIP)

Függj absztrakciótól, ne konkrét implementációtól.

```typescript
// ✅ Dependency Injection
interface ApiClient {
  get<T>(url: string): Promise<T>;
  post<T>(url: string, data: any): Promise<T>;
}

class AxiosApiClient implements ApiClient {
  async get<T>(url: string): Promise<T> {
    const response = await axios.get(url);
    return response.data;
  }
  
  async post<T>(url: string, data: any): Promise<T> {
    const response = await axios.post(url, data);
    return response.data;
  }
}

// Service réteg az absztrakciótól függ
class SearchService {
  constructor(private apiClient: ApiClient) {}
  
  async search(query: string): Promise<Result[]> {
    return this.apiClient.post('/query', { query });
  }
}

// Könnyen cserélhető implementáció (pl. mock teszteléshez)
```

---

### Folder Structure (Clean Architecture)

```
ui/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── app/                    # Application layer
│   │   ├── App.tsx
│   │   ├── Router.tsx
│   │   └── store/              # Global state
│   │       ├── useAppStore.ts
│   │       └── slices/
│   ├── features/               # Feature modules
│   │   ├── search/
│   │   │   ├── components/     # UI components
│   │   │   │   ├── SearchBar.tsx
│   │   │   │   ├── ResultsList.tsx
│   │   │   │   └── CodeSnippet.tsx
│   │   │   ├── hooks/          # Custom hooks
│   │   │   │   ├── useSearch.ts
│   │   │   │   └── useSearchHistory.ts
│   │   │   ├── services/       # Business logic
│   │   │   │   └── searchService.ts
│   │   │   └── types/          # TypeScript types
│   │   │       └── search.types.ts
│   │   ├── projects/
│   │   │   ├── components/
│   │   │   │   ├── ProjectList.tsx
│   │   │   │   ├── ProjectCard.tsx
│   │   │   │   └── ProjectSelector.tsx
│   │   │   ├── hooks/
│   │   │   │   └── useProjects.ts
│   │   │   └── services/
│   │   │       └── projectService.ts
│   │   ├── indexing/
│   │   │   ├── components/
│   │   │   │   ├── IndexProgress.tsx
│   │   │   │   └── IndexButton.tsx
│   │   │   ├── hooks/
│   │   │   │   └── useIndexing.ts
│   │   │   └── services/
│   │   │       └── indexService.ts
│   │   └── settings/
│   │       ├── components/
│   │       │   ├── ThemeToggle.tsx
│   │       │   └── SettingsPanel.tsx
│   │       └── hooks/
│   │           └── useSettings.ts
│   ├── shared/                 # Shared/Common
│   │   ├── components/         # Reusable UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Modal.tsx
│   │   │   └── Spinner.tsx
│   │   ├── hooks/              # Reusable hooks
│   │   │   ├── useDebounce.ts
│   │   │   └── useLocalStorage.ts
│   │   ├── utils/              # Helper functions
│   │   │   ├── formatters.ts
│   │   │   └── validators.ts
│   │   └── constants/          # Constants
│   │       └── api.constants.ts
│   ├── core/                   # Core/Infrastructure
│   │   ├── api/                # API client
│   │   │   ├── apiClient.ts    # Base API client
│   │   │   └── websocket.ts    # WebSocket client
│   │   ├── config/             # Configuration
│   │   │   └── app.config.ts
│   │   └── types/              # Global types
│   │       └── global.types.ts
│   ├── styles/                 # Global styles
│   │   ├── globals.css
│   │   └── themes.css
│   └── main.tsx                # Entry point
├── package.json
├── tsconfig.json
├── vite.config.ts              # Vite config (vagy CRA)
└── tailwind.config.js
```

---

### Component Architecture (Clean Code)

#### Példa: SearchBar Component

```typescript
// src/features/search/components/SearchBar.tsx

import React, { useState, useCallback } from 'react';
import { useDebounce } from '@/shared/hooks/useDebounce';
import { Input } from '@/shared/components/Input';
import { Button } from '@/shared/components/Button';

interface SearchBarProps {
  onSearch: (query: string) => void;
  placeholder?: string;
  debounceMs?: number;
}

/**
 * SearchBar component - Handles user input and triggers search
 * 
 * Responsibilities:
 * - Display search input
 * - Debounce user input
 * - Trigger search callback
 * 
 * @param onSearch - Callback function when search is triggered
 * @param placeholder - Placeholder text for input
 * @param debounceMs - Debounce delay in milliseconds
 */
export const SearchBar: React.FC<SearchBarProps> = ({
  onSearch,
  placeholder = 'Search code...',
  debounceMs = 300,
}) => {
  const [query, setQuery] = useState('');
  const debouncedQuery = useDebounce(query, debounceMs);

  // Trigger search when debounced query changes
  React.useEffect(() => {
    if (debouncedQuery.trim()) {
      onSearch(debouncedQuery);
    }
  }, [debouncedQuery, onSearch]);

  const handleClear = useCallback(() => {
    setQuery('');
  }, []);

  const handleSubmit = useCallback((e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query);
    }
  }, [query, onSearch]);

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 w-full max-w-2xl">
      <Input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder={placeholder}
        className="flex-1"
        aria-label="Search query"
      />
      {query && (
        <Button
          type="button"
          onClick={handleClear}
          variant="ghost"
          aria-label="Clear search"
        >
          Clear
        </Button>
      )}
      <Button type="submit" disabled={!query.trim()}>
        Search
      </Button>
    </form>
  );
};
```

#### Példa: useSearch Custom Hook

```typescript
// src/features/search/hooks/useSearch.ts

import { useState, useCallback } from 'react';
import { useQuery } from '@tanstack/react-query';
import { searchService } from '../services/searchService';
import { SearchResult, SearchOptions } from '../types/search.types';

interface UseSearchReturn {
  results: SearchResult[];
  isLoading: boolean;
  error: Error | null;
  search: (query: string, options?: SearchOptions) => void;
  clear: () => void;
}

/**
 * Custom hook for search functionality
 * 
 * Encapsulates search logic, state management, and API interaction
 * 
 * @returns Search state and methods
 */
export const useSearch = (): UseSearchReturn => {
  const [query, setQuery] = useState<string>('');
  const [options, setOptions] = useState<SearchOptions>({});

  const {
    data: results = [],
    isLoading,
    error,
    refetch,
  } = useQuery({
    queryKey: ['search', query, options],
    queryFn: () => searchService.search(query, options),
    enabled: !!query.trim(),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  const search = useCallback((newQuery: string, newOptions?: SearchOptions) => {
    setQuery(newQuery);
    if (newOptions) {
      setOptions(newOptions);
    }
    refetch();
  }, [refetch]);

  const clear = useCallback(() => {
    setQuery('');
    setOptions({});
  }, []);

  return {
    results,
    isLoading,
    error: error as Error | null,
    search,
    clear,
  };
};
```

#### Példa: SearchService (Business Logic)

```typescript
// src/features/search/services/searchService.ts

import { apiClient } from '@/core/api/apiClient';
import { SearchResult, SearchOptions } from '../types/search.types';
import { API_ENDPOINTS } from '@/shared/constants/api.constants';

/**
 * Search Service - Handles all search-related API calls
 * 
 * Responsibilities:
 * - Make API requests
 * - Transform API responses
 * - Handle errors
 */
class SearchService {
  /**
   * Search for code snippets
   * 
   * @param query - Search query string
   * @param options - Additional search options (filters, pagination, etc.)
   * @returns Array of search results
   */
  async search(query: string, options?: SearchOptions): Promise<SearchResult[]> {
    try {
      const response = await apiClient.post<SearchApiResponse>(
        API_ENDPOINTS.QUERY,
        {
          query,
          max_results: options?.maxResults ?? 10,
          project_path: options?.projectPath,
          include_metadata: true,
        }
      );

      return this.transformResults(response);
    } catch (error) {
      console.error('Search failed:', error);
      throw new Error('Failed to fetch search results');
    }
  }

  /**
   * Transform API response to frontend format
   */
  private transformResults(response: SearchApiResponse): SearchResult[] {
    // Transform logic here
    return response.results.map(result => ({
      id: result.id,
      content: result.content,
      filePath: result.metadata.file_path,
      lineNumbers: {
        start: result.metadata.start_line,
        end: result.metadata.end_line,
      },
      relevance: result.score,
      language: this.detectLanguage(result.metadata.file_extension),
    }));
  }

  private detectLanguage(extension: string): string {
    const languageMap: Record<string, string> = {
      '.py': 'python',
      '.js': 'javascript',
      '.ts': 'typescript',
      '.cs': 'csharp',
      // ... more mappings
    };
    return languageMap[extension] || 'text';
  }
}

export const searchService = new SearchService();
```

---

## 🔧 Backend Módosítások

### Új Endpointok

#### 1. Web UI Statikus Fájlok Kiszolgálása

```python
# src/main.py

from fastapi.staticfiles import StaticFiles
from pathlib import Path

# Mount static files for Web UI
ui_dist_path = Path("/app/ui/dist")
if ui_dist_path.exists():
    app.mount("/ui", StaticFiles(directory=str(ui_dist_path), html=True), name="ui")
    logger.info("Web UI mounted at /ui")
else:
    logger.warning("Web UI dist folder not found")

# Redirect root to Web UI
@app.get("/")
async def root():
    return RedirectResponse(url="/ui")
```

#### 2. WebSocket Endpoint (Real-time Indexing Status)

```python
# src/websocket_handler.py (ÚJ)

from fastapi import WebSocket, WebSocketDisconnect
from typing import List
import asyncio
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manages WebSocket connections for real-time updates"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Client connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")

manager = ConnectionManager()

# Add to main.py
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            data = await websocket.receive_text()
            # Echo back (optional)
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

#### 3. Indexing Status Endpoint

```python
# src/main.py

class IndexingStatus(BaseModel):
    is_running: bool
    project_path: Optional[str] = None
    progress: Optional[dict] = None
    started_at: Optional[datetime] = None

# Global indexing state
indexing_state = {
    "is_running": False,
    "project_path": None,
    "progress": None,
    "started_at": None,
}

@app.get("/indexing/status", response_model=IndexingStatus)
async def get_indexing_status():
    """Get current indexing status"""
    return IndexingStatus(**indexing_state)

# Modify index_project to update status
@app.post("/index")
async def index_project(request: IndexRequest, background_tasks: BackgroundTasks):
    global indexing_state
    
    # Update state
    indexing_state["is_running"] = True
    indexing_state["project_path"] = wsl_path
    indexing_state["started_at"] = datetime.now()
    
    # Start indexing in background
    background_tasks.add_task(
        index_with_progress,
        rag_system,
        request.file_extensions,
        request.force_reindex,
        wsl_path
    )
    
    return {"status": "indexing_started", ...}

async def index_with_progress(rag_system, file_extensions, force_reindex, project_path):
    """Index with progress updates via WebSocket"""
    global indexing_state
    
    try:
        # Custom callback to report progress
        def progress_callback(current: int, total: int, file: str):
            progress = {
                "current": current,
                "total": total,
                "file": file,
                "percentage": (current / total * 100) if total > 0 else 0
            }
            indexing_state["progress"] = progress
            
            # Broadcast via WebSocket
            asyncio.create_task(manager.broadcast({
                "type": "indexing_progress",
                "data": progress
            }))
        
        # Run indexing with callback
        result = rag_system.index_project(
            file_extensions=file_extensions,
            force_reindex=force_reindex,
            progress_callback=progress_callback  # NEW parameter
        )
        
        # Broadcast completion
        await manager.broadcast({
            "type": "indexing_complete",
            "data": result
        })
        
    finally:
        # Reset state
        indexing_state["is_running"] = False
        indexing_state["progress"] = None
```

#### 4. Code File Content Endpoint

```python
# src/main.py

class FileContentRequest(BaseModel):
    file_path: str
    project_path: Optional[str] = None

class FileContentResponse(BaseModel):
    content: str
    language: str
    lines: int

@app.post("/file/content", response_model=FileContentResponse)
async def get_file_content(request: FileContentRequest):
    """Get content of a specific file for preview"""
    global rag_systems, current_project
    
    # Determine project
    target_project = request.project_path or current_project
    if not target_project or target_project not in rag_systems:
        raise HTTPException(status_code=404, detail="Project not found")
    
    rag_system = rag_systems[target_project]
    full_path = Path(rag_system.project_root) / request.file_path
    
    if not full_path.exists() or not full_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return FileContentResponse(
            content=content,
            language=full_path.suffix.lstrip('.'),
            lines=len(content.splitlines())
        )
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        raise HTTPException(status_code=500, detail="Failed to read file")
```

---

## 📱 UI Wireframes & Features

### MVP Features (V1)

#### 1. Main Search Page

```
┌────────────────────────────────────────────────────────┐
│  RAG Code Search                    [☀️/🌙] [Settings] │
├────────────────────────────────────────────────────────┤
│                                                        │
│  Project: [AdvancedDatabaseExplorer ▼]                │
│                                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │ 🔍 Search code...                      [Search]  │ │
│  └──────────────────────────────────────────────────┘ │
│                                                        │
│  Results (8 found):                                   │
│  ┌──────────────────────────────────────────────────┐ │
│  │ 📄 python/database_connection.py (lines 25-40)   │ │
│  │ ⭐ Relevance: 95%                     [Copy] [↗] │ │
│  │                                                   │ │
│  │  25  class DatabaseConnection:                   │ │
│  │  26      def __init__(self, conn_string):       │ │
│  │  27          self.connection = ...              │ │
│  │  ...                                             │ │
│  └──────────────────────────────────────────────────┘ │
│  ┌──────────────────────────────────────────────────┐ │
│  │ 📄 csharp/Database/Connection.cs (lines 15-30)   │ │
│  │ ⭐ Relevance: 88%                     [Copy] [↗] │ │
│  │                                                   │ │
│  │  15  public class DatabaseConnection            │ │
│  │  16  {                                           │ │
│  │  17      public DatabaseConnection(string conn) │ │
│  │  ...                                             │ │
│  └──────────────────────────────────────────────────┘ │
│                                                        │
│  [Load More...]                                        │
│                                                        │
└────────────────────────────────────────────────────────┘
```

#### 2. Project Dashboard

```
┌────────────────────────────────────────────────────────┐
│  Projects                           [+ Add Project]    │
├────────────────────────────────────────────────────────┤
│                                                        │
│  ┌─────────────────────┐  ┌─────────────────────┐    │
│  │ AdvancedDatabase... │  │ MyWebApp           │    │
│  │ [CURRENT]           │  │                     │    │
│  │                     │  │                     │    │
│  │ 📁 199 files        │  │ 📁 95 files         │    │
│  │ 📦 1335 chunks      │  │ 📦 723 chunks       │    │
│  │ 🕐 2 hours ago      │  │ 🕐 1 day ago        │    │
│  │                     │  │                     │    │
│  │ [Switch] [Reindex]  │  │ [Switch] [Reindex]  │    │
│  └─────────────────────┘  └─────────────────────┘    │
│                                                        │
│  ┌─────────────────────┐                              │
│  │ BackendAPI         │                              │
│  │                     │                              │
│  │ 📁 150 files        │                              │
│  │ 📦 980 chunks       │                              │
│  │ 🕐 3 days ago       │                              │
│  │                     │                              │
│  │ [Switch] [Reindex]  │                              │
│  └─────────────────────┘                              │
│                                                        │
└────────────────────────────────────────────────────────┘
```

#### 3. Settings Panel

```
┌────────────────────────────────────────────────────────┐
│  Settings                                        [✕]   │
├────────────────────────────────────────────────────────┤
│                                                        │
│  Appearance                                            │
│  ┌──────────────────────────────────────────────────┐ │
│  │ Theme: [🌙 Dark Mode] ☑️                          │ │
│  │ Font size: [Medium ▼]                            │ │
│  │ Syntax theme: [VS Dark ▼]                        │ │
│  └──────────────────────────────────────────────────┘ │
│                                                        │
│  Search Settings                                       │
│  ┌──────────────────────────────────────────────────┐ │
│  │ Max results: [10 ▼]                              │ │
│  │ Auto-search delay: [300ms]                       │ │
│  │ Save search history: ☑️                          │ │
│  └──────────────────────────────────────────────────┘ │
│                                                        │
│  Advanced                                              │
│  ┌──────────────────────────────────────────────────┐ │
│  │ API URL: [http://localhost:8000]                 │ │
│  │ WebSocket: [Enabled ☑️]                          │ │
│  └──────────────────────────────────────────────────┘ │
│                                                        │
│                                    [Cancel] [Save]     │
└────────────────────────────────────────────────────────┘
```

---

## 🚀 Implementation Roadmap

### Phase 1: MVP (Week 1-2)

**Frontend:**
- [x] Setup React + TypeScript + Vite *(kész)*
- [ ] Setup Tailwind CSS + shadcn/ui
- [x] Create basic layout (header, sidebar, main) *(kész)*
- [x] Implement SearchBar component *(kész, dummy)*
- [x] Implement ResultsList component *(kész, dummy)*
- [ ] Implement CodeSnippet component with syntax highlighting
- [ ] Setup API client with Axios
- [x] Implement useSearch hook *(dummy, alap logika)*
- [ ] Connect to backend `/query` endpoint
- [x] Add dark mode toggle *(kész)*
- [x] Basic responsive design *(alap szint, kész)*

**Backend:**
- [ ] Add static file serving for Web UI
- [ ] Test existing `/query` endpoint with Web UI
- [ ] Add CORS headers for local development
- [ ] Add `/file/content` endpoint for file preview

**Testing:**
- [ ] Manual testing on Chrome, Firefox, Safari
- [ ] Test responsive design on mobile

---

### Phase 2: Enhanced Features (Week 3-4)

**Frontend:**
- [ ] Implement ProjectSelector component
- [ ] Implement ProjectDashboard page
- [ ] Add search history with localStorage
- [ ] Implement copy-to-clipboard functionality
- [ ] Add "Share link" feature (URL params)
- [ ] Implement SettingsPanel
- [ ] Add export to Markdown functionality
- [ ] Improve accessibility (ARIA labels, keyboard nav)

**Backend:**
- [ ] Add WebSocket endpoint for real-time updates
- [ ] Modify indexing to report progress
- [ ] Add `/indexing/status` endpoint
- [ ] Add `/projects/tree` endpoint (file browser)

---

### Phase 3: Advanced Features (Week 5-6)

**Frontend:**
- [ ] Implement file browser view
- [ ] Add Monaco Editor for full file preview
- [ ] Implement advanced filters (file type, language, path)
- [ ] Add query history panel
- [ ] Add bookmarks/favorites
- [ ] Implement real-time indexing progress UI
- [ ] Add animations and loading states
- [ ] Performance optimization (code splitting, lazy loading)

**Backend:**
- [ ] Optimize API responses for large result sets
- [ ] Add pagination support
- [ ] Add query caching improvements
- [ ] Add API rate limiting (if needed)

---

### Phase 4: Optional Enhancements (Future)

- [ ] Multi-user support (authentication)
- [ ] Collaborative features (shared projects)
- [ ] Code diff viewer
- [ ] AI-powered query suggestions
- [ ] Browser extension
- [ ] Mobile app (React Native or PWA)

---

## 🧪 Testing Strategy

### Unit Tests

```typescript
// Example: SearchBar.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { SearchBar } from './SearchBar';

describe('SearchBar', () => {
  it('should render search input', () => {
    render(<SearchBar onSearch={jest.fn()} />);
    expect(screen.getByPlaceholderText(/search/i)).toBeInTheDocument();
  });

  it('should call onSearch with debounced value', async () => {
    const onSearch = jest.fn();
    render(<SearchBar onSearch={onSearch} debounceMs={100} />);
    
    const input = screen.getByRole('textbox');
    fireEvent.change(input, { target: { value: 'test query' } });
    
    await waitFor(() => {
      expect(onSearch).toHaveBeenCalledWith('test query');
    }, { timeout: 200 });
  });

  it('should clear search when clear button clicked', () => {
    render(<SearchBar onSearch={jest.fn()} />);
    
    const input = screen.getByRole('textbox');
    fireEvent.change(input, { target: { value: 'test' } });
    
    const clearButton = screen.getByLabelText(/clear/i);
    fireEvent.click(clearButton);
    
    expect(input).toHaveValue('');
  });
});
```

### Integration Tests

```typescript
// Example: Search flow integration test
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { SearchPage } from './SearchPage';
import { searchService } from './services/searchService';

jest.mock('./services/searchService');

describe('Search Integration', () => {
  it('should display results after search', async () => {
    const mockResults = [
      { id: '1', content: 'test code', filePath: 'test.py' }
    ];
    
    (searchService.search as jest.Mock).mockResolvedValue(mockResults);
    
    const queryClient = new QueryClient();
    render(
      <QueryClientProvider client={queryClient}>
        <SearchPage />
      </QueryClientProvider>
    );
    
    const input = screen.getByPlaceholderText(/search/i);
    fireEvent.change(input, { target: { value: 'database' } });
    
    const searchButton = screen.getByText(/search/i);
    fireEvent.click(searchButton);
    
    await waitFor(() => {
      expect(screen.getByText('test code')).toBeInTheDocument();
      expect(screen.getByText('test.py')).toBeInTheDocument();
    });
  });
});
```

### E2E Tests (Playwright)

```typescript
// e2e/search.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Search functionality', () => {
  test('should search and display results', async ({ page }) => {
    await page.goto('http://localhost:3000');
    
    // Enter search query
    await page.fill('input[aria-label="Search query"]', 'database connection');
    await page.click('button:has-text("Search")');
    
    // Wait for results
    await page.waitForSelector('[data-testid="search-results"]');
    
    // Verify results are displayed
    const results = await page.locator('[data-testid="result-item"]').count();
    expect(results).toBeGreaterThan(0);
    
    // Verify syntax highlighting
    await expect(page.locator('.language-python')).toBeVisible();
  });
  
  test('should copy code to clipboard', async ({ page, context }) => {
    await context.grantPermissions(['clipboard-read', 'clipboard-write']);
    
    await page.goto('http://localhost:3000');
    await page.fill('input[aria-label="Search query"]', 'test');
    await page.click('button:has-text("Search")');
    
    await page.waitForSelector('[data-testid="copy-button"]');
    await page.click('[data-testid="copy-button"]');
    
    // Verify clipboard content
    const clipboardText = await page.evaluate(() => navigator.clipboard.readText());
    expect(clipboardText).toContain('class');
  });
});
```

---

## 📦 Deployment

### Docker Integration

```dockerfile
# Dockerfile (módosított)

# Stage 1: Build Frontend
FROM node:18-alpine AS frontend-builder
WORKDIR /app/ui
COPY ui/package*.json ./
RUN npm ci
COPY ui/ ./
RUN npm run build

# Stage 2: Python Backend
FROM python:3.11-slim

WORKDIR /app

# Copy backend
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
COPY config/ ./config/

# Copy frontend build
COPY --from=frontend-builder /app/ui/dist /app/ui/dist

# Expose ports
EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml (módosított)

```yaml
version: '3.9'

```
┌────────────────────────────────────────────────────────┐
│  Project Details                                      │
├────────────────────────────────────────────────────────┤
│                                                        │
│  ┌─────────────────────┐                              │
│  │ AdvancedDatabase... │                              │
│  │ [CURRENT]           │                              │
│  │                     │                              │
│  │ 📁 199 files        │                              │
│  │ 📦 1335 chunks      │                              │
│  │ 🕐 2 hours ago      │                              │
│  │                     │                              │
│  │ [Reindex]           │                              │
│  └─────────────────────┘                              │
│                                                        │
└────────────────────────────────────────────────────────┘
```
        proxy_set_header X-Real-IP $remote_addr;
    }

    # API
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # WebSocket
    location /ws {
        proxy_pass http://localhost:8000/ws;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

2. **SSL/HTTPS** (Let's Encrypt)
3. **Authentication** (ha nem local-only)
4. **Rate Limiting** (API protection)
5. **Monitoring** (Prometheus + Grafana)

---

## 📚 Documentation

### User Documentation

Create `ui/README.md`:
- How to use the Web UI
- Features overview
- Keyboard shortcuts
- Troubleshooting

### Developer Documentation

Create `ui/CONTRIBUTING.md`:
- Setup development environment
- Code style guide (ESLint, Prettier)
- Component guidelines
- Testing requirements
- Pull request process

---

## 🎯 Success Metrics

### Performance Targets

- **Initial Load**: < 2 seconds
- **Search Response**: < 500ms (with cache)
- **Search Response**: < 3 seconds (without cache)
- **WebSocket Latency**: < 100ms
- **Lighthouse Score**: > 90

### User Experience Targets

- **Accessibility Score**: WCAG 2.1 AA compliant
- **Mobile Responsive**: 100% functional on mobile
- **Browser Support**: Chrome, Firefox, Safari, Edge (latest 2 versions)

---

## 📝 Code Quality Standards

### TypeScript

- Strict mode enabled
- No `any` types (use `unknown` if needed)
- Explicit return types for functions
- Interfaces over types (for extensibility)

### React

- Functional components only (no class components)
- Custom hooks for reusable logic
- PropTypes or TypeScript interfaces for props
- Memoization for expensive computations (useMemo, useCallback)

### CSS

- Tailwind utility classes preferred
- BEM naming for custom CSS (if needed)
- No inline styles (use className)

### Testing

- Unit test coverage: > 80%
- Integration tests for critical flows
- E2E tests for main user journeys

### Code Review

- All PRs require review
- Automated checks: ESLint, Prettier, TypeScript, Tests
- No merge if CI fails

---

## 🔮 Future Enhancements

1. **AI Query Suggestions**: Suggest related queries based on search
2. **Code Visualization**: Dependency graphs, call trees
3. **Collaborative Features**: Real-time multi-user editing/browsing
4. **Browser Extension**: Quick search from any page
5. **Mobile App**: Native iOS/Android or PWA
6. **API Playground**: Test API endpoints directly from UI
7. **Code Snippets Library**: Save and organize frequently used snippets
8. **Integration with IDEs**: VS Code extension that embeds the UI

---

## 📞 Contact & Support

For questions or issues:
- GitHub Issues: [repo]/issues
- Documentation: [repo]/docs
- Email: support@example.com

---

**Happy Coding! 🚀**
