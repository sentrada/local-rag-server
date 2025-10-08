# Embedding Model Support - Implementation Summary

## Implementált Funkciók

### 1. Backend (Python/FastAPI)

#### Új API Endpointok:
- `GET /models` - Elérhető embedding modellek listája
- `GET /projects/model?project_path=...` - Projekt aktuális modellje
- `POST /projects/model/change?project_path=...` - Modell váltás (index törlés + opcionális reindex)

#### Modell Kezelés:
- 4 embedding modell támogatása:
  - `all-MiniLM-L6-v2` (~80MB)
  - `paraphrase-multilingual-MiniLM-L12-v2` (~120MB)
  - `paraphrase-multilingual-mpnet-base-v2` (~1GB)
  - `intfloat/multilingual-e5-large` (~2.2GB)

#### Projekt Metadata:
- Minden projekt metadata tartalmazza az `embedding_model` mezőt
- Mentés: `src/rag_system.py` `_save_metadata()` metódus
- Betöltés: Automatikus startup-kor

#### Index Endpoint Bővítés:
- `POST /index` most fogadja a `model` paramétert
- Ha nincs megadva, az előző projekt modellt vagy az alapértelmezettet használja

### 2. Frontend (React/TypeScript)

#### Új Komponensek:
- `ModelSelector.tsx` - Dropdown modell választáshoz
- `ModelInfo.tsx` - Modell részletek megjelenítése (méret, sebesség, pontosság)
- `ModelChangeModal.tsx` - Megerősítő modal modellváltáshoz (figyelmeztetéssel)
- `Select.tsx` - Általános select komponens

#### Szolgáltatások:
- `modelService.ts` - API hívások modellkezeléshez
  - `getAvailableModels()`
  - `getCurrentModel(projectPath)`
  - `setProjectModel(projectPath, model, autoReindex)`

#### Hookok:
- `useModelChange.ts` - Modellváltás logika (loading, error, success states)

#### UI Integráció:
- `SettingsPanel.tsx` frissítve modell választóval
- Progress indikátor újraindexeléshez
- Success/Error üzenetek

#### API Client:
- `apiClient.ts` konfigurálva axios-szal (base URL: http://localhost:8000)

### 3. PowerShell Scriptek

#### Frissített Scriptek:
- `Reindex-Project.ps1` - Új `-Model` paraméter hozzáadva
- `Change-Model.ps1` - Új script modellváltáshoz interaktív megerősítéssel

#### Használat:
```powershell
# Indexelés megadott modellel
.\Reindex-Project.ps1 -ProjectPath "C:\..." -Model "paraphrase-multilingual-MiniLM-L12-v2"

# Modellváltás
.\Change-Model.ps1 -ProjectPath "C:\..." -Model "intfloat/multilingual-e5-large" -AutoReindex
```

### 4. Dokumentáció

#### Új Dokumentumok:
- `docs/EMBEDDING_MODELS.md` - Modellek összehasonlítása, használati útmutató
- `docs/API_REFERENCE.md` - Új API endpointok dokumentációja

#### Frissített Dokumentumok:
- `README.md` - Modellek szekció, API példák
- `docs/QUICKSTART.md` - Modell választás példákkal

## Fontos Megjegyzések

### Modellváltás Folyamata:
1. Felhasználó kiválasztja az új modellt UI-ból vagy scriptből
2. Megerősítő modal/prompt jelenik meg (figyelmeztetés az index törlésről)
3. Backend törli a régi projekt indexet és cache-t
4. Ha `auto_reindex=true`, új RAG system jön létre az új modellel
5. Háttérben újraindexelés indul (vagy manuálisan később)

### Teljesítmény:
- Nagyobb modellek (mpnet, e5-large) lassabbak, de pontosabbak
- UI figyelmezteti a felhasználót
- Modell info megjelenik minden modellnél (sebesség, méret, pontosság)

### Docker Image Méret:
- A nagyobb modellek növelik az image méretet
- Első használatkor automatikusan letöltődnek (sentence-transformers)
- Offline használathoz pre-download szükséges (Dockerfile módosítás)

### Cache Kezelés:
- Modellváltáskor a Redis cache törlődik az adott projekthez
- Új modellel új embeddings generálódnak

## Jövőbeli Fejlesztések

1. **Pre-download modellek Dockerfile-ban**: Hozzáadni a modelleket a build-hez, hogy offline is működjön
2. **Model warm-up**: Első query-nél előre betölteni a modellt
3. **Progressbar újraindexeléshez**: Real-time progress WebSocket-tel
4. **Model performance metrikák**: Indexelési idő, query sebesség mérése
5. **Model összehasonlító view**: Több modell teljesítményének összehasonlítása

## Tesztelés

### Backend Tesztelés:
```powershell
# Server indítása
docker-compose up -d

# Modellek listázása
curl http://localhost:8000/models

# Projekt modelljének lekérdezése
curl "http://localhost:8000/projects/model?project_path=/app/data/projects/TestProject"

# Modellváltás
curl -X POST "http://localhost:8000/projects/model/change?project_path=/app/data/projects/TestProject" `
  -H "Content-Type: application/json" `
  -d '{"model": "intfloat/multilingual-e5-large", "auto_reindex": true}'
```

### Frontend Tesztelés:
```powershell
cd ui
npm install
npm run build
npm run dev
```
Böngésző: http://localhost:5173

### Script Tesztelés:
```powershell
.\Reindex-Project.ps1 -ProjectPath "/app/data/projects/TestProject" -Model "all-MiniLM-L6-v2"
.\Change-Model.ps1 -ProjectPath "/app/data/projects/TestProject" -Model "paraphrase-multilingual-mpnet-base-v2"
```

## Státusz

✅ Backend API implementálva  
✅ Frontend komponensek implementálva  
✅ PowerShell scriptek frissítve  
✅ Dokumentáció frissítve  
✅ Build sikeres  
⏳ Docker image frissítés (pre-download modellek)  
⏳ Integrációs tesztek  
⏳ Production deployment  

---

**Implementáció dátuma**: 2025-10-08  
**Verzió**: 2.1.0 (embedding model support)
