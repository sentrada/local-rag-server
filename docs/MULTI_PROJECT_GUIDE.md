# 🗂️ Multi-Project RAG Server Guide

## Koncepció

A RAG szerver **több projektet is tud kezelni** egyszerre! Mindegyik projekt külön indexelhető, és külön lekérdezhető.

### Hogyan Működik?

```
┌────────────────────────────────────────────────────────┐
│  RAG SERVER (Docker Container)                         │
│                                                         │
│  /app/data/projects/                                   │
│    ├─ local-rag-server/          (saját maga)        │
│    ├─ AdvancedDatabaseExplorer/  (Python→C#)         │
│    ├─ MyWebApp/                  (React app)          │
│    ├─ BackendAPI/                (Node.js API)        │
│    └─ external/                  (változó projekt)    │
│                                                         │
│  ChromaDB (Vector Database)                            │
│    └─ Minden projekt külön van tárolva                │
└────────────────────────────────────────────────────────┘
```

---

## 🚀 Gyors Használat

### 1. Lista az Aktuális Projektekről

```powershell
.\List-Projects.ps1
```

**Kimenet:**
```
[1] local-rag-server
    Host: ./
    Container: /app/data/projects/local-rag-server
    Status: ✅ Exists (45 files)

[2] AdvancedDatabaseExplorer
    Host: G:/Sources/Local/AdvancedDatabaseExplorer
    Container: /app/data/projects/AdvancedDatabaseExplorer
    Status: ✅ Exists (184 files)
```

### 2. Új Projekt Hozzáadása

```powershell
.\Add-Project.ps1 `
    -ProjectName "MyWebApp" `
    -ProjectPath "G:\Sources\MyWebApp"
```

**Lépések:**
1. Script megmutatja, mit kell hozzáadni a `docker-compose.yml`-hez
2. Újraindítod a konténereket
3. Indexeled az új projektet

### 3. Projekt Indexelése

```powershell
# Alapértelmezett (AdvancedDatabaseExplorer)
.\Reindex-Project.ps1

# Másik projekt
.\Reindex-Project.ps1 -ProjectPath "/app/data/projects/MyWebApp"

# Force reindex
.\Reindex-Project.ps1 -ProjectPath "/app/data/projects/MyWebApp" -ForceReindex
```

### 4. Kérdezz Konkrét Projektről

```powershell
# Általános kérdés (az utoljára indexelt projektről)
.\Ask-RAG.ps1 "Show me the authentication implementation"

# Ha több projekt van, légy konkrét a kérdésben
.\Ask-RAG.ps1 "In the AdvancedDatabaseExplorer project, show me database connections"
```

---

## 📝 Új Projekt Hozzáadása (Manuális)

### Lépés 1: Szerkeszd a `docker-compose.yml`-t

```yaml
volumes:
  # Meglévő projektek
  - ./:/app/data/projects/local-rag-server:ro
  - G:/Sources/Local/AdvancedDatabaseExplorer:/app/data/projects/AdvancedDatabaseExplorer:ro
  
  # ÚJ PROJEKT - Add hozzá ezt a sort
  - G:/Sources/MyNewProject:/app/data/projects/MyNewProject:ro
  
  # További projektek...
```

### Lépés 2: Újraindítás

```powershell
docker-compose down
docker-compose up -d
```

### Lépés 3: Indexelés

```powershell
.\Reindex-Project.ps1 `
    -ProjectPath "/app/data/projects/MyNewProject" `
    -FileExtensions @(".py", ".ts", ".js", ".tsx", ".jsx")
```

### Lépés 4: Ellenőrzés

```powershell
# Nézd meg a statisztikákat
Invoke-RestMethod -Uri "http://localhost:8000/stats"

# Próbálj ki egy kérdést
.\Ask-RAG.ps1 "Show me the main entry point in MyNewProject"
```

---

## 🎯 Gyakori Használati Esetek

### 1. **Microservices Architecture (Több Projekt)**

```yaml
volumes:
  - G:/Sources/Frontend:/app/data/projects/Frontend:ro
  - G:/Sources/AuthService:/app/data/projects/AuthService:ro
  - G:/Sources/DataService:/app/data/projects/DataService:ro
  - G:/Sources/APIGateway:/app/data/projects/APIGateway:ro
```

**Workflow:**
```powershell
# Index all services
.\Reindex-Project.ps1 -ProjectPath "/app/data/projects/Frontend"
.\Reindex-Project.ps1 -ProjectPath "/app/data/projects/AuthService"
.\Reindex-Project.ps1 -ProjectPath "/app/data/projects/DataService"
.\Reindex-Project.ps1 -ProjectPath "/app/data/projects/APIGateway"

# Ask cross-service questions
.\Ask-RAG.ps1 "How does the Frontend communicate with AuthService?"
.\Ask-RAG.ps1 "Show me the API contracts between services"
```

### 2. **Migration Projects (Python → C#, React → Vue, etc.)**

```yaml
volumes:
  - G:/Sources/OldPythonApp:/app/data/projects/OldPythonApp:ro
  - G:/Sources/NewCSharpApp:/app/data/projects/NewCSharpApp:ro
```

**Workflow:**
```powershell
# Index both versions
.\Reindex-Project.ps1 -ProjectPath "/app/data/projects/OldPythonApp"
.\Reindex-Project.ps1 -ProjectPath "/app/data/projects/NewCSharpApp"

# Compare implementations
.\Ask-RAG.ps1 "Compare database access patterns in both projects"
.\Ask-RAG.ps1 "Show me how authentication is implemented in Python vs C#"
```

### 3. **Multi-Language Monorepo**

```yaml
volumes:
  - G:/Sources/Monorepo:/app/data/projects/Monorepo:ro
```

**Workflow:**
```powershell
# Index the entire monorepo
.\Reindex-Project.ps1 `
    -ProjectPath "/app/data/projects/Monorepo" `
    -FileExtensions @(".py", ".ts", ".js", ".go", ".rs")

# Ask language-specific questions
.\Ask-RAG.ps1 "Show me the Python implementation of the payment module"
.\Ask-RAG.ps1 "How is the same feature implemented in TypeScript?"
```

---

## 🔄 Projekt Váltás Workflow

### Amikor Több Projekten Dolgozol

```powershell
# Reggel: Python projekt
.\Reindex-Project.ps1 -ProjectPath "/app/data/projects/PythonApp" -ForceReindex
.\Ask-RAG.ps1 "Show me the database models"
# ... dolgozol ...

# Délután: C# projekt
.\Reindex-Project.ps1 -ProjectPath "/app/data/projects/CSharpApp" -ForceReindex
.\Ask-RAG.ps1 "Show me the Entity Framework setup"
# ... dolgozol ...
```

### Automatizálás Wrapper Scriptekkel

Készíts projekt-specifikus scripteket:

```powershell
# work-on-python.ps1
.\Reindex-Project.ps1 -ProjectPath "/app/data/projects/PythonApp"
Write-Host "✅ Ready to work on Python project!" -ForegroundColor Green

# work-on-csharp.ps1
.\Reindex-Project.ps1 -ProjectPath "/app/data/projects/CSharpApp"
Write-Host "✅ Ready to work on C# project!" -ForegroundColor Green
```

---

## 💡 Pro Tips

### 1. **Környezeti Változó Használata**

```yaml
# docker-compose.yml
volumes:
  - ${MY_PROJECT_1}:/app/data/projects/Project1:ro
  - ${MY_PROJECT_2}:/app/data/projects/Project2:ro
```

```powershell
# .env fájl
MY_PROJECT_1=G:/Sources/Project1
MY_PROJECT_2=G:/Sources/Project2
```

### 2. **Szelektív Fájltípusok**

```powershell
# Csak backend kód (Python + SQL)
.\Reindex-Project.ps1 `
    -ProjectPath "/app/data/projects/Backend" `
    -FileExtensions @(".py", ".sql")

# Csak frontend kód (TypeScript + styles)
.\Reindex-Project.ps1 `
    -ProjectPath "/app/data/projects/Frontend" `
    -FileExtensions @(".ts", ".tsx", ".css", ".scss")
```

### 3. **Egyedi Projekt Scriptek**

```powershell
# reindex-all.ps1
@(
    "/app/data/projects/Frontend",
    "/app/data/projects/Backend",
    "/app/data/projects/Mobile"
) | ForEach-Object {
    Write-Host "Indexing $_..." -ForegroundColor Cyan
    .\Reindex-Project.ps1 -ProjectPath $_ -ForceReindex
}
Write-Host "✅ All projects reindexed!" -ForegroundColor Green
```

---

## ⚡ Teljesítmény

### Indexelési Idők (közelítő)

| Projekt Méret | Fájlok | Chunks | Idő |
|--------------|--------|--------|-----|
| Kicsi        | ~50    | ~400   | ~10s |
| Közepes      | ~200   | ~1500  | ~40s |
| Nagy         | ~500   | ~4000  | ~2min |
| Óriás        | ~1000+ | ~8000+ | ~5min |

### Tárhely

```
ChromaDB méret ≈ (chunks × 384 dimensions × 4 bytes) + metadata
Példa: 1500 chunks ≈ 2.3 MB
```

### Optimalizálás

```powershell
# Csak a szükséges fájltípusok
-FileExtensions @(".py", ".cs")  # Gyorsabb mint az összes

# Exclude mappák (implementáld egyénileg)
# node_modules/, venv/, bin/, obj/ ne legyenek indexelve
```

---

## 🧹 Karbantartás

### Cache Törlése

```powershell
# API endpoint
Invoke-RestMethod -Method Delete -Uri "http://localhost:8000/clear"
```

### ChromaDB Újraindítása

```powershell
# Töröld a volume-ot
docker-compose down -v
docker-compose up -d

# Index újra minden projektet
.\Reindex-Project.ps1 -ProjectPath "/app/data/projects/Project1" -ForceReindex
```

### Stats Monitoring

```powershell
# Folyamatos monitoring
while ($true) {
    Clear-Host
    Invoke-RestMethod -Uri "http://localhost:8000/stats" | ConvertTo-Json
    Start-Sleep -Seconds 5
}
```

---

## 🎯 GitHub Copilot Integráció

### Teljes Workflow

```
1. Fejlesztés közben változtatasz fájlokat
   ↓
2. .\Reindex-Project.ps1 -ForceReindex
   ↓
3. .\Ask-RAG.ps1 "Your implementation question"
   ↓
4. Copilot Chat (Ctrl+Shift+I) → Paste (Ctrl+V)
   ↓
5. Add konkrét instrukciót: "Convert this to async/await"
   ↓
6. Copilot generál RELEVÁNS kódot (nem timeout!)
   ↓
7. Profit! 🎉
```

---

## ❓ FAQ

**Q: Hány projektet tudok egyszerre indexelni?**  
A: Nincs hard limit, de gyakorlatilag 5-10 projekt optimális.

**Q: Minden projektet újra kell indexelni naponta?**  
A: Nem, csak akkor, ha változtak a fájlok. A RAG szerver file hash-t használ.

**Q: Mi történik, ha két projekt ugyanazt a fájlnevet használja?**  
A: Nincs probléma, a teljes path tárolva van a metadatában.

**Q: Törölhetek egy projektet?**  
A: Igen, töröld a volume mount-ot a `docker-compose.yml`-ből és indítsd újra.

**Q: Működik WSL projektekkel?**  
A: Igen! Használd a WSL path-ot: `/mnt/g/Sources/Project`

---

**Több projekt = Több kontextus = Jobb Copilot válaszok! 🚀**
