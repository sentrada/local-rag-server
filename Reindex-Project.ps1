# Re-index Project Script
# Usage: .\Reindex-Project.ps1

param(
    [Parameter(Mandatory=$false)]
    [string]$ProjectPath = "/app/data/projects/AdvancedDatabaseExplorer",

    [Parameter(Mandatory=$false)]
    [string[]]$FileExtensions = @(".py", ".ps1", ".md", ".ts", ".js", ".tsx", ".cs", ".csproj", ".sln"),

    [Parameter(Mandatory=$false)]
    [string]$Model = "all-MiniLM-L6-v2",

    [Parameter(Mandatory=$false)]
    [switch]$ForceReindex = $false
)

# Colors
$cyan = "Cyan"
$green = "Green"
$yellow = "Yellow"
$red = "Red"
$white = "White"

# RAG Server URL
$RAG_URL = "http://localhost:8000"

Write-Host "`n=== RAG Project Re-indexing ===" -ForegroundColor $cyan
Write-Host ""

# Show current settings
Write-Host "Settings:" -ForegroundColor $yellow
Write-Host "  Project: $ProjectPath" -ForegroundColor $white
Write-Host "  File types: $($FileExtensions -join ', ')" -ForegroundColor $white
Write-Host "  Embedding model: $Model" -ForegroundColor $white
Write-Host "  Force reindex: $ForceReindex" -ForegroundColor $white
Write-Host ""

# Confirm
$confirm = Read-Host "Proceed with indexing? (Y/n)"
if ($confirm -eq "n" -or $confirm -eq "N") {
    Write-Host "Cancelled." -ForegroundColor $yellow
    exit 0
}

Write-Host "`nStarting indexing..." -ForegroundColor $cyan

# Build request body
$body = @{
    project_path = $ProjectPath
    file_extensions = $FileExtensions
    model = $Model
    force_reindex = $ForceReindex.IsPresent
} | ConvertTo-Json

try {
    # Send index request
    $response = Invoke-RestMethod -Method Post `
        -Uri "$RAG_URL/index" `
        -Body $body `
        -ContentType "application/json" `
        -TimeoutSec 30
    
    Write-Host "✅ Indexing Started!" -ForegroundColor $green
    Write-Host ""
    Write-Host "Status: $($response.status)" -ForegroundColor $white
    Write-Host "Project: $($response.project_path)" -ForegroundColor $white
    Write-Host "File types: $($response.file_extensions -join ', ')" -ForegroundColor $white
    if ($response.PSObject.Properties.Name -contains 'embedding_model') {
        Write-Host "Embedding model: $($response.embedding_model)" -ForegroundColor $white
    }
    Write-Host ""
    Write-Host "⏳ Indexing is running in the background..." -ForegroundColor $yellow
    Write-Host "This may take 30-60 seconds for medium projects." -ForegroundColor $yellow
    Write-Host ""
    
    # Wait a bit
    Write-Host "Waiting 40 seconds for indexing to complete..." -ForegroundColor $cyan
    Start-Sleep -Seconds 40
    
    # Check stats
    Write-Host "`nChecking results..." -ForegroundColor $cyan
    try {
        $stats = Invoke-RestMethod -Method Get -Uri "$RAG_URL/stats" -TimeoutSec 10
        
        Write-Host ""
        Write-Host "=== Indexing Complete ===" -ForegroundColor $green
        Write-Host ""
        Write-Host "Project: $($stats.project_root)" -ForegroundColor $white
        Write-Host "Indexed files: $($stats.indexed_files)" -ForegroundColor $cyan
        Write-Host "Total chunks: $($stats.total_chunks)" -ForegroundColor $cyan
        Write-Host "DB size: $($stats.vector_db_size)" -ForegroundColor $cyan
        Write-Host "Embedding model: $($stats.embedding_model)" -ForegroundColor $white
        Write-Host ""
        Write-Host "✅ Ready for queries!" -ForegroundColor $green
        Write-Host ""
        
    } catch {
        Write-Host "⚠️  Could not fetch stats (indexing might still be running)" -ForegroundColor $yellow
        Write-Host "Check logs with: docker logs local-rag-server --tail 50" -ForegroundColor $white
    }
    
} catch {
    Write-Host "❌ Error starting indexing!" -ForegroundColor $red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor $red
    Write-Host ""
    Write-Host "Is the RAG server running?" -ForegroundColor $yellow
    Write-Host "Check with: docker ps" -ForegroundColor $white
    Write-Host ""
    exit 1
}

Write-Host ""
Write-Host "To view detailed logs:" -ForegroundColor $yellow
Write-Host "  docker logs local-rag-server -f" -ForegroundColor $white
Write-Host ""
