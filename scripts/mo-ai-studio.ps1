# TTomorrow Studio - launcher for Windows.
# Console messages use ASCII so they remain readable on older systems.

$TenApp = 'TTomorrow Studio'
$ErrorActionPreference = 'Stop'
$Root = $null
$GuidePath = $null
$LogPath = "$env:TEMP\ttomorrow-studio.log"

function Ghi-Log($Message) {
    try {
        $stamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
        Add-Content -LiteralPath $LogPath -Value "[$stamp] $Message" -Encoding ASCII -ErrorAction Stop
    } catch { }
}

try {
    Ghi-Log 'START launcher'
    Ghi-Log 'STEP setup workspace'
    $Root = Split-Path -Parent $PSScriptRoot
    Set-Location -LiteralPath $Root
    $GuidePath = Join-Path $Root 'HUONG-DAN-NHANH.html'

    Ghi-Log 'STEP check environment'
    $venvPath = Join-Path $Root '.venv'
    if (-not (Test-Path -LiteralPath $venvPath -PathType Container)) {
        Ghi-Log 'STEP start installer'
        $installerPath = Join-Path $Root 'CAI-DAT.bat'
        Start-Process -FilePath $installerPath -WorkingDirectory $Root
        Ghi-Log 'END installer started'
        exit 0
    }

    Ghi-Log 'STEP copy workspace path'
    try {
        Set-Clipboard -Value $Root -ErrorAction Stop
    } catch {
        Ghi-Log "ERROR clipboard: $($_.Exception.Message)"
        Write-Host "Khong sao chep duoc duong dan workspace vao clipboard." -ForegroundColor Yellow
    }

    Ghi-Log 'STEP quick guide'
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
            Ghi-Log "ERROR quick guide: $($_.Exception.Message)"
            Write-Host "Khong luu duoc trang thai huong dan lan dau." -ForegroundColor Yellow
        }
    }

    $daMoClaude = $false

    Ghi-Log 'STEP find registered Claude app'
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
        Ghi-Log "ERROR registered Claude app: $($_.Exception.Message)"
        $daMoClaude = $false
    }

    if (-not $daMoClaude) {
        Ghi-Log 'STEP find local Claude app'
        $claudeLocal = Join-Path $env:LOCALAPPDATA 'AnthropicClaude\claude.exe'
        if (Test-Path -LiteralPath $claudeLocal -PathType Leaf) {
            try {
                Start-Process -FilePath $claudeLocal -WorkingDirectory $Root
                $daMoClaude = $true
            } catch {
                Ghi-Log "ERROR local Claude app: $($_.Exception.Message)"
                $daMoClaude = $false
            }
        }
    }

    if (-not $daMoClaude) {
        Ghi-Log 'STEP scan Programs for Claude app'
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
            Ghi-Log "ERROR scan Programs: $($_.Exception.Message)"
            $daMoClaude = $false
        }
    }

    if (-not $daMoClaude) {
        Ghi-Log 'STEP open Claude download fallback'
        try {
            Start-Process -FilePath 'https://claude.com/download'
        } catch {
            Ghi-Log "ERROR Claude download fallback: $($_.Exception.Message)"
        }
        try {
            if (Test-Path -LiteralPath $GuidePath -PathType Leaf) {
                Start-Process -FilePath $GuidePath
            }
        } catch {
            Ghi-Log "ERROR guide fallback: $($_.Exception.Message)"
        }
    }
    Ghi-Log 'END launcher'
} catch {
    Ghi-Log "ERROR launcher: $($_.Exception.Message)"
    Write-Host "$TenApp khong mo duoc. Dang mo trang huong dan." -ForegroundColor Yellow
    try {
        if (-not $GuidePath -and $PSScriptRoot) {
            $fallbackRoot = Split-Path -Parent $PSScriptRoot
            $GuidePath = Join-Path $fallbackRoot 'HUONG-DAN-NHANH.html'
        }
        if ($GuidePath -and (Test-Path -LiteralPath $GuidePath -PathType Leaf)) {
            Start-Process -FilePath $GuidePath
        }
    } catch {
        Ghi-Log "ERROR final guide fallback: $($_.Exception.Message)"
    }
}
