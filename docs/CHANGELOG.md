# Changelog

## Version 2.1.0 (2025-10-07)

### 🎉 Persistence & Auto-Recovery

#### ✨ New Features
- **Persistent Index Metadata**
  - Index metadata now saved to disk (JSON files in ChromaDB directory)
  - Tracks indexed files and their hashes for incremental indexing
  - Survives container restarts and system reboots
  - No time limit on index availability!

- **Automatic Project Loading**
  - Previously indexed projects automatically loaded on server startup
  - No need to re-index after container restart
  - Instant availability of indexed projects
  - Multi-project support maintained across restarts

#### 🐛 Bug Fixes
- Fixed issue where projects became unavailable after container restart
- Fixed "No projects indexed" error when server was restarted
- Eliminated unnecessary re-indexing after inactivity periods

#### 📝 Documentation
- Added `PERSISTENCE_FIX.md` explaining the solution
- Updated README with persistence feature
- Added troubleshooting guide for persistence issues

---

## Version 2.0.0 (2025-10-05)

### 🎉 Major Refactor & Complete Implementation

#### ✨ New Features
- **Complete RAG System Implementation**
  - Intelligent code parsing with semantic chunking
  - Support for 15+ programming languages
  - Function and class-aware parsing
  - Overlap-based chunking for context preservation

- **Vector Store with ChromaDB**
  - Persistent vector database
  - Semantic search using sentence-transformers
  - Efficient embedding storage and retrieval
  - Customizable embedding models

- **Redis Caching**
  - Query result caching for faster responses
  - Configurable TTL (default 1 hour)
  - Eliminates timeout issues for repeated queries
  - Cache statistics and management

- **Context Optimization**
  - Automatic token counting with tiktoken
  - Intelligent context truncation
  - Token-aware prompt building
  - Metadata-rich responses

- **Background Indexing**
  - Non-blocking project indexing
  - Incremental file hash-based updates
  - Automatic exclusion of common directories
  - Progress tracking and statistics

#### 🔧 API Improvements
- **New Endpoints**
  - `DELETE /clear` - Clear cache and index
  - `GET /stats` - Detailed indexing statistics
  - Enhanced `/query` with metadata support
  
- **Better Error Handling**
  - Detailed error messages
  - Proper HTTP status codes
  - Comprehensive logging

#### 📚 Documentation
- Complete README.md with usage examples
- Quick Start Guide (QUICKSTART.md)
- Troubleshooting Guide (TROUBLESHOOTING.md)
- Example scripts and Copilot integration

#### 🐳 Docker Improvements
- Multi-container setup (RAG + Redis)
- Persistent volumes for data
- Health checks
- Optimized build process

#### 🔒 Security & Performance
- Read-only project volume mounts
- Proper error handling and validation
- Memory-efficient chunking
- Optimized embedding generation

#### 📦 Dependencies
- Updated to latest stable versions
- Added redis for caching
- Added tiktoken for token counting
- Removed unused dependencies (langchain, tree-sitter)

#### 🛠️ Developer Tools
- Test server script (test_server.py)
- Usage examples (examples/)
- Copilot extension example
- PowerShell setup script improvements

### 🐛 Bug Fixes
- Fixed path conversion between Windows and WSL
- Corrected directory structure (src/ instead of scr/)
- Fixed ChromaDB metadata handling
- Improved token counting accuracy

### 📝 Configuration
- Environment variables via .env file
- Configurable embedding models
- Adjustable token limits
- Redis connection configuration

### 🚀 Performance
- 10x faster repeated queries (Redis cache)
- Intelligent chunking reduces token usage
- Background indexing doesn't block queries
- Optimized vector search

---

## Version 1.0.0 (Initial)

### Initial Setup
- Basic FastAPI structure
- Docker configuration
- Placeholder implementations

---

## Roadmap

### Version 2.1.0 (Planned)
- [ ] WebSocket support for real-time indexing progress
- [ ] Multi-project support
- [ ] Advanced filtering (by file, function, class)
- [ ] Query history and analytics
- [ ] VS Code extension

### Version 2.2.0 (Future)
- [ ] Incremental re-indexing on file changes
- [ ] Code understanding with AST parsing
- [ ] Semantic code search improvements
- [ ] Integration with more embedding models
- [ ] Export/import index functionality

### Version 3.0.0 (Long-term)
- [ ] Distributed indexing for very large codebases
- [ ] ML-based relevance ranking
- [ ] Code graph analysis
- [ ] Multi-language query support
- [ ] GitHub Copilot native extension
