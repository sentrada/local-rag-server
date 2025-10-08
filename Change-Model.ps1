# Change-Model.ps1
# Interaktív modell váltó script
# Usage: .\Change-Model.ps1 -ProjectPath "/app/..." -Model "intfloat/multilingual-e5-large" [-AutoReindex]

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectPath,

    [Parameter(Mandatory=$true)]
    [string]$Model,

    [Parameter(Mandatory=$false)]
    [switch]$AutoReindex = $false
)

$cyan = "Cyan"
$green = "Green"
$yellow = "Yellow"
$red = "Red"
$white = "White"

$RAG_URL = "http://localhost:8000"

Write-Host "`n=== Change Embedding Model ===" -ForegroundColor $cyan
Write-Host ""
Write-Host "Project: $ProjectPath" -ForegroundColor $white
Write-Host "New model: $Model" -ForegroundColor $white
Write-Host "Auto reindex: $AutoReindex" -ForegroundColor $white
Write-Host ""

# Confirm
$confirm = Read-Host "WARNING: Model change will DELETE the current index and require reindexing! Continue? (Y/n)"
if ($confirm -eq "n" -or $confirm -eq "N") {
    Write-Host "Cancelled." -ForegroundColor $yellow
    exit 0
}

# Build request body
$body = @{ model = $Model; auto_reindex = $AutoReindex.IsPresent } | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Method Post `
        -Uri "$RAG_URL/projects/model/change?project_path=$([uri]::EscapeDataString($ProjectPath))" `
        -Body $body `
        -ContentType "application/json" `
        -TimeoutSec 30

    Write-Host "✅ Model changed!" -ForegroundColor $green
    Write-Host "Status: $($response.status)" -ForegroundColor $white
    Write-Host "Project: $($response.project_path)" -ForegroundColor $white
    Write-Host "Embedding model: $($response.embedding_model)" -ForegroundColor $white
    if ($response.PSObject.Properties.Name -contains 'reindex_started' -and $response.reindex_started) {
        Write-Host "Reindexing started automatically." -ForegroundColor $yellow
    }
    Write-Host ""
} catch {
    Write-Host "❌ Error changing model!" -ForegroundColor $red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor $red
    Write-Host ""
    exit 1
}
