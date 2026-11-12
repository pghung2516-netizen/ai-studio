$TenApp = 'TTomorrow Studio'
# Tao loi tat cho Desktop va Start Menu. Console chi dung ky tu ASCII.

$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
$TenBoFile = "$TenApp - Bỏ file vào đây"
$TenThanhPham = "$TenApp - Thành phẩm"

$launcherPath = Join-Path $PSScriptRoot 'mo-ai-studio.ps1'
$dauVaoPath = Join-Path $Root '01-DAU-VAO'
$thanhPhamPath = Join-Path $Root '02-THANH-PHAM'
$iconApp = Join-Path $Root 'assets\icon\ai-studio.ico'
$iconDauVao = Join-Path $Root 'assets\icon\dau-vao.ico'
$iconThanhPham = Join-Path $Root 'assets\icon\thanh-pham.ico'

function Tao-LoiTatMoApp($Wsh, $NoiDat) {
    if (-not $Wsh) { return $false }
    try {
        $lnkPath = Join-Path $NoiDat "$TenApp.lnk"
        $shortcut = $Wsh.CreateShortcut($lnkPath)
        $shortcut.TargetPath = 'powershell.exe'
        $shortcut.Arguments = "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$launcherPath`""
        $shortcut.WorkingDirectory = $Root
        if (Test-Path -LiteralPath $iconApp -PathType Leaf) {
            $shortcut.IconLocation = "$iconApp,0"
        }
        $shortcut.WindowStyle = 7
        $shortcut.Save()
        return $true
    } catch {
        return $false
    }
}

function Tao-LoiTatThuMuc($Wsh, $NoiDat, $TenLoiTat, $ThuMucDich, $IconPath) {
    $lnkPath = Join-Path $NoiDat "$TenLoiTat.lnk"
    $urlPath = Join-Path $NoiDat "$TenLoiTat.url"

    if ($Wsh) {
        try {
            $shortcut = $Wsh.CreateShortcut($lnkPath)
            $shortcut.TargetPath = $ThuMucDich
            if (Test-Path -LiteralPath $IconPath -PathType Leaf) {
                $shortcut.IconLocation = "$IconPath,0"
            }
            $shortcut.WindowStyle = 1
            $shortcut.Save()
            if (Test-Path -LiteralPath $urlPath -PathType Leaf) {
                Remove-Item -LiteralPath $urlPath -Force
            }
            return $true
        } catch { }
    }

    try {
        if (Test-Path -LiteralPath $lnkPath -PathType Leaf) {
            Remove-Item -LiteralPath $lnkPath -Force
        }
        $fileUrl = $ThuMucDich -replace '\\', '/'
        $fileUrl = $fileUrl -replace ' ', '%20'
        $urlLines = @('[InternetShortcut]', "URL=file:///$fileUrl")
        if (Test-Path -LiteralPath $IconPath -PathType Leaf) {
            $urlLines += "IconFile=$IconPath"
            $urlLines += 'IconIndex=0'
        }
        Set-Content -LiteralPath $urlPath -Value $urlLines -Encoding UTF8
        return $true
    } catch {
        return $false
    }
}

try {
    $desktopPath = $null
    try {
        $desktopPath = (Get-ItemProperty -LiteralPath 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders' -Name 'Desktop' -ErrorAction Stop).Desktop
        if ($desktopPath) {
            $desktopPath = $desktopPath.Replace('%USERPROFILE%', $env:USERPROFILE)
        }
    } catch {
        $desktopPath = $null
    }
    if (-not $desktopPath) {
        $desktopPath = Join-Path $env:USERPROFILE 'Desktop'
    }

    try {
        if (-not (Test-Path -LiteralPath $desktopPath -PathType Container)) {
            New-Item -ItemType Directory -Path $desktopPath -Force | Out-Null
        }
    } catch {
        $desktopPath = Join-Path $env:USERPROFILE 'Desktop'
        if (-not (Test-Path -LiteralPath $desktopPath -PathType Container)) {
            New-Item -ItemType Directory -Path $desktopPath -Force | Out-Null
        }
    }

    $startMenuBase = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs'
    $startMenuPath = Join-Path $startMenuBase $TenApp
    if (-not (Test-Path -LiteralPath $startMenuPath -PathType Container)) {
        New-Item -ItemType Directory -Path $startMenuPath -Force | Out-Null
    }

    $languageMode = $ExecutionContext.SessionState.LanguageMode
    $wsh = $null
    try {
        if ($languageMode -ne 'FullLanguage') {
            throw 'COM is not available in this language mode.'
        }
        $wsh = New-Object -ComObject WScript.Shell -ErrorAction Stop
    } catch {
        $wsh = $null
    }

    $launcherFallback = $false
    $folderFailure = $false
    foreach ($noiDat in @($desktopPath, $startMenuPath)) {
        if (-not (Tao-LoiTatMoApp $wsh $noiDat)) {
            $launcherFallback = $true
        }
        if (-not (Tao-LoiTatThuMuc $wsh $noiDat $TenBoFile $dauVaoPath $iconDauVao)) {
            $folderFailure = $true
        }
        if (-not (Tao-LoiTatThuMuc $wsh $noiDat $TenThanhPham $thanhPhamPath $iconThanhPham)) {
            $folderFailure = $true
        }
    }

    if ($launcherFallback) {
        Write-Host "Khong tao duoc loi tat mo $TenApp trong che do bao mat nay." -ForegroundColor Yellow
        Write-Host "Hay dung MO-TTOMORROW-STUDIO.bat trong thu muc workspace." -ForegroundColor Yellow
    }
    if ($folderFailure) {
        Write-Host "Khong tao duoc mot so loi tat thu muc." -ForegroundColor Yellow
    } else {
        Write-Host "Da tao loi tat tren Desktop va Start Menu." -ForegroundColor Green
    }
} catch {
    Write-Host "Khong tao duoc loi tat. Hay dung MO-TTOMORROW-STUDIO.bat trong thu muc workspace." -ForegroundColor Yellow
}
