# Quick Start Guide - Local RAG Server

## 🚀 5 Perces Gyors Start

### 1. Előfeltételek Ellenőrzése

```powershell
# Docker ellenőrzése
docker --version

# Docker Compose ellenőrzése
docker-compose --version
```

Ha nincs telepítve, töltsd le: https://www.docker.com/products/docker-desktop

### 2. Környezet Beállítása

```powershell
# Navigálj a projekt mappába
cd g:\Docker\local-rag-server

# Másold át a környezeti változók fájlt
Copy-Item .env.example .env

# Szerkeszd a .env fájlt - állítsd be a PROJECT_PATH-t!
notepad .env
```

**Fontos**: Módosítsd a `PROJECT_PATH` értéket WSL formátumra:
- Windows: `C:\Users\YourName\Projects`
- WSL: `/mnt/c/Users/YourName/Projects`

### 3. Indítás

```powershell
# Automatikus setup (ajánlott)
.\setup_rag_windows.ps1

# VAGY manuálisan:
docker-compose up -d
```

### 4. Ellenőrzés

```powershell
# Egészség ellenőrzése
curl http://localhost:8000/health

# API dokumentáció
Start-Process "http://localhost:8000/docs"
```

### 5. Első Projekt Indexelése

```powershell
$body = @{
    project_path = "C:\Users\YourName\YourProject"
    file_extensions = @(".py", ".js", ".ts")
    force_reindex = $false
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://localhost:8000/index" `
    -Body $body -ContentType "application/json"
```

### 6. Első Lekérdezés

```powershell
$body = @{
    query = "How does authentication work?"
    max_results = 5
    include_metadata = $true
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://localhost:8000/query" `
    -Body $body -ContentType "application/json"
```

## 📊 Hasznos Parancsok

```powershell
# Logok megtekintése
docker-compose logs -f rag-server

# Újraindítás
docker-compose restart

# Leállítás
docker-compose down

# Teljes törlés (adatokkal együtt)
docker-compose down -v

# Statisztikák
Invoke-RestMethod -Method Get -Uri "http://localhost:8000/stats"
```

## 🎯 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Server állapot |
| `/index` | POST | Projekt indexelése |
| `/query` | POST | Kontextus lekérdezés |
| `/stats` | GET | Statisztikák |
| `/clear` | DELETE | Cache törlése |
| `/docs` | GET | API dokumentáció |

## 💡 Tippek

### Gyorsabb Indexelés
```powershell
# Csak a fontos fájltípusok
$body = @{
    project_path = "C:\Your\Project"
    file_extensions = @(".py")  # Csak Python
    force_reindex = $false
} | ConvertTo-Json
```

### Több Kontextus
```powershell
# Több releváns kódrészlet
$body = @{
    query = "Your question"
    max_results = 10  # Több eredmény
} | ConvertTo-Json
```

### Cache Törlése
```powershell
# Ha régi eredményeket látsz
Invoke-RestMethod -Method Delete -Uri "http://localhost:8000/clear"
```

## 🔧 Gyakori Problémák

### "Cannot connect" hiba
```powershell
# Ellenőrizd, hogy futnak-e a konténerek
docker ps

# Ha nem futnak, indítsd el őket
docker-compose up -d
```

### "No project indexed" hiba
```powershell
# Először indexeld a projektet
# Lásd "Első Projekt Indexelése" fent
```

### Port foglalt
```powershell
# Ha a 8000-es port foglalt
# Szerkeszd a docker-compose.yml-t:
# ports: - "8001:8000"  # Más port használata
```

## 📚 További Információk

- **README.md** - Teljes dokumentáció
- **examples/** - Példa scriptek
- **http://localhost:8000/docs** - Interaktív API dokumentáció

## 🆘 Segítség

Ha elakadtál:
1. Nézd meg a logokat: `docker-compose logs -f`
2. Futtasd a test scriptet: `python test_server.py`
3. Ellenőrizd a `.env` fájlt
4. Próbáld újraindítani: `docker-compose restart`

---

**Kész! Most már használhatod a RAG szervert a GitHub Copilot kiterjesztésére! 🎉**
