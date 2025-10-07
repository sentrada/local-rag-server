# 🎯 Multi-Project Support - Quick Guide

## ✅ Elkülönülnek a Projektek?

**IGEN!** A RAG szerver most már **több projektet is kezel egyszerre**, teljesen elkülönítve őket!

```
┌────────────────────────────────────────────────────┐
│  RAG SERVER (Multi-Project Support)                │
│                                                     │
│  Project 1: AdvancedDatabaseExplorer               │
│    ├─ 184 files, 1284 chunks                      │
│    └─ [CURRENT] ← Ezt kérdezi alapból            │
│                                                     │
│  Project 2: MyWebApp                               │
│    ├─ 95 files, 723 chunks                        │
│    └─ Elérhető, ha explicit megadod              │
│                                                     │
│  Project 3: BackendAPI                             │
│    └─ Hozzáadható bármikor                        │
└────────────────────────────────────────────────────┘
```

---

## 🚀 Új Funkciók

### 1️⃣ Interaktív Projekt Választó (Ask-RAG.ps1)

```powershell
# Ha több projekt van indexelve, automatikusan kérdezi!
.\Ask-RAG.ps1 "Your question"

# Kimenet:
# === Available Projects ===
#   [1] AdvancedDatabaseExplorer [CURRENT]
#       Path: /app/data/projects/AdvancedDatabaseExplorer
#       Files: 184, Chunks: 1284
#
#   [2] MyWebApp
#       Path: /app/data/projects/MyWebApp
#       Files: 95, Chunks: 723
#
# Select project (1-2, or Enter for current): 2
```

### 2️⃣ Explicit Projekt Megadás

```powershell
# Kérdezz egy konkrét projektről
.\Ask-RAG.ps1 "Show me database connections" `
    -ProjectPath "/app/data/projects/AdvancedDatabaseExplorer"

# Másik projekt
.\Ask-RAG.ps1 "Show me React components" `
    -ProjectPath "/app/data/projects/MyWebApp"
```

### 3️⃣ Projekt Váltás (Switch-Project.ps1)

```powershell
# Interaktív projekt váltás
.\Switch-Project.ps1

# Vagy direkt
.\Switch-Project.ps1 -ProjectPath "/app/data/projects/MyWebApp"
```

### 4️⃣ Projektek Listázása

```powershell
.\List-Projects.ps1

# Kimenet:
# === Indexed Projects ===
#
# [1] AdvancedDatabaseExplorer [CURRENT]
#     Path: /app/data/projects/AdvancedDatabaseExplorer
#     Files: 184
#     Chunks: 1284
#
# [2] MyWebApp
#     Path: /app/data/projects/MyWebApp
#     Files: 95
#     Chunks: 723
```

---

## 📚 API Endpoints (Új)

### GET /projects
Lista az összes indexelt projektről:

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/projects"
```

**Válasz:**
```json
{
  "total_projects": 2,
  "current_project": "/app/data/projects/AdvancedDatabaseExplorer",
  "projects": [
    {
      "path": "/app/data/projects/AdvancedDatabaseExplorer",
      "name": "AdvancedDatabaseExplorer",
      "indexed_files": 184,
      "total_chunks": 1284,
      "is_current": true
    },
    {
      "path": "/app/data/projects/MyWebApp",
      "name": "MyWebApp",
      "indexed_files": 95,
      "total_chunks": 723,
      "is_current": false
    }
  ]
}
```

### POST /switch
Aktív projekt váltás:

```powershell
$body = @{ project_path = "/app/data/projects/MyWebApp" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/switch" -Body $body -ContentType "application/json"
```

### POST /query (Frissítve)
Most már opcionális `project_path` paraméter:

```powershell
$body = @{
    query = "Show me authentication"
    max_results = 8
    project_path = "/app/data/projects/AdvancedDatabaseExplorer"  # Opcionális!
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://localhost:8000/query" -Body $body -ContentType "application/json"
```

### GET /stats (Frissítve)
Most már project-specifikus stats:

```powershell
# Current project stats
Invoke-RestMethod -Uri "http://localhost:8000/stats"

# Specific project stats
Invoke-RestMethod -Uri "http://localhost:8000/stats?project_path=/app/data/projects/MyWebApp"
```

### DELETE /clear (Frissítve)
Most már törölhetsz egy projektet vagy mindet:

```powershell
# Egy projekt törlése
$body = @{ project_path = "/app/data/projects/MyWebApp" } | ConvertTo-Json
Invoke-RestMethod -Method Delete -Uri "http://localhost:8000/clear" -Body $body -ContentType "application/json"

# Minden projekt törlése
Invoke-RestMethod -Method Delete -Uri "http://localhost:8000/clear"
```

---

## 🎯 Gyakorlati Példák

### Példa 1: Python→C# Migration (2 projekt)

```powershell
# 1. Index mindkét projektet
.\Reindex-Project.ps1 -ProjectPath "/app/data/projects/PythonApp"
.\Reindex-Project.ps1 -ProjectPath "/app/data/projects/CSharpApp"

# 2. Kérdezz az egyik projektről
.\Ask-RAG.ps1 "Show me the authentication implementation"
# Választasz: [1] PythonApp

# 3. Váltás a másik projektre
.\Switch-Project.ps1
# Választasz: [2] CSharpApp

# 4. Ugyanaz a kérdés, másik kontextus
.\Ask-RAG.ps1 "Show me the authentication implementation"
# Most a C# kódot adja vissza!

# 5. Vagy explicit megadod
.\Ask-RAG.ps1 "Compare implementations" -ProjectPath "/app/data/projects/PythonApp"
```

### Példa 2: Microservices (4 projekt)

```powershell
# Index all services
.\Reindex-Project.ps1 -ProjectPath "/app/data/projects/Frontend"
.\Reindex-Project.ps1 -ProjectPath "/app/data/projects/AuthService"
.\Reindex-Project.ps1 -ProjectPath "/app/data/projects/DataService"
.\Reindex-Project.ps1 -ProjectPath "/app/data/projects/APIGateway"

# Lista
.\List-Projects.ps1
# [1] Frontend [CURRENT]
# [2] AuthService
# [3] DataService
# [4] APIGateway

# Kérdezz a Frontend-ről
.\Ask-RAG.ps1 "How does the login form work?"
# Automatikusan a Frontend-et kérdezi (current)

# Kérdezz az AuthService-ről
.\Ask-RAG.ps1 "How is JWT validation done?" -ProjectPath "/app/data/projects/AuthService"
# Explicit az AuthService-t kérdezi
```

### Példa 3: Fejlesztés Közben

```powershell
# Reggel: Index a projekt
.\Reindex-Project.ps1 -ProjectPath "/app/data/projects/MyProject"

# Délben: Módosítottál fájlokat, force reindex
.\Reindex-Project.ps1 -ProjectPath "/app/data/projects/MyProject" -ForceReindex

# Query egész nap
.\Ask-RAG.ps1 "Show me the database schema"
.\Ask-RAG.ps1 "How is error handling done?"
.\Ask-RAG.ps1 "Show me the API endpoints"

# Közben dolgozol egy másik projekten is
.\Switch-Project.ps1  # Váltasz
.\Ask-RAG.ps1 "Show me the config files"
```

---

## 💡 Pro Tips

### 1. Alias-ok a Profile-ban

```powershell
# Microsoft.PowerShell_profile.ps1
function rag { .\Ask-RAG.ps1 $args }
function switch { .\Switch-Project.ps1 $args }
function projects { .\List-Projects.ps1 }
function reindex { .\Reindex-Project.ps1 $args }

# Használat:
# rag "Your question"
# switch
# projects
# reindex -ForceReindex
```

### 2. Projekt-Specifikus Wrapper Scriptek

```powershell
# work-on-frontend.ps1
.\Switch-Project.ps1 -ProjectPath "/app/data/projects/Frontend"
Write-Host "✅ Ready for Frontend development!" -ForegroundColor Green

# work-on-backend.ps1
.\Switch-Project.ps1 -ProjectPath "/app/data/projects/Backend"
Write-Host "✅ Ready for Backend development!" -ForegroundColor Green
```

### 3. Tömeges Reindex

```powershell
# reindex-all-projects.ps1
$projects = @(
    "/app/data/projects/Frontend",
    "/app/data/projects/Backend",
    "/app/data/projects/Mobile"
)

foreach ($proj in $projects) {
    Write-Host "Reindexing $proj..." -ForegroundColor Cyan
    .\Reindex-Project.ps1 -ProjectPath $proj -ForceReindex
    Start-Sleep -Seconds 5
}

Write-Host "✅ All projects reindexed!" -ForegroundColor Green
```

---

## 🔍 Hogyan Működik Belül?

```python
# Régi (egy projekt):
rag_system: Optional[LocalRAGSystem] = None

# Új (több projekt):
rag_systems: dict[str, LocalRAGSystem] = {}
current_project: Optional[str] = None

# Query:
if request.project_path:
    rag_system = rag_systems[request.project_path]  # Explicit
else:
    rag_system = rag_systems[current_project]  # Current
```

**Minden projekt:**
- ✅ Saját RAGSystem példány
- ✅ Saját index a ChromaDB-ben
- ✅ Elkülönített cache Redis-ben
- ✅ Független hash tracking

---

## ❓ FAQ

**Q: Hány projektet tudok indexelni?**  
A: Nincs hard limit. Memória: ~50-100 MB / projekt.

**Q: Ha váltok projektet, az előző elvész?**  
A: Nem! Minden projekt memory-ban marad, csak a "current" változik.

**Q: Tudok egyszerre több projektről kérdezni?**  
A: Nem, egy query = egy projekt. De gyorsan váltasz vagy explicit megadod.

**Q: Automatikus project detection a kérdésből?**  
A: Nem (még), de az interaktív választó megoldja.

**Q: Mi van, ha újraindítom a szervert?**  
A: ChromaDB perzisztens, de a projektek újraindexelése szükséges.

---

## ✅ Összefoglalás

| Feature | Előtte | Most |
|---------|--------|------|
| Projektek | 1 | ∞ |
| Váltás | Reindex | `Switch-Project.ps1` |
| Explicit query | ❌ | ✅ `-ProjectPath` |
| Lista | `/stats` | `/projects` |
| Projekt választó | ❌ | ✅ Interaktív |

**Most már teljesen multi-project! 🎉**

---

**Használd:**
```powershell
.\Ask-RAG.ps1 "Your question"  # Interaktív választó ha több projekt van
.\Switch-Project.ps1             # Gyors váltás
.\List-Projects.ps1              # Mi van indexelve?
```

**Kész! 🚀**
