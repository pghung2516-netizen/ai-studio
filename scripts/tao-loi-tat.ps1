$TenApp = 'TTomorrow Studio'
# Tao loi tat cho Desktop va Start Menu. Console chi dung ky tu ASCII.

$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
$TenBoFile = "$TenApp - Hộp thư đến"
$TenBoFileCu = "$TenApp - Bỏ file vào đây"   # ten cu, se bi xoa
$TenThanhPham = "$TenApp - Dự án của tôi"
$TenThanhPhamCu = "$TenApp - Thành phẩm"   # ten loi tat cua ban truoc, se bi xoa

$launcherPath = Join-Path $PSScriptRoot 'mo-ai-studio.ps1'
$dauVaoPath = Join-Path $Root '01-DAU-VAO'
$thanhPhamPath = Join-Path $Root '02-DU-AN'
if (-not (Test-Path -LiteralPath $thanhPhamPath -PathType Container)) { New-Item -ItemType Directory -Path $thanhPhamPath -Force | Out-Null }
$iconApp = Join-Path $Root 'assets\icon\ai-studio.ico'
$iconDauVao = Join-Path $Root 'assets\icon\dau-vao.ico'
$iconThanhPham = Join-Path $Root 'assets\icon\thanh-pham.ico'

function Kiem-TraAscii($Text) {
    if ($null -eq $Text) { return $false }
    for ($i = 0; $i -lt $Text.Length; $i++) {
        if ([int][char]$Text[$i] -gt 127) { return $false }
    }
    return $true
}

function Ma-HoaFileUrl($Path) {
    # Tu ma hoa UTF-8 de chay duoc ca trong ConstrainedLanguage.
    $text = $Path -replace '\\', '/'
    $hex = '0123456789ABCDEF'
    $result = ''
    for ($i = 0; $i -lt $text.Length; $i++) {
        $code = [int][char]$text[$i]
        if ($code -eq 32) {
            $result += '%20'
            continue
        }
        if ($code -le 127) {
            $result += [char]$code
            continue
        }
        if ($code -ge 55296 -and $code -le 56319 -and ($i + 1) -lt $text.Length) {
            $low = [int][char]$text[$i + 1]
            if ($low -ge 56320 -and $low -le 57343) {
                $code = 65536 + (($code - 55296) * 1024) + ($low - 56320)
                $i++
            } else {
                $code = 65533
            }
        } elseif ($code -ge 55296 -and $code -le 57343) {
            $code = 65533
        }
        if ($code -le 2047) {
            $bytes = @()
            $bytes += (192 -bor ($code -shr 6))
            $bytes += (128 -bor ($code -band 63))
        } elseif ($code -le 65535) {
            $bytes = @()
            $bytes += (224 -bor ($code -shr 12))
            $bytes += (128 -bor (($code -shr 6) -band 63))
            $bytes += (128 -bor ($code -band 63))
        } else {
            $bytes = @()
            $bytes += (240 -bor ($code -shr 18))
            $bytes += (128 -bor (($code -shr 12) -band 63))
            $bytes += (128 -bor (($code -shr 6) -band 63))
            $bytes += (128 -bor ($code -band 63))
        }
        foreach ($byte in $bytes) {
            $result += '%' + $hex[($byte -shr 4) -band 15] + $hex[$byte -band 15]
        }
    }
    return $result
}

function Xoa-LoiTatCu($NoiDat) {
    foreach ($name in @("$TenApp.lnk", "$TenBoFile.url", "$TenBoFile.lnk", "$TenBoFileCu.url", "$TenBoFileCu.lnk", "$TenThanhPham.url", "$TenThanhPham.lnk", "$TenThanhPhamCu.url", "$TenThanhPhamCu.lnk")) {
        $path = Join-Path $NoiDat $name
        if (Test-Path -LiteralPath $path) {
            Remove-Item -LiteralPath $path -Force
        }
    }
    Get-ChildItem -LiteralPath $NoiDat -Filter 'ttomorrow-tmp-*.lnk' -File -ErrorAction SilentlyContinue |
        Remove-Item -Force -ErrorAction SilentlyContinue
}

function Tao-LoiTatUnicode($Wsh, $ShellApp, $NoiDat, $TempName, $FinalName, $TargetPath, $Arguments, $WorkingDirectory, $ShowCommand, $IconPath, $KiemTraRoot) {
    if (-not $Wsh -or -not $ShellApp) { return 0 }
    $tmpPath = Join-Path $NoiDat $TempName
    $finalPath = Join-Path $NoiDat $FinalName
    try {
        if (-not (Test-Path -LiteralPath $TargetPath) -or
            -not (Test-Path -LiteralPath $WorkingDirectory -PathType Container) -or
            -not (Test-Path -LiteralPath $IconPath -PathType Leaf)) {
            return 0
        }

        if (Test-Path -LiteralPath $tmpPath) { Remove-Item -LiteralPath $tmpPath -Force }
        $placeholder = $Wsh.CreateShortcut($tmpPath)
        $placeholder.TargetPath = 'C:\Windows\explorer.exe'
        $placeholder.Arguments = ''
        $placeholder.WorkingDirectory = 'C:\Windows'
        $placeholder.WindowStyle = 1
        $placeholder.Save()

        $folder = $ShellApp.Namespace($NoiDat)
        if (-not $folder) { throw 'Shell namespace is not available.' }
        $item = $folder.ParseName($TempName)
        if (-not $item) { throw 'Temporary shortcut is not available.' }
        $link = $item.GetLink
        if (-not $link) { throw 'Shell link is not available.' }
        $link.Path = $TargetPath
        $link.Arguments = $Arguments
        $link.WorkingDirectory = $WorkingDirectory
        $link.ShowCommand = $ShowCommand
        $link.SetIconLocation($IconPath, 0)
        $link.Save()

        if (Test-Path -LiteralPath $finalPath) { Remove-Item -LiteralPath $finalPath -Force }
        Move-Item -LiteralPath $tmpPath -Destination $finalPath -Force

        $verifyFolder = $ShellApp.Namespace($NoiDat)
        $verifyItem = $verifyFolder.ParseName($FinalName)
        if (-not $verifyItem) { throw 'Saved shortcut is not available.' }
        $verifyLink = $verifyItem.GetLink
        if (-not $verifyLink) { throw 'Saved Shell link is not available.' }
        # Icon chi la phu: doc icon qua COM [ref] co the khong chay, khong duoc xoa loi tat chi vi icon.
        $verifyIconPath = ''
        try { $null = $verifyLink.GetIconLocation([ref]$verifyIconPath) } catch { $verifyIconPath = '' }
        if ($verifyIconPath -and -not (Test-Path -LiteralPath $verifyIconPath -PathType Leaf)) {
            Write-Host "Canh bao: icon cua loi tat co the khong hien dung." -ForegroundColor Yellow
        }
        $verified = ((Test-Path -LiteralPath $verifyLink.Path) -and
            (Test-Path -LiteralPath $verifyLink.WorkingDirectory -PathType Container))
        if ($KiemTraRoot -and -not $verifyLink.Arguments.Contains($Root)) {
            $verified = $false
        }
        if (-not $verified) {
            Remove-Item -LiteralPath $finalPath -Force -ErrorAction SilentlyContinue
            return 0
        }
        return 2
    } catch {
        Remove-Item -LiteralPath $tmpPath -Force -ErrorAction SilentlyContinue
        Remove-Item -LiteralPath $finalPath -Force -ErrorAction SilentlyContinue
        return 0
    }
}

function Tao-LoiTatMoApp($Wsh, $ShellApp, $NoiDat) {
    $powershellPath = Join-Path $PSHOME 'powershell.exe'
    $arguments = "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$launcherPath`""
    return Tao-LoiTatUnicode $Wsh $ShellApp $NoiDat 'ttomorrow-tmp-1.lnk' "$TenApp.lnk" $powershellPath $arguments $Root 7 $iconApp $true
}

function Tao-LoiTatThuMuc($Wsh, $ShellApp, $NoiDat, $TempName, $TenLoiTat, $ThuMucDich, $IconPath) {
    $lnkPath = Join-Path $NoiDat "$TenLoiTat.lnk"
    $urlPath = Join-Path $NoiDat "$TenLoiTat.url"
    $status = Tao-LoiTatUnicode $Wsh $ShellApp $NoiDat $TempName "$TenLoiTat.lnk" $ThuMucDich '' $ThuMucDich 1 $IconPath $false
    if ($status -eq 2) {
        if (Test-Path -LiteralPath $urlPath) { Remove-Item -LiteralPath $urlPath -Force }
        return 2
    }

    try {
        if (Test-Path -LiteralPath $lnkPath) { Remove-Item -LiteralPath $lnkPath -Force }
        $fileUrl = Ma-HoaFileUrl $ThuMucDich
        $urlLines = @('[InternetShortcut]', "URL=file:///$fileUrl")
        if ((Kiem-TraAscii $IconPath) -and (Test-Path -LiteralPath $IconPath -PathType Leaf)) {
            $urlLines += "IconFile=$IconPath"
            $urlLines += 'IconIndex=0'
        }
        Set-Content -LiteralPath $urlPath -Value $urlLines -Encoding ASCII
        return 1
    } catch {
        Remove-Item -LiteralPath $urlPath -Force -ErrorAction SilentlyContinue
        return 0
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

    foreach ($noiDat in @($desktopPath, $startMenuPath)) {
        Xoa-LoiTatCu $noiDat
    }

    $languageMode = $ExecutionContext.SessionState.LanguageMode
    $wsh = $null
    $shellApp = $null
    if ($languageMode -eq 'FullLanguage') {
        try {
            $wsh = New-Object -ComObject WScript.Shell -ErrorAction Stop
            $shellApp = New-Object -ComObject Shell.Application -ErrorAction Stop
        } catch {
            $wsh = $null
            $shellApp = $null
        }
    }

    $launcherFallback = $false
    $folderFailure = $false
    $folderFallback = $false
    $allVerified = $true
    $failedCount = 0
    foreach ($noiDat in @($desktopPath, $startMenuPath)) {
        $launcherStatus = Tao-LoiTatMoApp $wsh $shellApp $noiDat
        if ($launcherStatus -ne 2) {
            $allVerified = $false
            $launcherFallback = $true
        }
        if ($launcherStatus -eq 0) { $failedCount++ }
        $inputStatus = Tao-LoiTatThuMuc $wsh $shellApp $noiDat 'ttomorrow-tmp-2.lnk' $TenBoFile $dauVaoPath $iconDauVao
        if ($inputStatus -ne 2) { $allVerified = $false }
        if ($inputStatus -eq 1) { $folderFallback = $true }
        if ($inputStatus -eq 0) {
            $failedCount++
            $folderFailure = $true
        }
        $outputStatus = Tao-LoiTatThuMuc $wsh $shellApp $noiDat 'ttomorrow-tmp-3.lnk' $TenThanhPham $thanhPhamPath $iconThanhPham
        if ($outputStatus -ne 2) { $allVerified = $false }
        if ($outputStatus -eq 1) { $folderFallback = $true }
        if ($outputStatus -eq 0) {
            $failedCount++
            $folderFailure = $true
        }
    }

    if ($allVerified -and $failedCount -eq 0) {
        Write-Host "Da tao loi tat tren Desktop va Start Menu." -ForegroundColor Green
    } else {
        if ($launcherFallback) {
            Write-Host "Khong tao hoac xac minh duoc loi tat mo $TenApp." -ForegroundColor Yellow
            Write-Host "Hay dung MO-TTOMORROW-STUDIO.bat trong thu muc workspace." -ForegroundColor Yellow
        }
        if ($folderFailure) {
            Write-Host "Khong tao duoc mot so loi tat thu muc. Hay mo thu muc dau vao/thanh pham thu cong." -ForegroundColor Yellow
        } elseif ($folderFallback) {
            Write-Host "Da tao loi tat thu muc dang .url; neu khong mo duoc, hay mo thu muc thu cong." -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host "Khong tao duoc loi tat. Hay dung MO-TTOMORROW-STUDIO.bat trong thu muc workspace." -ForegroundColor Yellow
}
