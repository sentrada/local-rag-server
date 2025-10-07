# File Watcher Automatikus Indexelés

## ✅ MŰKÖDIK!

Az automatikus reindexelés **SIKERESEN MŰKÖDIK** WSL2 Docker környezetben a következő megoldással:

### Implementált Megoldás

1. **PollingObserver használata** - Mivel a natív Observer nem kapja meg a fájlrendszer eseményeket Docker volume-okon keresztül, polling-alapú megfigyelést használunk
2. **Háttérszál** - Periodikus ellenőrzés (1 másodpercenként) a pending változásokra
3. **Debouncing** - 2 másodperc várakozás több változás összevonásához
4. **Read-Write volume** - A projekt mappának írható/olvasható módban kell lennie

### Működés

```
Fájl módosítás → PollingObserver (1s) → Event Detection → 
→ Pending Changes (2s debounce) → Background Thread → 
→ Automatic Reindexing
```

### Példa logból:

```
2025-10-06 22:42:08 - 🔔 File modified detected: /app/data/projects/Local-Rag-Server/test_auto_index.md
2025-10-06 22:42:11 - Reindexing 1 changed file(s)
2025-10-06 22:42:11 - Starting indexing...
2025-10-06 22:42:11 - Reindexing complete
```

## Követelmények

1. **WSL2 Docker** - Docker Desktop WSL2 backend-del
2. **PollingObserver** - `watchdog` library polling observer
3. **Read-Write Volume** - Projekt mappa ne legyen `:ro` (read-only) módban
4. **Háttérszál** - `file_watcher_background_task()` periodikusan hívja a `process_all_pending_changes()`

## Konfiguráció

### docker-compose.yml:
```yaml
volumes:
  # Source code for development (hot-reload)
  - ./src:/app/src
  # Project directory (READ-WRITE for file watcher)
  - g:/Docker/local-rag-server/:/app/data/projects/Local-Rag-Server  # NO :ro flag!
```

### Környezeti változók:
```yaml
environment:
  - FILE_WATCHER_ENABLED=true
  - FILE_WATCHER_DEBOUNCE_SECONDS=2.0
```

## Manuális Reindexelés (Alternatíva)

Ha bármilyen okból nem működne az automatikus, használd a PowerShell scripteket:
- `.\Reindex-Project.ps1` - Manuális reindexelés
- `.\Add-Project.ps1` - Új projekt hozzáadása
- `.\List-Projects.ps1` - Indexelt projektek listázása

## Teljesítmény

- **Polling gyakoriság**: 1 másodperc
- **Debounce idő**: 2 másodperc
- **CPU használat**: Minimális (polling csak metaadatokat ellenőriz)
- **Reakcióidő**: 3-5 másodperc a fájlmódosítás után

## Korlátok

- Windows fájlrendszeren lévő fájlok esetén a Docker volume mount keresztül a polling szükséges
- Natív Linux fájlrendszeren (WSL2 belső) gyorsabb és hatékonyabb lenne az inotify-alapú Observer
