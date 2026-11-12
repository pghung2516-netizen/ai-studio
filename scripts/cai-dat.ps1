# AI STUDIO - cai dat tu dong cho Windows (khong can quyen Administrator)
# Chay bang cach nhap dup CAI-DAT.bat o thu muc goc.
# Thong bao viet khong dau de khong bi loi font tren cua so dong lenh Windows.

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $Root
$env:PYTHONUTF8 = '1'
$env:UV_LINK_MODE = 'copy'
$env:UV_SYSTEM_CERTS = '1'
$env:UV_NATIVE_TLS = '1'   # ten cu cua UV_SYSTEM_CERTS, cho uv ban cu
$env:UV_PYTHON_DOWNLOADS = 'never'
$env:UV_NO_MANAGED_PYTHON = '1'
$env:NODE_USE_SYSTEM_CA = '1'

function Buoc($so, $msg) { Write-Host ""; Write-Host "[$so/5] $msg" -ForegroundColor Cyan }
function Loi($msg) {
    Write-Host ""
    Write-Host "LOI: $msg" -ForegroundColor Red
    Write-Host "Ban hay chup man hinh nay, hoac mo Claude va noi: 'cai dat bi loi' de Claude sua giup." -ForegroundColor Yellow
    exit 1
}

try {
    [Environment]::SetEnvironmentVariable('UV_SYSTEM_CERTS', '1', 'User')
    [Environment]::SetEnvironmentVariable('UV_PYTHON_DOWNLOADS', 'never', 'User')
    [Environment]::SetEnvironmentVariable('UV_NO_MANAGED_PYTHON', '1', 'User')
    [Environment]::SetEnvironmentVariable('NODE_USE_SYSTEM_CA', '1', 'User')
} catch {
    Loi "Khong luu duoc cau hinh moi truong cho nguoi dung hien tai: $($_.Exception.Message)"
}
Write-Host "Da dung Python co chu ky va kho chung chi Windows cho uv, npm va cac lan chay sau." -ForegroundColor Green

function Kiem-TraPython312($duongDan) {
    if (-not $duongDan -or -not (Test-Path -LiteralPath $duongDan -PathType Leaf)) { return $false }
    try {
        $file = Get-Item -LiteralPath $duongDan
        if ($file.VersionInfo.ProductVersion -notmatch '^3\.12(\.|$)') { return $false }
        $chuKy = Get-AuthenticodeSignature -LiteralPath $duongDan
        if ($chuKy.Status -ne 'Valid') { return $false }
        if (-not $chuKy.SignerCertificate -or $chuKy.SignerCertificate.Subject -notmatch 'Python Software Foundation') { return $false }
        return $true
    } catch {
        return $false
    }
}

function Tim-Python312 {
    $cands = @((Join-Path $env:LOCALAPPDATA 'Programs\Python\Python312\python.exe'))

    $launcher = Get-Command py.exe -ErrorAction SilentlyContinue
    if ($launcher) {
        try {
            $pyPath = & $launcher.Source -3.12 -c "import sys; print(sys.executable)" 2>$null | Select-Object -Last 1
            if ($pyPath) { $cands += $pyPath.Trim() }
        } catch { }
    }

    if ($env:ProgramFiles) {
        $cands += (Join-Path $env:ProgramFiles 'Python312\python.exe')
        $cands += (Join-Path $env:ProgramFiles 'Python 3.12\python.exe')
    }
    foreach ($c in $cands) {
        if (Kiem-TraPython312 $c) { return $c }
    }
    return $null
}

function Cai-PythonBangInstaller {
    $pythonVersion = '3.12.10'
    $installerUrl = "https://www.python.org/ftp/python/$pythonVersion/python-$pythonVersion-amd64.exe"
    $installerPath = Join-Path ([IO.Path]::GetTempPath()) "python-$pythonVersion-amd64.exe"
    Write-Host "   Dang tai Python $pythonVersion chinh thuc tu python.org..."
    try {
        Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath -UseBasicParsing
    } catch {
        Loi "Khong tai duoc Python tu python.org: $($_.Exception.Message)"
    }

    $chuKy = Get-AuthenticodeSignature -LiteralPath $installerPath
    if ($chuKy.Status -ne 'Valid') {
        Loi "Bo cai Python tai ve khong co chu ky hop le (trang thai: $($chuKy.Status))."
    }
    Write-Host "   Chu ky bo cai: $($chuKy.Status) - $($chuKy.SignerCertificate.Subject)" -ForegroundColor Green

    $process = Start-Process -FilePath $installerPath -ArgumentList '/quiet', 'InstallAllUsers=0', 'PrependPath=0', 'Include_launcher=1', 'Include_test=0' -Wait -PassThru
    if ($process.ExitCode -ne 0 -and $process.ExitCode -ne 3010) {
        Loi "Bo cai Python that bai (ma loi $($process.ExitCode))."
    }
}

function Dam-BaoPython312 {
    $python = Tim-Python312
    if ($python) { return $python }

    $winget = Get-Command winget.exe -ErrorAction SilentlyContinue
    if ($winget) {
        Write-Host "   Dang cai Python 3.12 chinh thuc bang winget..."
        $oldErrorActionPreference = $ErrorActionPreference
        $ErrorActionPreference = 'Continue'
        try {
            & $winget.Source install --id Python.Python.3.12 -e --source winget --scope user --silent --accept-package-agreements --accept-source-agreements 2>&1 | Out-Host
            $wingetExitCode = $LASTEXITCODE
        } finally {
            $ErrorActionPreference = $oldErrorActionPreference
        }
        if ($wingetExitCode -eq 0) {
            $python = Tim-Python312
            if ($python) { return $python }
            Write-Host "   Winget da chay xong nhung chua tim thay Python co chu ky. Chuyen sang bo cai python.org..." -ForegroundColor Yellow
        } else {
            Write-Host "   Winget khong cai duoc Python (ma loi $wingetExitCode). Chuyen sang bo cai python.org..." -ForegroundColor Yellow
        }
    } else {
        Write-Host "   Khong co winget. Chuyen sang bo cai python.org..." -ForegroundColor Yellow
    }

    Cai-PythonBangInstaller
    $python = Tim-Python312
    if (-not $python) { Loi "Da cai Python nhung khong tim thay Python 3.12 co chu ky hop le." }
    return $python
}

function Chay-UvSync($uv, $python) {
    $syncLines = @()
    $oldErrorActionPreference = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        # Khong dung co --system-certs: uv ban cu khong biet co nay se bao loi. Bien moi truong UV_SYSTEM_CERTS / UV_NATIVE_TLS da du.
        & $uv sync --python $python 2>&1 | Tee-Object -Variable syncLines
        $script:UvSyncExitCode = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $oldErrorActionPreference
    }
    $script:UvSyncText = ($syncLines | Out-String)
}

function Loi-UvSync($noiDung) {
    # KHONG bao nguoi dung tat Smart App Control: tinh nang nay khong the bat lai neu khong cai lai Windows.
    if ($noiDung -match '(?i)4551|Application Control') {
        Loi "Windows Smart App Control dang chan Python chua ky. Script se dung Python chinh thuc tu python.org; hay chay lai CAI-DAT.bat. Khong tat Smart App Control."
    }
    if ($noiDung -match '(?i)UnknownIssuer|certificate|SSL|CERTIFICATE_VERIFY_FAILED') {
        Loi "Antivirus (Avast/Kaspersky/ESET) co the dang quet HTTPS. Script da dung kho chung chi Windows. Neu van loi, tam tat 'Web Shield / HTTPS scanning' chi trong luc cai dat, chay lai, roi bat lai ngay."
    }
    if ($noiDung -match '(?i)timed out|timeout|\bdns\b|could not resolve|name resolution|connect') {
        Loi "Khong ket noi duoc may chu (timeout/DNS). Kiem tra ket noi hoac thu doi mang, roi chay lai."
    }
    Loi "Cai thu vien that bai. Hay chup man hinh gui cho Claude de kiem tra loi cu the."
}

Write-Host "==============================================" -ForegroundColor Green
Write-Host "   AI STUDIO - CAI DAT LAN DAU (5-15 phut)" -ForegroundColor Green
Write-Host "==============================================" -ForegroundColor Green
Write-Host "Thu muc: $Root"

if ($Root -match 'OneDrive') {
    Write-Host ""
    Write-Host "CANH BAO: thu muc dang nam trong OneDrive. Video nang se bi dong bo len mang, de cham/loi." -ForegroundColor Yellow
    Write-Host "Nen chep ca thu muc sang C:\AI-Studio roi chay lai file CAI-DAT.bat o do." -ForegroundColor Yellow
    Write-Host "Nhan Enter de tiep tuc cai o day, hoac dong cua so nay de chuyen thu muc truoc."
    Read-Host | Out-Null
}

# 1. uv: cong cu quan ly Python (cai rieng cho nguoi dung hien tai)
Buoc 1 "Kiem tra cong cu uv..."
$uvExe = $null
$cmd = Get-Command uv -ErrorAction SilentlyContinue
if ($cmd) { $uvExe = $cmd.Source }
if (-not $uvExe) {
    $cands = @("$env:USERPROFILE\.local\bin\uv.exe", "$env:USERPROFILE\.cargo\bin\uv.exe", "$env:LOCALAPPDATA\Programs\uv\uv.exe")
    foreach ($c in $cands) { if (Test-Path -LiteralPath $c) { $uvExe = $c; break } }
}
if (-not $uvExe) {
    Write-Host "   Dang tai uv (khoang 15 MB)..."
    try {
        powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex"
    } catch { Loi "Khong tai duoc uv. Kiem tra ket noi mang roi chay lai CAI-DAT.bat." }
    foreach ($c in @("$env:USERPROFILE\.local\bin\uv.exe", "$env:USERPROFILE\.cargo\bin\uv.exe")) {
        if (Test-Path -LiteralPath $c) { $uvExe = $c; break }
    }
    if (-not $uvExe) { Loi "Da tai uv nhung khong tim thay file uv.exe." }
}
Write-Host "   OK: $uvExe" -ForegroundColor Green

# 2. Python 3.12 chinh thuc tu python.org, co chu ky hop le
Buoc 2 "Kiem tra Python 3.12 co chu ky..."
$pythonExe = Dam-BaoPython312
$pythonSignature = Get-AuthenticodeSignature -LiteralPath $pythonExe
Write-Host "   OK: $pythonExe" -ForegroundColor Green
Write-Host "   Chu ky Python: $($pythonSignature.Status) - $($pythonSignature.SignerCertificate.Subject)" -ForegroundColor Green

# 3. Thu vien Python cua workspace
Buoc 3 "Cai thu vien xu ly video/anh (lan dau tai 300-600 MB)..."
Chay-UvSync $uvExe $pythonExe
if ($UvSyncExitCode -ne 0) {
    $loiLanDau = $UvSyncText
    if ($loiLanDau -match '(?i)4551|Application Control') {
        Write-Host "   Windows Smart App Control dang chan Python chua ky. Script se dung Python chinh thuc tu python.org..." -ForegroundColor Yellow
        if (-not (Kiem-TraPython312 $pythonExe)) {
            $pythonExe = Dam-BaoPython312
        }
    }
    Write-Host "   Thu lai lan 2 voi Python chinh thuc va kho chung chi Windows..." -ForegroundColor Yellow
    Chay-UvSync $uvExe $pythonExe
    if ($UvSyncExitCode -ne 0) { Loi-UvSync $UvSyncText }
}
Write-Host "   OK" -ForegroundColor Green

# 4. Mo hinh AI chay tren may: nghe giong noi (phu de) + xoa nen anh
Buoc 4 "Tai mo hinh AI cho phu de va xoa nen (khoang 650 MB)..."
Write-Host "   Lan dau co the mat 2-3 phut, khong phai treo may" -ForegroundColor Yellow
& $uvExe run python -m studio tai-mo-hinh
if ($LASTEXITCODE -ne 0) {
    Write-Host "   Chua tai duoc mo hinh - khong sao, se tu tai o lan dung dau tien." -ForegroundColor Yellow
}

# 5. Kiem tra tong the
Buoc 5 "Kiem tra lai toan bo..."
Write-Host "   Lan dau co the mat 2-3 phut, khong phai treo may" -ForegroundColor Yellow
& $uvExe run python -m studio kiem-tra
$ok = ($LASTEXITCODE -eq 0)

Write-Host ""
if ($ok) {
    Write-Host "==============================================" -ForegroundColor Green
    Write-Host "  XONG! Workspace da san sang." -ForegroundColor Green
    Write-Host "==============================================" -ForegroundColor Green
} else {
    Write-Host "Co muc chua on (xem cac dong X o tren). Mo Claude va noi: 'kiem tra cai dat giup minh'." -ForegroundColor Yellow
}
Write-Host ""
Write-Host "BUOC TIEP THEO:"
Write-Host "  1. Mo ung dung Claude (Claude Desktop), chon tab 'Code'."
Write-Host "  2. Chon thu muc nay: $Root"
Write-Host "  3. Go: menu"
Write-Host ""
