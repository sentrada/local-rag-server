# List All Mounted Projects
# Usage: .\List-Projects.ps1

$cyan = "Cyan"
$green = "Green"
$yellow = "Yellow"
$white = "White"

Write-Host "`n=== Mounted Projects ===" -ForegroundColor $cyan
Write-Host ""

# Read docker-compose.yml
$composeFile = Get-Content "docker-compose.yml" -Raw

# Find volume mounts
$volumePattern = '-\s+([^:]+):(/app/data/projects/[^:]+):ro'
$matches = [regex]::Matches($composeFile, $volumePattern)

$projectCount = 0
foreach ($match in $matches) {
    $projectCount++
    $hostPath = $match.Groups[1].Value.Trim()
    $containerPath = $match.Groups[2].Value.Trim()
    $projectName = ($containerPath -split '/')[-1]
    
    Write-Host "[$projectCount] $projectName" -ForegroundColor $green
    Write-Host "    Host: $hostPath" -ForegroundColor $white
    Write-Host "    Container: $containerPath" -ForegroundColor $white
    
    # Check if path exists
    $expandedPath = [System.Environment]::ExpandEnvironmentVariables($hostPath)
    if ($hostPath -eq './') {
        $expandedPath = (Get-Location).Path
    }
    
    if (Test-Path $expandedPath) {
        $fileCount = (Get-ChildItem -Path $expandedPath -Recurse -File -ErrorAction SilentlyContinue | Measure-Object).Count
        Write-Host "    Status: ✅ Exists ($fileCount files)" -ForegroundColor $green
    } else {
        Write-Host "    Status: ⚠️  Path not found" -ForegroundColor $yellow
    }
    Write-Host ""
}

Write-Host "Total mounted projects: $projectCount" -ForegroundColor $cyan
Write-Host ""

# Get RAG server stats
Write-Host "=== RAG Server Stats ===" -ForegroundColor $cyan
Write-Host ""

try {
    $projectsInfo = Invoke-RestMethod -Uri "http://localhost:8000/projects" -Method Get -TimeoutSec 5
    
    if ($projectsInfo.total_projects -eq 0) {
        Write-Host "⚠️  No projects indexed yet" -ForegroundColor $yellow
        Write-Host ""
    } else {
        Write-Host "Total indexed projects: $($projectsInfo.total_projects)" -ForegroundColor $cyan
        Write-Host "Current project: $($projectsInfo.current_project)" -ForegroundColor $green
        Write-Host ""
        
        Write-Host "=== Indexed Projects ===" -ForegroundColor $cyan
        Write-Host ""
        
        $index = 1
        foreach ($proj in $projectsInfo.projects) {
            $current = if ($proj.is_current) { " [CURRENT]" } else { "" }
            Write-Host "[$index] $($proj.name)$current" -ForegroundColor $(if ($proj.is_current) { $green } else { $white })
            Write-Host "    Path: $($proj.path)" -ForegroundColor $white
            Write-Host "    Files: $($proj.indexed_files)" -ForegroundColor $white
            Write-Host "    Chunks: $($proj.total_chunks)" -ForegroundColor $white
            Write-Host ""
            $index++
        }
    }
    
} catch {
    Write-Host "⚠️  RAG server not responding" -ForegroundColor $yellow
    Write-Host "Is it running? Check with: docker ps" -ForegroundColor $white
    Write-Host ""
}

Write-Host "To add a new project:" -ForegroundColor $yellow
Write-Host "  .\Add-Project.ps1 -ProjectName 'MyProject' -ProjectPath 'G:\Sources\MyProject'" -ForegroundColor $white
Write-Host ""

Write-Host "To switch active project:" -ForegroundColor $yellow
Write-Host "  .\Switch-Project.ps1" -ForegroundColor $white
Write-Host ""

Write-Host "To reindex a project:" -ForegroundColor $yellow
Write-Host "  .\Reindex-Project.ps1 -ProjectPath '/app/data/projects/ProjectName'" -ForegroundColor $white
Write-Host ""

Write-Host "To query a specific project:" -ForegroundColor $yellow
Write-Host "  .\Ask-RAG.ps1 'Your question' -ProjectPath '/app/data/projects/ProjectName'" -ForegroundColor $white
Write-Host ""
