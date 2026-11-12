"""Quản lý dự án: bản gốc, bản nháp, thành phẩm và nhật ký."""
from __future__ import annotations

import datetime as _dt
import re
import shutil
import unicodedata
from pathlib import Path

from .common import (DAU_VAO, DU_AN, GOC, NHAP, NHAT_KY, ROOT, THANH_PHAM_DA, LoiNguoiDung, bao,
                     ket_qua, ten_an_toan, ten_tieng_viet_an_toan, thu_muc_nhap_du_an, tim_file)


def _khong_dau(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).replace("đ", "d").replace("Đ", "D")
    return "".join(c for c in s if not unicodedata.combining(c)).casefold()


def danh_sach_du_an() -> list[Path]:
    if not DU_AN.exists():
        return []
    return [p for p in DU_AN.iterdir() if p.is_dir() and not p.name.startswith(".")]


def tim_du_an(ten: str) -> Path:
    """Tìm tên chính xác, nếu không có thì tìm chuỗi con không phân biệt dấu/hoa thường."""
    raw = ten.strip().strip('"').strip("'")
    projects = danh_sach_du_an()
    exact = [p for p in projects if p.name == raw]
    if exact:
        return exact[0]
    needle = _khong_dau(raw)
    hits = [p for p in projects if needle in _khong_dau(p.name)]
    if len(hits) == 1:
        return hits[0]
    if len(hits) > 1:
        ds = "\n  ".join(p.name for p in sorted(hits, key=lambda x: x.name))
        raise LoiNguoiDung(f"Có nhiều dự án khớp với '{ten}':\n  {ds}\nHãy ghi rõ hơn.")
    raise LoiNguoiDung(f"Không tìm thấy dự án '{ten}'. Hãy chạy 'studio du-an ds' để xem danh sách.")


def _ten_du_an(project: Path) -> str:
    log = project / NHAT_KY
    if log.exists():
        try:
            first = log.read_text(encoding="utf-8-sig").splitlines()[0]
            if first.startswith("# Dự án: "):
                return first.removeprefix("# Dự án: ").strip()
        except (OSError, UnicodeError, IndexError):
            pass
    return re.sub(r"^\d{4}-\d{2}-\d{2}\s+", "", project.name)


def _tao_cau_truc(project: Path, ten: str) -> None:
    (project / GOC).mkdir(parents=True)
    (project / THANH_PHAM_DA).mkdir()
    now = _dt.datetime.now().astimezone()
    (project / NHAT_KY).write_text(
        f"# Dự án: {ten}\n\n- Tạo lúc: {now:%H:%M %d/%m/%Y}\n\n## Nhật ký\n",
        encoding="utf-8",
    )


def _ten_khong_trung(folder: Path, name: str) -> Path:
    p = folder / name
    i = 2
    while p.exists():
        p = folder / f"{Path(name).stem} ({i}){Path(name).suffix}"
        i += 1
    return p


def _la_ben_trong(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def _nguon(raw: str) -> Path:
    text = raw.strip().strip('"').strip("'")
    for p in (Path(text), ROOT / text, DAU_VAO / text):
        if p.exists():
            if not p.is_file():
                raise LoiNguoiDung(f"'{p}' không phải là file.")
            return p.resolve()
    p = tim_file(text)
    if not p.is_file():
        raise LoiNguoiDung(f"'{p}' không phải là file.")
    return p


def _them_nguon(project: Path, raws: list[str], lay_hop_thu: bool) -> list[Path]:
    sources = [_nguon(x) for x in raws]
    if lay_hop_thu and DAU_VAO.exists():
        sources += [p.resolve() for p in DAU_VAO.iterdir()
                    if p.is_file() and not p.name.startswith(".") and p.name != "DOC-TOI.txt"]
    unique: list[Path] = []
    seen: set[Path] = set()
    for src in sources:
        if src not in seen:
            seen.add(src)
            unique.append(src)

    dests: list[Path] = []
    folder = project / GOC
    for src in unique:
        dest = _ten_khong_trung(folder, ten_tieng_viet_an_toan(src.name))
        if _la_ben_trong(src, DAU_VAO):
            try:
                shutil.move(str(src), str(dest))
                kieu = "chuyển"
            except OSError:
                # Windows không cho chuyển file đang mở (vd đang phát video) -> chép, để nguyên bản gốc
                if dest.exists():
                    dest.unlink()
                shutil.copy2(src, dest)
                kieu = "sao chép (file đang mở ở chương trình khác nên chưa chuyển được)"
        else:
            shutil.copy2(src, dest)
            kieu = "sao chép"
        dests.append(dest)
        bao(f"✅ Đã {kieu}: {src.name} → {GOC}/{dest.name}")
    if dests:
        _ghi(project, f"Thêm {len(dests)} file gốc: " + ", ".join(p.name for p in dests))
    return dests


def _ghi(project: Path, noi_dung: str) -> Path:
    log = project / NHAT_KY
    now = _dt.datetime.now()
    text = str(noi_dung).replace("\r\n", "\n").replace("\r", "\n")
    with log.open("a", encoding="utf-8", newline="\n") as f:
        f.write(f"- [{now:%H:%M %d/%m}] {text}\n")
    return log


def lenh_moi(a) -> None:
    ten = ten_tieng_viet_an_toan(a.ten.strip(), 100)
    if not a.ten.strip():
        raise LoiNguoiDung("Tên dự án không được để trống.")
    DU_AN.mkdir(parents=True, exist_ok=True)
    base = f"{_dt.date.today().isoformat()} {ten}"
    project = DU_AN / base
    i = 2
    while project.exists():
        project = DU_AN / f"{base} ({i})"
        i += 1
    _tao_cau_truc(project, ten)
    goc = _them_nguon(project, a.file, a.lay_hop_thu)
    bao(f"📁 Đã tạo dự án: {project.name}")
    ket_qua(project, du_an=project.name, goc=[str(p) for p in goc])


def lenh_them(a) -> None:
    project = tim_du_an(a.du_an)
    if not a.file and not a.lay_hop_thu:
        raise LoiNguoiDung("Hãy ghi file cần thêm hoặc dùng --lay-hop-thu.")
    goc = _them_nguon(project, a.file, a.lay_hop_thu)
    ket_qua(project, du_an=project.name, goc=[str(p) for p in goc])


def _files(folder: Path) -> list[Path]:
    return sorted((p for p in folder.rglob("*") if p.is_file()), key=lambda p: p.name.casefold()) if folder.exists() else []


def _size(folder: Path) -> int:
    total = 0
    for p in _files(folder):
        try:
            total += p.stat().st_size
        except OSError:
            pass
    return total


def _mtime(folder: Path) -> float:
    vals = []
    try:
        vals.append(folder.stat().st_mtime)
    except OSError:
        return 0.0
    for p in folder.rglob("*"):
        try:
            vals.append(p.stat().st_mtime)
        except OSError:
            pass
    return max(vals)


def lenh_ds(a) -> None:
    projects = sorted(danh_sach_du_an(), key=_mtime, reverse=True)[:max(0, a.so)]
    ds = []
    for p in projects:
        item = {
            "ten": p.name,
            "goc": len(_files(p / GOC)),
            "thanh_pham": len(_files(p / THANH_PHAM_DA)),
            "mb": round(_size(p) / 1048576, 2),
            "sua_luc": _dt.datetime.fromtimestamp(_mtime(p)).strftime("%H:%M %d/%m/%Y"),
        }
        ds.append(item)
        bao(f"📁 {item['ten']} — {item['goc']} gốc, {item['thanh_pham']} thành phẩm — "
            f"{item['mb']:.2f} MB — {item['sua_luc']}")
    if not ds:
        bao("(Chưa có dự án nào)")
    ket_qua(projects, ds=ds)


def lenh_xem(a) -> None:
    project = tim_du_an(a.du_an)
    draft = thu_muc_nhap_du_an(project)
    originals = _files(project / GOC)
    finals = _files(project / THANH_PHAM_DA)
    drafts = _files(draft) if draft else []
    log = project / NHAT_KY
    lines = log.read_text(encoding="utf-8-sig").splitlines()[-40:] if log.exists() else []
    bao(f"📁 {project.name}")
    for title, files in (("Gốc", originals), ("Thành phẩm", finals), ("Bản nháp", drafts)):
        bao(f"\n{title} ({len(files)}):")
        for p in files:
            bao(f"  - {p.name}")
    bao("\nNhật ký (40 dòng cuối):\n" + ("\n".join(lines) if lines else "(trống)"))
    ket_qua(project, du_an=project.name, goc=[str(p) for p in originals],
            thanh_pham=[str(p) for p in finals], nhap=[str(p) for p in drafts], nhat_ky=lines)


def lenh_ghi(a) -> None:
    project = tim_du_an(a.du_an)
    log = _ghi(project, a.noi_dung)
    bao("✅ Đã ghi vào nhật ký dự án.")
    ket_qua(log, du_an=project.name)


def _file_chot(project: Path, raw: str) -> Path:
    from .common import dat_du_an_hien_tai

    dat_du_an_hien_tai(project)
    p = tim_file(raw)
    if not p.is_file():
        raise LoiNguoiDung(f"'{p}' không phải là file để chốt.")
    return p


def lenh_chot(a) -> None:
    project = tim_du_an(a.du_an)
    src = _file_chot(project, a.file)
    title = ten_tieng_viet_an_toan(_ten_du_an(project), 80)
    label = ten_tieng_viet_an_toan(a.ten.strip(), 50)
    if not a.ten.strip():
        raise LoiNguoiDung("Nhãn --ten không được để trống.")
    note = ten_tieng_viet_an_toan(a.ghi_chu.strip(), 50) if a.ghi_chu else ""
    finals = project / THANH_PHAM_DA
    prefix = f"{title} - {label} - bản "
    rx = re.compile(rf"^{re.escape(prefix)}(\d+)(?:\s+\(.*\))?\.[^.]+$", re.IGNORECASE)
    versions = [int(m.group(1)) for p in finals.iterdir() if p.is_file() and (m := rx.match(p.name))]
    version = max(versions, default=0) + 1
    note_part = f" ({note})" if note else ""
    name = ten_tieng_viet_an_toan(f"{prefix}{version}{note_part}{src.suffix.lower()}")
    dest = finals / name
    if dest.exists():
        raise LoiNguoiDung(f"Thành phẩm '{dest.name}' đã có; không ghi đè.")
    shutil.copy2(src, dest)
    kem = []
    if a.kem_phu_de:
        for ext in (".srt", ".txt"):
            sibling = src.with_suffix(ext)
            if sibling.exists() and sibling.resolve() != src.resolve():
                sub_dest = finals / ten_tieng_viet_an_toan(f"{prefix}{version}{note_part}{ext}")
                if sub_dest.exists():
                    raise LoiNguoiDung(f"Thành phẩm '{sub_dest.name}' đã có; không ghi đè.")
                shutil.copy2(sibling, sub_dest)
                kem.append(sub_dest)
    _ghi(project, f"Chốt bản {version}: {dest.name}" + (f" (kèm {len(kem)} file phụ đề)" if kem else ""))
    bao(f"✅ Chốt bản {version}: {dest.name}")
    ket_qua(dest, ban=version)


def lenh_don_dep(a) -> None:
    now = _dt.datetime.now().timestamp()
    selected = tim_du_an(a.du_an_studio) if getattr(a, "du_an_studio", None) else None
    projects = [selected] if selected else [p for p in danh_sach_du_an()
                                            if now - _mtime(p) > max(0, a.cu_hon) * 86400]
    drafts: list[Path] = []
    if NHAP.exists():
        wanted = ten_an_toan(selected.name) if selected else None
        # dọn 1 dự án cụ thể -> dọn luôn nháp của nó; dọn chung -> chỉ nháp cũ hơn 7 ngày
        drafts = [p for p in NHAP.iterdir() if p.is_dir()
                  and (p.name == wanted if wanted else now - _mtime(p) > 7 * 86400)]
    targets = [("dự án", p, _size(p)) for p in projects] + [("bản nháp", p, _size(p)) for p in drafts]
    total = sum(size for _, _, size in targets)
    for kind, p, size in targets:
        bao(f"- {kind}: {p.name} — {size / 1048576:.2f} MB")
    if not targets:
        bao("Không có thư mục nào cần dọn.")
    elif not a.xac_nhan:
        bao("Chỉ xem trước; thêm --xac-nhan để chuyển các thư mục trên vào Thùng rác.")
    if a.xac_nhan:
        from send2trash import send2trash

        for _, p, _ in targets:
            send2trash(str(p))
            bao(f"♻️  Đã chuyển vào Thùng rác: {p.name}")
    info = [{"loai": kind, "duong_dan": str(p), "mb": round(size / 1048576, 2)} for kind, p, size in targets]
    ket_qua([] if a.xac_nhan else [p for _, p, _ in targets], ds=info,
            tong_mb=round(total / 1048576, 2), da_xac_nhan=bool(a.xac_nhan))
