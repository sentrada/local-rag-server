# 🔄 Python to C# Migration Helper - RAG Server

## Project: AdvancedDatabaseExplorer

**Állapot**: ✅ INDEXED  
**Fájlok**: 184 (Python + C#)  
**Chunks**: 1278 kódrészlet  
**DB méret**: 18.47 MB

---

## 🎯 Használati Példák a Migrációhoz

### 1. Kód Összehasonlítás

```powershell
# Python és C# kód összehasonlítása
$query = @{
    query = "Compare Python and C# database connection code"
    max_results = 8
} | ConvertTo-Json

$result = Invoke-RestMethod -Method Post -Uri "http://localhost:8000/query" `
    -Body $query -ContentType "application/json"

# Másold a Copilot-ba
$result.optimized_prompt | Set-Clipboard
```

### 2. Implementáció Keresése

```powershell
# Keress Python implementációt, amit C#-ba kell portolni
$query = @{
    query = "Show me the Python implementation of data extraction"
    max_results = 5
} | ConvertTo-Json

$result = Invoke-RestMethod -Method Post -Uri "http://localhost:8000/query" `
    -Body $query -ContentType "application/json"

$result.optimized_prompt | Set-Clipboard
```

### 3. C# Minták Keresése

```powershell
# Nézd meg, hogyan van már implementálva C#-ban
$query = @{
    query = "Show me existing C# implementations of database queries"
    max_results = 6
} | ConvertTo-Json

$result = Invoke-RestMethod -Method Post -Uri "http://localhost:8000/query" `
    -Body $query -ContentType "application/json"

$result.optimized_prompt | Set-Clipboard
```

### 4. Osztály Struktúra

```powershell
# Összehasonlítás: osztálystruktúra Python vs C#
$query = @{
    query = "Compare class structure between Python and C# versions"
    max_results = 10
} | ConvertTo-Json

$result = Invoke-RestMethod -Method Post -Uri "http://localhost:8000/query" `
    -Body $query -ContentType "application/json"

$result.optimized_prompt | Set-Clipboard
```

---

## 🤖 GitHub Copilot Workflow

### Workflow 1: Python → C# Konverzió

1. **Lekérdezés**:
   ```powershell
   $query = "Show me the Python TableComparator class implementation"
   # ... RAG query
   ```

2. **Copilot Chat**:
   ```
   I have this Python code [paste RAG context].
   
   Convert it to C# with:
   - Proper async/await patterns
   - LINQ where appropriate
   - Strong typing
   - XML documentation comments
   ```

3. **Eredmény**: Copilot generálja a C# kódot a teljes kontextussal!

### Workflow 2: Hiányzó Funkciók

1. **Kérdezz**:
   ```powershell
   $query = "What Python features are not yet implemented in C#?"
   ```

2. **Copilot Chat**:
   ```
   Based on this context [paste], what's missing in the C# version?
   Create a TODO list with priorities.
   ```

### Workflow 3: Refactoring Javaslatok

1. **Lekérdezés**:
   ```powershell
   $query = "Show me the database connection handling in both languages"
   ```

2. **Copilot Chat**:
   ```
   Compare these implementations [paste].
   Suggest improvements for the C# version following best practices.
   ```

---

## 🛠️ Hasznos PowerShell Függvények

Mentsd el a PowerShell profile-odba:

```powershell
# Microsoft.PowerShell_profile.ps1

function Ask-Migration {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Question,
        [int]$MaxResults = 8
    )
    
    $body = @{
        query = $Question
        max_results = $MaxResults
        include_metadata = $true
    } | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Method Post `
            -Uri "http://localhost:8000/query" `
            -Body $body `
            -ContentType "application/json"
        
        # Másold vágólapra
        $response.optimized_prompt | Set-Clipboard
        
        Write-Host "`n✅ RAG Context copied to clipboard!" -ForegroundColor Green
        Write-Host "Chunks: $($response.context_chunks)" -ForegroundColor Cyan
        Write-Host "Tokens: $($response.token_count)" -ForegroundColor Cyan
        Write-Host "`nPaste into GitHub Copilot Chat now!" -ForegroundColor Yellow
        
        return $response
    }
    catch {
        Write-Host "❌ Error: $_" -ForegroundColor Red
    }
}

# Használat:
# Ask-Migration "Compare Python and C# error handling"
```

---

## 📝 Gyakori Migration Kérdések

### Adatbázis Műveletek
```powershell
Ask-Migration "How is database connection handled in Python vs C#?"
Ask-Migration "Show me query execution in both languages"
Ask-Migration "Compare transaction handling"
```

### Osztály Struktúra
```powershell
Ask-Migration "Show me the DataExtractor class in both languages"
Ask-Migration "Compare inheritance patterns"
Ask-Migration "How are interfaces/abstract classes used?"
```

### Aszinkron Programozás
```powershell
Ask-Migration "Show async/await patterns in Python and C#"
Ask-Migration "How is parallel processing implemented?"
```

### Error Handling
```powershell
Ask-Migration "Compare exception handling strategies"
Ask-Migration "Show error logging implementations"
```

### Dependency Injection
```powershell
Ask-Migration "How is dependency injection done in C#?"
Ask-Migration "Show configuration management"
```

---

## 🎯 Példa Session

```powershell
# 1. Kérdezz a Python kódról
Ask-Migration "Show me the Python DatabaseComparator class"

# 2. Nyisd meg a Copilot Chat-et (Ctrl+Shift+I)
# 3. Paste (Ctrl+V)
# 4. Kiegészítés:
"Convert this Python class to C# following these guidelines:
- Use async/await for database operations
- Implement IDisposable for resource cleanup
- Use dependency injection for DatabaseConnector
- Add XML documentation
- Use LINQ for data operations"

# 5. Copilot generálja a C# kódot!

# 6. Ha kérdésed van az eredeti C# kódról:
Ask-Migration "Show me the existing C# DatabaseComparator implementation"

# 7. Összehasonlítás:
"Compare my generated code with the existing implementation.
What are the differences and which approach is better?"
```

---

## 📊 Migration Progress Tracking

```powershell
# Keress "TODO" vagy "NotImplemented" mintákat
Ask-Migration "Find all TODO comments and not implemented features in C# code"

# Keress hiányzó osztályokat
Ask-Migration "Which Python classes don't have C# equivalents yet?"

# Keress különbségeket
Ask-Migration "What are the main architectural differences between Python and C# versions?"
```

---

## 🚀 Pro Tips

1. **Specifikus legyen a kérdés**:
   - ❌ "Show me code"
   - ✅ "Show me the Python DatabaseConnection class and its C# equivalent"

2. **Használj kontextust**:
   - "Compare error handling in DatabaseComparator between Python and C#"

3. **Több chunk nagyobb projekt esetén**:
   ```powershell
   max_results = 10  # Több releváns kód
   ```

4. **Cache használata**:
   - Ugyanaz a query másodszor gyorsabb (Redis cache)
   - Ha friss eredmény kell: `force_reindex = $true`

5. **Token limit figyelése**:
   - Max 4000 token (alapértelmezett)
   - Ha túl sok: csökkentsd a `max_results`-t

---

## 🔄 Re-indexelés

Ha változtatsz a kódon:

```powershell
$body = @{
    project_path = "/app/data/projects/AdvancedDatabaseExplorer"
    file_extensions = @(".py", ".cs", ".csproj", ".sln")
    force_reindex = $true  # Kényszerített újraindexelés
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://localhost:8000/index" `
    -Body $body -ContentType "application/json"
```

---

## 📚 További Erőforrások

- **API Docs**: http://localhost:8000/docs
- **Statisztikák**: 
  ```powershell
  Invoke-RestMethod -Method Get -Uri "http://localhost:8000/stats"
  ```
- **Cache törlése**:
  ```powershell
  Invoke-RestMethod -Method Delete -Uri "http://localhost:8000/clear"
  ```

---

**Boldog migrálást Python-ról C#-ra a RAG szerver segítségével! 🚀**
