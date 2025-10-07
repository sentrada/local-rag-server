# Troubleshooting Guide

## 🔍 Gyakori Problémák és Megoldások

### 1. Docker Problémák

#### "Docker daemon is not running"
```powershell
# Megoldás: Indítsd el a Docker Desktop-ot
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
```

#### "Cannot connect to Docker daemon"
```powershell
# Ellenőrizd a Docker Desktop státuszát
# Újraindítás segíthet
Get-Process "*docker*"
```

#### "Port 8000 is already in use"
```powershell
# Találd meg, mi használja a portot
netstat -ano | findstr :8000

# Állj le a folyamatot (replace PID with actual process ID)
Stop-Process -Id PID -Force

# VAGY használj másik portot a docker-compose.yml-ben:
# ports: - "8001:8000"
```

---

### 2. Indexelési Problémák

#### "Invalid path" hiba
```powershell
# Ellenőrizd az útvonalat
# Windows: C:\Users\Name\Project
# WSL: /mnt/c/Users/Name/Project

# Teszteld az útvonalat WSL-ben:
wsl ls /mnt/c/Users/Name/Project
```

#### Lassú indexelés
```powershell
# 1. Csökkentsd a fájltípusok számát
$body = @{
    file_extensions = @(".py")  # Csak egy nyelv
} | ConvertTo-Json

# 2. Ellenőrizd, hogy nem indexelsz-e node_modules-t vagy hasonlót
# A .gitignore-ban lévő mappák automatikusan ki vannak hagyva

# 3. Nézd meg a logokat
docker-compose logs -f rag-server | Select-String "Indexed"
```

#### "Permission denied" hiba
```powershell
# WSL jogosultságok ellenőrzése
wsl ls -la /mnt/c/Users/Name/Project

# Docker volume jogok
docker-compose down
docker volume rm local-rag-server_chroma-data
docker-compose up -d
```

---

### 3. Lekérdezési Problémák

#### "No project indexed" hiba
```powershell
# Megoldás: Indexeld előbb a projektet
$body = @{
    project_path = "C:\Your\Project"
    file_extensions = @(".py", ".js")
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://localhost:8000/index" `
    -Body $body -ContentType "application/json"

# Várj pár másodpercet, majd ellenőrizd:
Invoke-RestMethod -Method Get -Uri "http://localhost:8000/stats"
```

#### "No relevant context found"
```powershell
# 1. Ellenőrizd, hogy megfelelő fájlok lettek-e indexelve
Invoke-RestMethod -Method Get -Uri "http://localhost:8000/stats"

# 2. Próbálj konkrétabb kérdést feltenni
$body = @{
    query = "Show me the login function in auth.py"  # Konkrét
    max_results = 10
} | ConvertTo-Json

# 3. Force reindex
$body = @{
    project_path = "C:\Your\Project"
    force_reindex = $true
} | ConvertTo-Json
```

#### Timeout problémák
```powershell
# 1. Ellenőrizd a Redis-t
docker-compose ps | Select-String redis

# 2. Redis újraindítása
docker-compose restart redis

# 3. Cache törlése
Invoke-RestMethod -Method Delete -Uri "http://localhost:8000/clear"

# 4. Csökkentsd a max_results-t
$body = @{
    query = "Your question"
    max_results = 3  # Kevesebb eredmény = gyorsabb
} | ConvertTo-Json
```

---

### 4. Memory és Performance

#### "Out of memory" hiba
```powershell
# 1. Állj le minden konténert
docker-compose down

# 2. Tisztítsd meg a Docker cache-t
docker system prune -a

# 3. Növeld a Docker Desktop memory limitjét
# Settings -> Resources -> Memory -> 4GB vagy több

# 4. Indítsd újra
docker-compose up -d
```

#### Lassú válaszidők
```powershell
# 1. Ellenőrizd a Redis cache-t
docker-compose logs redis | Select-String -Pattern "error|warning"

# 2. Csökkentsd a chunk size-t
# Szerkeszd: src/code_parser.py
# chunk_size = 500  # Kisebb chunkók

# 3. Használj kisebb embedding modellt
# .env fájlban:
# EMBEDDING_MODEL=all-MiniLM-L6-v2  # Gyorsabb
```

---

### 5. ChromaDB Problémák

#### "Collection not found" hiba
```powershell
# Töröld és újraindexeld
docker-compose down
Remove-Item -Path "data/chroma_db/*" -Recurse -Force
docker-compose up -d

# Indexeld újra a projektet
```

#### "Database is locked" hiba
```powershell
# ChromaDB lock feloldása
docker-compose restart rag-server
```

---

### 6. Redis Cache Problémák

#### Redis nem érhető el
```powershell
# Ellenőrizd a Redis konténert
docker-compose ps redis

# Ha nem fut, indítsd el
docker-compose up -d redis

# Teszteld a kapcsolatot
docker-compose exec redis redis-cli ping
# Válasz: PONG
```

#### Cache nem működik
```powershell
# Cache statisztikák
docker-compose exec redis redis-cli INFO stats

# Cache törlése
docker-compose exec redis redis-cli FLUSHALL
```

---

### 7. Logging és Debugging

#### Részletes logok
```powershell
# Szerkeszd a .env fájlt
LOG_LEVEL=DEBUG

# Újraindítás
docker-compose restart rag-server

# Nézd a logokat
docker-compose logs -f rag-server
```

#### Hiba nyomkövetés
```powershell
# Összes log mentése fájlba
docker-compose logs > logs/debug.log

# Csak hibák
docker-compose logs rag-server 2>&1 | Select-String "ERROR"

# Real-time követés
docker-compose logs -f --tail=100 rag-server
```

---

### 8. Windows Specifikus Problémák

#### WSL path konverzió
```powershell
# Windows -> WSL
C:\Users\Name\Project -> /mnt/c/Users/Name/Project

# PowerShell helper:
function Convert-ToWSLPath {
    param([string]$WindowsPath)
    $wslPath = $WindowsPath -replace '^([A-Z]):', {'/mnt/' + $_.Groups[1].Value.ToLower()}
    $wslPath = $wslPath -replace '\\', '/'
    return $wslPath
}

# Használat:
$wslPath = Convert-ToWSLPath "C:\Users\Name\Project"
```

#### Line ending problémák
```powershell
# Git beállítás
git config --global core.autocrlf false

# Konvertálás LF-re
(Get-Content file.py -Raw) -replace "`r`n", "`n" | Set-Content file.py
```

---

### 9. API Hibák

#### 400 Bad Request
```powershell
# Ellenőrizd a JSON formátumot
$body = @{
    project_path = "C:\Project"  # string
    file_extensions = @(".py")    # array
    force_reindex = $false        # boolean
} | ConvertTo-Json

# Content-Type header fontos!
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/index" `
    -Body $body -ContentType "application/json"
```

#### 500 Internal Server Error
```powershell
# Nézd meg a server logokat
docker-compose logs -f rag-server | Select-String "ERROR"

# Restart segíthet
docker-compose restart rag-server
```

---

### 10. Teljes Reset

Ha minden más sikertelen, teljes újraindítás:

```powershell
# 1. Állj le minden konténert
docker-compose down -v

# 2. Töröld az adatokat
Remove-Item -Path "data/chroma_db/*" -Recurse -Force
Remove-Item -Path "logs/*" -Recurse -Force

# 3. Docker cache tisztítás
docker system prune -a

# 4. Rebuild
docker-compose build --no-cache

# 5. Indítás
docker-compose up -d

# 6. Várj kicsit
Start-Sleep -Seconds 10

# 7. Health check
Invoke-RestMethod -Method Get -Uri "http://localhost:8000/health"

# 8. Indexeld újra a projektet
# ... lásd QUICKSTART.md
```

---

## 🆘 További Segítség

### Diagnosztikai Script

```powershell
# Mentsd el: diagnose.ps1
Write-Host "RAG Server Diagnostics" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan

# Docker
Write-Host "`nDocker:" -ForegroundColor Yellow
docker --version
docker-compose --version

# Containers
Write-Host "`nContainers:" -ForegroundColor Yellow
docker-compose ps

# Health
Write-Host "`nHealth:" -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Method Get -Uri "http://localhost:8000/health"
    $health | ConvertTo-Json
} catch {
    Write-Host "Health check failed: $_" -ForegroundColor Red
}

# Logs
Write-Host "`nRecent Errors:" -ForegroundColor Yellow
docker-compose logs --tail=20 rag-server | Select-String "ERROR"

Write-Host "`nDone!" -ForegroundColor Green
```

### Hasznos Parancsok

```powershell
# Összes konténer info
docker-compose ps -a

# Resource használat
docker stats --no-stream

# Network ellenőrzés
docker network ls
docker network inspect local-rag-server_rag-network

# Volume info
docker volume ls
docker volume inspect local-rag-server_chroma-data
```

---

**Ha továbbra is problémád van, nyiss egy issue-t a projekten vagy ellenőrizd a logokat részletesen!**
