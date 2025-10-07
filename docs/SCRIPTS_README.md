# Quick RAG Helper Scripts - README

## 📝 Gyors Használat

### 1. Ask-RAG.ps1 - Kérdések Feltevése

**Alapvető használat:**
```powershell
.\Ask-RAG.ps1 "Your question here"
```

**Interaktív mód (ha nem adsz meg kérdést):**
```powershell
.\Ask-RAG.ps1
# Bekéri a kérdést
```

**Több eredménnyel:**
```powershell
.\Ask-RAG.ps1 "Compare Python and C# code" -MaxResults 10
```

**Példák:**
```powershell
# Database kapcsolatok összehasonlítása
.\Ask-RAG.ps1 "Compare Python and C# database connections"

# Error handling
.\Ask-RAG.ps1 "Show me error handling in both languages"

# Osztály implementációk
.\Ask-RAG.ps1 "Show me the TableComparator class implementation"

# Dependency injection
.\Ask-RAG.ps1 "How is dependency injection used in C#?"
```

**Mit csinál:**
- ✅ Elküldi a kérdést a RAG szervernek
- ✅ Megkapja a releváns kód kontextust
- ✅ **Automatikusan vágólapra másolja**
- ✅ Előnézetet mutat
- ✅ Megmondja a következő lépéseket

**Kimenet:**
- Prompt a vágólapon → Ctrl+V a Copilot Chat-be!

---

### 2. Reindex-Project.ps1 - Projekt Újraindexelése

**Alapvető használat (AdvancedDatabaseExplorer):**
```powershell
.\Reindex-Project.ps1
```

**Force reindex (minden fájl újraindexelése):**
```powershell
.\Reindex-Project.ps1 -ForceReindex
```

**Másik projekt indexelése:**
```powershell
.\Reindex-Project.ps1 -ProjectPath "/app/data/projects/MyOtherProject"
```

**Egyedi fájltípusok:**
```powershell
.\Reindex-Project.ps1 -FileExtensions @(".py", ".cs", ".ts", ".js")
```

**Teljes példa:**
```powershell
.\Reindex-Project.ps1 `
    -ProjectPath "/app/data/projects/AdvancedDatabaseExplorer" `
    -FileExtensions @(".py", ".cs", ".csproj", ".sln", ".json") `
    -ForceReindex
```

**Mikor használd:**
- 📝 Új fájlokat adtál hozzá
- 🔄 Módosítottad a kódot
- 🆕 Új osztályokat/függvényeket írtál
- ⚡ Friss kontextust akarsz

**Mit csinál:**
- ✅ Újraindexeli a projektet
- ✅ Vár az indexelés befejezésére
- ✅ Mutatja a statisztikákat
- ✅ Jelzi, ha kész

---

## 🚀 Gyors Workflow

### Tipikus Migration Workflow:

```powershell
# 1. Ha változtattál a kódon, indexeld újra
.\Reindex-Project.ps1 -ForceReindex

# 2. Kérdezz
.\Ask-RAG.ps1 "Compare error handling in Python and C#"

# 3. Nyisd meg a Copilot Chat-et (Ctrl+Shift+I)
# 4. Paste (Ctrl+V)
# 5. Add hozzá az instrukciót:
"Convert the Python version to idiomatic C# with async/await"

# 6. Profit! 🎉
```

### Napi Használat:

**Reggel (friss projekt):**
```powershell
.\Reindex-Project.ps1
```

**Munkavégzés közben:**
```powershell
# Gyors kérdések
.\Ask-RAG.ps1 "How is database connection pooling handled?"
.\Ask-RAG.ps1 "Show me the query builder implementation"
.\Ask-RAG.ps1 "Compare async patterns"
```

**Nagyobb változás után:**
```powershell
.\Reindex-Project.ps1 -ForceReindex
```

---

## 💡 Pro Tips

### 1. Alias-ok (Microsoft.PowerShell_profile.ps1)

Adj hozzá alias-okat a profile-odhoz:

```powershell
# Gyors alias-ok
function rag { .\Ask-RAG.ps1 $args }
function reindex { .\Reindex-Project.ps1 $args }

# Használat:
# rag "Your question"
# reindex
```

### 2. Tab Completion

PowerShell-ben használd a Tab-ot a paraméterekhez:
```powershell
.\Ask-RAG.ps1 -Max<TAB>  # kiegészíti: -MaxResults
```

### 3. Pipeline

```powershell
# Mentsd el a választ
$response = .\Ask-RAG.ps1 "Your question"
$response.optimized_prompt > output.txt
```

### 4. Több Projektet

Ha több projekted van, készíts wrapper scripteket:

```powershell
# reindex-db-explorer.ps1
.\Reindex-Project.ps1 `
    -ProjectPath "/app/data/projects/AdvancedDatabaseExplorer" `
    -FileExtensions @(".py", ".cs", ".csproj", ".sln")

# reindex-other-project.ps1
.\Reindex-Project.ps1 `
    -ProjectPath "/app/data/projects/OtherProject" `
    -FileExtensions @(".ts", ".tsx", ".js")
```

---

## 🔧 Troubleshooting

### "Cannot connect to RAG server"

```powershell
# Ellenőrizd, hogy fut-e
docker ps

# Ha nem fut, indítsd el
docker-compose up -d

# Várj 5 másodpercet
Start-Sleep -Seconds 5

# Próbáld újra
.\Ask-RAG.ps1 "test"
```

### "No results found"

```powershell
# Lehet, hogy nem indexelt projekt
# Indexeld újra:
.\Reindex-Project.ps1 -ForceReindex
```

### "Slow indexing"

```powershell
# Csökkentsd a fájltípusokat
.\Reindex-Project.ps1 -FileExtensions @(".py", ".cs")  # Csak Python és C#
```

---

## 📊 Statisztikák

```powershell
# Nézd meg a projekt statisztikáit
Invoke-RestMethod -Uri "http://localhost:8000/stats" | ConvertTo-Json
```

## 🧹 Cache Törlése

```powershell
# Ha régi eredményeket látsz
Invoke-RestMethod -Method Delete -Uri "http://localhost:8000/clear"
```

---

## 🎯 Gyakori Kérdések (Migration)

```powershell
# Adatbázis
.\Ask-RAG.ps1 "Compare database connection handling"
.\Ask-RAG.ps1 "Show query execution patterns"
.\Ask-RAG.ps1 "How is transaction management done?"

# Osztályok
.\Ask-RAG.ps1 "Show the DataExtractor class in both languages"
.\Ask-RAG.ps1 "Compare class inheritance patterns"

# Async
.\Ask-RAG.ps1 "Show async/await usage"
.\Ask-RAG.ps1 "Compare parallel processing implementations"

# Error Handling
.\Ask-RAG.ps1 "Compare exception handling strategies"
.\Ask-RAG.ps1 "Show error logging implementations"

# Architecture
.\Ask-RAG.ps1 "What are the main architectural differences?"
.\Ask-RAG.ps1 "How is dependency injection configured?"
```

---

## 📚 További Dokumentáció

- **MIGRATION_GUIDE.md** - Részletes migration útmutató
- **README.md** - Projekt dokumentáció
- **QUICKSTART.md** - Gyors kezdés
- **TROUBLESHOOTING.md** - Hibaelhárítás

---

**Egyszerű, gyors és hatékony! 🚀**
