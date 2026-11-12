# TTomorrow Studio - launcher for Windows.
# Console messages use ASCII so they remain readable on older systems.

$TenApp = 'TTomorrow Studio'
$ErrorActionPreference = 'Stop'
$Root = $null
$GuidePath = $null

try {
    $Root = Split-Path -Parent $PSScriptRoot
    Set-Location -LiteralPath $Root
    $GuidePath = Join-Path $Root 'HUONG-DAN-NHANH.html'

    $venvPath = Join-Path $Root '.venv'
    if (-not (Test-Path -LiteralPath $venvPath -PathType Container)) {
        $installerPath = Join-Path $Root 'CAI-DAT.bat'
        Start-Process -FilePath $installerPath -WorkingDirectory $Root
        exit 0
    }

    try {
        Set-Clipboard -Value $Root -ErrorAction Stop
    } catch {
        Write-Host "Khong sao chep duoc duong dan workspace vao clipboard." -ForegroundColor Yellow
    }

    $cachePath = Join-Path $Root '.cache'
    $markerPath = Join-Path $cachePath 'da-xem-huong-dan.txt'
    if (-not (Test-Path -LiteralPath $markerPath -PathType Leaf)) {
        try {
            if (Test-Path -LiteralPath $GuidePath -PathType Leaf) {
                Start-Process -FilePath $GuidePath
            }
            if (-not (Test-Path -LiteralPath $cachePath -PathType Container)) {
                New-Item -ItemType Directory -Path $cachePath -Force | Out-Null
            }
            Set-Content -LiteralPath $markerPath -Value 'Da mo huong dan nhanh.' -Encoding ASCII
        } catch {
            Write-Host "Khong luu duoc trang thai huong dan lan dau." -ForegroundColor Yellow
        }
    }

    $daMoClaude = $false

    try {
        $claudeApp = Get-StartApps -ErrorAction Stop |
            Where-Object { $_.Name -eq 'Claude' } |
            Select-Object -First 1
        if ($claudeApp -and $claudeApp.AppID) {
            $appTarget = "shell:AppsFolder\$($claudeApp.AppID)"
            Start-Process -FilePath 'explorer.exe' -ArgumentList $appTarget
            $daMoClaude = $true
        }
    } catch {
        $daMoClaude = $false
    }

    if (-not $daMoClaude) {
        $claudeLocal = Join-Path $env:LOCALAPPDATA 'AnthropicClaude\claude.exe'
        if (Test-Path -LiteralPath $claudeLocal -PathType Leaf) {
            try {
                Start-Process -FilePath $claudeLocal -WorkingDirectory $Root
                $daMoClaude = $true
            } catch {
                $daMoClaude = $false
            }
        }
    }

    if (-not $daMoClaude) {
        try {
            $programsPath = Join-Path $env:LOCALAPPDATA 'Programs'
            $claudePattern = Join-Path $programsPath '*\claude.exe'
            $claudeExe = Get-ChildItem -Path $claudePattern -File -ErrorAction SilentlyContinue |
                Select-Object -First 1
            if ($claudeExe) {
                Start-Process -FilePath $claudeExe.FullName -WorkingDirectory $Root
                $daMoClaude = $true
            }
        } catch {
            $daMoClaude = $false
        }
    }

    if (-not $daMoClaude) {
        try {
            Start-Process -FilePath 'https://claude.com/download'
        } catch { }
        try {
            if (Test-Path -LiteralPath $GuidePath -PathType Leaf) {
                Start-Process -FilePath $GuidePath
            }
        } catch { }
    }
} catch {
    Write-Host "$TenApp khong mo duoc. Dang mo trang huong dan." -ForegroundColor Yellow
    try {
        if (-not $GuidePath -and $PSScriptRoot) {
            $fallbackRoot = Split-Path -Parent $PSScriptRoot
            $GuidePath = Join-Path $fallbackRoot 'HUONG-DAN-NHANH.html'
        }
        if ($GuidePath -and (Test-Path -LiteralPath $GuidePath -PathType Leaf)) {
            Start-Process -FilePath $GuidePath
        }
    } catch { }
}
