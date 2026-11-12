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

function Mo-Ide($Candidates, $CanClaude, $LyDo, $RootPath) {
    foreach ($candidate in $Candidates) {
        if ($candidate.HasClaude -ne $CanClaude) {
            continue
        }

        try {
            $folderArgument = '"' + $RootPath + '"'
            if ($candidate.IsShim) {
                Start-Process -FilePath $candidate.Path -ArgumentList $folderArgument -WindowStyle Hidden
            } else {
                Start-Process -FilePath $candidate.Path -ArgumentList $folderArgument
            }
            Ghi-Log "CHOSEN app=$($candidate.Name) path=$($candidate.Path) reason=$LyDo"
            return $true
        } catch {
            Ghi-Log "ERROR launch $($candidate.Name): $($_.Exception.Message)"
        }
    }

    return $false
}

function Mo-ClaudeDesktop($LyDo, $RootPath) {
    Ghi-Log 'STEP find registered Claude app'
    try {
        $claudeApp = Get-StartApps -ErrorAction Stop |
            Where-Object { $_.Name -eq 'Claude' } |
            Select-Object -First 1
        if ($claudeApp -and $claudeApp.AppID) {
            $appTarget = "shell:AppsFolder\$($claudeApp.AppID)"
            Start-Process -FilePath 'explorer.exe' -ArgumentList $appTarget
            Ghi-Log "CHOSEN app=Claude Desktop source=registered reason=$LyDo"
            return $true
        }
    } catch {
        Ghi-Log "ERROR registered Claude app: $($_.Exception.Message)"
    }

    Ghi-Log 'STEP find local Claude app'
    try {
        $claudeLocal = Join-Path $env:LOCALAPPDATA 'AnthropicClaude\claude.exe'
        if (Test-Path -LiteralPath $claudeLocal -PathType Leaf) {
            Start-Process -FilePath $claudeLocal -WorkingDirectory $RootPath
            Ghi-Log "CHOSEN app=Claude Desktop source=local reason=$LyDo"
            return $true
        }
    } catch {
        Ghi-Log "ERROR local Claude app: $($_.Exception.Message)"
    }

    Ghi-Log 'STEP scan Programs for Claude app'
    try {
        $programsPath = Join-Path $env:LOCALAPPDATA 'Programs'
        $claudePattern = Join-Path $programsPath '*\claude.exe'
        $claudeExe = Get-ChildItem -Path $claudePattern -File -ErrorAction SilentlyContinue |
            Select-Object -First 1
        if ($claudeExe) {
            Start-Process -FilePath $claudeExe.FullName -WorkingDirectory $RootPath
            Ghi-Log "CHOSEN app=Claude Desktop source=Programs-scan reason=$LyDo"
            return $true
        }
    } catch {
        Ghi-Log "ERROR scan Programs: $($_.Exception.Message)"
    }

    return $false
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

    Ghi-Log 'STEP read launch preference'
    $preferencePath = Join-Path $cachePath 'mo-bang.txt'
    $preference = 'tu-dong'
    try {
        if (Test-Path -LiteralPath $preferencePath -PathType Leaf) {
            $savedPreference = Get-Content -LiteralPath $preferencePath -ErrorAction Stop |
                Select-Object -First 1
            if ($savedPreference -in @('ide', 'claude-desktop', 'tu-dong')) {
                $preference = $savedPreference
            } else {
                Ghi-Log 'INFO invalid launch preference; using tu-dong'
            }
        }
    } catch {
        Ghi-Log "ERROR launch preference: $($_.Exception.Message)"
        $preference = 'tu-dong'
    }
    Ghi-Log "INFO launch preference=$preference"

    Ghi-Log 'STEP find IDE candidates'
    $antigravityExtensions = "$env:USERPROFILE\.antigravity\extensions"
    $codeExtensions = "$env:USERPROFILE\.vscode\extensions"
    $cursorExtensions = "$env:USERPROFILE\.cursor\extensions"
    $possibleIde = @(
        @{ Name = 'Antigravity'; Path = "$env:LOCALAPPDATA\Programs\Antigravity\Antigravity.exe"; Extensions = $antigravityExtensions },
        @{ Name = 'Antigravity'; Path = "$env:ProgramFiles\Antigravity\Antigravity.exe"; Extensions = $antigravityExtensions },
        @{ Name = 'VS Code'; Path = "$env:LOCALAPPDATA\Programs\Microsoft VS Code\Code.exe"; Extensions = $codeExtensions },
        @{ Name = 'VS Code'; Path = "$env:ProgramFiles\Microsoft VS Code\Code.exe"; Extensions = $codeExtensions },
        @{ Name = 'Cursor'; Path = "$env:LOCALAPPDATA\Programs\cursor\Cursor.exe"; Extensions = $cursorExtensions }
    )
    $ideCandidates = @()
    foreach ($possible in $possibleIde) {
        if (Test-Path -LiteralPath $possible.Path -PathType Leaf) {
            $hasClaude = $false
            if (Test-Path -LiteralPath $possible.Extensions -PathType Container) {
                $claudeExtension = Get-ChildItem -LiteralPath $possible.Extensions -Directory -Filter 'anthropic.claude-code*' -ErrorAction SilentlyContinue |
                    Select-Object -First 1
                $hasClaude = $null -ne $claudeExtension
            }
            $ideCandidates += @{
                Name = $possible.Name
                Path = $possible.Path
                HasClaude = $hasClaude
                IsShim = $false
            }
        }
    }

    try {
        $ideShims = Get-Command antigravity, code, cursor -ErrorAction SilentlyContinue |
            Where-Object { $_.CommandType -eq 'Application' -and $_.Name -like '*.cmd' }
        foreach ($shim in $ideShims) {
            $shimName = $null
            $shimExtensions = $null
            if ($shim.Name -like 'antigravity*') {
                $shimName = 'Antigravity'
                $shimExtensions = $antigravityExtensions
            } elseif ($shim.Name -like 'code*') {
                $shimName = 'VS Code'
                $shimExtensions = $codeExtensions
            } elseif ($shim.Name -like 'cursor*') {
                $shimName = 'Cursor'
                $shimExtensions = $cursorExtensions
            }

            if ($shimName) {
                $hasClaude = $false
                if (Test-Path -LiteralPath $shimExtensions -PathType Container) {
                    $claudeExtension = Get-ChildItem -LiteralPath $shimExtensions -Directory -Filter 'anthropic.claude-code*' -ErrorAction SilentlyContinue |
                        Select-Object -First 1
                    $hasClaude = $null -ne $claudeExtension
                }
                $ideCandidates += @{
                    Name = $shimName
                    Path = $shim.Source
                    HasClaude = $hasClaude
                    IsShim = $true
                }
            }
        }
    } catch {
        Ghi-Log "ERROR find IDE shims: $($_.Exception.Message)"
    }

    $daMoApp = $false
    if ($preference -eq 'claude-desktop') {
        $daMoApp = Mo-ClaudeDesktop 'preference=claude-desktop' $Root
        if (-not $daMoApp) {
            $daMoApp = Mo-Ide $ideCandidates $true 'Claude Desktop unavailable; Claude Code extension installed' $Root
        }
        if (-not $daMoApp) {
            $daMoApp = Mo-Ide $ideCandidates $false 'Claude Desktop unavailable; IDE fallback' $Root
        }
    } elseif ($preference -eq 'ide') {
        $daMoApp = Mo-Ide $ideCandidates $true 'preference=ide; Claude Code extension installed' $Root
        if (-not $daMoApp) {
            $daMoApp = Mo-Ide $ideCandidates $false 'preference=ide; IDE without Claude Code extension' $Root
        }
        if (-not $daMoApp) {
            $daMoApp = Mo-ClaudeDesktop 'no IDE available for preference=ide' $Root
        }
    } else {
        $daMoApp = Mo-Ide $ideCandidates $true 'preference=tu-dong; Claude Code extension installed' $Root
        if (-not $daMoApp) {
            $daMoApp = Mo-ClaudeDesktop 'no IDE with Claude Code extension' $Root
        }
        if (-not $daMoApp) {
            $daMoApp = Mo-Ide $ideCandidates $false 'Claude Desktop unavailable; IDE fallback' $Root
        }
    }

    if (-not $daMoApp) {
        Ghi-Log 'CHOSEN app=fallback reason=no supported app could be opened'
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
