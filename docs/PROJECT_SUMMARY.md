# Project Summary - Local RAG Server

## 📋 Overview

A production-ready RAG (Retrieval-Augmented Generation) server designed to enhance GitHub Copilot's capabilities for large projects while avoiding timeout issues.

## 🎯 Purpose

GitHub Copilot has limited context window and can timeout on large projects. This server:
- Indexes your codebase intelligently
- Provides relevant context on-demand
- Caches results for fast responses
- Integrates seamlessly with your workflow

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    GitHub Copilot                       │
│                                                         │
│  User Query: "How does authentication work?"           │
└────────────────────┬───────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   RAG Server (FastAPI)                  │
│                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Query     │──│  Cache Check │──│   Respond    │  │
│  │  Processor  │  │    (Redis)   │  │  with Context│  │
│  └─────────────┘  └──────────────┘  └──────────────┘  │
│         │                                    ▲          │
│         │                                    │          │
│         ▼                                    │          │
│  ┌─────────────┐                            │          │
│  │   Vector    │                            │          │
│  │   Search    │───────────────────────────┘          │
│  │  (ChromaDB) │                                       │
│  └─────────────┘                                       │
└─────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Your Project Files                         │
│                                                         │
│  /projects/MyApp/                                       │
│    ├── backend/  (Python, .py)                         │
│    ├── frontend/ (TypeScript, .tsx)                    │
│    └── shared/   (JavaScript, .js)                     │
└─────────────────────────────────────────────────────────┘
```

## 📦 Components

### Core Components

| Component | Technology | Purpose |
|-----------|------------|---------|
| **API Server** | FastAPI | REST API for indexing & queries |
| **Vector Store** | ChromaDB | Semantic search & embeddings |
| **Cache** | Redis | Fast query result caching |
| **Code Parser** | Python | Intelligent code chunking |
| **Context Manager** | tiktoken | Token optimization |

### File Structure

```
local-rag-server/
├── src/                      # Main application code
│   ├── main.py              # FastAPI app & endpoints
│   ├── rag_system.py        # Core RAG orchestration
│   ├── vector_store.py      # ChromaDB interface
│   ├── context_manager.py   # Token & context optimization
│   ├── code_parser.py       # Intelligent code chunking
│   ├── cache_manager.py     # Redis caching
│   └── utils.py             # Helper functions
├── examples/                 # Usage examples
│   ├── copilot_extension.py # GitHub Copilot integration
│   └── usage_examples.py    # API usage examples
├── config/                   # Configuration files
│   └── mcp-config.json      # MCP server config
├── data/                     # Data storage
│   ├── chroma_db/           # Vector database
│   └── projects/            # Mounted project files
├── logs/                     # Application logs
├── docker-compose.yml        # Production setup
├── docker-compose.dev.yml    # Development setup
├── Dockerfile               # Container definition
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
├── README.md                # Main documentation
├── QUICKSTART.md            # Quick start guide
├── TROUBLESHOOTING.md       # Common issues
├── COPILOT_INTEGRATION.md   # Copilot integration guide
└── CHANGELOG.md             # Version history
```

## 🚀 Key Features

### 1. Intelligent Indexing
- **Language-aware parsing**: Understands Python, JavaScript, TypeScript, etc.
- **Function/class detection**: Identifies code structure
- **Smart chunking**: Overlapping chunks for context preservation
- **Incremental updates**: Only re-indexes changed files
- **Auto-exclusion**: Skips node_modules, .git, etc.

### 2. Semantic Search
- **Vector embeddings**: Uses sentence-transformers
- **Similarity search**: Finds most relevant code
- **Metadata filtering**: Filter by file, function, class
- **Configurable results**: Adjust relevance threshold

### 3. Context Optimization
- **Token counting**: Accurate with tiktoken
- **Auto-truncation**: Fits within token limits
- **Smart ordering**: Most relevant first
- **Metadata enrichment**: File paths, line numbers, etc.

### 4. Caching & Performance
- **Redis cache**: Sub-second response for cached queries
- **1-hour TTL**: Configurable expiration
- **Hash-based keys**: Efficient storage
- **Cache stats**: Monitor hit/miss rates

### 5. API & Integration
- **RESTful API**: Standard HTTP endpoints
- **OpenAPI docs**: Interactive documentation
- **Async support**: Non-blocking operations
- **CORS enabled**: Frontend integration ready

## 📊 Performance Metrics

### Typical Performance

| Operation | First Time | Cached |
|-----------|------------|--------|
| Small project index (100 files) | 10-30s | - |
| Medium project (1000 files) | 1-3 min | - |
| Large project (5000 files) | 5-10 min | - |
| Query response | 1-3s | <100ms |
| Context generation | 500ms-2s | <50ms |

### Resource Usage

| Resource | Idle | Light Load | Heavy Load |
|----------|------|------------|------------|
| Memory | ~500MB | ~1GB | ~2GB |
| CPU | <5% | 20-40% | 60-80% |
| Disk | ~100MB | ~500MB | ~2GB |

## 🔧 Configuration Options

### Environment Variables

```env
# .env file
PROJECT_PATH=/mnt/c/Users/Name/Projects  # Your projects
LOG_LEVEL=INFO                           # DEBUG, INFO, WARNING, ERROR
MAX_CONTEXT_TOKENS=4000                  # Token limit
EMBEDDING_MODEL=all-MiniLM-L6-v2        # Embedding model
REDIS_URL=redis://redis:6379/0          # Cache connection
```

### Embedding Models

| Model | Size | Speed | Quality |
|-------|------|-------|---------|
| all-MiniLM-L6-v2 | 80MB | Fast | Good |
| all-mpnet-base-v2 | 420MB | Medium | Better |
| all-distilroberta-v1 | 290MB | Medium | Better |

**Recommendation**: Use `all-MiniLM-L6-v2` for best speed/quality balance

## 🎯 Use Cases

### 1. Code Understanding
```
Query: "How does the authentication system work?"
Result: Relevant auth code from multiple files
```

### 2. Pattern Discovery
```
Query: "Show me all API endpoint definitions"
Result: FastAPI/Express route handlers
```

### 3. Bug Investigation
```
Query: "Find error handling for database connections"
Result: Try-catch blocks, error handlers
```

### 4. Feature Development
```
Query: "How are user models structured?"
Result: Model definitions, schemas, migrations
```

### 5. Code Review
```
Query: "Show me all security-related code"
Result: Auth, validation, encryption code
```

## 📈 Scalability

### Project Size Limits

| Project Size | Files | LOC | Recommended Resources |
|--------------|-------|-----|----------------------|
| Small | <500 | <50K | 2GB RAM, 2 CPU |
| Medium | 500-2K | 50K-200K | 4GB RAM, 4 CPU |
| Large | 2K-10K | 200K-1M | 8GB RAM, 4+ CPU |
| Very Large | >10K | >1M | 16GB RAM, 8+ CPU |

### Optimization Tips

1. **Selective indexing**: Only index relevant file types
2. **Batch operations**: Index multiple projects separately
3. **Cache warmup**: Pre-cache common queries
4. **Regular cleanup**: Clear old cache entries
5. **Resource limits**: Docker memory/CPU limits

## 🔒 Security Considerations

### Data Privacy
- ✅ **Local only**: No data leaves your machine
- ✅ **Read-only mounts**: Projects mounted read-only
- ✅ **No telemetry**: ChromaDB telemetry disabled
- ✅ **No external calls**: All processing local

### Access Control
- 🔒 **No authentication**: Assumes local trusted environment
- 🔒 **CORS enabled**: Configure for production
- 🔒 **Docker isolation**: Containers isolated
- 🔒 **Volume permissions**: Proper file permissions

**Note**: This is designed for local development. Add authentication for production use.

## 🧪 Testing

### Manual Testing
```powershell
# Run test suite
python test_server.py

# Run examples
python examples/usage_examples.py
```

### API Testing
```powershell
# Health check
curl http://localhost:8000/health

# API docs
Start-Process "http://localhost:8000/docs"
```

## 📝 Maintenance

### Regular Tasks

**Daily**:
- Check logs for errors
- Monitor disk usage

**Weekly**:
- Clear cache: `DELETE /clear`
- Review statistics: `GET /stats`

**Monthly**:
- Update dependencies
- Rebuild containers
- Clean Docker volumes

### Backup

```powershell
# Backup ChromaDB
Copy-Item -Recurse data/chroma_db data/chroma_db.backup

# Restore
Remove-Item -Recurse data/chroma_db
Copy-Item -Recurse data/chroma_db.backup data/chroma_db
```

## 🎓 Learning Resources

### Internal Docs
- [README.md](README.md) - Complete documentation
- [QUICKSTART.md](QUICKSTART.md) - Quick setup
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Problem solving
- [COPILOT_INTEGRATION.md](COPILOT_INTEGRATION.md) - Copilot guide

### External Resources
- [ChromaDB Docs](https://docs.trychroma.com/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [Redis Docs](https://redis.io/docs/)

## 🤝 Contributing

### Development Setup

```powershell
# Clone and setup
git clone <repo>
cd local-rag-server

# Development mode
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Make changes in src/
# Server auto-reloads
```

### Code Style
- Python: PEP 8
- Docstrings: Google style
- Type hints: Required
- Logging: Use logger, not print

## 📄 License

MIT License - See LICENSE file

## 🆘 Support

### Getting Help
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Review logs: `docker-compose logs -f`
3. Run diagnostics: `python test_server.py`
4. Open an issue on GitHub

### Common Issues
- **Port 8000 busy**: Change port in docker-compose.yml
- **Out of memory**: Increase Docker memory limit
- **Slow indexing**: Reduce file types, exclude large dirs
- **No results**: Check `/stats`, verify indexing

---

## 📊 Project Stats

- **Lines of Code**: ~2,000
- **Files**: 25+
- **Languages**: Python, PowerShell, Docker
- **Dependencies**: 15+
- **Documentation**: 1,500+ lines
- **Version**: 2.0.0

---

**Built with ❤️ for better coding with GitHub Copilot**
