# setup_rag_server.ps1
param(
    [string]$RepoUrl = "https://github.com/sentrada/local-rag-server.git",
    [string]$TargetDir = "$PWD\local-rag-server"
)

Write-Host "=== RAG Server Telepítő ===" -ForegroundColor Cyan

# 1. Git ellenőrzése
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git nincs telepítve! Telepítsd a https://git-scm.com/ oldalról." -ForegroundColor Red
    exit 1
}

# 2. Docker vagy Podman ellenőrzése
if (-not (Get-Command docker -ErrorAction SilentlyContinue) -and -not (Get-Command podman -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker vagy Podman nincs telepítve! Telepítsd a https://www.docker.com/ vagy https://podman.io/ oldalról." -ForegroundColor Red
    exit 1
}

# 3. Repo klónozása
if (-not (Test-Path $TargetDir)) {
    git clone $RepoUrl $TargetDir
} else {
    Write-Host "📁 A célkönyvtár már létezik, frissítés..." -ForegroundColor Yellow
    Set-Location $TargetDir
    git pull
    Set-Location ..
}

# 4. .env beállítása
$envFile = Join-Path $TargetDir ".env"
$envExample = Join-Path $TargetDir ".env.example"
if (-not (Test-Path $envFile) -and (Test-Path $envExample)) {
    Copy-Item $envExample $envFile
    Write-Host "📝 .env fájl létrehozva. Szerkeszd a PROJECT_PATH sort!" -ForegroundColor Yellow
}

# 5. Konténer indítása
Set-Location $TargetDir
if (Get-Command docker -ErrorAction SilentlyContinue) {
    docker-compose up -d
} else {
    podman-compose up -d
}

Write-Host "✅ RAG szerver elindítva! API: http://localhost:8000/health" -ForegroundColor Green
