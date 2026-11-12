# AI STUDIO - cai dat tu dong cho Windows (khong can quyen Administrator)
# Chay bang cach nhap dup CAI-DAT.bat o thu muc goc.
# Thong bao viet khong dau de khong bi loi font tren cua so dong lenh Windows.

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $Root
$env:PYTHONUTF8 = '1'
$env:UV_LINK_MODE = 'copy'

function Buoc($so, $msg) { Write-Host ""; Write-Host "[$so/4] $msg" -ForegroundColor Cyan }
function Loi($msg) {
    Write-Host ""
    Write-Host "LOI: $msg" -ForegroundColor Red
    Write-Host "Ban hay chup man hinh nay, hoac mo Claude va noi: 'cai dat bi loi' de Claude sua giup." -ForegroundColor Yellow
    exit 1
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

# 2. Python 3.12 + thu vien (uv tu tai, khong dung den Python khac tren may)
Buoc 2 "Cai Python va thu vien xu ly video/anh (lan dau tai 300-600 MB)..."
& $uvExe sync
if ($LASTEXITCODE -ne 0) {
    Write-Host "   Thu lai lan 2..." -ForegroundColor Yellow
    & $uvExe sync
    if ($LASTEXITCODE -ne 0) { Loi "Cai thu vien that bai (thuong do mang yeu hoac bi chan). Thu doi mang roi chay lai." }
}
Write-Host "   OK" -ForegroundColor Green

# 3. Mo hinh AI chay tren may: nghe giong noi (phu de) + xoa nen anh
Buoc 3 "Tai mo hinh AI cho phu de va xoa nen (khoang 650 MB)..."
& $uvExe run python -m studio tai-mo-hinh
if ($LASTEXITCODE -ne 0) {
    Write-Host "   Chua tai duoc mo hinh - khong sao, se tu tai o lan dung dau tien." -ForegroundColor Yellow
}

# 4. Kiem tra tong the
Buoc 4 "Kiem tra lai toan bo..."
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
