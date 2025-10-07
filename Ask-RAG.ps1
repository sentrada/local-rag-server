# RAG Query Script - Ask migration questions easily
# Usage: .\Ask-RAG.ps1 "Your question here"

param(
    [Parameter(Mandatory=$false)]
    [string]$Question,
    
    [Parameter(Mandatory=$false)]
    [int]$MaxResults = 8,
    
    [Parameter(Mandatory=$false)]
    [string]$ProjectPath = $null  # Optional: specify project path
)

# Colors
$cyan = "Cyan"
$green = "Green"
$yellow = "Yellow"
$red = "Red"
$white = "White"

# RAG Server URL
$RAG_URL = "http://localhost:8000"

# Get available projects if no project specified
if ([string]::IsNullOrWhiteSpace($ProjectPath)) {
    try {
        $projectsResponse = Invoke-RestMethod -Method Get -Uri "$RAG_URL/projects" -TimeoutSec 5 -ErrorAction Stop
        
        if ($projectsResponse.total_projects -eq 0) {
            Write-Host "❌ No projects indexed!" -ForegroundColor $red
            Write-Host "Index a project first with: .\Reindex-Project.ps1" -ForegroundColor $yellow
            exit 1
        }
        
        if ($projectsResponse.total_projects -gt 1) {
            Write-Host "`n=== Available Projects ===" -ForegroundColor $cyan
            $index = 1
            foreach ($proj in $projectsResponse.projects) {
                $current = if ($proj.is_current) { " [CURRENT]" } else { "" }
                Write-Host "  [$index] $($proj.name)$current" -ForegroundColor $white
                Write-Host "      Path: $($proj.path)" -ForegroundColor $(if ($proj.is_current) { $green } else { $white })
                Write-Host "      Files: $($proj.indexed_files), Chunks: $($proj.total_chunks)" -ForegroundColor $white
                $index++
            }
            Write-Host ""
            
            $choice = Read-Host "Select project (1-$($projectsResponse.total_projects), or Enter for current)"
            
            if (![string]::IsNullOrWhiteSpace($choice)) {
                $choiceNum = [int]$choice
                if ($choiceNum -ge 1 -and $choiceNum -le $projectsResponse.total_projects) {
                    $ProjectPath = $projectsResponse.projects[$choiceNum - 1].path
                    Write-Host "Selected: $($projectsResponse.projects[$choiceNum - 1].name)" -ForegroundColor $green
                }
            }
        }
    } catch {
        # Server might not be running, continue without project list
    }
}

# If no question provided, prompt for it
if ([string]::IsNullOrWhiteSpace($Question)) {
    Write-Host "`n=== RAG Query Helper ===" -ForegroundColor $cyan
    Write-Host "`nExamples:" -ForegroundColor $yellow
    Write-Host "  - Compare Python and C# database connections" -ForegroundColor $white
    Write-Host "  - Show me error handling implementations" -ForegroundColor $white
    Write-Host "  - How is dependency injection used?" -ForegroundColor $white
    Write-Host ""
    
    $Question = Read-Host "Your question"
    
    if ([string]::IsNullOrWhiteSpace($Question)) {
        Write-Host "No question provided. Exiting." -ForegroundColor $red
        exit 1
    }
}

Write-Host "`n=== Querying RAG Server ===" -ForegroundColor $cyan
Write-Host "Question: $Question" -ForegroundColor $white
if (![string]::IsNullOrWhiteSpace($ProjectPath)) {
    Write-Host "Project: $ProjectPath" -ForegroundColor $yellow
} else {
    Write-Host "Project: [Current/Default]" -ForegroundColor $yellow
}
Write-Host ""

# Build request body
$body = @{
    query = $Question
    max_results = $MaxResults
    include_metadata = $true
}

if (![string]::IsNullOrWhiteSpace($ProjectPath)) {
    $body.project_path = $ProjectPath
}

$body = $body | ConvertTo-Json

try {
    # Query the RAG server
    $response = Invoke-RestMethod -Method Post `
        -Uri "$RAG_URL/query" `
        -Body $body `
        -ContentType "application/json" `
        -TimeoutSec 30
    
    Write-Host "✅ Query Successful!" -ForegroundColor $green
    Write-Host ""
    Write-Host "Results:" -ForegroundColor $yellow
    Write-Host "  - Context chunks: $($response.context_chunks)" -ForegroundColor $white
    Write-Host "  - Token count: $($response.token_count)" -ForegroundColor $white
    
    if ($response.metadata) {
        Write-Host "  - Project: $($response.metadata.queried_project)" -ForegroundColor $cyan
        Write-Host "  - Indexed files: $($response.metadata.indexed_files)" -ForegroundColor $white
        Write-Host "  - Total chunks: $($response.metadata.total_chunks)" -ForegroundColor $white
        
        if ($response.metadata.available_projects -and $response.metadata.available_projects.Count -gt 1) {
            Write-Host "  - Available projects: $($response.metadata.available_projects.Count)" -ForegroundColor $white
        }
    }
    
    # Copy to clipboard
    $response.optimized_prompt | Set-Clipboard
    
    Write-Host "`n✅ PROMPT COPIED TO CLIPBOARD!" -ForegroundColor $green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor $yellow
    Write-Host "  1. Open GitHub Copilot Chat (Ctrl+Shift+I)" -ForegroundColor $white
    Write-Host "  2. Paste (Ctrl+V)" -ForegroundColor $white
    Write-Host "  3. Add your follow-up instruction" -ForegroundColor $white
    Write-Host ""
    
    # Show preview
    Write-Host "Preview (first 800 chars):" -ForegroundColor $yellow
    Write-Host "----------------------------------------" -ForegroundColor $cyan
    $preview = $response.optimized_prompt.Substring(0, [Math]::Min(800, $response.optimized_prompt.Length))
    Write-Host $preview -ForegroundColor $white
    Write-Host "..." -ForegroundColor $cyan
    Write-Host "----------------------------------------" -ForegroundColor $cyan
    Write-Host ""
    
    # Return the response for further processing if needed
    return $response
    
} catch {
    Write-Host "❌ Error querying RAG server!" -ForegroundColor $red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor $red
    Write-Host ""
    Write-Host "Is the RAG server running?" -ForegroundColor $yellow
    Write-Host "Check with: docker ps" -ForegroundColor $white
    Write-Host ""
    exit 1
}
