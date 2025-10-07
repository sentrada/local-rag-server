param(
    [switch]$DryRun
)

Write-Host "Cleaning build artifacts, caches, and logs..." -ForegroundColor Cyan

$targets = @(
    @{ Path = "src\__pycache__"; Type = "Dir" },
    @{ Path = "**\__pycache__"; Type = "GlobDir" },
    @{ Path = "*.pyc"; Type = "GlobFile" },
    @{ Path = "*.pyo"; Type = "GlobFile" },
    @{ Path = "*.pyd"; Type = "GlobFile" },
    @{ Path = "logs\*.log"; Type = "GlobFile" }
)

foreach ($t in $targets) {
    switch ($t.Type) {
        "Dir" {
            if (Test-Path $t.Path) {
                if ($DryRun) { Write-Host "Would remove directory: $($t.Path)" -ForegroundColor Yellow }
                else { Remove-Item -Recurse -Force $t.Path -ErrorAction SilentlyContinue }
            }
        }
        "GlobDir" {
            Get-ChildItem -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue |
                ForEach-Object {
                    if ($DryRun) { Write-Host "Would remove directory: $($_.FullName)" -ForegroundColor Yellow }
                    else { Remove-Item -Recurse -Force $_.FullName -ErrorAction SilentlyContinue }
                }
        }
        "GlobFile" {
            Get-ChildItem -Recurse -File -Include $t.Path -ErrorAction SilentlyContinue |
                ForEach-Object {
                    if ($DryRun) { Write-Host "Would remove file: $($_.FullName)" -ForegroundColor Yellow }
                    else { Remove-Item -Force $_.FullName -ErrorAction SilentlyContinue }
                }
        }
    }
}

Write-Host "Cleanup complete." -ForegroundColor Green
