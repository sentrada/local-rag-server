# Local RAG Server for GitHub Copilot

Egy helyi RAG (Retrieval-Augmented Generation) szerver, amely kiterjeszti a GitHub Copilot képességeit nagyobb projektek kezelésére és a timeout problémák elkerülésére.

## Főbb Funkciók

- 🚀 **Intelligens kód indexelés** - Automatikusan indexeli a projekt fájljait
- 🔍 **Szemantikus keresés** - ChromaDB vektoros keresés használatával
- ⚡ **Redis cache** - Gyorsabb válaszidők és timeout elkerülése
- 🧩 **Okos chunking** - Intelligens kóddarabolás függvények és osztályok szerint
- 🎯 **Token optimalizálás** - Automatikus kontextus optimalizálás a token limithez
- 🐳 **Docker support** - Egyszerű telepítés és használat
- 💾 **Perzisztens index** - Az indexelés megmarad konténer újraindítás után (nincs időkorlát!)
- 🎨 **Multi-project support** - Több projekt egyidejű kezelése
- 🤖 **Választható embedding modellek** - 4 különböző modell közül választhatsz projektenként
- 🌐 **Web UI** - Modern React-alapú felület projektek kezelésére (✨ ÚJ!)

## Gyors Indítás

### 1. Backend indítása

```powershell
# Docker konténerek indítása
docker-compose up -d

# Egészség ellenőrzés
curl http://localhost:8000/health
```

### 2. Web UI indítása (ÚJ!)

```powershell
# UI könyvtárba lépés
cd ui

# Függőségek telepítése (első alkalommal)
npm install

# Fejlesztői szerver indítása
npm run dev
```

Majd nyisd meg a böngészőben: **http://localhost:5173**

### 3. Használat Web UI-ból

1. Kattints az "**Új projekt indexelése**" gombra
2. Add meg a projekt útvonalát (pl. `C:\Projects\myapp`)
3. Várd meg az indexelés befejezését
4. Használd a keresőt kontextus lekérdezéshez!

## Web UI Funkciók

A teljesen integrált Web UI a következőket teszi lehetővé:

- 📋 **Projektek kezelése** - Lista, váltás, statisztikák
- 🔍 **Keresés** - Valós idejű RAG keresés vizuális eredményekkel
- ⚙️ **Beállítások** - Embedding model váltás projektenként
- 📊 **Statisztikák** - Indexelt fájlok, chunks, token számok
- 🎯 **Optimalizált prompt** - Látható kontextus előnézet

### UI Dokumentáció
- 📖 [UI Integration Guide](ui/UI_INTEGRATION.md) - Részletes integráció dokumentáció
- 📝 [Integration Changelog](ui/INTEGRATION_CHANGELOG.md) - Változások listája

## API Használat

### Projekt indexelése

```powershell
# PowerShell
$body = @{
    project_path = "C:\Users\YourName\YourProject"
    file_extensions = @(".py", ".js", ".ts", ".jsx", ".tsx")
    model = "paraphrase-multilingual-MiniLM-L12-v2"  # Opcionális, választható embedding modell
    force_reindex = $false
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://localhost:8000/index" -Body $body -ContentType "application/json"
```

### Elérhető embedding modellek lekérdezése

```powershell
Invoke-RestMethod -Method Get -Uri "http://localhost:8000/models"
```

### Projekt aktuális modelljének lekérdezése

```powershell
$projectPath = "C:\Users\YourName\YourProject"
Invoke-RestMethod -Method Get -Uri "http://localhost:8000/projects/model?project_path=$projectPath"
```

### Modell váltása projektre

```powershell
$projectPath = "C:\Users\YourName\YourProject"
$body = @{
    model = "intfloat/multilingual-e5-large"
    auto_reindex = $true
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://localhost:8000/projects/model/change?project_path=$projectPath" -Body $body -ContentType "application/json"
```

### Kontextus lekérdezése

```powershell
$body = @{
    query = "How does the authentication system work?"
    max_results = 5
    include_metadata = $true
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://localhost:8000/query" -Body $body -ContentType "application/json"
```

### Statisztikák

```powershell
Invoke-RestMethod -Method Get -Uri "http://localhost:8000/stats"
```

## Támogatott Nyelvek

- Python (.py)
- JavaScript/TypeScript (.js, .ts, .jsx, .tsx)
- Java (.java)
- C# (.cs)
- C/C++ (.cpp, .c, .h)
- Go (.go)
- Rust (.rs)
- Ruby (.rb)
- PHP (.php)
- Swift (.swift)
- Kotlin (.kt)
- Vue (.vue)

## Konfiguráció

A `.env` fájlban:

```env
# Projekt útvonal (Windows vagy WSL formátum)
PROJECT_PATH=/mnt/c/Users/YourName/Projects

# Log szint
LOG_LEVEL=INFO

# Maximum token limit
MAX_CONTEXT_TOKENS=4000

# Embedding modell (alapértelmezett)
# Választható modellek:
# - all-MiniLM-L6-v2 (legkisebb, ~80MB, gyors)
# - paraphrase-multilingual-MiniLM-L12-v2 (ajánlott, ~120MB)
# - paraphrase-multilingual-mpnet-base-v2 (nagy, ~1GB, pontosabb)
# - intfloat/multilingual-e5-large (legnagyobb, ~2.2GB, legpontosabb)
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2

# Redis cache (opcionális de ajánlott)
REDIS_URL=redis://redis:6379/0
```

## Embedding Modellek

A rendszer 4 különböző embedding modellt támogat projektenként:

| Modell | Méret | Sebesség | Nyelvek | Pontosság | Használat |
|--------|-------|----------|---------|-----------|-----------|
| all-MiniLM-L6-v2 | ~80MB | Gyors | EN | Közepes | Kis projektek, angol |
| paraphrase-multilingual-MiniLM-L12-v2 | ~120MB | Gyors | Multi | Jó | Ajánlott általános használatra |
| paraphrase-multilingual-mpnet-base-v2 | ~1GB | Lassabb | Multi | Nagyon jó | Nagyobb projektek, pontosság fontos |
| intfloat/multilingual-e5-large | ~2.2GB | Lassú | Multi | Legjobb | Amikor a maximális pontosság számít |

**Fontos:** Modell váltáskor a projekt indexe törlődik és újraindexelés szükséges!

Részletes információ: [docs/EMBEDDING_MODELS.md](docs/EMBEDDING_MODELS.md)

## GitHub Copilot Integráció

### MCP (Model Context Protocol) használata

A szerver MCP szerverként is használható GitHub Copilot Extensions-zel:

1. Telepítsd a GitHub Copilot Chat MCP extensiont
2. Add hozzá ezt a szervered a konfigurációhoz
3. Használd a `/rag` parancsot a chatben

### Direkt API használat

Készíts egy VS Code extensiont vagy scriptet, amely:
1. Elküldi a kérdést a `/query` endpointra
2. A választ beilleszti a Copilot promptba
3. Profit! 🎉

## Architektúra

```
┌─────────────────┐
│  GitHub Copilot │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│   RAG Server    │◄────►│ Redis Cache  │
│   (FastAPI)     │      └──────────────┘
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│  Vector Store   │      │ Code Parser  │
│   (ChromaDB)    │◄────►│ (Chunking)   │
└─────────────────┘      └──────────────┘
```

## Teljesítmény Optimalizálás

### Timeout elkerülése
- **Redis cache**: A gyakori lekérdezések gyorsak (1 óra TTL)
- **Háttér indexelés**: Az indexelés nem blokkolja a queryket
- **Token limitelés**: Automatikus kontextus optimalizálás
- **Intelligens chunking**: Csak a releváns kódrészletek

### Nagyobb projektek
- **Inkrementális indexelés**: Csak a megváltozott fájlok újraindexelése
- **Fájl szűrés**: node_modules, .git stb. kihagyása
- **Batch processing**: Nagy fájlok darabolása
- **Persistent storage**: ChromaDB perzisztens tárolás

## Hibakeresés

### Logok megtekintése

```powershell
docker-compose logs -f rag-server
```

### Konténer újraindítása

```powershell
docker-compose restart rag-server
```

### Cache törlése

```powershell
Invoke-RestMethod -Method Delete -Uri "http://localhost:8000/clear"
```

## Fejlesztés

### Helyi futtatás (Docker nélkül)

```powershell
# Virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Függőségek
pip install -r requirements.txt

# Redis indítása (WSL vagy Docker)
docker run -d -p 6379:6379 redis:7-alpine

# Szerver indítása
python -m uvicorn src.main:app --reload --port 8000
```

## Troubleshooting

### "Connection refused" hiba
- Ellenőrizd, hogy a Docker konténerek futnak-e: `docker ps`
- Újraindítás: `docker-compose restart`

### "No project indexed" hiba
- Először indexeld a projektet a POST `/index` endpoint használatával

### Lassú indexelés
- Csökkentsd a fájl extensionök számát
- Zárj ki nagyobb könyvtárakat (node_modules, stb.)
- Használj kisebb embedding modellt

### High memory usage
- Csökkentsd a `chunk_size` értéket a code_parser.py-ban
- Töröld a cache-t rendszeresen
- Limitáld a `max_results` értéket a queryknél

## Licence

MIT

## Szerző

Készítette: [Your Name]

---

**Megjegyzés**: Ez egy lokális RAG szerver, amely privát és biztonságos - az adatok nem hagyják el a gépedet!
