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

## Gyors Indítás

### 1. Környezet beállítása

```powershell
# Projekt könyvtár beállítása a .env fájlban
# Másold át és szerkeszd:
Copy-Item .env.example .env

# Szerkeszd a PROJECT_PATH értékét a .env fájlban
# Példa: PROJECT_PATH=/mnt/c/Users/YourName/Projects
```

### 2. Docker konténerek indítása

```powershell
docker-compose up -d
```

### 3. Egészség ellenőrzés

```powershell
curl http://localhost:8000/health
```

## API Használat

### Projekt indexelése

```powershell
# PowerShell
$body = @{
    project_path = "C:\Users\YourName\YourProject"
    file_extensions = @(".py", ".js", ".ts", ".jsx", ".tsx")
    force_reindex = $false
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://localhost:8000/index" -Body $body -ContentType "application/json"
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

# Embedding modell
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Redis cache (opcionális de ajánlott)
REDIS_URL=redis://redis:6379/0
```

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
