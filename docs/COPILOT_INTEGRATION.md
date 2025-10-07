# GitHub Copilot Integration Guide

## 🤖 Hogyan Használd a RAG Szervert GitHub Copilot-tal

Ez az útmutató bemutatja, hogyan integráld a Local RAG Servert a GitHub Copilot-tal a jobb kódkontextus és kevesebb timeout érdekében.

---

## Megközelítések

### 1. 🔧 MCP (Model Context Protocol) Integration

Az MCP lehetővé teszi, hogy a Copilot közvetlenül használja a RAG szervert mint kontextus forrást.

#### Setup

1. **Telepítsd a GitHub Copilot Chat MCP bővítményt** (ha elérhető)

2. **Konfiguráld az MCP szervert**:

```json
// VS Code settings.json
{
  "github.copilot.advanced": {
    "mcp": {
      "servers": {
        "local-rag": {
          "command": "curl",
          "args": [
            "-X", "POST",
            "http://localhost:8000/query",
            "-H", "Content-Type: application/json",
            "-d", "{\"query\": \"{{prompt}}\", \"max_results\": 5}"
          ]
        }
      }
    }
  }
}
```

3. **Használd a `/rag` parancsot** a Copilot chatben:
```
/rag How does authentication work in this project?
```

---

### 2. 🎯 VS Code Extension (Egyedi)

Készíts egy saját VS Code bővítményt, amely összköti a Copilot-ot és a RAG szervert.

#### Extension.js példa:

```javascript
const vscode = require('vscode');
const axios = require('axios');

async function enhanceWithRAG(prompt) {
    try {
        const response = await axios.post('http://localhost:8000/query', {
            query: prompt,
            max_results: 5,
            include_metadata: true
        });
        
        return response.data.optimized_prompt;
    } catch (error) {
        console.error('RAG query failed:', error);
        return prompt; // Fallback to original
    }
}

async function activate(context) {
    // Register command
    let disposable = vscode.commands.registerCommand(
        'rag-copilot.enhanceQuery',
        async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) return;
            
            // Get current selection or prompt
            const selection = editor.selection;
            const text = editor.document.getText(selection);
            
            // Enhance with RAG
            const enhanced = await enhanceWithRAG(text);
            
            // Insert or show
            vscode.window.showInformationMessage('RAG Context Added!');
            // ... use enhanced prompt with Copilot API
        }
    );
    
    context.subscriptions.push(disposable);
}

module.exports = { activate };
```

---

### 3. 🐍 Python Helper Script

Használj egy Python scriptet, amely automatikusan hozzáadja a RAG kontextust.

#### rag_helper.py

```python
import sys
import requests
import json
import pyperclip  # pip install pyperclip

RAG_URL = "http://localhost:8000"

def enhance_prompt(prompt: str) -> str:
    """Enhance prompt with RAG context"""
    try:
        response = requests.post(
            f"{RAG_URL}/query",
            json={
                "query": prompt,
                "max_results": 5,
                "include_metadata": False
            },
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()["optimized_prompt"]
        else:
            print(f"Error: {response.status_code}")
            return prompt
            
    except Exception as e:
        print(f"RAG failed: {e}")
        return prompt

if __name__ == "__main__":
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        # Get from clipboard
        prompt = pyperclip.paste()
    
    enhanced = enhance_prompt(prompt)
    
    # Copy to clipboard
    pyperclip.copy(enhanced)
    print("✓ Enhanced prompt copied to clipboard!")
    print(f"\nOriginal: {len(prompt)} chars")
    print(f"Enhanced: {len(enhanced)} chars")
```

**Használat**:
```powershell
# Windows-on hotkey-hez kötve
python rag_helper.py "How does auth work?"

# Vagy clipboard-ról
# 1. Másold ki a kérdést
# 2. Futtasd: python rag_helper.py
# 3. Beillesztés Copilot-ba
```

---

### 4. 🔗 PowerShell Wrapper

Gyors PowerShell function a parancssorhoz.

```powershell
# Profil fájlba (Microsoft.PowerShell_profile.ps1):

function Get-RAGContext {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Query,
        
        [int]$MaxResults = 5
    )
    
    $body = @{
        query = $Query
        max_results = $MaxResults
        include_metadata = $false
    } | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Method Post `
            -Uri "http://localhost:8000/query" `
            -Body $body `
            -ContentType "application/json"
        
        # Copy to clipboard
        $response.optimized_prompt | Set-Clipboard
        
        Write-Host "✓ Context copied to clipboard!" -ForegroundColor Green
        Write-Host "Paste into Copilot Chat" -ForegroundColor Yellow
        
        return $response.optimized_prompt
    }
    catch {
        Write-Host "✗ RAG query failed: $_" -ForegroundColor Red
        return $Query
    }
}

# Alias
Set-Alias -Name rag -Value Get-RAGContext
```

**Használat**:
```powershell
# Terminal-ban
rag "How does authentication work?"

# Kimenet a clipboard-on, beillesztés Copilot-ba
```

---

## 📋 Workflow Példák

### Workflow 1: Code Review Prep

```powershell
# 1. Indexeld a projektet
$body = @{
    project_path = "C:\Projects\MyApp"
    file_extensions = @(".py", ".js")
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://localhost:8000/index" `
    -Body $body -ContentType "application/json"

# 2. Kérdezz review context-et
$body = @{
    query = "Show me all authentication and authorization code"
    max_results = 10
} | ConvertTo-Json

$context = Invoke-RestMethod -Method Post -Uri "http://localhost:8000/query" `
    -Body $body -ContentType "application/json"

# 3. Másold Copilot-ba
$context.optimized_prompt | Set-Clipboard

# 4. Nyisd meg a Copilot Chat-et és illesszd be
```

### Workflow 2: Bug Investigation

```powershell
# 1. Lekérdezés a problémás területről
rag "Find all error handling code related to database connections"

# 2. Copilot Chat-ben:
# "Based on this context [paste], why might we be getting connection timeout errors?"
```

### Workflow 3: Feature Development

```powershell
# 1. Research existing patterns
rag "Show me how API endpoints are structured in this project"

# 2. Copilot-ban:
# "Using these patterns [paste], help me create a new /api/users endpoint"
```

---

## 🎨 VS Code Tasks Integration

Készíts VS Code task-okat a gyakori műveletekhez.

### .vscode/tasks.json

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "RAG: Index Current Project",
      "type": "shell",
      "command": "powershell",
      "args": [
        "-Command",
        "$body = @{project_path = '${workspaceFolder}'; file_extensions = @('.py', '.js', '.ts')} | ConvertTo-Json; Invoke-RestMethod -Method Post -Uri 'http://localhost:8000/index' -Body $body -ContentType 'application/json'"
      ],
      "problemMatcher": [],
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "RAG: Get Project Stats",
      "type": "shell",
      "command": "powershell",
      "args": [
        "-Command",
        "Invoke-RestMethod -Method Get -Uri 'http://localhost:8000/stats' | ConvertTo-Json -Depth 10"
      ],
      "problemMatcher": [],
      "presentation": {
        "reveal": "always"
      }
    },
    {
      "label": "RAG: Clear Cache",
      "type": "shell",
      "command": "powershell",
      "args": [
        "-Command",
        "Invoke-RestMethod -Method Delete -Uri 'http://localhost:8000/clear'"
      ],
      "problemMatcher": []
    }
  ]
}
```

**Használat**: `Ctrl+Shift+P` → "Tasks: Run Task" → "RAG: Index Current Project"

---

## 🎯 Tippek a Legjobb Eredményekhez

### 1. **Konkrét Kérdések**
❌ Rossz: "How does this work?"
✅ Jó: "How does user authentication work in auth.py?"

### 2. **Kontextus Méret**
- Kisebb projektek: `max_results = 3-5`
- Nagyobb projektek: `max_results = 7-10`
- Specifikus keresés: `max_results = 3`

### 3. **Indexelési Stratégia**
```powershell
# Gyakran változó projektek - naponta egyszer
$body = @{force_reindex = $true}

# Stabil projektek - csak egyszer
$body = @{force_reindex = $false}
```

### 4. **Cache Használat**
- Első query lassabb (embedding generálás)
- Ugyanaz a query később gyors (cache)
- Cache TTL: 1 óra (konfigurálható)

### 5. **Multi-Project Setup**
```powershell
# Több projektet is indexelhetsz
function Index-AllProjects {
    $projects = @(
        "C:\Projects\Backend",
        "C:\Projects\Frontend",
        "C:\Projects\Shared"
    )
    
    foreach ($proj in $projects) {
        Write-Host "Indexing $proj..."
        # Index logic here
    }
}
```

---

## 🚀 Advanced: Automatic Context Injection

### Autopilot Script

```powershell
# auto_rag.ps1
# Figyeli a clipboard-ot és automatikusan bővíti RAG-gel

$lastClip = ""

while ($true) {
    $clip = Get-Clipboard
    
    if ($clip -ne $lastClip -and $clip -match "^Copilot:") {
        Write-Host "Detected Copilot query!" -ForegroundColor Cyan
        
        $query = $clip -replace "^Copilot:\s*", ""
        $enhanced = rag $query
        
        Write-Host "✓ Enhanced and copied!" -ForegroundColor Green
        
        $lastClip = $enhanced
    }
    
    Start-Sleep -Seconds 2
}
```

**Használat**:
1. Futtasd a scriptet a háttérben
2. Copilot Chat-ben írd: "Copilot: How does auth work?"
3. A script automatikusan bővíti RAG-gel
4. Illeszd be a bővített verziót

---

## 📊 Monitoring & Analytics

### Query Analytics Script

```python
# analytics.py
import requests
from collections import Counter
from datetime import datetime

def get_recent_queries():
    """Get Redis cache keys to see popular queries"""
    # This requires Redis CLI access
    pass

def track_query(query: str):
    """Track query for analytics"""
    timestamp = datetime.now().isoformat()
    with open("query_log.txt", "a") as f:
        f.write(f"{timestamp} | {query}\n")

# Usage
track_query("How does authentication work?")
```

---

## 🎓 Best Practices

1. **Index Before Starting**: Mindig indexeld a projektet munka előtt
2. **Update Regularly**: Nagy változások után újraindexelés
3. **Specific Queries**: Minél specifikusabb, annál jobb
4. **Monitor Performance**: Figyeld a token használatot
5. **Clear Cache**: Ha régi infót látsz, töröld a cache-t
6. **Use Stats**: Rendszeresen ellenőrizd a `/stats` endpoint-ot

---

## 🔮 Jövőbeli Lehetőségek

- **GitHub Copilot Native Extension**: Official Copilot extension
- **Automatic Context**: Auto-detect Copilot queries
- **Smart Ranking**: ML-based relevance
- **Multi-Modal**: Code + docs + comments
- **Team Sharing**: Shared index for teams

---

**Happy Coding with Enhanced Copilot! 🚀**
