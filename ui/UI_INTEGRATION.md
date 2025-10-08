# Local RAG Server - Web UI Integration

## Áttekintés

A Web UI teljes mértékben integrálva van a RAG szerverrel. Minden komponens és service bekötésre került, hogy a valós API végpontokat használják.

## Implementált funkciók

### 1. **API Client** (`src/core/api/apiClient.ts`)
- Axios alapú API kliens konfiguráció
- Automatikus hibakezelés
- Timeout és retry logika
- Environment változó alapú base URL

### 2. **Service réteg**

#### Project Service (`src/features/projects/services/projectService.ts`)
- `listProjects()` - Összes projekt listázása
- `switchProject()` - Aktív projekt váltása
- `getProjectStats()` - Projekt statisztikák lekérése
- `clearProject()` - Projekt törlése

#### Search Service (`src/features/search/services/searchService.ts`)
- `queryRAG()` - RAG lekérdezés végrehajtása
- `getHealth()` - Szerver health check

#### Index Service (`src/features/indexing/services/indexService.ts`)
- `indexProject()` - Új projekt indexelése
- `reindexProject()` - Projekt újraindexelése

#### Model Service (`src/features/settings/services/modelService.ts`)
- `getAvailableModels()` - Elérhető embedding modellek
- `getCurrentModel()` - Aktuális model lekérése
- `setProjectModel()` - Model beállítása projekthez

### 3. **Custom Hooks**

#### `useProjects()` - Projekt kezelés
```typescript
const { 
  projects,        // Projektek listája
  currentProject,  // Aktív projekt
  loading,         // Betöltés állapot
  error,           // Hiba üzenet
  refetch,         // Újratöltés
  selectProject    // Projekt váltás
} = useProjects();
```

#### `useSearch()` - Keresés
```typescript
const { 
  result,   // Keresési eredmény
  loading,  // Betöltés állapot
  error,    // Hiba üzenet
  search,   // Keresés függvény
  clear     // Eredmények törlése
} = useSearch();
```

#### `useIndexing()` - Indexelés
```typescript
const { 
  loading,        // Betöltés állapot
  error,          // Hiba üzenet
  status,         // Indexelés státusza
  startIndexing,  // Indexelés indítása
  reindex         // Újraindexelés
} = useIndexing();
```

### 4. **Komponensek**

#### `<SearchBar />` - Keresősáv
- Valós idejű keresés a RAG szerveren keresztül
- Betöltési állapot kezelés
- Hibakezelés

#### `<ResultsList />` - Eredmények megjelenítése
- Optimalizált prompt megjelenítése
- Context chunks és token számok
- Metadata információk
- Projekt részletek

#### `<ProjectSelector />` - Projekt választó
- Dropdown az indexelt projektek közötti váltáshoz
- Fájl számok megjelenítése
- Aktív projekt kiemelése

#### `<ProjectList />` - Projekt lista
- Összes projekt megjelenítése kártyákban
- Kattintással váltható projektek
- Aktív projekt jelzése

#### `<ProjectCard />` - Projekt kártya
- Projekt név, útvonal
- Indexelt fájlok és chunks száma
- Aktív státusz megjelenítése

#### `<ProjectDetails />` - Projekt részletek
- Teljes statisztika az aktív projektről
- Vector DB méret
- Embedding model információk

#### `<IndexButton />` - Indexelés gomb
- Új projekt hozzáadása
- Projekt útvonal megadása
- Indexelés indítása

#### `<ModelSelector />` - Model választó
- Elérhető embedding modellek listája
- Aktuális model megjelenítése
- Model váltás funkció

### 5. **App.tsx - Főkomponens**
Teljes mértékben átírt alkalmazás struktúra:
- Összes komponens integrációja
- Hibakezelés megjelenítése
- Indexelési státusz
- Keresési eredmények

## API Végpontok használata

### Backend endpointok (FastAPI):
- `GET /health` - Szerver állapot
- `GET /projects` - Projektek listázása
- `POST /switch` - Projekt váltás
- `GET /stats` - Statisztikák
- `POST /index` - Indexelés
- `POST /query` - RAG keresés
- `GET /models` - Elérhető modellek
- `GET /projects/model` - Projekt modellje
- `POST /projects/model/change` - Model váltás
- `DELETE /clear` - Projekt törlés

## Konfiguráció

### Environment változók (`.env`)
```env
VITE_API_URL=http://localhost:8000
```

### API Client beállítások
- Base URL: `http://localhost:8000` (default)
- Timeout: 30 másodperc
- Content-Type: application/json
- Automatikus error interceptor

## Használat

### 1. Backend indítása
```bash
docker-compose up -d
```

### 2. Frontend indítása
```bash
cd ui
npm install
npm run dev
```

### 3. Böngészőben nyisd meg
```
http://localhost:5173
```

## Funkciók használata

### Új projekt indexelése
1. Kattints az "Új projekt indexelése" gombra
2. Add meg a projekt útvonalát (pl. `C:\Projects\myapp`)
3. Kattints az "Indexelés indítása" gombra
4. Várd meg az indexelés befejezését

### Keresés
1. Válaszd ki a projekteket a dropdown menüből
2. Gépelje be a keresési lekérdezést
3. Kattints a "Keresés" gombra
4. Az eredmények megjelennek alul

### Projekt váltás
1. Használd a projekt dropdown menüt
2. Vagy kattints egy projekt kártyára a listában

### Model váltás
1. Válaszd ki az új modelt a dropdown menüből
2. A rendszer automatikusan újraindexeli a projektet

## Következő lépések

- [ ] WebSocket támogatás valós idejű indexelési progress-hez
- [ ] Dark/Light theme váltó implementálása
- [ ] Keresési előzmények megjelenítése
- [ ] Részletes error üzenetek
- [ ] Progress bar az indexeléshez
- [ ] Fájl böngésző a projekt struktúra megtekintéséhez

## Hibaelhárítás

### "Nem sikerült kapcsolódni a szerverhez"
- Ellenőrizd, hogy a backend fut-e: `docker-compose ps`
- Ellenőrizd az API URL-t a `.env` fájlban
- Nézd meg a browser console-t hibákért

### "No project indexed"
- Indexelj legalább egy projektet az "Új projekt indexelése" gombbal
- Ellenőrizd, hogy az útvonal helyes-e

### TypeScript hibák
- Futtasd: `npm run type-check`
- Ellenőrizd a típusdefiníciókat

## Fejlesztői jegyzetek

- Minden komponens TypeScript-ben van írva
- React Hooks használata állapotkezelésre
- Service layer pattern az API hívásokhoz
- Error boundary-k a hibakezeléshez (TODO)
- Responsive design (alapvető)
