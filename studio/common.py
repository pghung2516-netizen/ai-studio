"""Tiện ích dùng chung: đường dẫn workspace, đặt tên file kết quả, chạy ffmpeg, báo lỗi dễ hiểu."""
from __future__ import annotations

import datetime as _dt
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DAU_VAO = ROOT / "01-DAU-VAO"
# STUDIO_THANH_PHAM: chỉ dùng khi chạy kiểm thử (scripts/kiem-thu.py) để không làm rối thư mục kết quả thật
THANH_PHAM = Path(os.environ["STUDIO_THANH_PHAM"]) if os.environ.get("STUDIO_THANH_PHAM") else ROOT / "02-THANH-PHAM"
THUONG_HIEU = ROOT / "03-THUONG-HIEU"
FONTS = ROOT / "assets" / "fonts"
CACHE = ROOT / ".cache"

FONT_THUONG = FONTS / "BeVietnamPro-Regular.ttf"
FONT_DAM = FONTS / "BeVietnamPro-Bold.ttf"
FONT_RAT_DAM = FONTS / "BeVietnamPro-ExtraBold.ttf"
FONT_TEN = "Be Vietnam Pro"

VIDEO_EXT = {".mp4", ".mov", ".m4v", ".mkv", ".avi", ".webm", ".wmv", ".flv", ".3gp", ".mts", ".ts"}
ANH_EXT = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif", ".bmp", ".tif", ".tiff", ".gif"}
AM_THANH_EXT = {".mp3", ".wav", ".aiff", ".aif", ".m4a", ".aac", ".flac", ".ogg", ".opus", ".wma"}

# Model AI tải về nằm gọn trong workspace, không rải ra máy
os.environ.setdefault("HF_HOME", str(CACHE / "huggingface"))
os.environ.setdefault("U2NET_HOME", str(CACHE / "rembg"))
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")


class LoiNguoiDung(Exception):
    """Lỗi do đầu vào (file không có, tham số sai...) - in ra lời giải thích dễ hiểu."""


def bat_utf8() -> None:
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def bao(msg: str) -> None:
    print(msg, flush=True)


def ket_qua(path: Path | list[Path], **thong_tin) -> None:
    """Dòng chuẩn để Claude đọc được kết quả."""
    paths = path if isinstance(path, list) else [path]
    for p in paths:
        print(f"KET QUA: {p}", flush=True)
    if thong_tin:
        print("THONG TIN: " + json.dumps(thong_tin, ensure_ascii=False), flush=True)


def ffmpeg_exe() -> str:
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        exe = shutil.which("ffmpeg")
        if exe:
            return exe
        raise LoiNguoiDung("Chưa có công cụ ffmpeg. Hãy chạy lại bước cài đặt (nhấp đúp CAI-DAT.bat).")


def ten_an_toan(s: str, toi_da: int = 60) -> str:
    """Bỏ dấu, ký tự lạ -> tên file an toàn trên mọi máy."""
    s = unicodedata.normalize("NFKD", s).replace("đ", "d").replace("Đ", "D")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", s).strip("-._")
    return (s or "file")[:toi_da]


def thu_muc_hom_nay() -> Path:
    d = THANH_PHAM / _dt.date.today().isoformat()
    d.mkdir(parents=True, exist_ok=True)
    return d


def file_ra(goc: Path | str, hau_to: str, ext: str | None = None, thu_muc: Path | None = None) -> Path:
    """02-THANH-PHAM/<ngày>/<tên-gốc>_<hậu-tố>.<ext> - không bao giờ ghi đè file cũ."""
    goc = Path(goc)
    ext = ext or goc.suffix
    if not ext.startswith("."):
        ext = "." + ext
    d = thu_muc or thu_muc_hom_nay()
    d.mkdir(parents=True, exist_ok=True)
    base = f"{ten_an_toan(goc.stem)}_{ten_an_toan(hau_to, 30)}"
    p = d / f"{base}{ext}"
    i = 2
    while p.exists():
        p = d / f"{base}-{i}{ext}"
        i += 1
    return p


def tim_file(duong_dan: str, loai: set[str] | None = None) -> Path:
    """Nhận đường dẫn đầy đủ, tương đối, hoặc chỉ tên file nằm trong 01-DAU-VAO."""
    raw = duong_dan.strip().strip('"').strip("'")
    cands = [Path(raw), ROOT / raw, DAU_VAO / raw]
    for c in cands:
        if c.exists():
            p = c.resolve()
            break
    else:
        # tìm gần đúng theo tên trong 01-DAU-VAO
        ten = Path(raw).name.lower()
        hits = [f for f in DAU_VAO.rglob("*") if f.is_file() and ten in f.name.lower()] if DAU_VAO.exists() else []
        if len(hits) == 1:
            p = hits[0].resolve()
        elif len(hits) > 1:
            ds = "\n  ".join(str(h.relative_to(ROOT)) for h in hits[:10])
            raise LoiNguoiDung(f"Có nhiều file khớp với '{raw}':\n  {ds}\nHãy nói rõ file nào.")
        else:
            raise LoiNguoiDung(f"Không tìm thấy file '{raw}'. Hãy bỏ file vào thư mục 01-DAU-VAO rồi thử lại.")
    if loai and p.is_file() and p.suffix.lower() not in loai:
        raise LoiNguoiDung(f"File '{p.name}' không đúng loại (cần: {', '.join(sorted(loai))}).")
    return p


def liet_ke(duong_dan: str, loai: set[str]) -> list[Path]:
    """Một file, hoặc cả thư mục (lấy các file đúng loại, sắp theo tên)."""
    p = tim_file(duong_dan)
    if p.is_dir():
        files = sorted((f for f in p.iterdir() if f.is_file() and f.suffix.lower() in loai), key=lambda f: f.name.lower())
        if not files:
            raise LoiNguoiDung(f"Thư mục '{p.name}' không có file phù hợp ({', '.join(sorted(loai))}).")
        return files
    if p.suffix.lower() not in loai:
        raise LoiNguoiDung(f"File '{p.name}' không đúng loại (cần: {', '.join(sorted(loai))}).")
    return [p]


def chay_ffmpeg(args: list[str], cwd: Path | None = None, mo_ta: str = "") -> None:
    cmd = [ffmpeg_exe(), "-hide_banner", "-nostdin", "-loglevel", "error", "-y", *args]
    if mo_ta:
        bao(f"⏳ {mo_ta}...")
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        chi_tiet = (r.stderr or "").strip().splitlines()[-8:]
        raise RuntimeError("ffmpeg báo lỗi:\n" + "\n".join(chi_tiet))


@dataclass
class ThongTinMedia:
    path: Path
    thoi_luong: float = 0.0
    rong: int = 0
    cao: int = 0
    fps: float = 0.0
    co_hinh: bool = False
    co_tieng: bool = False
    xoay: int = 0
    dung_luong_mb: float = 0.0
    them: dict = field(default_factory=dict)

    @property
    def ti_le(self) -> str:
        if not self.rong or not self.cao:
            return "?"
        from math import gcd

        g = gcd(self.rong, self.cao)
        return f"{self.rong // g}:{self.cao // g}"


def doc_thong_tin(path: Path) -> ThongTinMedia:
    """Đọc thông tin bằng 'ffmpeg -i' (gói ffmpeg đóng sẵn không có ffprobe)."""
    r = subprocess.run([ffmpeg_exe(), "-hide_banner", "-i", str(path)], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    t = r.stderr
    info = ThongTinMedia(path=path, dung_luong_mb=round(path.stat().st_size / 1048576, 2))
    m = re.search(r"Duration: (\d+):(\d+):(\d+(?:\.\d+)?)", t)
    if m:
        info.thoi_luong = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
    for line in t.splitlines():
        if "Stream #" in line and "Video:" in line and not info.co_hinh:
            if "attached pic" in line:
                continue
            info.co_hinh = True
            m = re.search(r"(?<![0-9x])(\d{2,5})x(\d{2,5})(?![0-9x])", line)
            if m:
                info.rong, info.cao = int(m.group(1)), int(m.group(2))
            m = re.search(r"([\d.]+) fps", line) or re.search(r"([\d.]+) tbr", line)
            if m:
                info.fps = float(m.group(1))
        elif "Stream #" in line and "Audio:" in line:
            info.co_tieng = True
    m = re.search(r"rotation of (-?[\d.]+) degrees", t) or re.search(r"rotate\s*:\s*(-?\d+)", t)
    if m:
        info.xoay = int(round(float(m.group(1)))) % 360
        if info.xoay in (90, 270):
            info.rong, info.cao = info.cao, info.rong
    if not info.co_hinh and not info.co_tieng:
        raise LoiNguoiDung(f"Không đọc được file '{path.name}'. File có thể bị hỏng hoặc không phải video/ảnh/âm thanh.")
    return info


def thoi_gian(s: str | float | None) -> float | None:
    """'1:05' / '00:01:05.5' / '65' / '1p5s' -> giây."""
    if s is None or s == "":
        return None
    if isinstance(s, (int, float)):
        return float(s)
    s = str(s).strip().lower().replace(",", ".")
    m = re.fullmatch(r"(?:(\d+)\s*(?:h|g|giờ|gio))?\s*(?:(\d+)\s*(?:m|p|phút|phut))?\s*(?:([\d.]+)\s*(?:s|giây|giay))?", s)
    if m and any(m.groups()) and not re.fullmatch(r"[\d.]+", s):
        h, mi, se = m.groups()
        return int(h or 0) * 3600 + int(mi or 0) * 60 + float(se or 0)
    parts = s.split(":")
    try:
        parts_f = [float(x) for x in parts]
    except ValueError:
        raise LoiNguoiDung(f"Không hiểu mốc thời gian '{s}'. Ví dụ đúng: 0:15, 1:30, 00:01:05")
    v = 0.0
    for x in parts_f:
        v = v * 60 + x
    return v


def dinh_dang_tg(giay: float) -> str:
    giay = max(0.0, giay)
    h = int(giay // 3600)
    m = int(giay % 3600 // 60)
    s = giay % 60
    return f"{h}:{m:02d}:{s:04.1f}" if h else f"{m}:{s:04.1f}"


TI_LE = {
    "9:16": (1080, 1920),
    "16:9": (1920, 1080),
    "1:1": (1080, 1080),
    "4:5": (1080, 1350),
    "4:3": (1440, 1080),
    "3:4": (1080, 1440),
}


def kich_thuoc_ti_le(ti_le: str) -> tuple[int, int]:
    ti_le = ti_le.strip().lower().replace("x", ":").replace("/", ":")
    alias = {"doc": "9:16", "dọc": "9:16", "tiktok": "9:16", "reels": "9:16", "shorts": "9:16", "story": "9:16",
             "ngang": "16:9", "youtube": "16:9", "vuong": "1:1", "vuông": "1:1", "facebook": "4:5", "instagram": "4:5"}
    ti_le = alias.get(ti_le, ti_le)
    if ti_le not in TI_LE:
        raise LoiNguoiDung(f"Tỉ lệ '{ti_le}' chưa hỗ trợ. Chọn một trong: {', '.join(TI_LE)} (hoặc: doc, ngang, vuong).")
    return TI_LE[ti_le]


def mau_rgb(s: str) -> tuple[int, int, int]:
    ten = {"trang": "#ffffff", "đen": "#000000", "den": "#000000", "do": "#e53935", "đỏ": "#e53935",
           "vang": "#ffd600", "vàng": "#ffd600", "xanh": "#1e88e5", "xanh-la": "#43a047", "hong": "#ec407a",
           "cam": "#fb8c00", "xam": "#9e9e9e", "tim": "#8e24aa"}
    s = ten.get(s.strip().lower(), s.strip())
    m = re.fullmatch(r"#?([0-9a-fA-F]{6})", s)
    if not m:
        raise LoiNguoiDung(f"Màu '{s}' không hợp lệ. Dùng mã màu như #FF5722 hoặc tên: trang, den, do, vang, xanh...")
    h = m.group(1)
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
