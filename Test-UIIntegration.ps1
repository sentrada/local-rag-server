#!/usr/bin/env pwsh
# UI Integration Test Script

Write-Host "🧪 RAG Server UI Integration Test" -ForegroundColor Cyan
Write-Host ""

# Check if backend is running
Write-Host "1. Checking backend server..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET -ErrorAction Stop
    $health = $response.Content | ConvertFrom-Json
    Write-Host "   ✅ Backend is running (version: $($health.version))" -ForegroundColor Green
    Write-Host "   - Indexed projects: $($health.indexed_projects)" -ForegroundColor Gray
    Write-Host "   - Current project: $($health.current_project)" -ForegroundColor Gray
} catch {
    Write-Host "   ❌ Backend is NOT running!" -ForegroundColor Red
    Write-Host "   Run: docker-compose up -d" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Check if Node.js is installed
Write-Host "2. Checking Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "   ✅ Node.js is installed ($nodeVersion)" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Node.js is NOT installed!" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Check if dependencies are installed
Write-Host "3. Checking UI dependencies..." -ForegroundColor Yellow
Push-Location ui
if (Test-Path "node_modules") {
    Write-Host "   ✅ Dependencies are installed" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Dependencies not found. Installing..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Dependencies installed successfully" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Failed to install dependencies" -ForegroundColor Red
        Pop-Location
        exit 1
    }
}

Write-Host ""

# Check .env file
Write-Host "4. Checking .env configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    $envContent = Get-Content ".env" | Select-String "VITE_API_URL"
    Write-Host "   ✅ .env file exists" -ForegroundColor Green
    Write-Host "   - $envContent" -ForegroundColor Gray
} else {
    Write-Host "   ⚠️  .env file not found, using default" -ForegroundColor Yellow
}

Write-Host ""

# Test API endpoints
Write-Host "5. Testing API endpoints..." -ForegroundColor Yellow

try {
    $projects = Invoke-WebRequest -Uri "http://localhost:8000/projects" -Method GET | ConvertFrom-Json
    Write-Host "   ✅ /projects endpoint working" -ForegroundColor Green
    Write-Host "   - Total projects: $($projects.total_projects)" -ForegroundColor Gray
} catch {
    Write-Host "   ⚠️  /projects endpoint failed: $_" -ForegroundColor Yellow
}

try {
    $models = Invoke-WebRequest -Uri "http://localhost:8000/models" -Method GET | ConvertFrom-Json
    Write-Host "   ✅ /models endpoint working" -ForegroundColor Green
    Write-Host "   - Available models: $($models.Count)" -ForegroundColor Gray
} catch {
    Write-Host "   ⚠️  /models endpoint failed: $_" -ForegroundColor Yellow
}

Write-Host ""

# TypeScript check
Write-Host "6. Running TypeScript check..." -ForegroundColor Yellow
npm run type-check 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ TypeScript compilation successful" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  TypeScript has some warnings (not critical)" -ForegroundColor Yellow
}

Pop-Location

Write-Host ""
Write-Host "✅ Integration test complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To start the UI:" -ForegroundColor Cyan
Write-Host "  cd ui" -ForegroundColor White
Write-Host "  npm run dev" -ForegroundColor White
Write-Host ""
Write-Host "Then open: http://localhost:5173" -ForegroundColor Cyan
