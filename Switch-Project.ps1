# Switch Active Project
# Usage: .\Switch-Project.ps1 [-ProjectPath "/app/data/projects/MyProject"]

param(
    [Parameter(Mandatory=$false)]
    [string]$ProjectPath
)

$cyan = "Cyan"
$green = "Green"
$yellow = "Yellow"
$red = "Red"
$white = "White"

$RAG_URL = "http://localhost:8000"

Write-Host "`n=== Switch RAG Project ===" -ForegroundColor $cyan
Write-Host ""

try {
    # Get available projects
    $projects = Invoke-RestMethod -Method Get -Uri "$RAG_URL/projects" -TimeoutSec 5
    
    if ($projects.total_projects -eq 0) {
        Write-Host "❌ No projects indexed!" -ForegroundColor $red
        Write-Host "Index a project first with: .\Reindex-Project.ps1" -ForegroundColor $yellow
        exit 1
    }
    
    Write-Host "Available Projects:" -ForegroundColor $yellow
    Write-Host ""
    
    $index = 1
    foreach ($proj in $projects.projects) {
        $current = if ($proj.is_current) { " [CURRENT]" } else { "" }
        Write-Host "  [$index] $($proj.name)$current" -ForegroundColor $(if ($proj.is_current) { $green } else { $white })
        Write-Host "      Path: $($proj.path)" -ForegroundColor $white
        Write-Host "      Files: $($proj.indexed_files), Chunks: $($proj.total_chunks)" -ForegroundColor $white
        $index++
    }
    Write-Host ""
    
    # If no project specified, prompt
    if ([string]::IsNullOrWhiteSpace($ProjectPath)) {
        $choice = Read-Host "Select project (1-$($projects.total_projects))"
        
        if ([string]::IsNullOrWhiteSpace($choice)) {
            Write-Host "No selection. Exiting." -ForegroundColor $yellow
            exit 0
        }
        
        $choiceNum = [int]$choice
        if ($choiceNum -lt 1 -or $choiceNum -gt $projects.total_projects) {
            Write-Host "❌ Invalid selection!" -ForegroundColor $red
            exit 1
        }
        
        $ProjectPath = $projects.projects[$choiceNum - 1].path
    }
    
    # Switch project
    Write-Host "Switching to: $ProjectPath" -ForegroundColor $cyan
    
    $body = @{ project_path = $ProjectPath } | ConvertTo-Json
    $response = Invoke-RestMethod -Method Post `
        -Uri "$RAG_URL/switch" `
        -Body $body `
        -ContentType "application/json" `
        -TimeoutSec 10
    
    Write-Host ""
    Write-Host "✅ $($response.message)" -ForegroundColor $green
    Write-Host ""
    Write-Host "Current project: $($response.current_project)" -ForegroundColor $cyan
    Write-Host ""
    Write-Host "You can now query this project with:" -ForegroundColor $yellow
    Write-Host "  .\Ask-RAG.ps1 'Your question'" -ForegroundColor $white
    Write-Host ""
    
} catch {
    Write-Host "❌ Error switching project!" -ForegroundColor $red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor $red
    Write-Host ""
    Write-Host "Is the RAG server running?" -ForegroundColor $yellow
    Write-Host "Check with: docker ps" -ForegroundColor $white
    exit 1
}
