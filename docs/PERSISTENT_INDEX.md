# ✅ JAVÍTÁS KÉSZ - Perzisztens Index

## Mi volt a probléma?

Ha egy ideig nem kérdeztél a RAG szervertől, utána a projekt "eltűnt", és újra kellett indexelni.

## Mi a megoldás?

**Mostantól az indexelés PERZISZTENS** - amíg a Docker konténer (és volume) él, addig az index is elérhető!

## Mit jelent ez?

### ELŐTTE ❌
```
1. .\Reindex-Project.ps1     → Indexelés
2. .\Ask-RAG.ps1 "question"  → ✅ Működik
3. [Konténer újraindul]
4. .\Ask-RAG.ps1 "question"  → ❌ "No projects indexed!"
5. .\Reindex-Project.ps1     → Újra indexelni kell
```

### MOSTANTÓL ✅
```
1. .\Reindex-Project.ps1     → Indexelés (csak EGYSZER!)
2. .\Ask-RAG.ps1 "question"  → ✅ Működik
3. [Konténer újraindul]
4. .\Ask-RAG.ps1 "question"  → ✅ TOVÁBBRA IS MŰKÖDIK!
```

## Technikai részletek

- **Metadata fájlok**: Az indexelési információk JSON fájlba mentődnek
- **Automatikus betöltés**: Szerver indításkor automatikusan betölti a projekteket
- **Perzisztens tárolás**: ChromaDB + metadata mindkettő Docker volume-ban van
- **Nincs időkorlát**: Az index addig él, amíg a volume él

## Ellenőrzés

```powershell
# Nézd meg, hogy hány projekt van betöltve
Invoke-RestMethod http://localhost:8000/health | ConvertTo-Json

# Lista az összes projektről
.\List-Projects.ps1

# Nézd meg a metadata fájlokat
docker exec local-rag-server ls -la /app/data/chroma_db/ | Select-String "metadata"
```

## Mikor kell újraindexelni?

✅ **KELL újraindexelés:**
- Új fájlokat adtál hozzá a projekthez
- Jelentősen módosítottad a kódot
- Törlted a Docker volume-ot
- Új projektet szeretnél hozzáadni

❌ **NEM kell újraindexelés:**
- Konténer újraindítás után
- Egy nap/hét/hónap inaktivitás után
- Gép újraindítás után (ha WSL/Docker Desktop fut)

## Mikor vész el az index?

Csak ezekben az esetekben:
```powershell
# 1. Docker volume törlése
docker volume rm local-rag-server_chroma-data

# 2. Docker Compose down -v (volume törlés)
docker-compose down -v

# 3. Manuális törlés
docker exec local-rag-server rm -rf /app/data/chroma_db/*
```

## Gyors teszt

```powershell
# 1. Indexelj
.\Reindex-Project.ps1

# 2. Kérdezz
.\Ask-RAG.ps1 "Show me database connections"

# 3. Indítsd újra
docker-compose restart rag-server

# 4. Várj 10 másodpercet
Start-Sleep -Seconds 10

# 5. Kérdezz újra (ÚJRAINDEXELÉS NÉLKÜL!)
.\Ask-RAG.ps1 "Show me database connections"

# ✅ Ha működik → MINDEN RENDBEN!
```

## Logok ellenőrzése

Sikeres betöltés esetén ezeket látod a logokban:
```
Loading existing indexed projects...
Found 1 metadata files
Loading project: /app/data/projects/YourProject
Loaded 199 previously indexed files from metadata
✅ Loaded project: /app/data/projects/YourProject (199 files)
Successfully loaded 1 projects
```

```powershell
# Nézd meg a logokat
docker-compose logs --tail 50 rag-server | Select-String "Loading|Loaded"
```

## Hibaelhárítás

### Probléma: Mégsem töltődik be a projekt

```powershell
# Ellenőrizd a metadata fájlt
docker exec local-rag-server ls -la /app/data/chroma_db/ | Select-String "metadata"

# Ha nincs → Indexelj újra
.\Reindex-Project.ps1 -ForceReindex
```

### Probléma: Régi adatokat látsz

```powershell
# Force reindex
.\Reindex-Project.ps1 -ForceReindex
```

### Probléma: Mindent újra akarok kezdeni

```powershell
# Teljes törlés és újraindítás
docker-compose down
docker volume rm local-rag-server_chroma-data
docker-compose up -d
Start-Sleep -Seconds 15
.\Reindex-Project.ps1
```

---

## Verzió

- **Előző verzió**: 2.0.0 (index csak memóriában)
- **Jelenlegi verzió**: 2.1.0 (perzisztens index)
- **Dátum**: 2025-10-07

## További dokumentáció

- [PERSISTENCE_FIX.md](PERSISTENCE_FIX.md) - Részletes technikai leírás
- [CHANGELOG.md](CHANGELOG.md) - Teljes változásnapló
- [README.md](../README.md) - Főoldal

---

**🎉 Élvezd a perzisztens indexet!**
