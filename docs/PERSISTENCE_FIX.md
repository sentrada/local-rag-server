# Perzisztencia Javítás - Index Megőrzése Újraindítás Után

## Probléma

Ha egy ideig nem kérdeztél a RAG szervertől, utána a projekt "eltűnt", és újra kellett indexelni. Ez azért történt, mert:

1. **Az indexelési metadata csak memóriában volt** - Az `_indexed_files` dictionary nem volt perzisztensen tárolva
2. **A RAG system nem töltődött be automatikusan** - Konténer újraindítás után a `rag_systems` dictionary üres volt
3. **Az indexelési információ elveszett** - Bár a ChromaDB adatok megmaradtak, a rendszer nem tudta, hogy mely projektek vannak indexelve

## Megoldás

### 1. Perzisztens Metadata Tárolás

A `rag_system.py`-ban hozzáadtuk a metadata fájl kezelést:

```python
# Metadata fájl mentése indexelés után
self._metadata_file = self.vector_db_path / f"metadata_{collection_name}.json"

def _save_metadata(self):
    """Mentés: indexed files + total chunks + project root"""
    metadata = {
        "indexed_files": self._indexed_files,
        "total_chunks": self._total_chunks,
        "project_root": str(self.project_root)
    }
    with open(self._metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)

def _load_metadata(self) -> dict:
    """Betöltés induláskor"""
    if self._metadata_file.exists():
        with open(self._metadata_file, 'r') as f:
            metadata = json.load(f)
            self._total_chunks = metadata.get("total_chunks", 0)
            return metadata.get("indexed_files", {})
    return {}
```

### 2. Automatikus Projekt Betöltés

A `main.py`-ban hozzáadtuk az automatikus projekt betöltést a szerver indításakor:

```python
def load_existing_projects():
    """Automatikusan betölti a korábban indexelt projekteket"""
    
    # Megkeresi az összes metadata fájlt
    metadata_files = list(chroma_db_path.glob("metadata_*.json"))
    
    for metadata_file in metadata_files:
        # Beolvassa a projekt adatait
        metadata = json.load(open(metadata_file))
        project_root = metadata.get("project_root")
        
        # Létrehozza a RAG system-et
        rag_system = LocalRAGSystem(...)
        rag_systems[project_root] = rag_system

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Induláskor betölti a projekteket
    load_existing_projects()
    yield
```

## Eredmény

### Előtte

```
Konténer újraindul
  ↓
Ask-RAG.ps1 futtatása
  ↓
❌ "No projects indexed!"
  ↓
Újra kell indexelni .\Reindex-Project.ps1
```

### Utána

```
Konténer újraindul
  ↓
Automatikusan betölti a projekteket
  ↓
Ask-RAG.ps1 futtatása
  ↓
✅ Működik, azonnal válaszol!
```

## Tesztelés

```powershell
# 1. Indexelj egy projektet
.\Reindex-Project.ps1

# 2. Kérdezz
.\Ask-RAG.ps1 "Show me database connections"
# ✅ Működik

# 3. Indítsd újra a konténert
docker-compose restart rag-server

# 4. Várj 10 másodpercet, majd kérdezz újra
Start-Sleep -Seconds 10
.\Ask-RAG.ps1 "Show me database connections"
# ✅ Továbbra is működik, ÚJRAINDEXELÉS NÉLKÜL!
```

## Log Ellenőrzés

```powershell
docker-compose logs --tail 50 rag-server | Select-String "Loading|Loaded"
```

Sikeres betöltés esetén látható:
```
Loading existing indexed projects...
Found 1 metadata files
Loading project: /app/data/projects/AdvancedDatabaseExplorer
Loaded 199 previously indexed files from metadata
✅ Loaded project: /app/data/projects/AdvancedDatabaseExplorer (199 files)
Successfully loaded 1 projects
```

## Metadata Fájl Helye

```
/app/data/chroma_db/metadata_code_chunks_<ProjectName>_<Hash>.json
```

Windows-on (Docker volume):
```
\\wsl$\docker-desktop-data\data\docker\volumes\local-rag-server_chroma-data\_data\
```

## Előnyök

✅ **Nincs idő korlát** - Az index addig él, amíg a Docker volume
✅ **Automatikus helyreállítás** - Konténer újraindítás után azonnal használható
✅ **Nincs felesleges újraindexelés** - Időmegtakarítás
✅ **Multi-projekt támogatás** - Minden projekt külön metadata fájllal rendelkezik
✅ **Perzisztens tárolás** - ChromaDB + metadata JSON fájlok

## Megjegyzések

- A metadata fájl csak akkor jön létre, ha **legalább egyszer futott az indexelés az új kóddal**
- Ha törlöd a Docker volume-ot (`docker volume rm chroma-data`), akkor minden elveszik
- A metadata fájl mérete kis (kb. 30 KB 200 fájlnál)
- A betöltés gyors (1-2 másodperc)

## Hibaelhárítás

### Ha mégsem töltődik be a projekt

```powershell
# Ellenőrizd, hogy létezik-e a metadata fájl
docker exec local-rag-server ls -la /app/data/chroma_db/ | Select-String "metadata"

# Ha nincs, futtasd újra az indexelést
.\Reindex-Project.ps1 -ForceReindex

# Utána újraindítás
docker-compose restart rag-server
```

### Ha rossz adatokat látsz

```powershell
# Törölj mindent és kezdd újra
docker-compose down
docker volume rm local-rag-server_chroma-data
docker-compose up -d
.\Reindex-Project.ps1
```

---

**Verzió:** 2.1.0  
**Dátum:** 2025-10-07  
**Szerző:** RAG System Improvements
