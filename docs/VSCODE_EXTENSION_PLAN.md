# VS Code Extension for Local RAG Server

## 🎯 Cél

Integrált RAG Server elérés közvetlenül a VS Code-ból, mintha a GitHub Copilot része lenne.

## ✨ Funkciók

### 1. **Inline Code Suggestions**
- Kijelölt kód → Right-click → "Ask RAG about this"
- Gyors válasz tooltip-ben vagy side panel-ben

### 2. **RAG Chat Panel**
- Dedikált chat ablak a VS Code sidebar-ban
- Conversation history
- Project selector dropdown

### 3. **Status Bar Integration**
- RAG Server connection status (🟢/🔴)
- Aktuális projekt megjelenítése
- Indexelt fájlok száma
- Click → Quick actions

### 4. **Command Palette Commands**
- `RAG: Ask Question`
- `RAG: Reindex Current Project`
- `RAG: Switch Project`
- `RAG: Show Stats`
- `RAG: Clear Cache`

### 5. **Quick Actions**
- Right-click on file → "Index this file"
- Right-click on folder → "Index this folder"
- Hover over function → "Find similar implementations"

### 6. **Code Lens Integration**
- Inline hints a kód fölött:
  ```python
  # 👁️ 3 similar implementations found
  def authenticate_user(username, password):
  ```

### 7. **Hover Tooltips**
- Hover over function/class → Show RAG context
- Similar code snippets preview
- Usage examples

### 8. **Notifications**
- Indexing complete notification
- New relevant code found
- RAG server status changes

## 🏗️ Architektúra

```
┌─────────────────────────────────────────────────────────┐
│                   VS Code Extension                     │
│                                                         │
│  ┌───────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │  Sidebar View │  │ Status Bar   │  │ Commands    │ │
│  │  (Chat)       │  │ Widget       │  │ & Actions   │ │
│  └───────┬───────┘  └──────┬───────┘  └──────┬──────┘ │
│          │                  │                  │        │
│          └──────────────────┴──────────────────┘        │
│                             │                           │
│                    ┌────────▼────────┐                  │
│                    │  RAG Client     │                  │
│                    │  (HTTP/WS)      │                  │
│                    └────────┬────────┘                  │
└─────────────────────────────┼─────────────────────────┘
                              │
                              │ HTTP/WebSocket
                              ▼
                    ┌──────────────────┐
                    │   RAG Server     │
                    │   (FastAPI)      │
                    │   localhost:8000 │
                    └──────────────────┘
```

## 📦 Projekt Struktúra

```
vscode-rag-extension/
├── package.json
├── tsconfig.json
├── README.md
├── CHANGELOG.md
├── src/
│   ├── extension.ts          # Main entry point
│   ├── ragClient.ts           # RAG Server API client
│   ├── statusBar.ts           # Status bar widget
│   ├── chatPanel.ts           # Chat sidebar panel
│   ├── commands.ts            # Command handlers
│   ├── codeActions.ts         # Quick actions & code lens
│   └── config.ts              # Configuration management
├── media/
│   ├── icon.png
│   └── styles.css
└── resources/
    └── webview/
        ├── chat.html
        └── chat.js
```

## 🚀 Kezdeti Implementáció

### package.json Feature Highlights
```json
{
  "activationEvents": [
    "onStartupFinished",
    "onCommand:rag.askQuestion"
  ],
  "contributes": {
    "commands": [
      {
        "command": "rag.askQuestion",
        "title": "RAG: Ask Question",
        "icon": "$(search)"
      }
    ],
    "viewsContainers": {
      "activitybar": [
        {
          "id": "rag-sidebar",
          "title": "RAG Assistant",
          "icon": "media/icon.svg"
        }
      ]
    },
    "menus": {
      "editor/context": [
        {
          "command": "rag.askAboutSelection",
          "when": "editorHasSelection"
        }
      ]
    }
  }
}
```

## 🎨 UI Mockups

### Status Bar
```
🟢 RAG: AdvancedDatabaseExplorer (1,284 chunks) | Click for actions
```

### Chat Panel
```
┌─────────────────────────────────┐
│  RAG Assistant                  │
│  Project: [AdvancedDatabase ▼] │
├─────────────────────────────────┤
│                                 │
│  💬 You: How does auth work?   │
│                                 │
│  🤖 RAG: Based on your code:   │
│     • auth.py:123-145          │
│     • middleware.py:45-67      │
│     [Show full context]        │
│                                 │
│  ┌─────────────────────────┐   │
│  │ Type your question...   │   │
│  └─────────────────────────┘   │
└─────────────────────────────────┘
```

## 🔧 Fejlesztési Fázisok

### Phase 1: Core (MVP)
- [ ] RAG Server connection
- [ ] Status bar widget
- [ ] Basic command: Ask Question
- [ ] Simple output channel for responses

### Phase 2: Chat Interface
- [ ] Sidebar chat panel
- [ ] Conversation history
- [ ] Project selector
- [ ] Copy to clipboard button

### Phase 3: Code Integration
- [ ] Right-click context menu
- [ ] Selection-based queries
- [ ] Hover tooltips
- [ ] Code lens integration

### Phase 4: Advanced Features
- [ ] WebSocket for real-time updates
- [ ] Auto-indexing notifications
- [ ] Inline diff suggestions
- [ ] Multi-project comparison

## 💡 Használati Példák

### 1. Gyors kérdés
```
1. Select code
2. Right-click → "Ask RAG about this"
3. Response appears in chat panel
```

### 2. Chat használat
```
1. Open RAG sidebar (Ctrl+Shift+R)
2. Type: "Show me all database connections"
3. Get contextualized results with file links
4. Click file link → jumps to code
```

### 3. Status bar quick actions
```
1. Click RAG status in status bar
2. Quick menu:
   - Reindex current project
   - Switch project
   - Show statistics
   - Open chat
```

## 🔌 API Integration

### RAG Client Example
```typescript
class RAGClient {
  private baseUrl: string = 'http://localhost:8000';
  
  async query(text: string, project?: string) {
    const response = await fetch(`${this.baseUrl}/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: text,
        project_path: project,
        max_results: 5,
        include_metadata: true
      })
    });
    return response.json();
  }
  
  async getProjects() {
    const response = await fetch(`${this.baseUrl}/projects`);
    return response.json();
  }
}
```

## 📝 Következő Lépések

1. **Projekt inicializálás** - VS Code extension scaffold létrehozása
2. **RAG Client** - API wrapper implementálása
3. **Status Bar** - Egyszerű status widget
4. **Basic Command** - "Ask Question" command
5. **Chat Panel** - Webview-based chat interface
6. **Context Menu** - Right-click integration
7. **Testing** - Unit és integration tesztek
8. **Documentation** - Használati útmutató
9. **Publishing** - VS Code Marketplace release

Szeretnéd hogy kezdjem el implementálni? Milyen fázissal induljunk?
