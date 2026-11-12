"""Tìm nhanh media mới nhận trên các thư mục thường dùng."""
from __future__ import annotations

import datetime as _dt
import os
import sys
import time
from pathlib import Path

from .common import AM_THANH_EXT, ANH_EXT, DAU_VAO, ROOT, VIDEO_EXT, LoiNguoiDung, bao, ket_qua


def _desktop(home: Path) -> Path:
    if sys.platform != "win32":
        return home / "Desktop"
    try:
        import winreg

        key_name = r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_name) as key:
            value, _ = winreg.QueryValueEx(key, "Desktop")
        return Path(os.path.expandvars(value))
    except (OSError, ImportError):
        return home / "Desktop"


def _hidden(p: Path) -> bool:
    if p.name.startswith("."):
        return True
    try:
        attrs = getattr(p.stat(), "st_file_attributes", 0)
        return bool(attrs & 0x2 or attrs & 0x4)  # FILE_ATTRIBUTE_HIDDEN | SYSTEM
    except OSError:
        return True


def _inside(p: Path, parent: Path) -> bool:
    try:
        p.resolve().relative_to(parent.resolve())
        return True
    except (ValueError, OSError):
        return False


def _top(folder: Path):
    if folder.exists():
        try:
            yield from (p for p in folder.iterdir() if p.is_file())
        except OSError:
            return


def _zalo(folder: Path):
    if not folder.exists():
        return
    for base, dirs, files in os.walk(folder):
        current = Path(base)
        try:
            depth = len(current.relative_to(folder).parts)
        except ValueError:
            continue
        dirs[:] = [d for d in dirs if not d.startswith(".") and depth < 3]
        for name in files:
            yield current / name


def lenh_tim_file_moi(a) -> None:
    exts = {"video": VIDEO_EXT, "anh": ANH_EXT, "am-thanh": AM_THANH_EXT,
            "tat-ca": VIDEO_EXT | ANH_EXT | AM_THANH_EXT}[a.loai]
    if a.so <= 0 or a.gio < 0:
        raise LoiNguoiDung("--so phải lớn hơn 0 và --gio không được âm.")
    home = Path.home()
    top_folders = [DAU_VAO, home / "Downloads", _desktop(home), home / "Pictures", home / "Videos",
                   home / "Pictures" / "Screenshots"]
    zalo = home / "Documents" / "Zalo Received Files"
    candidates: list[Path] = []
    seen_dirs: set[Path] = set()
    for folder in top_folders:
        try:
            key = folder.resolve()
        except OSError:
            key = folder
        if key in seen_dirs:
            continue
        seen_dirs.add(key)
        candidates.extend(_top(folder))
    candidates.extend(_zalo(zalo) or [])

    cutoff = time.time() - a.gio * 3600
    found: dict[Path, tuple[Path, os.stat_result]] = {}
    for p in candidates:
        try:
            resolved = p.resolve()
            if _hidden(p) or p.suffix.lower() not in exts:
                continue
            if _inside(resolved, ROOT) and not _inside(resolved, DAU_VAO):
                continue
            st = resolved.stat()
            if st.st_mtime >= cutoff:
                found[resolved] = (resolved, st)
        except OSError:
            continue
    newest = sorted(found.values(), key=lambda x: x[1].st_mtime, reverse=True)[:a.so]
    if not newest:
        raise LoiNguoiDung(f"Không tìm thấy file {a.loai} nào mới trong {a.gio} giờ qua.")
    ds = []
    paths = []
    for i, (p, st) in enumerate(newest, 1):
        item = {"stt": i, "ten": p.name, "thu_muc": p.parent.name,
                "thoi_gian": _dt.datetime.fromtimestamp(st.st_mtime).strftime("%H:%M %d/%m"),
                "mb": round(st.st_size / 1048576, 2)}
        paths.append(p)
        ds.append(item)
        bao(f"{i}. {item['ten']} — {item['thu_muc']} — {item['thoi_gian']} — {item['mb']:.2f} MB")
    ket_qua(paths, ds=ds)
