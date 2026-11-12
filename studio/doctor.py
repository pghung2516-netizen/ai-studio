"""Kiểm tra máy, tải mô hình AI, sao lưu CapCut, liệt kê file đầu vào."""
from __future__ import annotations

import datetime as _dt
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

from .common import (CACHE, DAU_VAO, FONT_DAM, ROOT, THANH_PHAM, THUONG_HIEU, LoiNguoiDung, bao, ffmpeg_exe,
                     ket_qua)


def _ok(dk: bool, ten: str, goi_y: str = "") -> bool:
    bao(("✅ " if dk else "❌ ") + ten + ("" if dk or not goi_y else f"  → {goi_y}"))
    return dk


def lenh_kiem_tra(a) -> None:
    bao(f"Máy: {platform.system()} {platform.release()} | Python {sys.version.split()[0]}")
    bao(f"Thư mục làm việc: {ROOT}")
    tot = True
    tot &= _ok(sys.version_info[:2] == (3, 12), "Python 3.12", "chạy lại CAI-DAT.bat")
    try:
        exe = ffmpeg_exe()
        r = subprocess.run([exe, "-hide_banner", "-filters"], capture_output=True, text=True, encoding="utf-8",
                           errors="replace")
        tot &= _ok(r.returncode == 0, "Công cụ video (ffmpeg)")
        tot &= _ok(" subtitles " in r.stdout, "Đốt phụ đề vào video (libass)", "bản ffmpeg thiếu libass")
    except LoiNguoiDung as e:
        tot &= _ok(False, "Công cụ video (ffmpeg)", str(e))
    for mod, ten in [("PIL", "Xử lý ảnh"), ("pillow_heif", "Đọc ảnh iPhone (HEIC)"),
                     ("faster_whisper", "Nghe giọng nói → phụ đề"), ("rembg", "Xóa nền ảnh"),
                     ("pydantic", "Sửa dự án CapCut")]:
        try:
            __import__(mod)
            tot &= _ok(True, ten)
        except Exception as e:  # noqa: BLE001
            tot &= _ok(False, ten, f"lỗi nạp thư viện: {e}")
    tot &= _ok(FONT_DAM.exists(), "Phông chữ tiếng Việt (Be Vietnam Pro)", "thiếu thư mục assets/fonts")
    for d in (DAU_VAO, THANH_PHAM, THUONG_HIEU):
        d.mkdir(exist_ok=True)
    _ok(True, "Các thư mục 01-DAU-VAO, 02-THANH-PHAM, 03-THUONG-HIEU")
    whisper = any((CACHE / "huggingface").rglob("model.bin")) if (CACHE / "huggingface").exists() else False
    rembg = any((CACHE / "rembg").rglob("*.onnx")) if (CACHE / "rembg").exists() else False
    bao("✅ Mô hình nghe giọng nói đã tải sẵn" if whisper else "ℹ️  Mô hình nghe giọng nói chưa tải - sẽ tự tải ở lần làm phụ đề đầu tiên (~500MB)")
    bao("✅ Mô hình xóa nền đã tải sẵn" if rembg else "ℹ️  Mô hình xóa nền chưa tải - sẽ tự tải ở lần xóa nền đầu tiên (~170MB)")
    p = str(ROOT).lower()
    if "onedrive" in p:
        bao("⚠️  Thư mục đang nằm trong OneDrive - video nặng sẽ bị đồng bộ lên mạng, dễ chậm/lỗi. "
            "Nên chuyển cả thư mục sang C:\\AI-Studio")
    free = shutil.disk_usage(ROOT).free / 1024 ** 3
    _ok(free > 5, f"Ổ đĩa còn trống {free:.0f} GB", "nên dọn bớt, sửa video cần nhiều chỗ trống")
    bao("")
    bao("🎉 MỌI THỨ ĐÃ SẴN SÀNG" if tot else "⚠️  CÓ MỤC CHƯA ỔN - xem các dòng ❌ ở trên")
    if not tot:
        sys.exit(3)


def lenh_tai_mo_hinh(a) -> None:
    if a.loai in ("tat-ca", "phu-de"):
        bao(f"⏳ Tải mô hình nghe giọng nói '{a.whisper}'...")
        from faster_whisper import WhisperModel

        WhisperModel(a.whisper, device="cpu", compute_type="int8")
        bao("✅ Xong mô hình nghe giọng nói")
    if a.loai in ("tat-ca", "xoa-nen"):
        bao("⏳ Tải mô hình xóa nền...")
        from rembg import new_session

        new_session("isnet-general-use")
        bao("✅ Xong mô hình xóa nền")


def lenh_danh_sach(a) -> None:
    from .common import ANH_EXT, AM_THANH_EXT, VIDEO_EXT

    goc = DAU_VAO if not a.thu_muc else (ROOT / a.thu_muc)
    if not goc.exists():
        raise LoiNguoiDung(f"Không có thư mục {goc}")
    files = sorted((f for f in goc.rglob("*") if f.is_file() and not f.name.startswith(".")
                    and f.name != "DOC-TOI.txt"), key=lambda f: f.stat().st_mtime, reverse=True)
    if not files:
        bao(f"(Thư mục {goc.name} đang trống)")
        return
    for f in files[:200]:
        ext = f.suffix.lower()
        loai = "video" if ext in VIDEO_EXT else "ảnh" if ext in ANH_EXT else "âm thanh" if ext in AM_THANH_EXT else "khác"
        tg = _dt.datetime.fromtimestamp(f.stat().st_mtime).strftime("%d/%m %H:%M")
        bao(f"{tg}  {loai:<8} {f.stat().st_size / 1048576:7.1f} MB  {f.relative_to(ROOT)}")


# ---------------------------------------------------------------- CapCut
def thu_muc_capcut() -> Path | None:
    env = os.environ.get("CAPCUT_DRAFTS_DIR")
    if env:
        return Path(env)
    home = Path.home()
    cands = [home / "AppData" / "Local" / "CapCut" / "User Data" / "Projects" / "com.lveditor.draft",
             home / "Movies" / "CapCut" / "User Data" / "Projects" / "com.lveditor.draft"]
    return next((c for c in cands if c.exists()), None)


def lenh_capcut_sao_luu(a) -> None:
    goc = thu_muc_capcut()
    if not goc:
        raise LoiNguoiDung("Không tìm thấy thư mục dự án CapCut trên máy. Hãy mở CapCut và lưu ít nhất 1 dự án.")
    hits = [d for d in goc.iterdir() if d.is_dir() and a.du_an.lower() in d.name.lower()]
    if not hits:
        raise LoiNguoiDung(f"Không có dự án CapCut nào tên chứa '{a.du_an}'.")
    if len(hits) > 1:
        raise LoiNguoiDung("Có nhiều dự án trùng tên: " + ", ".join(h.name for h in hits) + ". Hãy nói rõ hơn.")
    src = hits[0]
    dst = THANH_PHAM / "_sao-luu-capcut" / f"{src.name}_{_dt.datetime.now():%Y%m%d-%H%M%S}"
    shutil.copytree(src, dst)
    bao(f"✅ Đã sao lưu dự án '{src.name}'. Nếu kết quả cắt không ưng, chép thư mục này đè lại vào:\n   {src}")
    ket_qua(dst)
