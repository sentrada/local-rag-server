# Add New Project to RAG Server
# Usage: .\Add-Project.ps1 -ProjectName "MyProject" -ProjectPath "G:\Sources\MyProject"

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectName,
    
    [Parameter(Mandatory=$true)]
    [string]$ProjectPath,
    
    [Parameter(Mandatory=$false)]
    [string[]]$FileExtensions = @(".py", ".cs", ".ts", ".js", ".jsx", ".tsx", ".java", ".cpp", ".h")
)

$cyan = "Cyan"
$green = "Green"
$yellow = "Yellow"
$red = "Red"
$white = "White"

Write-Host "`n=== Add Project to RAG Server ===" -ForegroundColor $cyan
Write-Host ""

# Validate project path exists
if (-not (Test-Path $ProjectPath)) {
    Write-Host "❌ Error: Project path does not exist!" -ForegroundColor $red
    Write-Host "Path: $ProjectPath" -ForegroundColor $white
    exit 1
}

Write-Host "Project Details:" -ForegroundColor $yellow
Write-Host "  Name: $ProjectName" -ForegroundColor $white
Write-Host "  Path: $ProjectPath" -ForegroundColor $white
Write-Host "  File types: $($FileExtensions -join ', ')" -ForegroundColor $white
Write-Host ""

# Convert Windows path to Docker-compatible path
$dockerPath = $ProjectPath -replace '\\', '/'

Write-Host "Step 1: Add volume mount to docker-compose.yml" -ForegroundColor $cyan
Write-Host ""
Write-Host "Add this line to the 'volumes:' section:" -ForegroundColor $yellow
Write-Host "  - ${dockerPath}:/app/data/projects/${ProjectName}:ro" -ForegroundColor $green
Write-Host ""

Write-Host "Step 2: Restart containers" -ForegroundColor $cyan
Write-Host "  docker-compose down" -ForegroundColor $white
Write-Host "  docker-compose up -d" -ForegroundColor $white
Write-Host ""

Write-Host "Step 3: Index the new project" -ForegroundColor $cyan
Write-Host ""

$confirm = Read-Host "Would you like me to generate the reindex command? (Y/n)"
if ($confirm -ne "n" -and $confirm -ne "N") {
    Write-Host ""
    Write-Host "Run this command after restarting containers:" -ForegroundColor $yellow
    Write-Host ""
    Write-Host ".\Reindex-Project.ps1 ``" -ForegroundColor $green
    Write-Host "    -ProjectPath `"/app/data/projects/$ProjectName`" ``" -ForegroundColor $green
    Write-Host "    -FileExtensions @($($FileExtensions | ForEach-Object { "'$_'" } | Join-String -Separator ', '))" -ForegroundColor $green
    Write-Host ""
}

Write-Host ""
Write-Host "=== Manual Steps ===" -ForegroundColor $yellow
Write-Host ""
Write-Host "1. Edit docker-compose.yml and add the volume mount" -ForegroundColor $white
Write-Host "2. Run: docker-compose down" -ForegroundColor $white
Write-Host "3. Run: docker-compose up -d" -ForegroundColor $white
Write-Host "4. Run: .\Reindex-Project.ps1 -ProjectPath '/app/data/projects/$ProjectName'" -ForegroundColor $white
Write-Host "5. Query: .\Ask-RAG.ps1 'Your question about $ProjectName'" -ForegroundColor $white
Write-Host ""
Write-Host "Done! 🎉" -ForegroundColor $green
